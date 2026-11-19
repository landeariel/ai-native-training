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

## Model comparison experiment (2026-11-18)

Same contract (`contract_clean.txt`) and same instruction ("Write a one-paragraph synthesis of this contract in 100 words.") sent to four models. Each model uses its default thinking settings. Thinking tokens are billed as output. Output is capped at 32,000 tokens per call. The full summaries are in `model_summaries.md`.

**Hypothesis:** each model's reasoning scales output tokens and time in proportion to its output price. (I expect this to be wrong, but I want to see the orders of magnitude.)

### Predictions

| Model | Input tokens | Output tokens | Input cost | Output cost | Total | Seconds |
|---|---|---|---|---|---|---|
| Haiku 5.5 | 16289 | 325 | $0.0016289 | $0.0001625 | $0.0017914 | 20 |
| Sonnet 5.5 | 16289 | 6500 | $0.0325780 | $0.0650000 | $0.0975780 | 400 |
| Opus 5.5 | 16289 | 13000 | $0.0651560 | $0.2600000 | $0.3251560 | 800 |
| Fable 5.2 | 16289 | 26000 | $0.1303120 | $1.0400000 | $1.1703120 | 1600 |

### Actual

| Model | Input tokens | Output tokens | Input cost | Output cost | Total | Seconds | Notes |
|---|---|---|---|---|---|---|---|
| Haiku (`claude-haiku-5-5`) | 16291 | 2824 | $0.0016291 | $0.0014120 | $0.0030411 | 10.6 | 100-word reply |
| Sonnet (`claude-sonnet-5-5`) | 16291 | 1527 | $0.0325820 | $0.0152700 | $0.0478520 | 10.3 | 99-word reply |
| Opus (`claude-opus-5-5`) | 16291 | 1189 | $0.0651640 | $0.0237800 | $0.0889440 | 10.7 | 101-word reply |
| Fable (`claude-fable-5-2`) | 16291 | 1374 | $0.1303280 | $0.0549600 | $0.1852880 | 12.1 | 100-word reply |

### Predicted vs. actual

| Model | Output tokens (pred → actual) | Total cost (pred → actual) | Seconds (pred → actual) | Cost per 1,000 summaries (actual) |
|---|---|---|---|---|
| Haiku 5.5 | 325 → **2,824** | $0.0018 → **$0.0030** | 20 → **10.6** | $3.04 |
| Sonnet 5.5 | 6,500 → **1,527** | $0.0976 → **$0.0479** | 400 → **10.3** | $47.85 |
| Opus 5.5 | 13,000 → **1,189** | $0.3252 → **$0.0889** | 800 → **10.7** | $88.94 |
| Fable 5.2 | 26,000 → **1,374** | $1.1703 → **$0.1853** | 1,600 → **12.1** | $185.29 |
| **All four** | | **$1.59 → $0.33** | **2,820 → 43.7** | |

### Notes

1. **The hypothesis was wrong, as expected.** Output tokens didn't grow with price. Haiku, the cheapest, used the most (2,824). Sonnet, Opus and Fable each used 1,200–1,500. The pricier models seem to need less thinking for a task this simple.
2. **Time was flat.** Every model took 10–12 seconds, not 20 to 1,600. ~~For a short task, most of the wait is probably reading the 16,000-token contract and the round trip, not the thinking.~~ **Corrected by the thinking-off run below:** without thinking, the same calls took 2–3 seconds, so most of the 10–12 seconds *was* thinking.
3. **Price per token drives the cost gap.** All four models counted the same 16,291 input tokens, so on input the gap is just the price difference: Fable's input costs 80× Haiku's. Overall Fable was 61× Haiku's cost, not 80×, because Haiku spent more on thinking.
4. **Input dominates on the big models.** Input was 70% of Fable's cost and 73% of Opus's. For Haiku it was about 54%, because of its heavy thinking.
5. **Yesterday's by-hand Fable estimate was too low, as the caveat warned.** It was $0.143 assuming 325 output tokens. Actual: $0.185, because Fable's thinking added about 1,000 output tokens.
6. **Thinking fixed the word count.** With thinking off, Haiku wrote 142 words for a 100-word request. With thinking on, all four landed at 99–101 words. Thinking cost Haiku about 2,500 extra output tokens, but it followed the instruction.
7. **Input was 16,291, not 16,289.** The 2-token difference likely comes from the thinking setting. Earlier runs sent "thinking off"; these runs used each model's default.
8. **Quality:** the four summaries are in `model_summaries.md`, checked by reading, not with an eval. Haiku's leaves out the $5 million offering size that the other three mention.

## Model comparison, thinking off (2026-11-18)

Same contract and instruction, with the least thinking each model allows. Haiku and Sonnet have thinking off. Opus 5.5 and Fable 5.2 can't turn thinking off, so they run at effort `low`. No predictions this round.

| Model | Input tokens | Output tokens | Input cost | Output cost | Total | Seconds | Notes |
|---|---|---|---|---|---|---|---|
| Haiku (`claude-haiku-5-5`) | 16289 | 279 | $0.0016289 | $0.0001395 | $0.0017684 | 1.8 | thinking off; 120-word reply |
| Sonnet (`claude-sonnet-5-5`) | 16289 | 228 | $0.0325780 | $0.0022800 | $0.0348580 | 2.2 | thinking off (between_tools); 103-word reply |
| Opus (`claude-opus-5-5`) | 16291 | 224 | $0.0651640 | $0.0044800 | $0.0696440 | 3.3 | effort low (can't turn off); 103-word reply |
| Fable (`claude-fable-5-2`) | 16291 | 224 | $0.1303280 | $0.0089600 | $0.1392880 | 2.7 | effort low (can't turn off); 102-word reply |

### Default thinking vs. thinking off

| Model | Output tokens (default → off) | Seconds (default → off) | Total cost (default → off) | Cost saved | Words (default → off) |
|---|---|---|---|---|---|
| Haiku 5.5 | 2,824 → 279 | 10.6 → 1.8 | $0.0030 → $0.0018 | 42% | 100 → 120 |
| Sonnet 5.5 | 1,527 → 228 | 10.3 → 2.2 | $0.0479 → $0.0349 | 27% | 99 → 103 |
| Opus 5.5 (effort low) | 1,189 → 224 | 10.7 → 3.3 | $0.0889 → $0.0696 | 22% | 101 → 103 |
| Fable 5.2 (effort low) | 1,374 → 224 | 12.1 → 2.7 | $0.1853 → $0.1393 | 25% | 100 → 102 |

### Notes

1. **Thinking was most of the wait.** Without it, every call took 2–3 seconds instead of 10–12, about 4–6× faster. This corrects note 2 of the previous experiment, which guessed that reading the contract was the slow part.
2. **Output tokens fell 5–10×, but cost fell only 22–42%.** Input (the 16,000-token contract) didn't change, and it's most of the bill on the bigger models. Turning thinking off only cuts the output side.
3. **At effort `low`, Opus and Fable barely thought.** Both used 224 output tokens, about what a 100-word reply costs by itself, so on this easy task "low" was close to off.
4. **Without thinking, the bigger models still mostly hit the word count; Haiku didn't.** Sonnet, Opus and Fable wrote 102–103 words. Haiku wrote 120 (142 in its first thinking-off run). For Haiku, thinking is what made it follow the 100-word instruction.
5. **The 2-token input difference is explained.** Haiku and Sonnet with thinking off counted 16,289 input tokens. Opus and Fable, still thinking at low effort, counted 16,291. Having thinking on adds 2 input tokens.
6. **The cheapest and most expensive options are now 105× apart:** Haiku with thinking off ($1.77 per 1,000 summaries) vs. Fable with default thinking ($185.29 per 1,000).

### Haiku 5.5: thinking on vs. thinking off

(This was planned as its own prediction experiment. The runs above already covered it, so no predictions were made.)

| | Thinking on (default) | Thinking off | Difference |
|---|---|---|---|
| Input tokens | 16,291 | 16,289 | +2 with thinking on |
| Output tokens | 2,824 | 279 | **10.1×** more with thinking on |
| Input cost | $0.0016291 | $0.0016289 | about the same |
| Output cost | $0.0014120 | $0.0001395 | **10.1×** more with thinking on |
| **Total cost** | **$0.0030411** | **$0.0017684** | **1.7×** more with thinking on |
| Cost per 1,000 summaries | $3.04 | $1.77 | +$1.27 |
| Seconds | 10.6 | 1.8 | **5.9×** slower with thinking on |
| Words in reply (asked for 100) | 100 | 120 | thinking on followed the limit |

## Prompt caching experiment (2026-11-18)

A 3-turn conversation with Haiku 5.5 (thinking off) about the SAFE contract. The contract is in the system prompt (16,299 tokens, measured with the free counter), so it's sent on every turn. The full chat history is sent each turn too. It was run twice: without caching, then with the contract cached. Caching prices for Haiku 5.5: cache write $0.125/M (1.25× normal), cache read $0.01/M (0.1× normal), normal input $0.10/M.

### SAFE conversation WITHOUT caching (2026-11-18)

| Turn | Question | Messages sent | Input at normal price | Cache write | Cache read | Input total | Predicted input cost | Actual input cost | Output tokens | Output cost | Reply |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Which company is issuing this SAFE? | 1 | 16318 | 0 | 0 | 16318 | — | $0.0016318 | 30 | $0.0000150 | YayYo, Inc., a Delaware corporation, is issuing this SAFE. |
| 2 | What annual dividend rate does the SAFE Preferred Stock accrue? | 3 | 16377 | 0 | 0 | 16377 | $0.0016440 | $0.0016377 | 60 | $0.0000300 | The SAFE Preferred Stock accrues a dividend at 8% per annum on the Purchase Amount, from the Sale Date until an Event described in Section 1 occurs. |
| 3 | Which state's law governs this agreement? | 5 | 16453 | 0 | 0 | 16453 | $0.0016501 | $0.0016453 | 34 | $0.0000170 | This agreement is governed by the laws of the State of California, without regard to conflict-of-laws principles. |

### SAFE conversation WITH caching (2026-11-18)

| Turn | Question | Messages sent | Input at normal price | Cache write | Cache read | Input total | Predicted input cost | Actual input cost | Output tokens | Output cost | Reply |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Which company is issuing this SAFE? | 1 | 19 | 16299 | 0 | 16318 | — | $0.0020393 | 30 | $0.0000150 | YayYo, Inc., a Delaware corporation, is issuing this SAFE. |
| 2 | What annual dividend rate does the SAFE Preferred Stock accrue? | 3 | 78 | 0 | 16299 | 16377 | $0.0001644 | $0.0001708 | 60 | $0.0000300 | The SAFE Preferred Stock accrues a dividend at 8% per annum on the Purchase Amount, from the Sale Date until an Event described in Section 1 occurs. |
| 3 | Which state's law governs this agreement? | 5 | 154 | 0 | 16299 | 16453 | $0.0001650 | $0.0001784 | 34 | $0.0000170 | This agreement is governed by the laws of the State of California, without regard to conflict-of-laws principles. |

### Predicted vs. actual

| Turn | Input tokens (pred → actual) | Input cost without caching (pred → actual) | Input cost with caching (pred → actual) | Without ÷ with (pred → actual) |
|---|---|---|---|---|
| 1 | 16,376 → 16,318 | $0.0016376 → $0.0016318 | $0.0020470 → $0.0020393 | 0.8 → **0.80** |
| 2 | 16,440 → 16,377 | $0.0016440 → $0.0016377 | $0.0001644 → $0.0001708 | 10 → **9.6** |
| 3 | 16,501 → 16,453 | $0.0016501 → $0.0016453 | $0.0001650 → $0.0001784 | 10 → **9.2** |
| **All 3 turns** | | **$0.0049148** | **$0.0023885** | **2.1×** (51% saved) |

Output tokens were predicted at 50 per turn. Actual: 30, 60, 34. The answers were word-for-word identical in both runs.

### Notes

1. **Turn 1 costs more with caching (0.8×).** Saving the contract to the cache costs 1.25× the normal price. The prediction got this exactly.
2. **The extra cost pays off on turn 2.** Turn 1's extra $0.0004 is far less than turn 2's saving of $0.0015. Caching pays off as soon as the saved copy is reused once.
3. **Only the cached part gets the discount.** The ratio was 9.6 and then 9.2, not 10, because only the 16,299-token system prompt was cached. The chat history after it (78 tokens on turn 2, 154 on turn 3) was billed at the normal price. That uncached part grows every turn, so the ratio slowly falls. (The predictions applied the 0.1× discount to the whole input.)
4. **Token totals were close.** Each prediction was about 50–60 tokens high. Turn 1's 16,318 already included question 1, so adding Q1 again double-counted it.
5. **Over 3 turns, caching cut input cost in half (51%).** Each extra turn adds about $0.0016 without caching vs. about $0.0002 with it, so longer conversations get closer to the 90% maximum saving.
6. **Caching doesn't change the answers.** It only changes how the input is billed. Both runs gave word-for-word identical replies.
7. **Saved copies expire.** This cache lasts 5 minutes after its last use. A conversation with long pauses would pay the write cost again.

### Revised predictions (made after the run)

These correct the double-counted Q1 by starting from the 16,299-token system prompt alone.

| Turn | Input tokens (revised pred → actual) | Input cost without caching (revised pred → actual) | Input cost with caching (revised pred → actual) | Without ÷ with (pred → actual) |
|---|---|---|---|---|
| 1 | 16,357 → 16,318 | $0.0016357 → $0.0016318 | $0.0020446 → $0.0020393 | 0.8 → 0.80 |
| 2 | 16,421 → 16,377 | $0.0016421 → $0.0016377 | $0.0001642 → $0.0001708 | 10 → 9.6 |
| 3 | 16,482 → 16,453 | $0.0016482 → $0.0016453 | $0.0001648 → $0.0001784 | 10 → 9.2 |

**Why each turn is still about 30–45 tokens high:** each turn's prediction includes that turn's own answer (50 tokens). A turn's input can't include its own answer, because the answer doesn't exist yet when the turn is sent. It joins the history and becomes input on the *next* turn. Without it, the predictions are 16,307 / 16,371 / 16,432 vs. actual 16,318 / 16,377 / 16,453. What's left is the hidden per-message wrapping: Q1 counted as 19 tokens, not 8.

**Rule:** turn N's input = system prompt + every question and answer *before* turn N + turn N's question.

### Final predictions (third round, made after the run)

| Turn | Input tokens (pred → actual) | Input cost without caching (pred → actual) | Input cost with caching (pred → actual) | Without ÷ with (pred → actual) |
|---|---|---|---|---|
| 1 | 16,307 → 16,318 (−11) | $0.0016307 → $0.0016318 | $0.0020384 → $0.0020393 | 0.8 → 0.80 |
| 2 | 16,371 → 16,377 (−6) | $0.0016371 → $0.0016377 | $0.0001637 → $0.0001708 | 10 → 9.6 |
| 3 | 16,432 → 16,453 (−21) | $0.0016432 → $0.0016453 | $0.0001643 → $0.0001784 | 10 → 9.2 |

### How the prediction was refined

| Round | Change | Turn 1–3 input tokens predicted | Off from actual by |
|---|---|---|---|
| 1 (before the run) | Started from 16,318, which already included Q1, so Q1 was counted twice | 16,376 / 16,440 / 16,501 | +48 to +63 |
| 2 (after) | Started from the 16,299-token system prompt alone. Still included each turn's own answer (50) in that turn's input | 16,357 / 16,421 / 16,482 | +29 to +44 |
| 3 (after) | Left each turn's own answer out. It only counts as input on the next turn | 16,307 / 16,371 / 16,432 | **−6 to −21** |

What's still off in round 3:
- **Token counts (6–21 low):** each message carries hidden wrapping that marks who it's from. Q1 counted as 19 tokens, not 8. The actual answers were also 30 and 60 tokens, not 50 each.
- **Cost without caching:** within 0.13% on turns 2 and 3. The structure is now right.
- **Cost with caching (4–8% low):** the 0.1× discount was applied to the whole input. Only the 16,299-token system prompt was cached. The chat history after it (78 tokens on turn 2, 154 on turn 3) was billed at the full $0.10/M. Correct formula: 16,299 × $0.01/M + chat history × $0.10/M.

## CLAUDE.md harness experiment (2026-11-18)

**Question:** if a fact is in `CLAUDE.md`, does a model "know" it? The fact "Ariel's club is Boca Juniors." was added to `CLAUDE.md`, Haiku 5.5 was asked "What is Ariel's club?" in a fresh call, the fact was removed, and Haiku was asked again. The harness (`club_harness.py`) was deleted and rewritten between runs. This was done twice: first with a harness that sent only the question, then with one that read `CLAUDE.md` and sent it as the system prompt.

| | Attempt 1, run 1 | Attempt 1, run 2 | Attempt 2, run 1 | Attempt 2, run 2 |
|---|---|---|---|---|
| Fact in `CLAUDE.md`? | Yes | No | **Yes** | No |
| Harness reads `CLAUDE.md`? | No | No | **Yes** (system prompt) | **Yes** (system prompt) |
| Input tokens | 15 | 15 | **572** | 556 |
| Output tokens | 130 | 162 | 29 | 160 |
| Did Haiku know? | No: asked which Ariel (suggested *The Little Mermaid*) | No: same | **Yes:** "Ariel's club is Boca Juniors, according to the instructions for this workspace." | No: "I don't have any information about someone named Ariel…" |
| Where the answer came from | Training only | Training only | **The request** (`CLAUDE.md` in the system prompt) | Nothing in the request |

### Notes

1. **A model knows only its training plus what's in the request.** A file on disk has no effect unless the harness reads it and sends it.
2. **The fact was worth 16 input tokens.** 572 vs. 556 tokens is the entire difference between "Boca Juniors" and "I don't know".
3. **This is how Claude Code works:** it reads `CLAUDE.md` and sends it with every request. That's why the rules in it get followed. It's context, not memory.
4. **Attempt 1 was a design miss.** The first harness was never told to read the file, so both runs had identical 15-token input. A harness's design determines what the model can see.
5. In attempt 2, run 2, Haiku claimed "nothing in this repo" mentions Ariel. It only saw `CLAUDE.md`, not the repo, so that was a small overclaim.

## Eval: scoring the SAFE summaries (2026-11-18)

Nine summaries (from the model comparison runs, plus the first Haiku summary) were scored against a 5-fact checklist: 1 = includes the fact, 0 = missing, partial or wrong. Scored by Claude; the "essential" rule for fact 1 was set by me.

**The checklist:**
1. **Issuer and offering:** YayYo, Inc. (Delaware) selling rights to SAFE Preferred Stock in a private placement of **up to $5 million** under Reg D Rule 506 and/or Reg S. Unregistered and resale-restricted.
2. **Economics:** 8% annual dividend. Discount depends on purchase date: 50% through Dec 31, 2016, then 30%, 20%, 10%, none after Feb 15, 2017.
3. **Conversion trigger:** on an Equity Financing (Reg A+ Tier 2 or IPO), purchase amount plus dividends converts automatically into common stock at the discount.
4. **Other outcomes:** liquidity event (investor chooses cash or shares), dissolution (repaid ahead of stockholders, pro rata if short), forced conversion if nothing happens by Dec 31, 2017 (subject to a $50M valuation cap).
5. **Investor status:** no voting or stockholder rights until shares are issued. Must certify as accredited, sophisticated (with a purchaser representative if needed) or non-U.S., and complete anti-money-laundering forms.

**Scoring rule:** 1 if the summary covers the core of the fact accurately. **Fact 1 requires the $5M** (rule tightened after the first round of scoring).

### Final scores ($5M required for fact 1)

| # | Summary | Words | 1. Issuer & offering | 2. Economics | 3. Conversion | 4. Other outcomes | 5. Investor status | **Score** |
|---|---|---|---|---|---|---|---|---|
| 1 | Haiku, default thinking | 100 | 0 | 1 | 1 | 0 | 0 | **2/5** |
| 2 | Sonnet, default thinking | 99 | 1 | 1 | 1 | 0 | 1 | **4/5** |
| 3 | Opus, default thinking | 101 | 1 | 1 | 1 | 1 | 0 | **4/5** |
| 4 | Fable, default thinking | 100 | 1 | 1 | 1 | 1 | 0 | **4/5** |
| 5 | Haiku, thinking off | 120 | 0 | 1 | 1 | 1 | 1 | **4/5** |
| 6 | Sonnet, thinking off | 103 | 0 | 1 | 1 | 1 | 1 | **4/5** |
| 7 | Opus, effort low | 103 | 1 | 1 | 1 | 1 | 0 | **4/5** |
| 8 | Fable, effort low | 102 | 1 | 1 | 1 | 1 | 0 | **4/5** |
| 9 | Haiku, thinking off (first run) | 142 | 0 | 1 | 1 | 1 | 1 | **4/5** |

**First round (before the $5M rule):** #5 and #9 scored 5/5, because naming the Reg D/S exemptions counted for fact 1. Requiring the $5M dropped both to 4/5.

### Why the 0s, and close calls

- **#1:** fact 1 has no offering details. Fact 4 leaves out dissolution. Fact 5 isn't mentioned.
- **#2:** fact 4 is wrong, not missing: "Liquidity or dissolution events trigger priority cash repayment." In a liquidity event the investor *chooses* cash or shares. This was the only factual error found.
- **Fact 5** was missed by Opus and Fable in both settings.
- **Close calls scored 1:** Fable (#4, #8) left out the $50M cap on forced conversion. #5 said "payout" on dissolution without saying the investor is repaid first.
- **No summary got every sub-detail.** None mentions "no voting rights" or "pro rata if funds are short".

### Notes

1. **No summary scored 5/5.** Eight of nine scored 4/5. Each model missed something different: Opus and Fable always had the $5M but never the investor certifications. Haiku had the certifications but **never the $5M, in any of its three runs**. Sonnet depended on the setting.
2. **The models were almost even on quality, not on price.** Fable at low effort costs about 80× Haiku with thinking off and scored the same.
3. **Haiku with default thinking scored lowest (2/5),** despite the most thinking tokens. It spent its 100 words on discount dates.
4. **The checklist and the 100-word limit pull against each other.** Fitting all five facts into 100 words is hard. In the first round, the two over-length Haiku summaries scored highest.
5. **One rule change changed the winner.** Deciding what's essential is the most important part of an eval, and it's a human call.
6. **This is a small eval:** one document, one run per setting, graded by an AI. Trusting a conclusion like "the cheap model is as good" would need more documents, repeated runs, and spot-checks of the grading.

## Cost model: SAFE & contract summarizer (2026-11-18)

A pricing model for selling a contract summarizer to startup finance teams: **$49 per user per month, 200 contracts per user per month** (so $0.245 revenue per contract), 1 summary + 5 follow-up questions per contract. Built from our measured token counts by `cost_model.py`. The full model, with assumptions and token breakdown, is in `cost_model.md` and `cost_model.csv`.

**Key assumptions:** contract = 16,299 tokens in the system prompt. Each model uses the least thinking it allows. Every call resends the full conversation. With caching on, the contract is written to the cache once and read on all 5 follow-ups (within 5 minutes). Follow-up answers are 41 tokens each (measured on Haiku, assumed for the others). Gross margin counts only the Claude API cost.

| Model | Caching | Contract size (tokens) | Tokens billed per contract (6 calls) | API cost per contract | Gross profit per contract | API cost per user/month | Gross profit per user/month | Gross margin |
|---|---|---|---|---|---|---|---|---|
| Haiku 5.5 (thinking off) | Off | 16,299 | 100,512 | $0.0102 | $0.2348 | $2.05 | $46.95 | **95.8%** |
| Haiku 5.5 (thinking off) | On | 16,299 | 100,512 | $0.0033 | $0.2417 | $0.66 | $48.34 | **98.6%** |
| Sonnet 5.5 (thinking off) | Off | 16,299 | 100,206 | $0.2039 | $0.0411 | $40.78 | $8.22 | **16.8%** |
| Sonnet 5.5 (thinking off) | On | 16,299 | 100,206 | $0.0572 | $0.1878 | $11.44 | $37.56 | **76.7%** |
| Opus 5.5 (effort low) | Off | 16,299 | 100,182 | $0.4076 | −$0.1626 | $81.52 | −$32.52 | **−66.4%** |
| Opus 5.5 (effort low) | On | 16,299 | 100,182 | $0.1142 | $0.1308 | $22.84 | $26.16 | **53.4%** |
| Fable 5.2 (effort low) | Off | 16,299 | 100,182 | $0.8152 | −$0.5702 | $163.04 | −$114.04 | **−232.7%** |
| Fable 5.2 (effort low) | On | 16,299 | 100,182 | $0.2121 | $0.0329 | $42.42 | $6.58 | **13.4%** |

"Tokens billed per contract" counts all 6 calls. Every call resends the 16,299-token contract plus the conversation so far, so 97,794 (6 × 16,299) of the ~100K total is the same contract sent 6 times. Caching doesn't change the number of tokens, only their price.

### Tokens per call

Each call's input = contract + summary request + every earlier question and answer + the new question. Calculated from the model's assumptions, not measured call by call.

**Haiku 5.5 (thinking off):**

| Call | What it is | Input tokens | Output tokens | Total | Caching on: cache write | Caching on: cache read | Caching on: normal-price input |
|---|---|---|---|---|---|---|---|
| 1 | Summary | 16,323 | 279 | 16,602 | 16,299 | 0 | 24 |
| 2 | Follow-up 1 | 16,621 | 41 | 16,662 | 0 | 16,299 | 322 |
| 3 | Follow-up 2 | 16,681 | 41 | 16,722 | 0 | 16,299 | 382 |
| 4 | Follow-up 3 | 16,741 | 41 | 16,782 | 0 | 16,299 | 442 |
| 5 | Follow-up 4 | 16,801 | 41 | 16,842 | 0 | 16,299 | 502 |
| 6 | Follow-up 5 | 16,861 | 41 | 16,902 | 0 | 16,299 | 562 |
| **All 6** | | **100,028** | **484** | **100,512** | **16,299** | **81,495** | **2,234** |

**Other models** differ only in summary length (Sonnet 228, Opus and Fable 224 output tokens), which changes call 1's output and the history on calls 2–6:

| Call | Sonnet input / output | Opus & Fable input / output |
|---|---|---|
| 1 | 16,323 / 228 | 16,323 / 224 |
| 2 | 16,570 / 41 | 16,566 / 41 |
| 3 | 16,630 / 41 | 16,626 / 41 |
| 4 | 16,690 / 41 | 16,686 / 41 |
| 5 | 16,750 / 41 | 16,746 / 41 |
| 6 | 16,810 / 41 | 16,806 / 41 |
| **All 6** | **99,773 / 433** | **99,753 / 429** |

With caching on, every model writes 16,299 on call 1 and reads 16,299 on calls 2–6. The full per-model tables are in `cost_model.md`.

### Notes

1. **Without caching, Opus and Fable lose money** on every user. Fable costs $163 a month to serve a $49 user.
2. **Caching is what makes Sonnet, Opus and Fable viable.** It cuts the cost per contract by about 70–75%, more than in the 3-turn experiment, because there are 5 follow-ups and these models get 95–97.5% off cache reads (Haiku gets 90%).
3. **Input is nearly all the cost.** About 100,000 tokens per contract, of which only about 430–480 are output. Contract size and the number of follow-ups set the price, not summary length.
4. **Fable's cached cost is mostly the one cache write** (77%) at $10 per million tokens. More follow-ups per contract would improve its margin. A healthy 60% margin would need about $106 per user per month.
5. **Combined with the eval:** Sonnet with caching (77% margin) and Opus with caching (53%) scored the same 4/5 as Fable (13%). Haiku has the best margin (99%) but never included the $5M offering size.
6. **Limits:** one contract type, one measured run per model, and API cost only. Longer contracts would lower margins in proportion.
