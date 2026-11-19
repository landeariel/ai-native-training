"""
Harness that reads CLAUDE.md (rewritten): asks Claude Haiku 5.5 one question in a
fresh call, with the current contents of CLAUDE.md sent as the system prompt.

    01-tokens/.venv/bin/python 01-tokens/club_harness.py
"""

from pathlib import Path

import anthropic

from count_tokens import MODEL, load_api_key

QUESTION = "What is Ariel's club?"
CLAUDE_MD = Path(__file__).parent.parent / "CLAUDE.md"

system_prompt = CLAUDE_MD.read_text()  # read fresh on every run

client = anthropic.Anthropic(api_key=load_api_key())
response = client.messages.create(
    model=MODEL,
    max_tokens=200,
    thinking={"type": "disabled"},
    system=system_prompt,
    messages=[{"role": "user", "content": QUESTION}],
)
answer = "".join(b.text for b in response.content if b.type == "text")
print(f"System prompt: CLAUDE.md ({len(system_prompt.split())} words; "
      f"mentions Boca: {'yes' if 'Boca' in system_prompt else 'no'})")
print(f"Sent:   {QUESTION}")
print(f"Reply:  {answer}")
print(f"Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
