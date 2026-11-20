# Glossary

| Term | My definition | Date |
|---|---|---|
| terminal | Finder in text form: a window where I type commands to access files and run programs | 2026-11-17 |
| PATH | The list of folders my shell searches when I type a command name | 2026-11-17 |
| repo | A folder whose files and history git tracks; I have a local one on my Mac and a public copy on GitHub | 2026-11-17 |
| commit | A record of my changes in the local repo's history | 2026-11-17 |
| staging area | The list of changes selected for the next commit; git add puts them there | 2026-11-17 |
| push | Sends my commits to the GitHub repo | 2026-11-17 |
| remote | A copy of my repo hosted elsewhere and known by a nickname; mine is origin, on GitHub | 2026-11-17 |
| token | (1) The unit of text a model reads and writes, and the unit I am billed in. (2) A secret that grants specific permissions, like my GitHub token scoped to one repo | 2026-11-17 |
| API key | A credential that authenticates programs I build to the model provider's API, billed by usage; separate from my Max login | 2026-11-17 |
| harness | The program that sends context to the model, executes the tool calls the model writes, and returns the results; mine is Claude Code | 2026-11-17 |
| tool call | The model's request for the harness to run a tool, with specific inputs; the tool lives in the harness | 2026-11-17 |
| SDK | A ready-made code library for talking to a service; mine is Anthropic's Python library, so my scripts don't build raw web requests | 2026-11-17 |
| virtual environment | A private folder of Python packages for one project, so installs don't touch the rest of my Mac; mine is 01-tokens/.venv | 2026-11-17 |
| input tokens / output tokens | Input is everything sent to the model on a call (instructions, documents, history); output is everything it writes back, including thinking. Output costs 5× input on Claude | 2026-11-17 |
| tokenizer | The tool that splits text into tokens; common words are one token, while names, rare words and all caps split into several. My English ran about 1.9 tokens per word | 2026-11-17 |
| token counting (count-only) | A free API call that reports how many input tokens a request would use, without running the model | 2026-11-17 |
| system prompt | Standing instructions sent ahead of the conversation on every call; billed as input every time | 2026-11-17 |
| context | Everything the model sees on one call: system prompt, documents, conversation history and the new message. Outside its training, the model knows only what's in it | 2026-11-17 |
| thinking tokens | Hidden reasoning the model writes before it answers; billed as output and most of the wait | 2026-11-18 |
| effort | A setting for how hard the model thinks; lower effort means fewer thinking tokens, so faster and cheaper | 2026-11-18 |
| prompt caching | Saving the start of a prompt on Anthropic's side so later calls reuse it at a discount; the copy expires 5 minutes after its last use | 2026-11-18 |
| cache write / cache read | A write saves the prompt to the cache at 1.25× the normal input price; a read reuses it at 0.1× (less on some models) | 2026-11-18 |
| eval | A fixed test that scores model outputs against agreed criteria, so setups and models can be compared fairly | 2026-11-18 |
| gross margin | Revenue minus the direct cost of serving it, as a share of revenue; in my cost model, revenue minus the Claude API cost | 2026-11-18 |
| rubric | The checklist an eval scores against; mine was five SAFE facts plus a length line, 1 point each | 2026-11-19 |
| blind grading | Scoring outputs without knowing which model or setup wrote them, so expectations can't bias the scores | 2026-11-19 |
| holdout | Examples kept out of rule-writing and used afterwards to test whether the rules hold on new cases | 2026-11-19 |
| retrieval | Fetching the relevant documents when a question comes in and adding them to the context, so the model can use information it wasn't trained on. The alternative to fine-tuning, which changes the model itself by training it further | 2026-11-19 |
| fine-tuning | Training an existing model further on my own examples, which adjusts its weights (the internal numbers that decide its outputs) so the new behavior is built into the model instead of being supplied in the context on every call | 2026-11-19 |
| weights | The billions of numbers inside a model, set during training, that decide what it outputs for any input; fine-tuning changes them, while prompts and context don't | 2026-11-19 |
