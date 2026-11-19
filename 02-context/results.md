# Module 2: context experiments

## Experiment 1: three setups (2026-11-19)

Same SAFE contract, Haiku 5.5 (thinking off), three setups, 5 runs each. Graded against the 5-fact rubric in `01-tokens/results.md` (fact 1 requires the $5M offering).

- **Setup 1:** bare instruction: "Write a one-paragraph synthesis of this contract in 100 words." + contract.
- **Setup 2:** Setup 1 + a system prompt listing the five required facts.
- **Setup 3:** Setup 1 + "Include every dollar amount and cap in the offering outlined in the contract, alongside terms specifics."

Run 1 of each setup was hand-graded by me first and compared with Claude's grading, before the other 12 runs.

### Predictions (made before any runs)

| Setup | Input tokens | Runs with $5M offering | Reasoning |
|---|---|---|---|
| 1: Bare instruction | 16,289 | 2 of 5 | Same as the Module 1 run: ~16,235 contract + ~50 instruction and overhead |
| 2: Rubric in system prompt | 16,650 | 5 of 5 | 184-word rubric × 2 tokens/word ≈ 368, + ~30 overhead ≈ 400 added |
| 3: Bare + general rule | 16,321 | 4 of 5 | Setup 1 + 15-word sentence with punctuation ≈ 32 tokens |

### Hand grading vs. Claude's grading (run 1 of each setup)

Claude's grades were saved before mine were shared.

| Summary | Grader | Fact 1 | Fact 2 | Fact 3 | Fact 4 | Fact 5 | Total |
|---|---|---|---|---|---|---|---|
| Setup 1, run 1 | Me | 1 | 0 | 1 | 1 | 0 | 3/5 |
| Setup 1, run 1 | Claude | 1 | 1 | 1 | 1 | 1 | 5/5 |
| Setup 2, run 1 | Me | 1 | 1 | 1 | 1 | 1 | 5/5 |
| Setup 2, run 1 | Claude | 1 | 1 | 1 | 1 | 1 | 5/5 |
| Setup 3, run 1 | Me | 0 | 1 | 0 | 1 | 0 | 2/5 |
| Setup 3, run 1 | Claude | 1 | 1 | 0 | 0 | 0 | 2/5 |

**Where we disagreed and how it was settled:**
- **Setup 1, fact 2:** I read the discount as missing. The summary has both "an 8% annual dividend" and "Conversion discounts range from 50% for early purchases down to 10%, then none after February 15, 2017." Settled as **1**.
- **Setup 1, fact 5:** it mentions accredited-investor certifications and AML forms, but not voting rights. **New rule: voting rights required.** Settled as **0**.
- **Setup 3, fact 1:** it adds "$50,000,000 Regulation A+ (Tier 2) offering". That's accurate (contract line 242: the Equity Financing includes "up to Fifty Million United States Dollars ($50,000,000)" of common stock under Reg A+). **Rule: accurate extra detail is fine.** Settled as **1**.
- **Setup 3, fact 4:** it describes only the forced conversion. **Rule: forced conversion is enough.** Settled as **1**.

### Grading rules for this experiment

The Module 1 rubric, with these rules (Module 1 scores were *not* re-graded under them):
- **Fact 1:** must include the $5M offering. Accurate extra figures are fine. **Describing the private placement as a Reg A+ offering (e.g. "a Regulation A+ (Tier 2) and Regulation D/S private placement") = 0.** They're different offerings. *(Added after Setup 4; applied to all 25 summaries.)*
- **Fact 4:** describing the forced conversion by Dec 31, 2017 is enough. Liquidity and dissolution aren't required. *(More lenient than Module 1, which required all three outcomes.)*
- **Fact 5:** must mention **no voting or stockholder rights until shares are issued**, plus the investor certification. *(Stricter than Module 1, where certifications + AML were enough.)*
- **Fact 6 (length):** under 150 words = 1, 150 or more = 0. Scored automatically from the word count. *(Added after Setup 4; applied to all 25 summaries.)* Totals are now **out of 6**.

**Final run 1 scores (5 facts):** Setup 1 = 4/5, Setup 2 = 5/5, Setup 3 = 3/5. **After the fact 1 and length rules:** Setup 1 = 3/6 (fact 1 → 0 for the Reg A+ wording; 156 words → length 0), Setup 2 = 6/6, Setup 3 = 4/6.

**Observation:** Setup 3's "include every dollar amount" rule pushed the summary toward numbers (the full 50/30/20/10% discount schedule, both dollar caps, the June 30, 2017 end date) and away from facts with no number in them (the conversion trigger, outcome choices, voting rights).

### Results per run

All 15 runs graded under the rules above, including the fact 1 Reg A+ rule and the length line. Claude graded runs 2–5. The "$5M" column is an automatic text check for whether the amount appears, confirmed by reading each summary. A summary can include the $5M and still score 0 on fact 1 if it describes the offering wrongly.

| Setup | Run | Input tokens | Output tokens | Cost | Words | Facts (out of 5) | Length <150 words | Total (out of 6) | Includes $5M offering? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 16,289 | 359 | $0.001808 | 156 | 3 | 0 | 3 | Yes |
| 1 | 2 | 16,289 | 311 | $0.001784 | 143 | 3 | 1 | 4 | No |
| 1 | 3 | 16,289 | 305 | $0.001781 | 133 | 3 | 1 | 4 | Yes |
| 1 | 4 | 16,289 | 292 | $0.001775 | 132 | 3 | 1 | 4 | No |
| 1 | 5 | 16,289 | 333 | $0.001795 | 151 | 3 | 0 | 3 | No |
| 2 | 1 | 16,678 | 310 | $0.001823 | 138 | 5 | 1 | 6 | Yes |
| 2 | 2 | 16,678 | 313 | $0.001824 | 140 | 5 | 1 | 6 | Yes |
| 2 | 3 | 16,678 | 309 | $0.001822 | 137 | 5 | 1 | 6 | Yes |
| 2 | 4 | 16,678 | 293 | $0.001814 | 127 | 5 | 1 | 6 | Yes |
| 2 | 5 | 16,678 | 334 | $0.001835 | 147 | 5 | 1 | 6 | Yes |
| 3 | 1 | 16,321 | 347 | $0.001806 | 142 | 3 | 1 | 4 | Yes |
| 3 | 2 | 16,321 | 348 | $0.001806 | 142 | 3 | 1 | 4 | Yes |
| 3 | 3 | 16,321 | 327 | $0.001796 | 137 | 3 | 1 | 4 | Yes |
| 3 | 4 | 16,321 | 363 | $0.001814 | 154 | 4 | 0 | 4 | Yes |
| 3 | 5 | 16,321 | 311 | $0.001788 | 131 | 3 | 1 | 4 | Yes |

Setup 1 runs 1 and 3 include the $5M but score 0 on fact 1: run 1 calls it "a Regulation A+ (Tier 2) and Regulation D/S private placement"; run 3 says the SAFE is "issued … under Regulation A+ (Tier 2) and Regulation D/S exemptions". Setup 3 run 3 ("up to $5,000,000, tied to a Regulation A+ (Tier 2) offering") is borderline and was kept at 1.

### Per setup

| Setup | Input tokens (avg) | Output tokens (avg) | Total cost (5 runs) | Avg facts (out of 5) | Avg total (out of 6) | Runs with $5M |
|---|---|---|---|---|---|---|
| Setup 1: bare instruction | 16,289 | 320 | $0.008945 | 3.0 | 3.6 | 2 of 5 |
| Setup 2: rubric in system prompt | 16,678 | 312 | $0.009119 | 5.0 | **6.0** | 5 of 5 |
| Setup 3: bare instruction + general rule | 16,321 | 339 | $0.009009 | 3.2 | 4.0 | 5 of 5 |

### Predicted vs. actual

| Setup | Input tokens (pred → actual) | Runs with $5M (pred → actual) | Avg total (out of 6) |
|---|---|---|---|
| 1: Bare instruction | 16,289 → **16,289** ✓ | 2 → **2** ✓ | 3.6 |
| 2: Rubric in system prompt | 16,650 → **16,678** (28 low) | 5 → **5** ✓ | **6.0** |
| 3: Bare + general rule | 16,321 → **16,321** ✓ | 4 → **5** | 4.0 |

### Which facts each setup got (out of 5 runs)

| Fact | Setup 1 | Setup 2 | Setup 3 |
|---|---|---|---|
| 1. Issuer & offering ($5M, described correctly) | 0 | 5 | 5 |
| 2. Economics | 5 | 5 | 5 |
| 3. Conversion trigger | 5 | 5 | 1 |
| 4. Other outcomes (forced conversion) | 5 | 5 | 5 |
| 5. Investor status (voting rights) | 0 | 5 | 0 |
| 6. Length (<150 words) | 3 | 5 | 4 |

### Notes

1. **Listing the facts in the system prompt was perfect:** 30 of 30 points across 5 runs, including length. It cost 389 more input tokens (+2.4%), about $0.00003 more per summary.
2. **The general rule got the $5M right every time but lost the facts without numbers.** Setup 3 averaged 4.0 vs. Setup 1's 3.6. It described the conversion trigger in only 1 of 5 runs and never mentioned voting rights. A broad rule moves the model's attention around. A specific list tells it exactly what's needed.
3. **The same input gives different outputs.** Setup 1 sent identical input 5 times and included the $5M in only 2, and both of those described the offering wrongly. In Module 1, Haiku never included it in 3 runs. That looked like a pattern but was partly chance. One run per setup isn't enough to draw conclusions.
4. **Voting rights appeared only when asked for.** Setups 1 and 3 mentioned it 0 times in 10 runs. Setup 2 mentioned it 5 of 5.
5. **No setup kept to 100 words.** Summaries ran 127–156 words, and 3 of 15 went over the 150-word line. The rubric didn't make Setup 2's summaries longer (312 output tokens on average vs. 320 for Setup 1). It changed what they covered, not how long they were.
6. **Input-token predictions were exact for Setups 1 and 3.** The rubric added 389 tokens for 184 words: 2.1 tokens per word vs. the predicted 2.0.
7. **Grading caveat:** Claude graded 12 of the 15. Hand vs. Claude grading on run 1 disagreed on 4 facts before the rules were settled, so expect some judgment in the per-run scores.

## Setup 4: general (not SAFE-specific) instruction, Haiku vs. Sonnet (2026-11-19)

**Instruction:** Setup 1's bare instruction + "Note who the parties are at hand, what are the core terms of the contract, what are any forcing mechanisms or clauses or deadlines, what are specific rights and privileges the parties have, etc. Include major contract numbers but do not ignore other terms and conditions in favor of only noting numbers. Start by identifying the type of contract." It's meant to work on any contract. It was graded with the unchanged SAFE rubric. Run 5 times each on Haiku 5.5 and Sonnet 5.5, thinking off. Input: 16,394 tokens on both models.

**Success bar (set before the reveal):** Sonnet must average at least 1 full point higher than Haiku to count as better.

### Blind grading process

1. All 10 summaries were shuffled into labels A–J. The key was saved without being shown (`blind_shuffle.py`, `blind_key.json`).
2. I hand-graded A–D without knowing the models. A separate Claude agent graded A–J blind (no key, no model names).
3. **First check: 17 of 20 facts agreed**, below the 18/20 bar. All 3 disagreements were in Summary C and came from unclear rules, so the rules were clarified (below).
4. A **fresh** blind agent re-graded all 10 under the clarified rules. As a holdout, I blind-graded 2 more summaries chosen at random (E, I).
5. **Second check, on the holdout: 9 of 10 facts agreed** (90%, the same rate as the 18/20 bar). The agent's scores were accepted, then the key was revealed. A–D also matched the new agent, but that isn't independent evidence, because the clarified rules were written from Summary C. **The honest agreement numbers are 17 of 20 on the first pass and 9 of 10 on the holdout.** The one holdout difference (E, fact 2) was later resolved in the agent's favor.

**Rules clarified during grading** (apply to Setup 4; Setups 1–3 were graded under the earlier rules):
- **Fact 3:** conversion must be explicitly stated to happen *upon* the Equity Financing (Reg A+ / IPO). "Converts at a discount to the Reg A+ offering price" alone = 0.
- **Fact 4:** the forced conversion must be described, **and any misstated outcome = 0**.
- **Fact 5:** "no voting or stockholder rights" alone is enough. Certifications are optional.

**Rules added after the reveal** (applied to all 25 summaries in this file):
- **Fact 1:** describing the private placement as a Reg A+ offering = 0 (different offerings). This changed Haiku run 2 (D) from 1 to 0.
- **Fact 6 (length):** under 150 words = 1, 150 or more = 0. Totals are out of 6.

### Agreement check (me vs. blind agent)

| Summary | Fact 1 | Fact 2 | Fact 3 | Fact 4 | Fact 5 | Total (me / agent) | Agree |
|---|---|---|---|---|---|---|---|
| A | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 0 / 0 | 4 / 4 | 5/5 |
| B | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 5 / 5 | 5/5 |
| C (revised under clarified rules) | 1 / 1 | 1 / 1 | 0 / 0 | 0 / 0 | 1 / 1 | 3 / 3 | 5/5 |
| D | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 0 / 0 | 4 / 4 | 5/5 |
| E (holdout) | 1 / 1 | **0 / 1** | 0 / 0 | 1 / 1 | 1 / 1 | 3 / 4 | 4/5 |
| I (holdout) | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 5 / 5 | 5/5 |

This table shows the grades as given at the time (5 facts, before the fact 1 Reg A+ rule and the length line).

- **The one holdout disagreement, E fact 2:** E has the 8% dividend and "50% through 12/31/16, falling to 0% after 2/15/17" but leaves out the 30/20/10% middle steps. Under the rule (full schedule not required), the agent's 1 was used. **I later agreed: my 0 was wrong.**
- **D fact 1** was scored 1 by both of us at the time. After the reveal, I set the rule that "a Regulation A+ (Tier 2) and Rule 506/Regulation S private placement" is wrong, so it's now 0.

### The reveal

| Label | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| Model, run | Sonnet 3 | Haiku 5 | Sonnet 5 | Haiku 2 | Sonnet 4 | Haiku 4 | Sonnet 2 | Haiku 3 | Haiku 1 | Sonnet 1 |
| Facts (out of 5) | 4 | 5 | 3 | 3 | 4 | 4 | 4 | 5 | 5 | 4 |
| Words | 140 | 200 | 143 | 202 | 114 | 183 | 108 | 204 | 185 | 114 |
| Total (out of 6) | 5 | 5 | 4 | 3 | 5 | 4 | 5 | 5 | 5 | 5 |

### Setup 4 results per run

| Model | Run | Input tokens | Output tokens | Cost | Words | Facts (out of 5) | Length <150 words | Total (out of 6) | Includes $5M offering? |
|---|---|---|---|---|---|---|---|---|---|
| Haiku 5.5 | 1 | 16,394 | 403 | $0.001841 | 185 | 5 | 0 | 5 | Yes |
| Haiku 5.5 | 2 | 16,394 | 471 | $0.001875 | 202 | 3 | 0 | 3 | Yes |
| Haiku 5.5 | 3 | 16,394 | 475 | $0.001877 | 204 | 5 | 0 | 5 | Yes |
| Haiku 5.5 | 4 | 16,394 | 425 | $0.001852 | 183 | 4 | 0 | 4 | Yes |
| Haiku 5.5 | 5 | 16,394 | 469 | $0.001874 | 200 | 5 | 0 | 5 | Yes |
| Sonnet 5.5 | 1 | 16,394 | 238 | $0.035168 | 114 | 4 | 1 | 5 | Yes |
| Sonnet 5.5 | 2 | 16,394 | 277 | $0.035558 | 108 | 4 | 1 | 5 | Yes |
| Sonnet 5.5 | 3 | 16,394 | 324 | $0.036028 | 140 | 4 | 1 | 5 | Yes |
| Sonnet 5.5 | 4 | 16,394 | 262 | $0.035408 | 114 | 4 | 1 | 5 | Yes |
| Sonnet 5.5 | 5 | 16,394 | 299 | $0.035778 | 143 | 3 | 1 | 4 | Yes |

### Setup 4 per model

| Model | Input tokens (avg) | Output tokens (avg) | Total cost (5 runs) | Avg facts (out of 5) | Avg total (out of 6) | Runs with $5M |
|---|---|---|---|---|---|---|
| Haiku 5.5 | 16,394 | 449 | $0.009319 | 4.4 | 4.4 | 5 of 5 |
| Sonnet 5.5 | 16,394 | 280 | $0.177940 | 3.8 | **4.8** | 5 of 5 |

### Which facts each model got (out of 5 runs)

| Fact | Haiku 5.5 | Sonnet 5.5 |
|---|---|---|
| 1. Issuer & offering ($5M, described correctly) | 4 | 5 |
| 2. Economics | 5 | 5 |
| 3. Conversion trigger (stated) | 5 | 3 |
| 4. Other outcomes (no misstatements) | 5 | 2 |
| 5. Investor status (voting rights) | 3 | 4 |
| 6. Length (<150 words) | 0 | 5 |

### Notes

1. **Sonnet did not meet the bar.** Out of 6, Sonnet averaged 4.8 and Haiku 4.4, a gap of 0.4, short of the 1-point bar. Sonnet costs about 19× as much ($0.0356 vs. $0.0019 per summary). On the 5 content facts alone, Haiku leads (4.4 vs. 3.8). Sonnet's lead comes entirely from length.
2. **Sonnet's lost points were split between precision and coverage.** It lost 6 fact points in total: 3 on fact 4 for describing an outcome loosely or wrongly (for example, "Liquidity or dissolution events trigger cash repayment or conversion"; the contract pays dissolution in cash only, and the conversion choice is the investor's), 2 on fact 3 for not stating the trigger, and 1 on fact 5.
3. **Haiku's longer summaries were a trade-off.** Haiku averaged 195 words and Sonnet 124, both against a 100-word request. Haiku used the extra room to be specific (5/5 on facts 3 and 4) but went over 150 words in all 5 runs, losing the length point every time.
4. **A general instruction got the $5M every time,** like the SAFE-specific rule in Setup 3, without its side effect: Haiku kept the conversion trigger and outcomes (5/5 each). Asking for "major numbers but not *only* numbers" fixed what Setup 3 broke. (One Haiku run still described the offering as a Reg A+ private placement.)
5. **The SAFE-specific rubric (Setup 2) is still clearly best:** 6.0 vs. 4.4 for Haiku with the general instruction. On the 5 content facts alone it's 5.0 vs. 4.4. Most of the gap is length: the general instruction asks for more, and Haiku wrote more. (Facts 3–5 in Setups 1–3 were graded under the earlier rules, so the comparison is approximate.)
6. **The grading rules decided a lot.** Agreement was 17 of 20 on the first pass, before three rules were clarified using Summary C. On the holdout it was 9 of 10. The misstatement rule accounts for 3 of Sonnet's 6 lost fact points. Adding the length line moved Sonnet from behind Haiku to ahead of it. A different, equally reasonable rubric could change the ranking.
7. **Blind grading worked.** Neither the hand grading nor the agent's grading knew the models. The holdout (E, I) tested the clarified rules on summaries they weren't designed around.
8. **Limits:** one contract, 5 runs per model, thinking off on both. Sonnet with thinking on might do better on precision, at a higher cost.
