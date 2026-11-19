# Module 1, day 2: cost model for a SAFE and contract summarizer

Assumptions: $49 per user per month, 200 contracts per user per month, one summary and five follow-up questions per contract. Full model in `01-tokens/cost_model.md`.

## Recommendation

I pick Sonnet because I hypothesize that it will prove more accurate than Haiku across other contract types. Currently it costs ~22 points of margin relative to Haiku (77% vs. 99%, with caching), but that is across one contract type, a SAFE agreement. I would switch to Haiku if we could test models by rerunning the same exercise 100 times and ensuring that Haiku is at least a 4/5 accuracy every time.

## Sonnet cost, checked by hand

The cache is only for the 16,299 of the tokens for the initial contract and system prompt. At the Sonnet cache cost, comes to $0.0407. Then the model reads the same amount of tokens five times at the cached rate, leading to $0.0081. There are a total of ~2k uncached input tokens across the turns, which are ~$0.004. Then there are about ~400 output tokens, which coincidentally also drive ~$0.004 of cost. The total is ~$0.0572 per contract, totaling the $11.44 of cost and the 77% margin.

## Heavy users

Heavy users, assuming the $11.44 of average cost calculated in the cost table, represent $57.2 of cost at 5x usage, with a (~17%) gross margin at a $49 revenue.

## Assumption I trust least

The assumption I am most concerned with is contract length in tokens. This uses one SAFE example. Different contract types will have different lengths, and could be much larger if for example the tool is summarizing an M&A agreement instead.

## What the eval shows

The eval does a spot check on if the summary includes the facts I mentioned, but it does not show if the facts themselves are right. It also is just off of one run on one contract, scored by the agent, so it does not adequately represent accuracy. More runs are needed.
