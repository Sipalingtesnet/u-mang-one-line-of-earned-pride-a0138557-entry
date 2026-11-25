#!/usr/bin/env python3
"""Self-check for the entry: determinism and gate limits.

Runs main.py twice into two separate temporary output directories, then
confirms the two entry.txt files are byte-identical, that the sha256 matches
the expected digest, and that the text satisfies the competition gate
(1 to 240 characters, not only white space, UTF-8).

Prints "Match: True" when everything holds.
"""

import hashlib
import os
import subprocess
import sys
import tempfile

EXPECTED_SHA256 = "debed306b4ab99305f5b125f435fa1b894f81929fdd5717918020ddd6e64afef"
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "main.py")


def run_into(out_dir: str) -> bytes:
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = out_dir
    subprocess.run([sys.executable, MAIN], check=True, env=env, cwd=HERE)
    with open(os.path.join(out_dir, "entry.txt"), "rb") as fh:
        return fh.read()


def main() -> int:
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        first = run_into(a)
        second = run_into(b)

    checks = {}
    checks["byte_identical"] = first == second
    checks["sha256"] = hashlib.sha256(first).hexdigest() == EXPECTED_SHA256
    checks["no_trailing_newline"] = not first.endswith(b"\n")

    text = first.decode("utf-8")
    checks["utf8"] = isinstance(text, str)
    checks["length_1_to_240"] = 1 <= len(text) <= 240
    checks["not_whitespace_only"] = text.strip() != ""

    ok = all(checks.values())
    for name, passed in checks.items():
        print(f"{name}: {passed}")
    print(f"characters: {len(text)}")
    print(f"sha256: {hashlib.sha256(first).hexdigest()}")
    print(f"Match: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
