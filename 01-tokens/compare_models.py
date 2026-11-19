"""
Model comparison experiment.

Sends the same contract + the same 100-word-summary instruction to one Claude
model, times the call, and records tokens, seconds and cost.

Each model uses its own default thinking settings (no thinking parameter sent).
Thinking tokens are billed as output tokens, so they show up in the output count.

How to run (from the repo folder), one model at a time:
    01-tokens/.venv/bin/python 01-tokens/compare_models.py haiku
    01-tokens/.venv/bin/python 01-tokens/compare_models.py sonnet
    01-tokens/.venv/bin/python 01-tokens/compare_models.py opus
    01-tokens/.venv/bin/python 01-tokens/compare_models.py fable
"""

import sys
import time
from pathlib import Path

import anthropic

from count_tokens import RESULTS_FILE, load_api_key

# name: (model ID, input $ per million tokens, output $ per million tokens)
MODELS = {
    "haiku": ("claude-haiku-5-5", 0.10, 0.50),
    "sonnet": ("claude-sonnet-5-5", 2.00, 10.00),
    "opus": ("claude-opus-5-5", 4.00, 20.00),
    "fable": ("claude-fable-5-2", 8.00, 40.00),
}

CONTRACT = Path(__file__).parent / "contract" / "contract_clean.txt"
INSTRUCTION = "Write a one-paragraph synthesis of this contract in 100 words."
SUMMARIES_FILE = Path(__file__).parent / "model_summaries.md"
MAX_OUTPUT_TOKENS = 32000  # spending ceiling per call


# "off" mode: the least thinking each model allows.
# Haiku can turn thinking off. Sonnet 5.5 turns it off with "between_tools" (no tools here,
# so no thinking). Opus 5.5 and Fable 5.2 can't turn it off, so we use the lowest effort.
OFF_SETTINGS = {
    "haiku": ({"thinking": {"type": "disabled"}}, "thinking off"),
    "sonnet": ({"thinking": {"type": "between_tools"}}, "thinking off (between_tools)"),
    "opus": ({"extra_body": {"output_config": {"effort": "low"}}}, "effort low (can't turn off)"),
    "fable": ({"extra_body": {"output_config": {"effort": "low"}}}, "effort low (can't turn off)"),
}


def main():
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in MODELS or sys.argv[2:] not in ([], ["off"]):
        sys.exit(f"Usage: compare_models.py {'|'.join(MODELS)} [off]")
    name = sys.argv[1]
    off = sys.argv[2:] == ["off"]
    model, in_price, out_price = MODELS[name]
    extra, setting = OFF_SETTINGS[name] if off else ({}, "default thinking")

    text = INSTRUCTION + "\n\n" + CONTRACT.read_text()
    client = anthropic.Anthropic(api_key=load_api_key())

    print(f"Sending the contract to {model} [{setting}]... (this can take a while)")
    start = time.perf_counter()
    try:
        # Streaming keeps long responses from timing out; we just wait for the final message.
        with client.messages.stream(
            model=model,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": text}],
            **extra,
        ) as stream:
            response = stream.get_final_message()
    except anthropic.APIStatusError as e:
        sys.exit(f"API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        sys.exit("Could not reach the Anthropic API. Check your internet connection.")
    seconds = time.perf_counter() - start

    if response.stop_reason == "refusal":
        sys.exit(f"{model} declined the request (stop_reason: refusal). Nothing recorded.")

    reply = "".join(b.text for b in response.content if b.type == "text").strip()
    in_tok = response.usage.input_tokens
    out_tok = response.usage.output_tokens
    in_cost = in_tok * in_price / 1_000_000
    out_cost = out_tok * out_price / 1_000_000
    words = len(reply.split())

    print(f"\n--- {model} reply ({words} words) ---\n{reply}\n")
    print(f"Input tokens:   {in_tok}")
    print(f"Output tokens:  {out_tok}   (includes any thinking tokens)")
    print(f"Input cost:     ${in_cost:.7f}")
    print(f"Output cost:    ${out_cost:.7f}")
    print(f"Total cost:     ${in_cost + out_cost:.7f}")
    print(f"Seconds:        {seconds:.1f}")
    if response.stop_reason == "max_tokens":
        print("Note: hit the output ceiling; the reply was cut off.")

    note = f"{setting}; {words}-word reply" + ("; cut off at ceiling" if response.stop_reason == "max_tokens" else "")
    with RESULTS_FILE.open("a") as f:
        f.write(f"| {name.capitalize()} (`{model}`) | {in_tok} | {out_tok} | ${in_cost:.7f} "
                f"| ${out_cost:.7f} | ${in_cost + out_cost:.7f} | {seconds:.1f} | {note} |\n")
    with SUMMARIES_FILE.open("a") as f:
        f.write(f"\n## {name.capitalize()} (`{model}`, {setting}): {words} words, {out_tok} output tokens, {seconds:.1f}s\n\n{reply}\n")
    print(f"\nSaved to {RESULTS_FILE.name} and {SUMMARIES_FILE.name}")


if __name__ == "__main__":
    main()
