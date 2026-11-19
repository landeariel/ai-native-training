"""
Prompt caching experiment.

A 3-turn conversation with Claude Haiku 5.5 about the SAFE contract. The
contract sits in the system prompt, so it is sent on EVERY turn. Run it twice:

    01-tokens/.venv/bin/python 01-tokens/cache_conversation.py
    01-tokens/.venv/bin/python 01-tokens/cache_conversation.py --cache

With --cache, the contract is marked for caching: turn 1 pays a little extra to
save a copy on Anthropic's side ("cache write"), and later turns re-use that copy
at a 90% discount ("cache read"). Without --cache, every turn pays full price
for the whole contract again.

Add your predicted input cost for turns 2 and 3 with --predict-cost, e.g.
    --predict-cost 0.0016,0.0016
"""

import argparse
import datetime
from pathlib import Path

import anthropic

from count_tokens import RESULTS_FILE, load_api_key

MODEL = "claude-haiku-5-5"
# US dollars per 1 million tokens, Haiku 5.5 (prompts under 100K tokens).
INPUT_PRICE = 0.10            # normal input
CACHE_WRITE_PRICE = 0.125     # 1.25x normal: saving the contract to the cache (5-minute cache)
CACHE_READ_PRICE = 0.01       # 0.1x normal: re-using the saved copy
OUTPUT_PRICE = 0.50

CONTRACT = Path(__file__).parent / "contract" / "contract_clean.txt"
RULE = "Answer every question about the contract below in exactly one sentence."

# Three short, independent questions. Turn 3 does NOT depend on turn 1.
QUESTIONS = [
    "Which company is issuing this SAFE?",
    "What annual dividend rate does the SAFE Preferred Stock accrue?",
    "Which state's law governs this agreement?",
]


def main():
    parser = argparse.ArgumentParser(description="3-turn SAFE conversation, with or without caching.")
    parser.add_argument("--cache", action="store_true", help="Cache the contract after turn 1.")
    parser.add_argument("--predict-cost", help="Predicted INPUT cost for turns 2 and 3, comma-separated.")
    args = parser.parse_args()

    predicted = [None, None, None]
    if args.predict_cost:
        parts = [p.strip().lstrip("$") for p in args.predict_cost.split(",")]
        if len(parts) != 2:
            raise SystemExit("--predict-cost needs 2 numbers: turn 2 and turn 3.")
        predicted[1], predicted[2] = float(parts[0]), float(parts[1])

    # The system prompt: the one-sentence rule plus the whole contract.
    contract_block = {"type": "text", "text": RULE + "\n\n<contract>\n" + CONTRACT.read_text() + "\n</contract>"}
    if args.cache:
        # The cache marker: "save everything up to and including this block."
        contract_block["cache_control"] = {"type": "ephemeral"}
    system = [contract_block]

    client = anthropic.Anthropic(api_key=load_api_key())
    mode = "WITH caching" if args.cache else "WITHOUT caching"
    history = []
    rows = []

    for i, question in enumerate(QUESTIONS):
        history.append({"role": "user", "content": question})
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            thinking={"type": "disabled"},  # keep output tokens = just the visible answer
            system=system,
            messages=history,
        )
        answer = "".join(b.text for b in response.content if b.type == "text")
        history.append({"role": "assistant", "content": answer})

        u = response.usage
        normal = u.input_tokens                              # billed at the normal price
        written = getattr(u, "cache_creation_input_tokens", 0) or 0
        read = getattr(u, "cache_read_input_tokens", 0) or 0
        input_cost = (normal * INPUT_PRICE + written * CACHE_WRITE_PRICE + read * CACHE_READ_PRICE) / 1_000_000
        output_cost = u.output_tokens * OUTPUT_PRICE / 1_000_000
        rows.append((i + 1, question, len(history) - 1, normal, written, read, input_cost,
                     u.output_tokens, output_cost, answer))

    # Print results.
    print(f"\n===== SAFE conversation {mode} =====")
    for (turn, question, sent, normal, written, read, input_cost, out_tok, output_cost, answer) in rows:
        print(f"\nTurn {turn}: {question}")
        print(f"  Reply:               {answer}")
        print(f"  Messages sent:       {sent} (+ system prompt with the contract)")
        print(f"  Input, normal price: {normal} tokens")
        print(f"  Input, cache write:  {written} tokens")
        print(f"  Input, cache read:   {read} tokens")
        print(f"  Input total:         {normal + written + read} tokens")
        pred = predicted[turn - 1]
        print(f"  Input cost:          ${input_cost:.7f}" + (f"   (you predicted ${pred:.7f})" if pred is not None else ""))
        print(f"  Output tokens:       {out_tok}   (output cost ${output_cost:.7f})")

    # Save to results.md.
    date = datetime.date.today().isoformat()
    with RESULTS_FILE.open("a") as f:
        f.write(f"\n### SAFE conversation {mode} ({date})\n\n")
        f.write("| Turn | Question | Messages sent | Input at normal price | Cache write | Cache read "
                "| Input total | Predicted input cost | Actual input cost | Output tokens | Output cost | Reply |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for (turn, question, sent, normal, written, read, input_cost, out_tok, output_cost, answer) in rows:
            pred = predicted[turn - 1]
            pred_text = "—" if pred is None else f"${pred:.7f}"
            reply = answer.replace("|", "/").replace("\n", " ")
            f.write(f"| {turn} | {question} | {sent} | {normal} | {written} | {read} | {normal + written + read} "
                    f"| {pred_text} | ${input_cost:.7f} | {out_tok} | ${output_cost:.7f} | {reply} |\n")
    print(f"\nSaved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
