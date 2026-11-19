"""
Module 2, experiment 1, Setup 4: a general (not SAFE-specific) contract instruction.

Setup 1's bare instruction + a general paragraph about what any contract summary
should cover. Run 5 times on Haiku 5.5 and 5 times on Sonnet 5.5, both with
thinking off. Graded with the same SAFE rubric as Setups 1-3.

    01-tokens/.venv/bin/python 02-context/setup_four.py run first   # run 1 on each model
    01-tokens/.venv/bin/python 02-context/setup_four.py run rest    # runs 2-5 on each model
    01-tokens/.venv/bin/python 02-context/setup_four.py report      # results table -> results.md
"""

import json
import sys
from pathlib import Path

import anthropic

from three_setups import BARE_INSTRUCTION, CONTRACT, FIVE_MILLION, RESULTS_FILE, length_point, load_api_key

HERE = Path(__file__).parent
RUNS_FILE = HERE / "runs_setup4.json"
SCORES_FILE = HERE / "scores_setup4.json"
SUMMARIES_FILE = HERE / "summaries_setup4.md"
RUNS_PER_MODEL = 5

GENERAL_INSTRUCTION = (
    "Note who the parties are at hand, what are the core terms of the contract, what are any forcing "
    "mechanisms or clauses or deadlines, what are specific rights and privileges the parties have, etc. "
    "Include major contract numbers but do not ignore other terms and conditions in favor of only noting "
    "numbers. Start by identifying the type of contract."
)
INSTRUCTION = BARE_INSTRUCTION + " " + GENERAL_INSTRUCTION

# name: (model ID, thinking-off setting, input $/M, output $/M)
MODELS = {
    "Haiku": ("claude-haiku-5-5", {"type": "disabled"}, 0.10, 0.50),
    "Sonnet": ("claude-sonnet-5-5", {"type": "between_tools"}, 2.00, 10.00),
}


def run(which):
    runs = json.loads(RUNS_FILE.read_text()) if RUNS_FILE.exists() else []
    run_numbers = [1] if which == "first" else list(range(2, RUNS_PER_MODEL + 1))
    if any(r["run"] in run_numbers for r in runs):
        sys.exit(f"Those runs are already in {RUNS_FILE.name}. Delete it to start over.")
    if which == "rest" and not runs:
        sys.exit("Do the first round first: setup_four.py run first")
    client = anthropic.Anthropic(api_key=load_api_key())
    contract = CONTRACT.read_text()
    new_cost = 0.0

    for name, (model, thinking, p_in, p_out) in MODELS.items():
        for n in run_numbers:
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    thinking=thinking,
                    messages=[{"role": "user", "content": INSTRUCTION + "\n\n" + contract}],
                )
            except anthropic.APIStatusError as e:
                sys.exit(f"API error {e.status_code}: {e.message}")
            except anthropic.APIConnectionError:
                sys.exit("Could not reach the Anthropic API. Check your internet connection.")
            if response.stop_reason == "refusal":
                sys.exit(f"{model} declined the request. Nothing recorded for this run.")

            summary = "".join(b.text for b in response.content if b.type == "text").strip()
            in_tok, out_tok = response.usage.input_tokens, response.usage.output_tokens
            cost = (in_tok * p_in + out_tok * p_out) / 1_000_000
            runs.append({"model": name, "run": n, "input_tokens": in_tok, "output_tokens": out_tok,
                         "cost": cost, "words": len(summary.split()), "summary": summary})
            new_cost += cost
            print(f"Setup 4 / {name}, run {n}: {in_tok} input, {out_tok} output, ${cost:.6f}")

    runs.sort(key=lambda r: (list(MODELS).index(r["model"]), r["run"]))
    RUNS_FILE.write_text(json.dumps(runs, indent=2))
    lines = ["# Setup 4: general contract instruction (thinking off)", "",
             f"Instruction: \"{INSTRUCTION}\"", ""]
    for name in MODELS:
        lines += [f"## {name} 5.5", ""]
        for r in (r for r in runs if r["model"] == name):
            lines += [f"### Setup 4 / {name}, run {r['run']} ({r['words']} words)", "", r["summary"], ""]
    SUMMARIES_FILE.write_text("\n".join(lines))
    print(f"\nCost of these runs: ${new_cost:.6f} ({len(runs)} runs saved so far)")
    print(f"Saved {SUMMARIES_FILE.name} and {RUNS_FILE.name}. Scores are not shown yet.")


def report():
    runs = json.loads(RUNS_FILE.read_text())
    scores = json.loads(SCORES_FILE.read_text()) if SCORES_FILE.exists() else {}
    lines = [
        "",
        "### Setup 4 results per run",
        "",
        "| Model | Run | Input tokens | Output tokens | Cost | Words | Facts (out of 5) | Length <150 words | Total (out of 6) | Includes $5M offering? |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in runs:
        score = scores.get(f"{r['model']}-{r['run']}")
        length_pt = length_point(r)
        total = "—" if score is None else score + length_pt
        has_5m = "Yes" if FIVE_MILLION.search(r["summary"]) else "No"
        lines.append(f"| {r['model']} 5.5 | {r['run']} | {r['input_tokens']:,} | {r['output_tokens']:,} "
                     f"| ${r['cost']:.6f} | {r['words']} | {'—' if score is None else score} | {length_pt} "
                     f"| {total} | {has_5m} |")
    lines += ["", "### Setup 4 per model", "",
              "| Model | Input tokens (avg) | Output tokens (avg) | Total cost (5 runs) | Avg total (out of 6) | Runs with $5M |",
              "|---|---|---|---|---|---|"]
    for name in MODELS:
        rs = [r for r in runs if r["model"] == name]
        got = [scores[f"{name}-{r['run']}"] + length_point(r) for r in rs if f"{name}-{r['run']}" in scores]
        avg_score = f"{sum(got) / len(got):.1f}" if got else "—"
        with_5m = sum(1 for r in rs if FIVE_MILLION.search(r["summary"]))
        lines.append(f"| {name} 5.5 | {sum(r['input_tokens'] for r in rs) / len(rs):,.0f} "
                     f"| {sum(r['output_tokens'] for r in rs) / len(rs):,.0f} "
                     f"| ${sum(r['cost'] for r in rs):.6f} | {avg_score} | {with_5m} of {len(rs)} |")
    with RESULTS_FILE.open("a") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nAppended to {RESULTS_FILE.name}")


if __name__ == "__main__":
    if sys.argv[1:] in (["run", "first"], ["run", "rest"]):
        run(sys.argv[2])
    elif sys.argv[1:] == ["report"]:
        report()
    else:
        sys.exit("Usage: setup_four.py run first | run rest | report")
