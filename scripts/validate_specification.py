#!/usr/bin/env python3
"""Validate Dopis specification artifacts.

Design rules for this validator:

1. Nothing is hard-coded that the artifacts can state themselves. There is no
   expected requirement count, epic count, gate count, or part count in this
   file. Every total is derived and then compared against the checksum the
   traceability matrix declares, so a stale checksum fails rather than passes.
2. Every claim the traceability matrix makes is recomputed here. An empty
   orphan array is only accepted when the computed set is also empty.
3. Cross-artifact references are resolved rather than assumed: canonical
   discovery sections, validation gates, epics, exclusions, dependencies, and
   the human-readable baseline are all checked against the machine registry.
4. Standard library only. Deterministic. Non-zero exit status on failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DISCOVERY_PATH = ROOT / "docs/current/DOPIS_TECHNICAL_DISCOVERY.md"
REGISTRY_PATH = ROOT / "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json"
GATES_PATH = ROOT / "docs/current/requirements/DOPIS_VALIDATION_GATES.json"
EXCLUSIONS_PATH = ROOT / "docs/current/requirements/DOPIS_EXCLUSIONS.json"
EPICS_PATH = ROOT / "docs/backlog/DOPIS_EPICS.json"
TRACE_PATH = ROOT / "docs/traceability/DOPIS_TRACEABILITY_MATRIX.json"
BASELINE_MD_PATH = ROOT / "docs/current/DOPIS_MVP_REQUIREMENTS.md"

CLASS_PREFIXES = ("FR", "BR", "DATA", "SEC", "PRIV", "NFR", "AUDIT", "PILOT", "OPS")
REQ_ID_RE = re.compile(
    r"^(?:PILOT-[0-9]{3}|(?:%s)-[A-Z][A-Z0-9]*-[0-9]{3})$" % "|".join(CLASS_PREFIXES)
)
EPIC_ID_RE = re.compile(r"^EPIC-[A-Z][A-Z-]*$")
GATE_ID_RE = re.compile(r"^JV-[A-Z][A-Z0-9-]*$")
EXCLUSION_ID_RE = re.compile(r"^EXC-[A-Z][A-Z0-9-]*$")

# Matches "## 1. Title", "### 2.1 Title", "## 10A. Title", "### 7.4A Title".
HEADING_RE = re.compile(r"^#{1,6}\s+(\d+[A-Z]?(?:\.\d+[A-Z]?)*)\.?(?:\s|$)")

ALLOWED_ACCEPTANCE = {"ACCEPTED", "PROVISIONAL", "CONDITIONAL"}
ALLOWED_MILESTONE = {"PILOT", "WITHOUT_JAIME", "PUBLIC_LAUNCH"}
ALLOWED_STATUS = {"BASELINED", "BLOCKED_BY_VALIDATION"}
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
ALLOWED_GATE_MILESTONE = {"PILOT", "WITHOUT_JAIME", "PUBLIC_LAUNCH", "CLOSED"}
ALLOWED_GATE_ORIGIN = {"CANONICAL", "DERIVED"}

REQUIRED_REQ_FIELDS = (
    "id",
    "statement",
    "class",
    "acceptance_state",
    "readiness_milestone",
    "status",
    "priority",
    "rationale",
    "business_source",
    "verification_method",
    "validation_links",
    "dependencies",
    "notes",
)

# Weak modal verbs must not carry the obligation of a requirement statement.
WEAK_OPENERS = ("should ", "could ", "might ", "may want", "ideally")


class Failure(Exception):
    """Raised with an accumulated list of human-readable problems."""


def load_json(path: Path) -> dict:
    if not path.exists():
        raise Failure([f"missing artifact: {path.relative_to(ROOT)}"])
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise Failure([f"invalid JSON in {path.relative_to(ROOT)}: {exc}"]) from exc


def discovery_sections() -> set[str]:
    if not DISCOVERY_PATH.exists():
        raise Failure([f"missing canonical discovery: {DISCOVERY_PATH.relative_to(ROOT)}"])
    sections: set[str] = set()
    for line in DISCOVERY_PATH.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match:
            sections.add(match.group(1))
    if not sections:
        raise Failure(["parsed zero sections from the canonical discovery"])
    return sections


def find_cycle(graph: dict[str, list[str]]) -> list[str]:
    """Return one dependency cycle as a list of ids, or an empty list."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}
    stack: list[str] = []

    def visit(node: str) -> list[str]:
        colour[node] = GREY
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in colour:
                continue
            if colour[nxt] == GREY:
                return stack[stack.index(nxt):] + [nxt]
            if colour[nxt] == WHITE:
                found = visit(nxt)
                if found:
                    return found
        stack.pop()
        colour[node] = BLACK
        return []

    for node in sorted(graph):
        if colour[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return []


def check_gates(gates_doc: dict) -> tuple[dict[str, dict], list[str]]:
    problems: list[str] = []
    gates = gates_doc.get("gates")
    if not isinstance(gates, list) or not gates:
        raise Failure(["validation gate registry contains no gates list"])
    by_id: dict[str, dict] = {}
    for gate in gates:
        gid = gate.get("id", "")
        if not GATE_ID_RE.fullmatch(str(gid)):
            problems.append(f"invalid gate id: {gid!r}")
            continue
        if gid in by_id:
            problems.append(f"duplicate gate id: {gid}")
            continue
        by_id[gid] = gate
        if gate.get("milestone") not in ALLOWED_GATE_MILESTONE:
            problems.append(f"{gid}: invalid milestone {gate.get('milestone')!r}")
        if gate.get("origin") not in ALLOWED_GATE_ORIGIN:
            problems.append(f"{gid}: invalid origin {gate.get('origin')!r}")
        if not str(gate.get("resolution_criteria", "")).strip():
            problems.append(f"{gid}: missing resolution_criteria")
        if not gate.get("source_sections"):
            problems.append(f"{gid}: missing source_sections")
        if gate.get("origin") == "DERIVED" and not str(
            gate.get("derivation_rationale", "")
        ).strip():
            problems.append(
                f"{gid}: a derived gate must state a derivation_rationale so it "
                f"cannot be mistaken for a canonically registered gate"
            )
    retired = {r.get("id") for r in gates_doc.get("retired_gates", [])}
    for gid in sorted(retired & set(by_id)):
        problems.append(
            f"{gid}: listed both as an active gate and as a retired gate"
        )
    for entry in gates_doc.get("retired_gates", []):
        if not str(entry.get("disposition", "")).strip():
            problems.append(
                f"{entry.get('id')!r}: a retired gate must record the gate that now "
                f"carries its concern"
            )
    return by_id, problems


def check_requirements(registry: dict, sections: set[str], gate_ids: set[str]) -> tuple:
    problems: list[str] = []
    requirements = registry.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise Failure(["requirement registry contains no requirements list"])

    by_id: dict[str, dict] = {}
    orphans: dict[str, list[str]] = {
        "requirements_without_business_source": [],
        "requirements_with_unresolved_business_source": [],
        "requirements_without_rationale": [],
        "blocked_requirements_without_block_gate": [],
        "baselined_requirements_with_block_gate": [],
        "unknown_gate_references": [],
        "unresolved_dependencies": [],
    }

    for index, req in enumerate(requirements):
        if not isinstance(req, dict):
            problems.append(f"requirement at index {index} is not an object")
            continue
        missing = [f for f in REQUIRED_REQ_FIELDS if f not in req]
        if missing:
            problems.append(f"{req.get('id', f'<index {index}>')} missing fields: {missing}")
            continue

        rid = req["id"]
        if not isinstance(rid, str) or not REQ_ID_RE.fullmatch(rid):
            problems.append(f"invalid requirement id: {rid!r}")
            continue
        if rid in by_id:
            problems.append(f"duplicate requirement id: {rid}")
            continue
        by_id[rid] = req

        if req["class"] != rid.split("-", 1)[0]:
            problems.append(f"{rid}: class {req['class']!r} does not match id prefix")
        for field, allowed in (
            ("acceptance_state", ALLOWED_ACCEPTANCE),
            ("readiness_milestone", ALLOWED_MILESTONE),
            ("status", ALLOWED_STATUS),
            ("priority", ALLOWED_PRIORITY),
            ("verification_method", ALLOWED_VERIFICATION),
        ):
            if req[field] not in allowed:
                problems.append(f"{rid}: invalid {field} {req[field]!r}")

        statement = req["statement"]
        if not isinstance(statement, str) or not statement.strip():
            problems.append(f"{rid}: empty statement")
        else:
            lowered = statement.strip().lower()
            if any(lowered.startswith(w) for w in WEAK_OPENERS):
                problems.append(f"{rid}: statement opens with a weak modal verb")
            if not statement.rstrip().endswith("."):
                problems.append(f"{rid}: statement must end with a full stop")

        if not str(req["rationale"]).strip():
            orphans["requirements_without_rationale"].append(rid)

        source = req["business_source"]
        if not isinstance(source, list) or not source:
            orphans["requirements_without_business_source"].append(rid)
        else:
            unresolved = [s for s in source if s not in sections]
            if unresolved:
                orphans["requirements_with_unresolved_business_source"].append(
                    f"{rid}->{sorted(unresolved)}"
                )

        has_block = False
        links = req["validation_links"]
        if not isinstance(links, list):
            problems.append(f"{rid}: validation_links must be a list")
            links = []
        seen_links: set[tuple] = set()
        for link in links:
            if not isinstance(link, list) or len(link) != 2:
                problems.append(f"{rid}: invalid validation link {link!r}")
                continue
            effect, gate = link
            if effect not in ALLOWED_EFFECT:
                problems.append(f"{rid}: invalid gate effect {effect!r}")
            if not isinstance(gate, str) or not GATE_ID_RE.fullmatch(gate):
                problems.append(f"{rid}: malformed gate id {gate!r}")
            elif gate not in gate_ids:
                orphans["unknown_gate_references"].append(f"{rid}->{gate}")
            if (effect, gate) in seen_links:
                problems.append(f"{rid}: duplicate validation link {effect} {gate}")
            seen_links.add((effect, gate))
            has_block |= effect == "BLOCK"

        if req["status"] == "BLOCKED_BY_VALIDATION" and not has_block:
            orphans["blocked_requirements_without_block_gate"].append(rid)
        if req["status"] == "BASELINED" and has_block:
            orphans["baselined_requirements_with_block_gate"].append(rid)

        if not isinstance(req["dependencies"], list):
            problems.append(f"{rid}: dependencies must be a list")

    for rid, req in by_id.items():
        for dep in req.get("dependencies", []):
            if dep == rid:
                orphans["unresolved_dependencies"].append(f"{rid}->self")
            elif dep not in by_id:
                orphans["unresolved_dependencies"].append(f"{rid}->{dep}")

    graph = {rid: [d for d in r.get("dependencies", []) if d in by_id] for rid, r in by_id.items()}
    cycle = find_cycle(graph)
    orphans["dependency_cycles"] = [" -> ".join(cycle)] if cycle else []

    for key in orphans:
        orphans[key] = sorted(orphans[key])
    return by_id, orphans, problems


def check_epics(epics_doc: dict, by_id: dict[str, dict]) -> tuple:
    problems: list[str] = []
    epics = epics_doc.get("epics")
    if not isinstance(epics, list) or not epics:
        raise Failure(["epic map contains no epics list"])

    primary_of: dict[str, list[str]] = {}
    unknown_links: list[str] = []
    duplicate_support: list[str] = []
    seen: set[str] = set()

    for epic in epics:
        eid = epic.get("id", "")
        if not EPIC_ID_RE.fullmatch(str(eid)):
            problems.append(f"invalid epic id: {eid!r}")
            continue
        if eid in seen:
            problems.append(f"duplicate epic id: {eid}")
            continue
        seen.add(eid)
        if not str(epic.get("goal", "")).strip():
            problems.append(f"{eid}: missing goal")

        primary = epic.get("primary", [])
        supporting = epic.get("supporting", [])
        if not isinstance(primary, list) or not primary:
            problems.append(f"{eid}: must own at least one primary requirement")
            primary = []
        if supporting and not str(epic.get("supporting_rationale", "")).strip():
            problems.append(f"{eid}: supporting mappings require a supporting_rationale")

        for rid in primary:
            if rid not in by_id:
                unknown_links.append(f"{eid}->primary:{rid}")
            else:
                primary_of.setdefault(rid, []).append(eid)
        for rid in supporting:
            if rid not in by_id:
                unknown_links.append(f"{eid}->supporting:{rid}")
            elif rid in primary:
                duplicate_support.append(f"{eid}->{rid}")

    without_primary = sorted(set(by_id) - set(primary_of))
    multiple_primary = sorted(r for r, e in primary_of.items() if len(e) > 1)
    return (
        epics,
        {
            "requirements_without_primary_epic": without_primary,
            "requirements_with_multiple_primary_epics": multiple_primary,
            "epic_links_to_unknown_requirements": sorted(unknown_links),
            "epic_supporting_duplicates_primary": sorted(duplicate_support),
        },
        problems,
    )


def check_exclusions(exclusions_doc: dict, by_id: dict[str, dict]) -> tuple:
    problems: list[str] = []
    exclusions = exclusions_doc.get("exclusions")
    if not isinstance(exclusions, list) or not exclusions:
        raise Failure(["exclusion registry contains no exclusions list"])

    contradicted: list[str] = []
    for exclusion in exclusions:
        xid = exclusion.get("id", "")
        if not EXCLUSION_ID_RE.fullmatch(str(xid)):
            problems.append(f"invalid exclusion id: {xid!r}")
            continue
        if not exclusion.get("source_sections"):
            problems.append(f"{xid}: missing source_sections")
        enforced_by = exclusion.get("enforced_by", [])
        for rid in enforced_by:
            if rid not in by_id:
                problems.append(f"{xid}: enforced_by references unknown requirement {rid}")
        terms = exclusion.get("forbidden_terms", [])
        if not terms:
            problems.append(f"{xid}: missing forbidden_terms, so it cannot be checked")
        allowed = set(enforced_by)
        for rid, req in sorted(by_id.items()):
            if rid in allowed:
                continue
            statement = str(req.get("statement", "")).lower()
            for term in terms:
                if term.lower() in statement:
                    contradicted.append(f"{xid}:{term!r} appears in {rid}")
    return sorted(contradicted), problems


def check_markdown(
    by_id: dict[str, dict], epics: list, gate_ids: set[str], registry: dict
) -> list[str]:
    """The human-readable baseline must agree with the machine registry."""
    if not BASELINE_MD_PATH.exists():
        return [f"missing artifact: {BASELINE_MD_PATH.relative_to(ROOT)}"]
    text = BASELINE_MD_PATH.read_text(encoding="utf-8")
    disagreements: list[str] = []

    for marker, computed in (
        ("REGISTRY-TOTAL", len(by_id)),
        ("REGISTRY-EPICS", len(epics)),
    ):
        found = re.search(rf"{marker}:\s*(\d+)", text)
        if not found:
            disagreements.append(f"baseline markdown does not declare {marker}")
        elif int(found.group(1)) != computed:
            disagreements.append(
                f"markdown {marker}={found.group(1)} but computed value is {computed}"
            )

    found_version = re.search(r"REGISTRY-VERSION:\s*([0-9.]+)", text)
    if not found_version:
        disagreements.append("baseline markdown does not declare REGISTRY-VERSION")
    elif found_version.group(1) != registry.get("baseline_version"):
        disagreements.append(
            f"markdown REGISTRY-VERSION={found_version.group(1)} but registry "
            f"baseline_version={registry.get('baseline_version')}"
        )

    epic_ids = {e.get("id") for e in epics}
    for eid in re.findall(r"\bEPIC-[A-Z][A-Z-]*\b", text):
        if eid not in epic_ids:
            disagreements.append(f"markdown references unknown epic {eid}")
    for gid in re.findall(r"\bJV-[A-Z][A-Z0-9-]*\b", text):
        if gid not in gate_ids:
            disagreements.append(f"markdown references unknown gate {gid}")
    pattern = r"\b(?:%s)-[A-Z][A-Z0-9]*-\d{3}\b" % "|".join(CLASS_PREFIXES)
    for rid in re.findall(pattern, text):
        if rid not in by_id:
            disagreements.append(f"markdown references unknown requirement {rid}")

    return sorted(set(disagreements))


def main() -> int:
    problems: list[str] = []

    sections = discovery_sections()
    registry = load_json(REGISTRY_PATH)
    gates_doc = load_json(GATES_PATH)
    exclusions_doc = load_json(EXCLUSIONS_PATH)
    epics_doc = load_json(EPICS_PATH)
    trace = load_json(TRACE_PATH)

    gate_by_id, gate_problems = check_gates(gates_doc)
    problems += gate_problems

    by_id, req_orphans, req_problems = check_requirements(registry, sections, set(gate_by_id))
    problems += req_problems

    epics, epic_orphans, epic_problems = check_epics(epics_doc, by_id)
    problems += epic_problems

    contradicted, exclusion_problems = check_exclusions(exclusions_doc, by_id)
    problems += exclusion_problems

    for gid, gate in sorted(gate_by_id.items()):
        unresolved = [s for s in gate.get("source_sections", []) if s not in sections]
        if unresolved:
            problems.append(f"{gid}: unresolved discovery sections {sorted(unresolved)}")

    closed_blockers = sorted(
        f"{rid}->{gate}"
        for rid, req in by_id.items()
        for effect, gate in req["validation_links"]
        if effect == "BLOCK"
        and gate in gate_by_id
        and gate_by_id[gate].get("milestone") == "CLOSED"
    )

    retired_ids = {r.get("id") for r in gates_doc.get("retired_gates", [])}
    retired_references = sorted(
        f"{rid}->{gate}"
        for rid, req in by_id.items()
        for _, gate in req["validation_links"]
        if gate in retired_ids
    )
    for reference in retired_references:
        problems.append(
            f"requirement references a gate retired from the canonical register: {reference}"
        )

    md_disagreements = check_markdown(by_id, epics, set(gate_by_id), registry)

    computed = {
        **req_orphans,
        **{k: v for k, v in epic_orphans.items() if k != "epic_supporting_duplicates_primary"},
        "closed_gates_used_as_blockers": closed_blockers,
        "contradicted_exclusions": contradicted,
        "registry_and_markdown_disagreements": md_disagreements,
        "stories_without_requirements": [],
        "tasks_without_requirements": [],
        "tasks_without_acceptance_criteria": [],
        "tests_without_acceptance_targets": [],
        "stale_superseded_links": [],
    }
    if epic_orphans["epic_supporting_duplicates_primary"]:
        problems.append(
            "epic supporting mappings duplicate their own primary: "
            f"{epic_orphans['epic_supporting_duplicates_primary']}"
        )

    for name, nodes in sorted(trace.get("future_nodes", {}).items()):
        if nodes:
            problems.append(
                f"future_nodes.{name} is populated but this milestone defines no "
                f"downstream linking rules yet"
            )

    declared = trace.get("orphan_checks", {})
    for key, value in sorted(computed.items()):
        if key not in declared:
            problems.append(f"traceability matrix does not declare orphan check {key!r}")
        elif declared[key] != value:
            problems.append(
                f"orphan declaration mismatch for {key}: "
                f"declared={declared[key]!r}, computed={value!r}"
            )

    referenced_gates = {gate for req in by_id.values() for _, gate in req["validation_links"]}
    derived_counts = {
        "requirements": len(by_id),
        "epics": len(epics),
        "gates_defined": len(gate_by_id),
        "gates_referenced": len(referenced_gates),
        "exclusions": len(exclusions_doc.get("exclusions", [])),
        "blocked_requirements": sum(
            1 for r in by_id.values() if r["status"] == "BLOCKED_BY_VALIDATION"
        ),
    }
    declared_counts = trace.get("derived_counts", {})
    for key, value in sorted(derived_counts.items()):
        if key not in declared_counts:
            problems.append(f"traceability matrix does not declare derived count {key!r}")
        elif declared_counts[key] != value:
            problems.append(
                f"derived count mismatch for {key}: "
                f"declared={declared_counts[key]!r}, computed={value!r}"
            )

    # Governance guard: no specification artifact may grant implementation authority.
    for path, doc in (
        (REGISTRY_PATH, registry),
        (GATES_PATH, gates_doc),
        (EXCLUSIONS_PATH, exclusions_doc),
        (EPICS_PATH, epics_doc),
        (TRACE_PATH, trace),
    ):
        authority = doc.get("implementation_authority")
        if authority != "NOT_GRANTED":
            problems.append(
                f"{path.relative_to(ROOT)}: implementation_authority must remain "
                f"NOT_GRANTED, found {authority!r}"
            )

    if problems:
        raise Failure(problems)

    unreferenced = sorted(set(gate_by_id) - referenced_gates)
    print(
        "PASS: {requirements} requirements, {epics} epics, {gates_referenced} of "
        "{gates_defined} gates referenced, {exclusions} exclusions, "
        "{blocked_requirements} blocked requirements".format(**derived_counts)
    )
    print(f"      canonical discovery sections resolved: {len(sections)}")
    print(f"      unreferenced gates (expected: closed only): {unreferenced or 'none'}")
    print("      all declared orphan checks recomputed and matching")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("FAIL: specification validation found problems:", file=sys.stderr)
        for problem in exc.args[0]:
            print(f"  - {problem}", file=sys.stderr)
        raise SystemExit(1)
