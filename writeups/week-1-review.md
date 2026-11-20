# Week 1 review (2026-11-20)

No new material on Fridays: a cold review of the week, then a 30-minute mock technical screen. Both were run and graded by Claude in chat, acting as tutor and then as interviewer. Scores are Claude's; the fixes are mine to make.

## Where the week started and ended

| | Monday 2026-11-16 | Friday 2026-11-20 |
|---|---|---|
| Diagnostic or screen | 11 of 30, no solid answers, 4 misses | Mock screen 7 of 12, 1 solid answer, no misses |
| Cold review | n/a | 4 of 8 cold, 8 of 8 after rewrites |
| Repo | None | Three write-ups, four context experiments, a cost model |

## Cold review: 4 of 8

Answered with no notes and no agent.

| Question | Result |
|---|---|
| Tool call: who does what | Pass |
| Training vs. inference, and why not fine-tune on contracts | Partial |
| Does a pricier model write more tokens | Partial |
| What has to match for a cache discount | Pass |
| Memory: who writes, who reads it back | Partial |
| Why 400 contracts cannot go in the window | Pass |
| Why not ship Setup 2 (5.0 of 5) | Pass |
| Haiku vs. Sonnet: what is robust | Partial |

The mechanics passed. The partials were mostly recall of my own results: I gave no numbers for what I measured, and I left the harness out of the memory read-back.

## Mock screen: 7 of 12

Scored 0 (miss), 1 (partial), 2 (solid). One question at a time, up to two follow-ups each, no feedback until the end.

| Question | Score | Note |
|---|---|---|
| What happens between "fix the failing test" and a passing test | 1 | Loop was right. I said the harness decides which files to read; the model decides and the harness fetches |
| The recommendation I reversed (Sonnet to Haiku) | 1 | Right structure. I quoted the gap as 0.6 to 1.0 when it is 0.2 to 1.0, and did not volunteer that Sonnet leads once length counts |
| Unit economics at $49 a seat | 1 | Live arithmetic was right. Asked why my own model says $0.66 and not $0.36, I gave a wrong cause instead of saying I did not remember (it is the five follow-up questions per contract) |
| "Just fine-tune the model on our contracts" | 1 | Right answer and right alternative. I had not built retrieval yet and should have said so |
| How to know a prompt change is better before shipping | 2 | Baseline, fixed criteria, many runs on many contracts, hand-calibrated grader |
| An agent that reads vendor emails and approves payments | 1 | Right instinct on fraud and human approval. Missed that an email can carry instructions to the agent |

## Three things to fix in week 2

1. Say "I don't know, I'd check" under pressure instead of constructing an answer.
2. Report the number that hurts my case first.
3. Know my own results cold. Keep a one-page card of my numbers and reread it before each session.

## Next

Module 2 day 2: retrieval. Then tools and agents, where "who decides" gets fixed properly.
