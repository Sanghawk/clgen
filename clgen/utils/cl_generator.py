# clgen/generator.py
import json
from typing import Dict, Sequence

from openai import OpenAI

PROMPT = """
You are an expert release‑note writer. Your task is to write a changelog based on a given list of commits (as JSON). Each commit contains the following:
- commit: full commit hash
- author: author name/email
- date: commit date
- summary: commit summary (subject)
- body: commit body (message excluding subject)

The changelog needs to be produced as Markdown.
Your audience is developers that are using the project and the developers of project itself.

The changelog follows the following format:

- Title of the changelog. If a version is provided, use that. Otherwise, use the date from the latest commit.
- Summary of the changes. Titled as "Summary". Summarize the changes in a few bullet points.
- Full list of changes. Titled as "Release Notes". Divide sections by date of the commit with the section header as "Month Day, Year".
    - Each commit should be summarized as a single bullet point.
    - If the commit is trivial, it can be omitted.
    - Include the commit hash at the end of the bullet point shortened to 5 characters - e.g. `(#12345)`
    - Don't include the author of the commit in the bullet point.
"""


class ChangelogGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, commits: Sequence[Dict[str, str]]) -> str:
        commits_block = json.dumps(commits, indent=2)
        resp = self.client.responses.create(
            model=self.model,
            instructions=PROMPT,
            input=commits_block,
        )
        return resp.output_text
