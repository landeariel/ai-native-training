"""
Cost model for a SAFE / contract summarizer sold to startup finance teams.

Builds the model from token counts we measured in our experiments (see results.md)
and writes it to 01-tokens/cost_model.md and 01-tokens/cost_model.csv.
No API calls are made. This is arithmetic only.

    01-tokens/.venv/bin/python 01-tokens/cost_model.py

Change any assumption below and re-run to update the model.
"""

import csv
import datetime
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------- business assumptions
PRICE_PER_USER_PER_MONTH = 49.00     # $ we charge each user per month
CONTRACTS_PER_USER_PER_MONTH = 200
FOLLOW_UPS_PER_CONTRACT = 5          # plus 1 summary = 6 API calls per contract

# ---------------------------------------------------------------- measured token counts
# The contract sits in the system prompt: 16,299 tokens (measured, prompt caching experiment).
CONTRACT_TOKENS = 16_299
# Summary request ("Write a one-paragraph synthesis of this contract in 100 words."),
# including hidden message wrapping: 16,289 - 16,265 = 24 tokens (measured).
SUMMARY_REQUEST_TOKENS = 24
# A short follow-up question, including wrapping: Q1 measured at 19 tokens.
QUESTION_TOKENS = 19
# A one-sentence follow-up answer: Haiku averaged 41 output tokens (30, 60, 34).
# Assumed the same for every model (not measured for Sonnet/Opus/Fable).
ANSWER_TOKENS = 41
# Assumption: an earlier answer costs about as many input tokens as it did output tokens.

# ---------------------------------------------------------------- models
# Summary output tokens measured with the least thinking each model allows
# (model comparison, thinking-off run). Scored 4/5 on our eval (2/5 for Haiku
# with default thinking).
# Prices: $ per million tokens. Cache write = 1.25x input (5-minute cache).
MODELS = [
    # name, setting, summary output tokens, input, output, cache write, cache read
    ("Haiku 5.5", "thinking off", 279, 0.10, 0.50, 0.125, 0.01),
    ("Sonnet 5.5", "thinking off", 228, 2.00, 10.00, 2.50, 0.10),
    ("Opus 5.5", "effort low", 224, 4.00, 20.00, 5.00, 0.20),
    ("Fable 5.2", "effort low", 224, 8.00, 40.00, 10.00, 0.20),
]


def tokens_per_call(summary_out, cached):
    """Tokens for each API call on one contract: 1 summary call + the follow-up calls.
    Returns a list of dicts, one per call: name, normal input, cache write, cache read, output."""
    calls = []
    history = SUMMARY_REQUEST_TOKENS  # chat so far, after the contract

    # Call 1: the summary. With caching, the contract is saved to the cache here.
    calls.append({
        "name": "Summary",
        "normal": history + (0 if cached else CONTRACT_TOKENS),
        "written": CONTRACT_TOKENS if cached else 0,
        "read": 0,
        "output": summary_out,
    })
    history += summary_out               # the summary joins the history

    # Calls 2..6: the follow-up questions, each sending the full history.
    for i in range(FOLLOW_UPS_PER_CONTRACT):
        calls.append({
            "name": f"Follow-up {i + 1}",
            "normal": history + QUESTION_TOKENS + (0 if cached else CONTRACT_TOKENS),
            "written": 0,
            "read": CONTRACT_TOKENS if cached else 0,  # re-use the saved contract
            "output": ANSWER_TOKENS,
        })
        history += QUESTION_TOKENS + ANSWER_TOKENS
    return calls


def tokens_per_contract(summary_out, cached):
    """Total tokens for one contract across all calls: (normal input, cache write, cache read, output)."""
    calls = tokens_per_call(summary_out, cached)
    return tuple(sum(c[k] for c in calls) for k in ("normal", "written", "read", "output"))


def money(x, places=4):
    return f"-${-x:,.{places}f}" if x < 0 else f"${x:,.{places}f}"


def main():
    revenue_per_contract = PRICE_PER_USER_PER_MONTH / CONTRACTS_PER_USER_PER_MONTH
    rows = []
    for name, setting, summary_out, p_in, p_out, p_write, p_read in MODELS:
        for cached in (False, True):
            normal, written, read, output = tokens_per_contract(summary_out, cached)
            cost = (normal * p_in + written * p_write + read * p_read + output * p_out) / 1_000_000
            monthly_cost = cost * CONTRACTS_PER_USER_PER_MONTH
            rows.append({
                "Model": name,
                "Setting": setting,
                "Caching": "On" if cached else "Off",
                "Input tokens (normal)": normal,
                "Input tokens (cache write)": written,
                "Input tokens (cache read)": read,
                "Output tokens": output,
                "Contract size (tokens)": CONTRACT_TOKENS,
                "Total tokens": normal + written + read + output,
                "API cost per contract": cost,
                "Revenue per contract": revenue_per_contract,
                "Gross profit per contract": revenue_per_contract - cost,
                "API cost per user per month": monthly_cost,
                "Revenue per user per month": PRICE_PER_USER_PER_MONTH,
                "Gross profit per user per month": PRICE_PER_USER_PER_MONTH - monthly_cost,
                "Gross margin": (revenue_per_contract - cost) / revenue_per_contract,
            })

    # ---- CSV (for a spreadsheet)
    with (HERE / "cost_model.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        for r in rows:
            writer.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})

    # ---- Markdown
    calls = 1 + FOLLOW_UPS_PER_CONTRACT
    lines = [
        "# Cost model: SAFE & contract summarizer",
        "",
        f"Generated by `cost_model.py` on {datetime.date.today().isoformat()}. "
        "Built from token counts measured in `results.md`. Change the assumptions in the script and re-run to update.",
        "",
        "## Assumptions",
        "",
        "| Assumption | Value | Source |",
        "|---|---|---|",
        f"| Price | ${PRICE_PER_USER_PER_MONTH:.2f} per user per month | Business assumption |",
        f"| Contracts | {CONTRACTS_PER_USER_PER_MONTH} per user per month | Business assumption |",
        f"| Revenue per contract | ${revenue_per_contract:.3f} | ${PRICE_PER_USER_PER_MONTH:.0f} ÷ {CONTRACTS_PER_USER_PER_MONTH} |",
        f"| Calls per contract | {calls} (1 summary + {FOLLOW_UPS_PER_CONTRACT} follow-ups, one conversation) | Business assumption |",
        f"| Contract size | {CONTRACT_TOKENS:,} tokens, in the system prompt | Measured (SAFE contract) |",
        f"| Summary request | {SUMMARY_REQUEST_TOKENS} tokens | Measured |",
        f"| Follow-up question | {QUESTION_TOKENS} tokens each | Measured (Q1) |",
        f"| Follow-up answer | {ANSWER_TOKENS} output tokens each, all models | Measured on Haiku; assumed for Sonnet/Opus/Fable |",
        "| Summary length (output) | Haiku 279, Sonnet 228, Opus 224, Fable 224 tokens | Measured, least-thinking runs |",
        "| History | Every call resends the full conversation so far | How the API works |",
        "| Caching | Contract written to cache on the summary call, read on all 5 follow-ups (within 5 minutes) | Prompt caching experiment |",
        "| Gross margin | Revenue minus Claude API cost only (no hosting, support, etc.) | Simplification |",
        "",
        "## Cost model (per contract and per user per month)",
        "",
        f"| Model | Caching | Contract size (tokens) | Tokens billed per contract ({calls} calls) | API cost per contract "
        "| Revenue per contract | Gross profit per contract "
        "| API cost per user/month | Revenue per user/month | Gross profit per user/month | Gross margin |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['Model']} ({r['Setting']}) | {r['Caching']} | {r['Contract size (tokens)']:,} | {r['Total tokens']:,} "
            f"| {money(r['API cost per contract'])} | {money(r['Revenue per contract'], 3)} "
            f"| {money(r['Gross profit per contract'])} | {money(r['API cost per user per month'], 2)} "
            f"| {money(r['Revenue per user per month'], 2)} | {money(r['Gross profit per user per month'], 2)} "
            f"| **{r['Gross margin']:.1%}** |"
        )
    lines += [
        "",
        "Gross margin is the same per contract and per month, because both cost and revenue scale with the number of contracts.",
        "",
        f"\"Tokens billed per contract\" counts all {calls} calls. Every call resends the {CONTRACT_TOKENS:,}-token contract "
        f"plus the conversation so far, so about {calls * CONTRACT_TOKENS:,} of the total is the same contract sent {calls} times. "
        "Caching doesn't change the number of tokens, only their price.",
        "",
        "## Tokens per call",
        "",
        "Each call's input = contract + summary request + every earlier question and answer + the new question.",
        "",
    ]
    for name, setting, summary_out, *_ in MODELS:
        plain = tokens_per_call(summary_out, cached=False)
        cached_calls = tokens_per_call(summary_out, cached=True)
        lines += [
            f"### {name} ({setting})",
            "",
            "| Call | What it is | Input tokens | Output tokens | Total | Caching on: cache write "
            "| Caching on: cache read | Caching on: normal-price input |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for n, (p, c) in enumerate(zip(plain, cached_calls), start=1):
            lines.append(
                f"| {n} | {p['name']} | {p['normal']:,} | {p['output']:,} | {p['normal'] + p['output']:,} "
                f"| {c['written']:,} | {c['read']:,} | {c['normal']:,} |"
            )
        tot = lambda calls_, k: sum(x[k] for x in calls_)
        lines += [
            f"| **All {calls}** | | **{tot(plain, 'normal'):,}** | **{tot(plain, 'output'):,}** "
            f"| **{tot(plain, 'normal') + tot(plain, 'output'):,}** | **{tot(cached_calls, 'written'):,}** "
            f"| **{tot(cached_calls, 'read'):,}** | **{tot(cached_calls, 'normal'):,}** |",
            "",
        ]
    lines += [
        "## Token breakdown per contract",
        "",
        "| Model | Caching | Input (normal price) | Input (cache write) | Input (cache read) | Output | Total |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['Model']} | {r['Caching']} | {r['Input tokens (normal)']:,} | {r['Input tokens (cache write)']:,} "
            f"| {r['Input tokens (cache read)']:,} | {r['Output tokens']:,} | {r['Total tokens']:,} |"
        )
    lines.append("")
    (HERE / "cost_model.md").write_text("\n".join(lines))

    for r in rows:
        print(f"{r['Model']:<11} caching {r['Caching']:<3}  cost/contract {money(r['API cost per contract'])}  "
              f"cost/user/month {money(r['API cost per user per month'], 2):>8}  margin {r['Gross margin']:.1%}")
    print("\nSaved cost_model.md and cost_model.csv")


if __name__ == "__main__":
    main()
