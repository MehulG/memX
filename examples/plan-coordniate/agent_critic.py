"""
CriticAgent (reactive to two keys)
- First pass: critiques research -> loop:critique_v1
- Second pass: reviews final -> loop:critique_v2
"""

import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI

import common


def main():
    common.ensure_google_api_key()
    ctx = common.make_ctx()
    llm = ChatGoogleGenerativeAI(model=common.MODEL_CRITIC, temperature=0.3)

    def critique_research(message):
        research = common.unwrap_value(message)
        if not research:
            return
        common.log("CriticAgent", f"Received {common.KEY_RESEARCH}: {common.preview(research)}")

        prompt = textwrap.dedent(
            """
            Critique this research.
            Output:
            - 3 strong points
            - 3 weak points
            - 2 missing angles
            """
        ).strip()
        out = llm.invoke(prompt + "\n\n" + research).content.strip()
        ctx.set(common.KEY_CRITIQUE_V1, out)
        common.log("CriticAgent", f"Wrote {common.KEY_CRITIQUE_V1} (preview: {common.preview(out)})")

    def critique_final(message):
        final = common.unwrap_value(message)
        if not final:
            return
        common.log("CriticAgent", f"Received {common.KEY_FINAL}: {common.preview(final)}")

        prompt = textwrap.dedent(
            """
            Review the final output.
            Suggest:
            - 3 improvements
            - 1 stronger closing line
            """
        ).strip()
        out = llm.invoke(prompt + "\n\n" + final).content.strip()
        ctx.set(common.KEY_CRITIQUE_V2, out)
        common.log("CriticAgent", f"Wrote {common.KEY_CRITIQUE_V2} (preview: {common.preview(out)})")

    common.log("CriticAgent", f"Waiting on {common.KEY_RESEARCH} and {common.KEY_FINAL}...")
    ctx.subscribe(common.KEY_RESEARCH, critique_research)
    ctx.subscribe(common.KEY_FINAL, critique_final)
    common.wait_forever()


if __name__ == "__main__":
    main()
