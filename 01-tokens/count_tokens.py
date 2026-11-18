"""
Token experiment script.

Sends text to Claude Haiku 5.5 (the cheapest Claude model), prints how many
input and output tokens the call used, and adds a row to results.md with
your prediction next to the actual numbers.

How to run (from the repo folder):
    01-tokens/.venv/bin/python 01-tokens/count_tokens.py "Say hi"
    01-tokens/.venv/bin/python 01-tokens/count_tokens.py --file some.txt
    01-tokens/.venv/bin/python 01-tokens/count_tokens.py "Say hi" --label "Tiny prompt" --predict-in 10 --predict-out 5

If you leave out --predict-in / --predict-out, the script asks you for them.
"""

import argparse
import datetime
import os
import sys
from pathlib import Path

import anthropic

MODEL = "claude-haiku-5-5"
# Prices in US dollars per 1 million tokens (Haiku 5.5, prompts under 100K tokens).
INPUT_PRICE_PER_MILLION = 0.10
OUTPUT_PRICE_PER_MILLION = 0.50

ENV_FILE = Path.home() / "code" / ".env"
RESULTS_FILE = Path(__file__).parent / "results.md"


def load_api_key():
    """Read ANTHROPIC_API_KEY from ~/code/.env. The key is never printed."""
    if not ENV_FILE.exists():
        sys.exit(f"Could not find {ENV_FILE}. Put ANTHROPIC_API_KEY=... in it.")
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("ANTHROPIC_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
            if key:
                return key
    sys.exit(f"ANTHROPIC_API_KEY is missing or empty in {ENV_FILE}.")


def ask_number(question):
    """Ask for a prediction. Blank answer means 'no prediction'."""
    if not sys.stdin.isatty():
        return None
    answer = input(question).strip()
    return int(answer) if answer.isdigit() else None


def append_result(label, predicted_in, predicted_out, actual_in, actual_out, cost, notes):
    def show(n):
        return "—" if n is None else str(n)

    date = datetime.date.today().isoformat()
    cost_text = "hidden" if cost is None else f"${cost:.6f}"
    row = (
        f"| {date} | {label} | {show(predicted_in)} | {actual_in} "
        f"| {show(predicted_out)} | {actual_out} | {cost_text} | {notes} |\n"
    )
    with RESULTS_FILE.open("a") as f:
        f.write(row)


def main():
    parser = argparse.ArgumentParser(description="Send text to Claude and count tokens.")
    parser.add_argument("text", nargs="?", help="The text to send to Claude.")
    parser.add_argument("--file", help="Send the contents of this file instead.")
    parser.add_argument("--label", help="A short name for this experiment (goes in results.md).")
    parser.add_argument("--predict-in", type=int, help="Your guess for input tokens.")
    parser.add_argument("--predict-out", type=int, help="Your guess for output tokens.")
    parser.add_argument("--max-tokens", type=int, default=1024,
                        help="Upper limit on output tokens (default 1024).")
    parser.add_argument("--think", action="store_true",
                        help="Let Claude 'think' before answering. Thinking tokens count as output tokens.")
    parser.add_argument("--notes", default="", help="Anything to remember about this run.")
    parser.add_argument("--instruction",
                        help="A request placed before the text, e.g. 'Summarize this in one paragraph.'")
    parser.add_argument("--count-only", action="store_true",
                        help="Only count input tokens (free). Claude does not write a reply.")
    parser.add_argument("--hide-cost", action="store_true",
                        help="Don't show the cost on screen or in results.md.")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text()
    elif args.text:
        text = args.text
    else:
        parser.error("Give some text in quotes, or use --file.")
    if args.instruction:
        text = args.instruction + "\n\n" + text

    label = args.label or (text[:40].replace("\n", " ").replace("|", "/") + ("…" if len(text) > 40 else ""))

    # Predictions: from the command line, or ask now (before the call happens).
    predicted_in = args.predict_in if args.predict_in is not None else ask_number("Your prediction for INPUT tokens (blank to skip): ")
    predicted_out = None
    if not args.count_only:
        predicted_out = args.predict_out if args.predict_out is not None else ask_number("Your prediction for OUTPUT tokens (blank to skip): ")

    client = anthropic.Anthropic(api_key=load_api_key())
    thinking = {"type": "adaptive"} if args.think else {"type": "disabled"}

    if args.count_only:
        try:
            counted = client.messages.count_tokens(
                model=MODEL,
                thinking=thinking,
                messages=[{"role": "user", "content": text}],
            )
        except anthropic.APIStatusError as e:
            sys.exit(f"API error {e.status_code}: {e.message}")
        except anthropic.APIConnectionError:
            sys.exit("Could not reach the Anthropic API. Check your internet connection.")
        actual_in = counted.input_tokens
        print("\n--- Tokens (count only, no reply generated) ---")
        print(f"Model:          {MODEL}")
        print(f"Input tokens:   {actual_in}" + (f"   (you predicted {predicted_in})" if predicted_in is not None else ""))
        append_result(label, predicted_in, None, actual_in, "— (count only)", None,
                      ("count only. " + args.notes).strip().replace("|", "/"))
        print(f"\nSaved to {RESULTS_FILE.name}")
        return

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=args.max_tokens,
            # Thinking is off unless you pass --think, so output tokens = only the visible reply.
            thinking=thinking,
            messages=[{"role": "user", "content": text}],
        )
    except anthropic.AuthenticationError as e:
        sys.exit(f"The API rejected your key ({e.message}). Check ANTHROPIC_API_KEY in ~/code/.env.")
    except anthropic.RateLimitError:
        sys.exit("Rate limited (too many requests). Wait a minute and try again.")
    except anthropic.APIStatusError as e:
        sys.exit(f"API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        sys.exit("Could not reach the Anthropic API. Check your internet connection.")

    reply = "".join(block.text for block in response.content if block.type == "text")
    actual_in = response.usage.input_tokens
    actual_out = response.usage.output_tokens
    cost = (actual_in * INPUT_PRICE_PER_MILLION + actual_out * OUTPUT_PRICE_PER_MILLION) / 1_000_000

    print("\n--- Claude's reply ---")
    print(reply)
    print("\n--- Tokens ---")
    print(f"Model:          {MODEL}{'  (thinking on)' if args.think else ''}")
    print(f"Input tokens:   {actual_in}" + (f"   (you predicted {predicted_in})" if predicted_in is not None else ""))
    print(f"Output tokens:  {actual_out}" + (f"   (you predicted {predicted_out})" if predicted_out is not None else ""))
    if not args.hide_cost:
        print(f"Cost:           ${cost:.6f}")
    if response.stop_reason == "max_tokens":
        print("Note: the reply was cut off because it hit --max-tokens.")

    notes = args.notes
    if args.think:
        notes = ("thinking on. " + notes).strip()
    if response.stop_reason == "max_tokens":
        notes = (notes + " cut off at max-tokens").strip()
    append_result(label, predicted_in, predicted_out, actual_in, actual_out,
                  None if args.hide_cost else cost, notes.replace("|", "/"))
    print(f"\nSaved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
