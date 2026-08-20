#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Iterable

IMPACT_RE = re.compile(
    r"(?im)^\s*Project-State-Impact\s*:\s*(none|state|roadmap|both)\s*$"
)


class IntegrityError(RuntimeError):
    pass


def normalize_paths(values: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise IntegrityError("configured paths must be non-empty strings")
        path = value.strip().lstrip("./")
        if path.startswith("../") or path == "..":
            raise IntegrityError("configured paths must stay inside the repository")
        normalized.append(path)
    return tuple(dict.fromkeys(normalized))


def load_config(path: pathlib.Path) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"cannot read config: {exc}") from exc

    if raw.get("schema_version") != "0.1.0":
        raise IntegrityError("unsupported schema_version; expected 0.1.0")

    project_id = raw.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise IntegrityError("project_id must be a non-empty string")

    state_paths = normalize_paths(raw.get("state_paths", []))
    roadmap_paths = normalize_paths(raw.get("roadmap_paths", []))
    if not state_paths:
        raise IntegrityError("at least one state path is required")
    if not roadmap_paths:
        raise IntegrityError("at least one roadmap path is required")

    return project_id.strip(), state_paths, roadmap_paths


def parse_impact(pr_body: str) -> str:
    matches = IMPACT_RE.findall(pr_body or "")
    if len(matches) != 1:
        raise IntegrityError(
            "PR body must contain exactly one Project-State-Impact declaration"
        )
    return matches[0].lower()


def validate(
    state_paths: tuple[str, ...],
    roadmap_paths: tuple[str, ...],
    impact: str,
    changed_files: Iterable[str],
) -> list[str]:
    changed = {item.strip().lstrip("./") for item in changed_files if item.strip()}
    state_changed = any(path in changed for path in state_paths)
    roadmap_changed = any(path in changed for path in roadmap_paths)

    declares_state = impact in {"state", "both"}
    declares_roadmap = impact in {"roadmap", "both"}

    errors: list[str] = []
    if declares_state and not state_changed:
        errors.append("impact declares state, but no configured state file changed")
    if declares_roadmap and not roadmap_changed:
        errors.append("impact declares roadmap, but no configured roadmap file changed")
    if state_changed and not declares_state:
        errors.append("a configured state file changed, but impact does not declare state")
    if roadmap_changed and not declares_roadmap:
        errors.append("a configured roadmap file changed, but impact does not declare roadmap")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=pathlib.Path, required=True)
    parser.add_argument("--pr-body-file", type=pathlib.Path, required=True)
    parser.add_argument("--changed-files-file", type=pathlib.Path, required=True)
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        project_id, state_paths, roadmap_paths = load_config(args.config)
        pr_body = args.pr_body_file.read_text(encoding="utf-8")
        impact = parse_impact(pr_body)
        changed_files = args.changed_files_file.read_text(encoding="utf-8").splitlines()
        errors = validate(state_paths, roadmap_paths, impact, changed_files)
    except (OSError, IntegrityError) as exc:
        print(f"PROJECT_STATE_INTEGRITY: ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"PROJECT_STATE_INTEGRITY: FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PROJECT_STATE_INTEGRITY: PASS project={project_id} impact={impact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
