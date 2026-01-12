"""
SynthesizerAgent
- Subscribes to loop:critique_v1, reads research, and writes loop:final.
"""

import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI

import common


def main():
    common.ensure_google_api_key()
    ctx = common.make_ctx()
    llm = ChatGoogleGenerativeAI(model=common.MODEL_SYNTHESIZER, temperature=0.2)

    def on_critique(message):
        critique = common.unwrap_value(message)
        if not critique:
            return
        research = common.unwrap_value(ctx.get(common.KEY_RESEARCH) or {}) or ""

        common.log("SynthesizerAgent", f"Received {common.KEY_CRITIQUE_V1}: {common.preview(critique)}")

        prompt = textwrap.dedent(
            """
            Create a polished final explanation using:
            - the research
            - the critique feedback

            Format:
            - 1-sentence hook
            - 5 bullet examples
            - 1 strong closing
            """
        ).strip()

        final = llm.invoke(
            prompt + "\n\nRESEARCH:\n" + research + "\n\nCRITIQUE:\n" + critique
        ).content.strip()
        ctx.set(common.KEY_FINAL, final)
        common.log("SynthesizerAgent", f"Wrote {common.KEY_FINAL} (preview: {common.preview(final)})")

    common.log("SynthesizerAgent", f"Waiting on {common.KEY_CRITIQUE_V1}...")
    ctx.subscribe(common.KEY_CRITIQUE_V1, on_critique)
    common.wait_forever()


if __name__ == "__main__":
    main()
