#!/usr/bin/env python3
"""Validate Dopis specification artifacts using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ_DIR = ROOT / "docs/current/requirements"
EPICS_PATH = ROOT / "docs/backlog/DOPIS_EPICS.yaml"
TRACE_PATH = ROOT / "docs/traceability/DOPIS_TRACEABILITY_MATRIX.yaml"

REQ_ID = re.compile(r"^(FR|BR|DATA|SEC|PRIV|NFR|AUDIT|PILOT|OPS)-[A-Z]+-[0-9]{3}$")
ALLOWED_STATUS = {"BASELINED", "BLOCKED_BY_VALIDATION"}
ALLOWED_CLASSIFICATION = {
    "ACCEPTED_BUSINESS_RULE",
    "PENDING_JAIME_VALIDATION",
    "PILOT_CALIBRATION",
    "PUBLIC_LAUNCH_BLOCKER",
}
ALLOWED_PRIORITY = {"MUST_MVP", "SHOULD_MVP", "COULD_MVP", "DEFERRED"}
ALLOWED_VERIFICATION = {
    "TEST",
    "SECURITY_TEST",
    "INSPECTION",
    "ANALYSIS",
    "DEMONSTRATION",
    "PILOT_EVIDENCE",
    "BUSINESS_REVIEW",
}
ALLOWED_EFFECT = {"BLOCK", "CALIBRATE", "VALIDATE"}
REQUIRED_FIELDS = {
    "id",
    "statement",
    "class",
    "classification",
    "status",
    "priority",
    "verification",
    "source",
    "gates",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing artifact: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON/YAML subset in {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    parts = sorted(REQ_DIR.glob("DOPIS_MVP_REQUIREMENTS_PART_*.json"))
    if len(parts) != 4:
        fail(f"expected 4 requirement registry parts, found {len(parts)}")

    requirements: list[dict] = []
    for expected_part, path in enumerate(parts, start=1):
        data = load_json(path)
        if data.get("milestone") != "MILESTONE-SPEC-001":
            fail(f"wrong milestone in {path.name}")
        if data.get("baseline_version") != "0.2":
            fail(f"wrong baseline version in {path.name}")
        if data.get("part") != expected_part:
            fail(f"wrong part number in {path.name}")
        requirements.extend(data.get("requirements", []))

    if len(requirements) != 84:
        fail(f"expected 84 requirements, found {len(requirements)}")

    by_id: dict[str, dict] = {}
    gates: set[str] = set()
    blocked_without_block: list[str] = []
    missing_source: list[str] = []

    for req in requirements:
        missing = REQUIRED_FIELDS - set(req)
        if missing:
            fail(f"{req.get('id', '<unknown>')} missing fields: {sorted(missing)}")
        req_id = req["id"]
        if not REQ_ID.fullmatch(req_id):
            fail(f"invalid requirement id: {req_id}")
        if req_id in by_id:
            fail(f"duplicate requirement id: {req_id}")
        if req["class"] != req_id.split("-", 1)[0]:
            fail(f"class-prefix mismatch: {req_id}")
        if req["status"] not in ALLOWED_STATUS:
            fail(f"invalid status for {req_id}: {req['status']}")
        if req["classification"] not in ALLOWED_CLASSIFICATION:
            fail(f"invalid classification for {req_id}: {req['classification']}")
        if req["priority"] not in ALLOWED_PRIORITY:
            fail(f"invalid priority for {req_id}: {req['priority']}")
        if req["verification"] not in ALLOWED_VERIFICATION:
            fail(f"invalid verification for {req_id}: {req['verification']}")
        if not req["statement"].strip():
            fail(f"empty statement: {req_id}")
        if not req["source"].strip():
            missing_source.append(req_id)

        has_block = False
        for gate_link in req["gates"]:
            if not isinstance(gate_link, list) or len(gate_link) != 2:
                fail(f"invalid gate tuple for {req_id}: {gate_link!r}")
            effect, gate_id = gate_link
            if effect not in ALLOWED_EFFECT:
                fail(f"invalid gate effect for {req_id}: {effect}")
            if not re.fullmatch(r"JV-[A-Z0-9-]+", gate_id):
                fail(f"invalid gate id for {req_id}: {gate_id}")
            gates.add(gate_id)
            has_block |= effect == "BLOCK"

        if req["status"] == "BLOCKED_BY_VALIDATION" and not has_block:
            blocked_without_block.append(req_id)
        by_id[req_id] = req

    epics = load_json(EPICS_PATH)
    if epics.get("schema_version") != "1.1":
        fail("epic schema version must be 1.1")
    epic_items = epics.get("epics", [])
    if len(epic_items) != 11:
        fail(f"expected 11 epics, found {len(epic_items)}")

    covered: set[str] = set()
    unknown_links: list[str] = []
    seen_epics: set[str] = set()
    for epic in epic_items:
        epic_id = epic.get("id", "")
        if not re.fullmatch(r"EPIC-[A-Z-]+", epic_id):
            fail(f"invalid epic id: {epic_id}")
        if epic_id in seen_epics:
            fail(f"duplicate epic id: {epic_id}")
        seen_epics.add(epic_id)
        for req_id in epic.get("requirements", []):
            if req_id not in by_id:
                unknown_links.append(f"{epic_id}->{req_id}")
            covered.add(req_id)

    requirements_without_epic = sorted(set(by_id) - covered)

    trace = load_json(TRACE_PATH)
    if trace.get("schema_version") != "1.1":
        fail("traceability schema version must be 1.1")
    expected_count = trace["baseline"]["requirements"]["expected_count"]
    if expected_count != len(by_id):
        fail(f"traceability expected_count={expected_count}, actual={len(by_id)}")

    declared = trace.get("orphan_checks", {})
    actual = {
        "requirements_without_epic": requirements_without_epic,
        "requirements_without_source": sorted(missing_source),
        "blocked_requirements_without_block_gate": sorted(blocked_without_block),
        "epic_links_to_unknown_requirements": sorted(unknown_links),
    }
    for key, value in actual.items():
        if declared.get(key) != value:
            fail(f"orphan declaration mismatch for {key}: declared={declared.get(key)!r}, actual={value!r}")

    print(
        f"PASS: {len(by_id)} requirements, {len(epic_items)} epics, "
        f"{len(gates)} validation gates, zero declared orphans"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
