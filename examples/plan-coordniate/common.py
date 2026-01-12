import os
import time
from pathlib import Path
from dotenv import load_dotenv
from memx_sdk import memxContext

# Load a local .env if present (keeps per-demo config contained).
ENV_FILE = Path(__file__).resolve().parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# Shared config for the loop demo.
API_KEY = os.getenv("MEMX_API_KEY", "local_dev_key")
BASE_URL = os.getenv("MEMX_BASE_URL")

KEY_RESEARCH = "loop:research"
KEY_CRITIQUE_V1 = "loop:critique_v1"
KEY_FINAL = "loop:final"
KEY_CRITIQUE_V2 = "loop:critique_v2"

MODEL_RESEARCH = os.getenv("MEMX_DEMO_MODEL_RESEARCH", "gemini-1.5-flash")
MODEL_CRITIC = os.getenv("MEMX_DEMO_MODEL_CRITIC", "gemini-1.5-flash")
MODEL_SYNTHESIZER = os.getenv("MEMX_DEMO_MODEL_SYNTHESIZER", "gemini-1.5-flash")


def make_ctx() -> memxContext:
    """Create a memX client honoring MEMX_API_KEY / MEMX_BASE_URL env vars."""
    return memxContext(api_key=API_KEY, base_url=BASE_URL)


def unwrap_value(payload):
    """
    memX responses are envelopes with `value` + `ts`; subscription events also use `value`.
    This helper extracts the underlying value.
    """
    if isinstance(payload, dict) and "value" in payload:
        return payload["value"]
    return payload


def ensure_google_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY env var is required for the Google GenAI LLM client.")


def wait_forever():
    """Keep the process alive so subscription callbacks can fire indefinitely."""
    while True:
        time.sleep(3600)


def log(agent: str, message: str):
    """Lightweight log helper to keep output consistent."""
    print(f"[{agent}] {message}")


def preview(text, length: int = 120) -> str:
    """Return a short, single-line preview of text values for logging."""
    if text is None:
        return ""
    line = str(text).replace("\n", " ").strip()
    return line[:length] + ("..." if len(line) > length else "")
