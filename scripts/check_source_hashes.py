#!/usr/bin/env python3
"""Verify preserved raw-source files against data/SHA256SUMS."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "SHA256SUMS"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    failures: list[str] = []
    checked = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing: {relative}")
            continue
        actual = sha256(path)
        checked += 1
        if actual != expected:
            failures.append(
                f"mismatch: {relative}\n  expected {expected}\n  actual   {actual}"
            )

    if failures:
        raise SystemExit("Source-integrity check failed:\n" + "\n".join(failures))
    print(f"Source-integrity check passed ({checked} files)")


if __name__ == "__main__":
    main()
