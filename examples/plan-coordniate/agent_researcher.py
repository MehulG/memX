"""
ResearcherAgent
- Seeds loop:research with base research content.
"""

import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI

import common


def main():
    common.ensure_google_api_key()
    ctx = common.make_ctx()
    llm = ChatGoogleGenerativeAI(model=common.MODEL_RESEARCH, temperature=0.2)

    prompt = textwrap.dedent(
        """
        Explain shared memory in multi-agent systems with 5 concrete examples.
        """
    ).strip()

    research = llm.invoke(prompt).content.strip()
    ctx.set(common.KEY_RESEARCH, research)
    common.log("ResearcherAgent", f"Wrote {common.KEY_RESEARCH} (preview: {common.preview(research)})")


if __name__ == "__main__":
    main()
