#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes a single line of text to entry.txt in the output directory named by
MAKEFUN_OUTPUT_DIR (default: /output). The line is a plain string constant so
two runs produce byte-identical output: no clock, no randomness, no network.
No trailing newline is written, so the byte count is exactly the line.
"""

import os

LINE = (
    "Third try in bed four, the old man's vein held, and Nadia walked "
    "to the linen room before she let herself grin."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "wb") as fh:
        fh.write(LINE.encode("utf-8"))


if __name__ == "__main__":
    main()
# entry.txt is written with no trailing newline, so its byte count equals the line exactly.
