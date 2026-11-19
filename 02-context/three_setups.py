"""
Module 2, experiment 1: three context setups for summarizing the SAFE contract.

Each setup is run 5 times on Claude Haiku 5.5 (thinking off) = 15 runs.

  Setup 1: the bare instruction from Module 1.
  Setup 2: the bare instruction + a system prompt listing the five required facts (our rubric).
  Setup 3: the bare instruction + one general rule about dollar amounts and caps.

Two steps (run from the repo folder):

    01-tokens/.venv/bin/python 02-context/three_setups.py run first
        Run 1 of each setup (3 calls), for hand-grading before the rest.
    01-tokens/.venv/bin/python 02-context/three_setups.py run rest
        Runs 2-5 of each setup (12 calls).
        Both save every summary to summaries.md and the raw numbers to runs.json,
        and print only tokens and cost (no scores).

    01-tokens/.venv/bin/python 02-context/three_setups.py report
        Builds the per-run results table in results.md: tokens, cost, fact score
        (from scores.json, filled in after grading) and whether the $5M offering is included.
"""

import json
import re
import sys
from pathlib import Path

import anthropic

HERE = Path(__file__).parent
CONTRACT = HERE.parent / "01-tokens" / "contract" / "contract_clean.txt"
ENV_FILE = Path.home() / "code" / ".env"
RUNS_FILE = HERE / "runs.json"
SCORES_FILE = HERE / "scores.json"
SUMMARIES_FILE = HERE / "summaries.md"
RESULTS_FILE = HERE / "results.md"

MODEL = "claude-haiku-5-5"
INPUT_PRICE = 0.10    # $ per million input tokens
OUTPUT_PRICE = 0.50   # $ per million output tokens
RUNS_PER_SETUP = 5

# ---------------------------------------------------------------- the three setups
BARE_INSTRUCTION = "Write a one-paragraph synthesis of this contract in 100 words."

# The five facts, exactly as written in 01-tokens/results.md.
RUBRIC_SYSTEM_PROMPT = """A summary of this contract must include these five facts:

1. Issuer and offering: YayYo, Inc. (Delaware) selling rights to SAFE Preferred Stock in a private placement of up to $5 million under Reg D Rule 506 and/or Reg S. Unregistered and resale-restricted.
2. Economics: 8% annual dividend. Discount depends on purchase date: 50% through Dec 31, 2016, then 30%, 20%, 10%, none after Feb 15, 2017.
3. Conversion trigger: on an Equity Financing (Reg A+ Tier 2 or IPO), purchase amount plus dividends converts automatically into common stock at the discount.
4. Other outcomes: liquidity event (investor chooses cash or shares), dissolution (repaid ahead of stockholders, pro rata if short), forced conversion if nothing happens by Dec 31, 2017 (subject to a $50M valuation cap).
5. Investor status: no voting or stockholder rights until shares are issued. Must certify as accredited, sophisticated (with a purchaser representative if needed) or non-U.S., and complete anti-money-laundering forms."""

GENERAL_RULE = ("Include every dollar amount and cap in the offering outlined in the contract, "
                "alongside terms specifics.")

SETUPS = {
    1: {"name": "Setup 1: bare instruction", "system": None,
        "instruction": BARE_INSTRUCTION},
    2: {"name": "Setup 2: rubric in system prompt", "system": RUBRIC_SYSTEM_PROMPT,
        "instruction": BARE_INSTRUCTION},
    3: {"name": "Setup 3: bare instruction + general rule", "system": None,
        "instruction": BARE_INSTRUCTION + " " + GENERAL_RULE},
}

# Rubric line 6 (length): under 150 words = 1, 150 or more = 0.
MAX_WORDS = 150


def length_point(run_record):
    return 1 if run_record["words"] < MAX_WORDS else 0


# Matches the $5M offering amount ("$5 million", "$5,000,000", "$5M"), but not "$50 million".
FIVE_MILLION = re.compile(r"\$\s?5(?:\.0+)?\s?(?:million\b|M\b)|\$5,000,000\b|\bfive million\b", re.I)


def load_api_key():
    """Read ANTHROPIC_API_KEY from ~/code/.env. The key is never printed."""
    for line in ENV_FILE.read_text().splitlines():
        if line.strip().startswith("ANTHROPIC_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
            if key:
                return key
    sys.exit(f"ANTHROPIC_API_KEY is missing or empty in {ENV_FILE}.")


def run(which):
    """which = "first" (run 1 of each setup) or "rest" (runs 2-5 of each setup)."""
    runs = json.loads(RUNS_FILE.read_text()) if RUNS_FILE.exists() else []
    run_numbers = [1] if which == "first" else list(range(2, RUNS_PER_SETUP + 1))
    if any(r["run"] in run_numbers for r in runs):
        sys.exit(f"Those runs are already in {RUNS_FILE.name}. Delete it to start over.")
    if which == "rest" and not runs:
        sys.exit("Do the first round first: three_setups.py run first")
    client = anthropic.Anthropic(api_key=load_api_key())
    contract = CONTRACT.read_text()
    new_cost = 0.0

    for setup_id, setup in SETUPS.items():
        for n in run_numbers:
            request = {
                "model": MODEL,
                "max_tokens": 1024,
                "thinking": {"type": "disabled"},
                "messages": [{"role": "user", "content": setup["instruction"] + "\n\n" + contract}],
            }
            if setup["system"]:
                request["system"] = setup["system"]
            try:
                response = client.messages.create(**request)
            except anthropic.APIStatusError as e:
                sys.exit(f"API error {e.status_code}: {e.message}")
            except anthropic.APIConnectionError:
                sys.exit("Could not reach the Anthropic API. Check your internet connection.")

            summary = "".join(b.text for b in response.content if b.type == "text").strip()
            in_tok, out_tok = response.usage.input_tokens, response.usage.output_tokens
            cost = (in_tok * INPUT_PRICE + out_tok * OUTPUT_PRICE) / 1_000_000
            runs.append({"setup": setup_id, "run": n, "input_tokens": in_tok, "output_tokens": out_tok,
                         "cost": cost, "words": len(summary.split()), "summary": summary})
            new_cost += cost
            print(f"Setup {setup_id}, run {n}: {in_tok} input, {out_tok} output, ${cost:.6f}")

    runs.sort(key=lambda r: (r["setup"], r["run"]))
    RUNS_FILE.write_text(json.dumps(runs, indent=2))
    lines = ["# Three setups: SAFE summaries (Haiku 5.5, thinking off)", ""]
    for setup_id, setup in SETUPS.items():
        lines += [f"## {setup['name']}", ""]
        for r in (r for r in runs if r["setup"] == setup_id):
            lines += [f"### Setup {setup_id}, run {r['run']} ({r['words']} words)", "", r["summary"], ""]
    SUMMARIES_FILE.write_text("\n".join(lines))
    print(f"\nCost of these runs: ${new_cost:.6f} ({len(runs)} runs saved so far)")
    print(f"Saved {SUMMARIES_FILE.name} and {RUNS_FILE.name}. Scores are not shown yet.")


def report():
    runs = json.loads(RUNS_FILE.read_text())
    scores = json.loads(SCORES_FILE.read_text()) if SCORES_FILE.exists() else {}
    lines = [
        "",
        "## Results per run",
        "",
        "| Setup | Run | Input tokens | Output tokens | Cost | Words | Facts (out of 5) | Length <150 words | Total (out of 6) | Includes $5M offering? |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in runs:
        key = f"{r['setup']}-{r['run']}"
        score = scores.get(key)
        length_pt = length_point(r)
        total = "—" if score is None else score + length_pt
        has_5m = "Yes" if FIVE_MILLION.search(r["summary"]) else "No"
        lines.append(f"| {r['setup']} | {r['run']} | {r['input_tokens']:,} | {r['output_tokens']:,} "
                     f"| ${r['cost']:.6f} | {r['words']} | {'—' if score is None else score} | {length_pt} "
                     f"| {total} | {has_5m} |")
    lines += ["", "## Per setup", "",
              "| Setup | Input tokens (avg) | Output tokens (avg) | Total cost (5 runs) | Avg total (out of 6) | Runs with $5M |",
              "|---|---|---|---|---|---|"]
    for setup_id, setup in SETUPS.items():
        rs = [r for r in runs if r["setup"] == setup_id]
        got = [scores[f"{setup_id}-{r['run']}"] + length_point(r) for r in rs if f"{setup_id}-{r['run']}" in scores]
        avg_score = f"{sum(got) / len(got):.1f}" if got else "—"
        with_5m = sum(1 for r in rs if FIVE_MILLION.search(r["summary"]))
        lines.append(f"| {setup['name']} | {sum(r['input_tokens'] for r in rs) / len(rs):,.0f} "
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
        sys.exit("Usage: three_setups.py run first | run rest | report")
