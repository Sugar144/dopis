#!/usr/bin/env python3
"""Acquire exactly the GOV-GEN revision named by Dopis's consumer lock."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "framework-lock.json"
REMOTE = "https://github.com/Sugar144/general-governance.git"


def run(*args: str) -> str:
    return subprocess.run(
        args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.strip()


def fail(message: str) -> None:
    raise ValueError(message)


def lock_identity() -> dict[str, str]:
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        identity = lock["framework"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"invalid consumer lock: {exc}")
    required = {"repository", "version", "commit_sha", "release_manifest_sha256"}
    if not isinstance(identity, dict) or set(identity) != required:
        fail("consumer lock framework identity is invalid")
    if identity["repository"] != "Sugar144/general-governance":
        fail("consumer lock repository is invalid")
    return identity


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_clean_checkout(destination: Path, commit_sha: str) -> None:
    """Restore the dedicated immutable cache before any framework bytes are used."""
    run("git", "-C", str(destination), "reset", "--hard", commit_sha)
    run("git", "-C", str(destination), "clean", "-ffdx")
    if run(
        "git",
        "-C",
        str(destination),
        "status",
        "--porcelain",
        "--untracked-files=all",
        "--ignored",
    ):
        fail("acquired framework checkout is not clean")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    cache_home = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    parser.add_argument(
        "--cache-root",
        type=Path,
        default=cache_home / "dopis" / "general-governance",
    )
    args = parser.parse_args()
    try:
        identity = lock_identity()
        destination = args.cache_root / identity["commit_sha"]
        if not (destination / ".git").is_dir():
            destination.parent.mkdir(parents=True, exist_ok=True)
            run("git", "clone", "--no-checkout", REMOTE, str(destination))
        remote = run("git", "-C", str(destination), "remote", "get-url", "origin")
        if remote != REMOTE:
            fail("cache origin does not equal the durable GOV-GEN remote")
        run("git", "-C", str(destination), "fetch", "--no-tags", "origin", identity["commit_sha"])
        ensure_clean_checkout(destination, identity["commit_sha"])
        if run("git", "-C", str(destination), "rev-parse", "HEAD") != identity["commit_sha"]:
            fail("acquired framework HEAD does not equal locked commit")
        if digest(destination / "release-manifest.json") != identity["release_manifest_sha256"]:
            fail("acquired release manifest does not equal locked digest")
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
