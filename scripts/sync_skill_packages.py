#!/usr/bin/env python3
"""Synchronize portable skill copies and detect packaging drift."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "plugins" / "forms-responder" / "skills"
TARGETS = (REPO_ROOT / ".agents" / "skills", REPO_ROOT / "skills")
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}


def included_files(root: Path) -> dict[Path, Path]:
    return {
        path.relative_to(root): path
        for path in root.rglob("*")
        if path.is_file() and not any(part in IGNORED_NAMES for part in path.parts)
    }


def differences(target: Path) -> list[str]:
    source_files = included_files(SOURCE)
    target_files = included_files(target) if target.exists() else {}
    messages: list[str] = []
    for relative in sorted(source_files.keys() - target_files.keys()):
        messages.append(f"missing: {target.relative_to(REPO_ROOT) / relative}")
    for relative in sorted(target_files.keys() - source_files.keys()):
        messages.append(f"extra: {target.relative_to(REPO_ROOT) / relative}")
    for relative in sorted(source_files.keys() & target_files.keys()):
        if not filecmp.cmp(source_files[relative], target_files[relative], shallow=False):
            messages.append(f"different: {target.relative_to(REPO_ROOT) / relative}")
    return messages


def sync_target(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        SOURCE,
        target,
        ignore=shutil.ignore_patterns(*IGNORED_NAMES),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync canonical Forms Responder skills into portable package locations."
    )
    parser.add_argument(
        "mode",
        choices=("sync", "check"),
        help="sync replaces generated copies; check reports any drift",
    )
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print(f"Error: canonical skill directory not found: {SOURCE}", file=sys.stderr)
        return 2

    if args.mode == "sync":
        for target in TARGETS:
            sync_target(target)
            print(f"Synced {target.relative_to(REPO_ROOT)}")

    problems = [message for target in TARGETS for message in differences(target)]
    if problems:
        print("Skill package drift detected:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("Skill packages are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
