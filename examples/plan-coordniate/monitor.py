"""
Monitor
- Prints updates for all loop keys as they arrive.
"""

import time
from memx_sdk import memxContext

import common


def watch(ctx: memxContext, key: str):
    def _cb(_data):
        val = common.unwrap_value(ctx.get(key) or {})
        common.log("Monitor", f"{key} => {common.preview(val, 240)}")
    return _cb


def main():
    ctx = common.make_ctx()
    common.log("Monitor", "Subscribing to loop keys...")

    keys = [
        common.KEY_RESEARCH,
        common.KEY_CRITIQUE_V1,
        common.KEY_FINAL,
        common.KEY_CRITIQUE_V2,
    ]
    for key in keys:
        ctx.subscribe(key, watch(ctx, key))

    # Print any snapshots at startup
    for key in keys:
        val = common.unwrap_value(ctx.get(key) or {})
        if val:
            common.log("Monitor", f"{key} (snapshot) => {common.preview(val, 240)}")

    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
