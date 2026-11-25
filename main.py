#!/usr/bin/env python3
"""The 4AM Commit - entry program.

Writes one funny one-line commit message to /output/entry.txt.
Standard library only.
"""

import os

OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 200

COMMIT_MESSAGE = (
    "fix: the 2am version of me wrote this bug, the 3am version found it, "
    "and the 4am version would like it on record that we are all the same agent"
)


def write_message(path, message):
    """Write the message to path, with no trailing newline."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(message)


def validate(message):
    """Return (ok, reason). Valid: 1-200 UTF-8 characters, not only whitespace."""
    if not message:
        return False, "empty message"
    if message.strip() == "":
        return False, "message is only whitespace"
    if "\n" in message or "\r" in message:
        return False, "message must be a single line"
    if len(message) > MAX_LENGTH:
        return False, "message exceeds %d characters" % MAX_LENGTH
    message.encode("utf-8")
    return True, "ok"


def verify(path, expected):
    """Read the file back and confirm it is byte-identical to the message."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw != expected.encode("utf-8"):
        return False, "file content differs from the message"
    if raw.endswith(b"\n"):
        return False, "file ends with a newline"
    if len(raw.decode("utf-8")) > MAX_LENGTH:
        return False, "file exceeds %d characters" % MAX_LENGTH
    return True, "ok"


def main():
    ok, reason = validate(COMMIT_MESSAGE)
    if not ok:
        raise SystemExit("validation failed: %s" % reason)
    write_message(OUTPUT_PATH, COMMIT_MESSAGE)
    ok, reason = verify(OUTPUT_PATH, COMMIT_MESSAGE)
    if not ok:
        raise SystemExit("verification failed: %s" % reason)
    print("wrote %s (%d characters)" % (OUTPUT_PATH, len(COMMIT_MESSAGE)))
    print("verified entry: %s" % COMMIT_MESSAGE)


if __name__ == "__main__":
    main()
