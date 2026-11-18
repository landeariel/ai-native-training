# Module 1, day 1: tokens

Tokens have two definitions. They are the unit of text a model reads and writes (common words are a token, my experiment measured ~2 tokens per word by dividing tokens by word count). Most interactions with a model will have input tokens (everything sent on model call) + output tokens (model response). That is the main token definition we are working with. The other is a secret that grants specific permissions, like my GitHub token.

Call 3 in our experiment C was 131 tokens, despite the question asked being <10 words, because in a multi-turn conversation, the input needs to carry all the messages prior in the conversation. This is because the model stores nothing in between calls. So each successive step carries an amount equal to the prior call's input tokens + the model's output for the prior turn + the new turn's message or question or request. The math here is 69 input tokens from call 2 + 47 tokens for the model's answer to call 2 + 15 tokens for the new question, totaling 131. There are also overhead tokens on each message.

My largest error was in the Spanish email, where I predicted 575 input tokens, assuming that each word in Spanish was 2 or 3 tokens, when in reality most were still one token and the real count was 350.

Experiment D touches on this and we will look in further modules, but tokens have a different price if they're input vs. output, and vary heavily by model. I calculated, but did not run, the same summary at Fable's prices using Haiku's token counts, and it came to 80 times as much ($0.143 vs. $0.0018 per summary).
