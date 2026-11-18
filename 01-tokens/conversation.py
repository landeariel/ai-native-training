"""
Conversation-turns experiment.

Holds a 3-turn conversation with Claude Haiku 5.5. The script keeps a list of
every message so far and sends the WHOLE list on every turn, because the model
itself remembers nothing between calls. Then it makes a 4th call that asks the
turn-3 question with NO history, to show what the model "knows" without it.

For each call it prints exactly what was sent, how many messages that was, and
your predicted vs. actual input/output tokens. Results go to results.md.

How to run (from the repo folder):
    01-tokens/.venv/bin/python 01-tokens/conversation.py \
        --predict-in 30,60,90,30 --predict-out 15,15,20,20 \
        --predict-reply "It will say it doesn't know"
"""

import argparse
import datetime

import anthropic

from count_tokens import MODEL, RESULTS_FILE, load_api_key

# The one-sentence rule goes in the system prompt (standing instructions sent
# with every call) so it doesn't get mixed into the questions themselves.
SYSTEM_PROMPT = "Answer every question in exactly one sentence."

QUESTIONS = [
    "What is the capital of Argentina?",
    "What is the tallest mountain in South America?",
    "What was the first thing I asked you?",
]


def parse_numbers(text, count, name):
    """Turn '30,60,90,30' into [30, 60, 90, 30]. Blank or missing means no prediction."""
    if not text:
        return [None] * count
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != count:
        raise SystemExit(f"{name} needs {count} numbers separated by commas, one per call.")
    return [int(p) if p.isdigit() else None for p in parts]


def show(n):
    return "—" if n is None else str(n)


def main():
    parser = argparse.ArgumentParser(description="3-turn conversation + 1 no-history call.")
    parser.add_argument("--predict-in", help="Predicted input tokens for calls 1-4, comma-separated.")
    parser.add_argument("--predict-out", help="Predicted output tokens for calls 1-4, comma-separated.")
    parser.add_argument("--predict-reply", default="", help="What you think call 4 (no history) will say.")
    args = parser.parse_args()

    predicted_in = parse_numbers(args.predict_in, 4, "--predict-in")
    predicted_out = parse_numbers(args.predict_out, 4, "--predict-out")

    client = anthropic.Anthropic(api_key=load_api_key())

    def call(messages):
        return client.messages.create(
            model=MODEL,
            max_tokens=200,
            thinking={"type": "disabled"},  # so output tokens = only the visible answer
            system=SYSTEM_PROMPT,
            messages=messages,
        )

    def print_sent(label, messages):
        print(f"\n===== {label} =====")
        print(f"Sent: system prompt + {len(messages)} message(s)")
        print(f"  [system]    {SYSTEM_PROMPT}")
        for m in messages:
            print(f"  [{m['role']:<9}] {m['content']}")

    rows = []
    history = []  # the running list of messages; grows every turn

    # Calls 1-3: the conversation, sending the full history each time.
    for i, question in enumerate(QUESTIONS):
        history.append({"role": "user", "content": question})
        print_sent(f"Call {i + 1} (turn {i + 1}, with history)", history)
        response = call(history)
        answer = "".join(b.text for b in response.content if b.type == "text")
        history.append({"role": "assistant", "content": answer})
        rows.append((f"{i + 1}. Turn {i + 1}", question, len(history) - 1, response, answer, i))

    # Call 4: the turn-3 question again, but with NO history.
    fresh = [{"role": "user", "content": QUESTIONS[2]}]
    print_sent("Call 4 (turn-3 question, NO history)", fresh)
    if args.predict_reply:
        print(f"  Your prediction for the reply: {args.predict_reply}")
    response = call(fresh)
    answer = "".join(b.text for b in response.content if b.type == "text")
    rows.append(("4. No history", QUESTIONS[2], 1, response, answer, 3))

    # Print results.
    print("\n===== Results =====")
    for label, question, sent, resp, answer, idx in rows:
        print(f"\n{label}: {question}")
        print(f"  Reply:          {answer}")
        print(f"  Messages sent:  {sent} (+ system prompt)")
        print(f"  Input tokens:   {resp.usage.input_tokens}   (you predicted {show(predicted_in[idx])})")
        print(f"  Output tokens:  {resp.usage.output_tokens}   (you predicted {show(predicted_out[idx])})")

    # Save to results.md.
    date = datetime.date.today().isoformat()
    with RESULTS_FILE.open("a") as f:
        f.write(f"\n## Conversation turns experiment ({date})\n\n")
        f.write(f"System prompt on every call: \"{SYSTEM_PROMPT}\"\n\n")
        f.write("| Call | Question | Messages sent | Predicted input | Actual input "
                "| Predicted output | Actual output | Reply |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for label, question, sent, resp, answer, idx in rows:
            reply = answer.replace("|", "/").replace("\n", " ")
            f.write(f"| {label} | {question} | {sent} | {show(predicted_in[idx])} "
                    f"| {resp.usage.input_tokens} | {show(predicted_out[idx])} "
                    f"| {resp.usage.output_tokens} | {reply} |\n")
        if args.predict_reply:
            f.write(f"\nPredicted reply for call 4 (no history): \"{args.predict_reply}\"\n")
    print(f"\nSaved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
