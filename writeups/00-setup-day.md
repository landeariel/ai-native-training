# Setup day write-up (2026-11-16)

I set up a local repo on my Mac, a public repo on GitHub, and a harness on my Mac (Claude Code), which reaches models such as Opus that run on Anthropic's servers. I made two credentials. A GitHub token lets git on my Mac push changes to my GitHub repo. An Anthropic API key authenticates programs I build to the model and bills by usage; Claude Code does not use it, because it is authenticated with my Max login.

The four-step loop: I type a request into the harness. The harness contacts the model via my subscription. The model decides which tool to use and tells the harness, which executes the tool and sends the output back to the model. The model then writes the final answer, which reaches me through the harness. With scratch.txt, I asked the harness to make a file, the model chose the command, the harness ran it, and the model, having seen the output, reported that the file was created.

git add is the step before commit, where I select the changes I have made. git commit creates a record of them in my local repo's history. git push sends my commits to the GitHub repo as the public record.
