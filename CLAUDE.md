# Instructions for Claude

This repo is my AI learning workspace. I'm a non-engineer spending 4 weeks learning how AI systems work. I direct agents and review what they produce. I don't write code myself.

## How to work with me

- **Use plain language.** Skip jargon where you can. When you do need a technical term, define it in one short sentence the first time it comes up in a session.
- **Show me every command.** Before you run a terminal command (or as you run it), show me the exact command and say in plain words what it does and why.
- **Explain what changed.** After you create or edit files, tell me which files changed and what's different, so I can review it.
- **Teach as you go.** If something you're doing relates to a block in PROGRESS.md, say so. If a term would fit in GLOSSARY.md, suggest adding it, but leave the "My definition" column for me.

## Rules you must always follow

- **Never commit or push unless I ask.** A commit is a saved snapshot of the files. A push sends commits to a remote copy, like GitHub. Both wait until I explicitly ask for them.
- **Never write secrets or API keys into this repo.** That includes passwords, tokens, and credentials of any kind. If a secret is needed, tell me to put it in a `.env` file (which `.gitignore` keeps out of git) or somewhere outside the repo. Never print it back to me.

## Files in this repo

- `PROGRESS.md`: my tracker for the 4-week course, one row per block.
- `GLOSSARY.md`: terms I'm learning, with definitions in my own words.
- `.gitignore`: a list of files git should ignore and never track.
