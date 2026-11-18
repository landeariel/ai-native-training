# Token experiments

Model: Claude Haiku 5.5 (`claude-haiku-5-5`). Price: $0.10 per million input tokens, $0.50 per million output tokens.

Before each run, write down a prediction. The script adds one row per run.

| Date | Experiment | Predicted input | Actual input | Predicted output | Actual output | Cost | Notes |
|---|---|---|---|---|---|---|---|
| 2026-11-17 | Email - English | 225 | 269 | — | 552 | $0.000303 | 142 words |
| 2026-11-17 | Email - Spanish | 575 | 350 | — | 779 | $0.000425 | 149 words, no accent marks |
| 2026-11-17 | Email - Spanish with accents | 365 | 344 | — | 909 | $0.000489 | 149 words, 17 accents, plus 3 small non-accent edits |
| 2026-11-17 | SAFE contract (input only) | 16300 | 16265 | — | — (count only) | $0 (free) | count only. 7155 words, headers/footers removed |
| 2026-11-17 | SAFE contract summary (100 words) | — | 16289 | 227 | 325 | $0.001791 | 7155-word contract + instruction. Reply was 142 words, not 100 |

## Contract experiment: cost predictions

| Call | Predicted cost | Actual cost | Why the difference |
|---|---|---|---|
| Count-only check | $0.001625 | $0 | Token counting is free |
| Summary call, input (16,289 tokens) | $0.001625 | $0.0016289 | Used 16,250 tokens instead of 16,289 |
| Summary call, output (325 tokens) | $0.0001625 | $0.0001625 | Exact |
| **Summary call, total** | **$0.0017875** | **$0.0017914** | Off by 0.2% |

Input was 98% of the tokens and 91% of the cost. Output tokens cost 5× more each, but the reply was short.

## Experiment 4 (preview): Haiku 5.5 vs. Fable 5.2, same contract summary

I calculated the Fable 5.2 costs by hand. Nothing was sent to Fable. Both models use the same token counts from the Haiku run: 16,289 input, 325 output.

| Model | Input price (per million) | Output price (per million) | Input cost | Output cost | Cost per summary | Cost per 1,000 summaries |
|---|---|---|---|---|---|---|
| Haiku 5.5 (actual) | $0.10 | $0.50 | $0.0016289 | $0.0001625 | $0.0017914 | **$1.79** |
| Fable 5.2 (by hand) | $8.00 | $40.00 | $0.13 | $0.013 | $0.143 | **$143** |

Fable 5.2 costs **80× more** for the same tokens: $1.79 vs. $143 per 1,000 summaries.

Caveats:
- This assumes Fable would use the same number of tokens. It may not. Fable always "thinks" before it answers, and those thinking tokens are billed as output at $40 per million, so a real Fable run would likely cost more than $0.143. Its tokenizer may also split text differently. A real call would settle it.
- I checked the summary's quality by reading it myself, not with an eval. An eval is a structured test that scores outputs against agreed criteria. So "is Fable's summary worth 80× more?" is still an open question.

## Conversation turns experiment (2026-11-17)

System prompt on every call: "Answer every question in exactly one sentence."

| Call | Question | Messages sent | Predicted input | Actual input | Predicted output | Actual output | Reply |
|---|---|---|---|---|---|---|---|
| 1. Turn 1 | What is the capital of Argentina? | 1 | 19 | 33 | 10 | 19 | The capital of Argentina is Buenos Aires. |
| 2. Turn 2 | What is the tallest mountain in South America? | 3 | 41 | 69 | 12 | 47 | The tallest mountain in South America is Aconcagua, located in Argentina, which rises to about 6,961 meters (22,838 feet). |
| 3. Turn 3 | What was the first thing I asked you? | 5 | 65 | 131 | 9 | 24 | The first thing you asked me was "What is the capital of Argentina?" |
| 4. No history | What was the first thing I asked you? | 1 | 22 | 33 | 6 | 30 | This is the first message you've sent me in our conversation, so there's no earlier question to recall. |

Predicted reply for call 4 (no history): "What is my name?"

### Notes

1. **The prediction's structure was right.** Each call's input = previous input + previous answer + new question.
   - Call 2: 33 + 19 (answer 1) + 17 (Q2) = 69 ✓
   - Call 3: 69 + 47 (answer 2) + 15 (Q3) = 131 ✓
2. **Answers get billed twice.** Each answer is billed once as output, then again as input on every later turn. Turn 3 used 4× the input of turn 1 for a question of the same size, so long chats get more expensive with every turn.
3. **Each item cost about twice the estimate.** Every message carries hidden wrapping that marks who it's from, and the system prompt has some too. In short messages that wrapping outweighs the words: calls 1 and 4 used 33 input tokens for about 14 words. The 1.3 tokens-per-word rule of thumb was also low; earlier experiments measured 1.9–2.3.
4. **"One sentence" didn't keep answers minimal.** Answer 2 added the location and height in meters and feet: 47 tokens vs. a predicted 12. As with the 100-word summary, you can only influence output length, not set it. The output counts also seem higher than the visible words, probably because of a few hidden end-of-reply tokens (not confirmed).
5. **The model has no memory of its own.** With no history, call 4 didn't make up an earlier question (the prediction was "What is my name?"). It said there was nothing to recall. The same question got different answers depending only on the history list. Chat apps "remember" by resending the whole conversation every turn, and that resending is billed.
