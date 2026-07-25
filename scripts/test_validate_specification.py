#!/usr/bin/env python3
"""Negative tests for scripts/validate_specification.py.

A validator that only ever passes proves nothing. Each case below copies the
real specification artifacts into a temporary tree, introduces one controlled
defect, and asserts that the validator rejects it with a recognisable message.
A control case runs the unmutated copy and asserts it passes.

The repository itself is never mutated: every fixture lives in a temporary
directory that is removed when the run finishes, whether or not it succeeds.

Standard library only. Exits non-zero if any case behaves unexpectedly.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = "scripts/validate_specification.py"

ARTIFACTS = [
    "docs/current/DOPIS_TECHNICAL_DISCOVERY.md",
    "docs/current/DOPIS_MVP_REQUIREMENTS.md",
    "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json",
    "docs/current/requirements/DOPIS_VALIDATION_GATES.json",
    "docs/current/requirements/DOPIS_EXCLUSIONS.json",
    "docs/backlog/DOPIS_EPICS.json",
    "docs/traceability/DOPIS_TRACEABILITY_MATRIX.json",
    VALIDATOR,
]

REGISTRY = "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json"
GATES = "docs/current/requirements/DOPIS_VALIDATION_GATES.json"
EPICS = "docs/backlog/DOPIS_EPICS.json"
TRACE = "docs/traceability/DOPIS_TRACEABILITY_MATRIX.json"
BASELINE_MD = "docs/current/DOPIS_MVP_REQUIREMENTS.md"


def build_tree(destination: Path) -> None:
    for relative in ARTIFACTS:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)


def read_json(tree: Path, relative: str) -> dict:
    return json.loads((tree / relative).read_text(encoding="utf-8"))


def write_json(tree: Path, relative: str, data: dict) -> None:
    (tree / relative).write_text(json.dumps(data, indent=2), encoding="utf-8")


def run(tree: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tree / VALIDATOR)],
        capture_output=True,
        text=True,
        cwd=str(tree),
    )


# --- mutations -------------------------------------------------------------


def mutate_duplicate_id(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"].append(dict(data["requirements"][0]))
    write_json(tree, REGISTRY, data)


def mutate_unknown_gate(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"][0]["validation_links"] = [["VALIDATE", "JV-DOES-NOT-EXIST"]]
    write_json(tree, REGISTRY, data)


def mutate_unresolvable_source(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"][0]["business_source"] = ["99.99"]
    write_json(tree, REGISTRY, data)


def mutate_baselined_with_block(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    for req in data["requirements"]:
        if req["status"] == "BASELINED":
            req["validation_links"] = [["BLOCK", "JV-PILOT"]]
            break
    write_json(tree, REGISTRY, data)


def mutate_blocked_without_block(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    for req in data["requirements"]:
        if req["status"] == "BLOCKED_BY_VALIDATION":
            req["validation_links"] = [["CALIBRATE", "JV-PILOT"]]
            break
    write_json(tree, REGISTRY, data)


def mutate_missing_field(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    del data["requirements"][0]["rationale"]
    write_json(tree, REGISTRY, data)


def mutate_orphan_requirement(tree: Path) -> None:
    """Drop a requirement from its owning epic so it has no primary epic."""
    epics = read_json(tree, EPICS)
    epics["epics"][0]["primary"] = epics["epics"][0]["primary"][1:]
    write_json(tree, EPICS, epics)


def mutate_epic_unknown_requirement(tree: Path) -> None:
    epics = read_json(tree, EPICS)
    epics["epics"][0]["primary"].append("FR-DOES-NOT-EXIST-999")
    write_json(tree, EPICS, epics)


def mutate_stale_counts(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    trace["derived_counts"]["requirements"] += 1
    write_json(tree, TRACE, trace)


def mutate_dependency_cycle(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    first, second = data["requirements"][0], data["requirements"][1]
    first["dependencies"] = [second["id"]]
    second["dependencies"] = [first["id"]]
    write_json(tree, REGISTRY, data)


def mutate_unresolved_dependency(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"][0]["dependencies"] = ["FR-NOWHERE-001"]
    write_json(tree, REGISTRY, data)


def mutate_contradicted_exclusion(tree: Path) -> None:
    """Reintroduce excluded scope through an unrelated requirement."""
    data = read_json(tree, REGISTRY)
    for req in data["requirements"]:
        if req["id"] == "FR-ORDER-001":
            req["statement"] = "Allow a customer to redeem a coupon during checkout."
            break
    write_json(tree, REGISTRY, data)


def mutate_derived_gate_without_rationale(tree: Path) -> None:
    gates = read_json(tree, GATES)
    for gate in gates["gates"]:
        if gate.get("origin") == "DERIVED":
            gate.pop("derivation_rationale", None)
            break
    write_json(tree, GATES, gates)


def mutate_closed_gate_blocks(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    for req in data["requirements"]:
        if req["status"] == "BLOCKED_BY_VALIDATION":
            req["validation_links"] = [["BLOCK", "JV-COHERENCE"]]
            break
    write_json(tree, REGISTRY, data)


def mutate_markdown_disagreement(tree: Path) -> None:
    path = tree / BASELINE_MD
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("REGISTRY-TOTAL: 210", "REGISTRY-TOTAL: 84"), encoding="utf-8")


def mutate_implementation_authority(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["implementation_authority"] = "GRANTED"
    write_json(tree, REGISTRY, data)


def mutate_weak_statement(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"][0]["statement"] = "Should probably show the menu."
    write_json(tree, REGISTRY, data)


CASES = [
    ("duplicate requirement id", mutate_duplicate_id, "duplicate requirement id"),
    ("unknown gate reference", mutate_unknown_gate, "unknown_gate_references"),
    ("unresolvable canonical source", mutate_unresolvable_source, "unresolved_business_source"),
    ("baselined requirement carrying a BLOCK gate", mutate_baselined_with_block,
     "baselined_requirements_with_block_gate"),
    ("blocked requirement without a BLOCK gate", mutate_blocked_without_block,
     "blocked_requirements_without_block_gate"),
    ("missing mandatory metadata field", mutate_missing_field, "missing fields"),
    ("requirement with no primary epic", mutate_orphan_requirement,
     "requirements_without_primary_epic"),
    ("epic linking an unknown requirement", mutate_epic_unknown_requirement,
     "epic_links_to_unknown_requirements"),
    ("stale derived count", mutate_stale_counts, "derived count mismatch"),
    ("dependency cycle", mutate_dependency_cycle, "dependency_cycles"),
    ("unresolved dependency", mutate_unresolved_dependency, "unresolved_dependencies"),
    ("contradicted exclusion", mutate_contradicted_exclusion, "contradicted_exclusions"),
    ("derived gate without rationale", mutate_derived_gate_without_rationale,
     "derivation_rationale"),
    ("closed gate used as a blocker", mutate_closed_gate_blocks,
     "closed_gates_used_as_blockers"),
    ("markdown disagreeing with registry", mutate_markdown_disagreement,
     "registry_and_markdown_disagreements"),
    ("implementation authority granted", mutate_implementation_authority,
     "implementation_authority must remain"),
    ("weak modal statement", mutate_weak_statement, "weak modal verb"),
]


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="dopis-spec-fixtures-") as workspace:
        base = Path(workspace)

        control = base / "control"
        build_tree(control)
        result = run(control)
        if result.returncode != 0:
            failures.append(
                f"control: unmutated artifacts must pass, got exit {result.returncode}\n"
                f"{result.stderr}"
            )
        else:
            print("ok   control: unmutated artifacts pass")

        for index, (name, mutate, expected) in enumerate(CASES):
            tree = base / f"case{index:02d}"
            build_tree(tree)
            mutate(tree)
            result = run(tree)
            if result.returncode == 0:
                failures.append(f"{name}: validator passed a defective fixture")
                print(f"FAIL {name}: validator passed a defective fixture")
                continue
            output = result.stdout + result.stderr
            if expected not in output:
                failures.append(
                    f"{name}: rejected, but no message matching {expected!r}\n{output}"
                )
                print(f"FAIL {name}: rejected without a recognisable message")
                continue
            print(f"ok   {name}: rejected with a message naming {expected!r}")

    print()
    if failures:
        print(f"NEGATIVE TESTS FAILED: {len(failures)} of {len(CASES) + 1} cases", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"PASS: {len(CASES)} defect fixtures rejected, control fixture accepted")
    print("      no fixture state written to the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
