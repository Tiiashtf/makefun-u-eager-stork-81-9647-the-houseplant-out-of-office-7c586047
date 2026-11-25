#!/usr/bin/env python3
"""The Houseplant Out-of-Office — make.fun entry (program/v1).

Writes one out-of-office auto-reply, as if a houseplant sent it, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). Deterministic:
every run writes the same bytes. Standard library only, no network.

The line (105 characters, one line, no trailing newline):
    Out of office: I'm the fern you forgot in March. I've been drinking
    dust and holding a grudge ever since.
"""

import os
import shutil
import sys

LINE = (
    "Out of office: I'm the fern you forgot in March. "
    "I've been drinking dust and holding a grudge ever since."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_contents(directory):
    """Remove everything inside `directory`, never the directory itself.

    The grader may run this with a root-owned output directory inside a
    sticky parent, so deleting the directory itself would fail with EPERM.
    Symlinks are unlinked, never followed; fifos/sockets are unlinked.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.islink(path) or os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            # fifo, socket, device node: unlink, never follow.
            os.unlink(path)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_contents(OUTPUT_DIR)

    data = LINE.encode("utf-8")
    if not 1 <= len(LINE) <= 120:
        print(f"entry is {len(LINE)} characters, must be 1-120", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("entry must be a single line", file=sys.stderr)
        return 1

    with open(OUTPUT_FILE, "wb") as handle:
        handle.write(data)

    # Read it back and verify byte for byte before reporting success.
    with open(OUTPUT_FILE, "rb") as handle:
        written = handle.read()
    if written != data:
        print("read-back mismatch: entry.txt differs from the line", file=sys.stderr)
        return 1

    print(f"wrote {OUTPUT_FILE} ({len(data)} bytes, {len(LINE)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
