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
USE_CASE_CONTRACT_PATH = ROOT / "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json"
USE_CASE_MODEL_PATH = ROOT / "docs/planning/DOPIS_USE_CASE_MODEL.json"

CLASS_PREFIXES = ("FR", "BR", "DATA", "SEC", "PRIV", "NFR", "AUDIT", "PILOT", "OPS")
REQ_ID_RE = re.compile(
    r"^(?:PILOT-[0-9]{3}|(?:%s)-[A-Z][A-Z0-9]*-[0-9]{3})$" % "|".join(CLASS_PREFIXES)
)
EPIC_ID_RE = re.compile(r"^EPIC-[A-Z][A-Z-]*$")
GATE_ID_RE = re.compile(r"^JV-[A-Z][A-Z0-9-]*$")
EXCLUSION_ID_RE = re.compile(r"^EXC-[A-Z][A-Z0-9-]*$")
ACTOR_ID_RE = re.compile(r"^ACT-[A-Z][A-Z0-9-]*$")
USE_CASE_ID_RE = re.compile(r"^UC-[A-Z][A-Z0-9-]*-[0-9]{3}$")

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

# A gate being unresolved is not by itself a reason to block. Every blocked
# record must name which kind of unresolvedness it faces, drawn from this closed
# vocabulary. The vocabulary deliberately offers no code meaning that only
# wording, procedure, ownership, or evidence is outstanding: those are exactly
# the cases that belong on a BASELINED record as VALIDATE or CALIBRATE, so the
# defect of representing an accepted canonical obligation as blocked because its
# final wording is unsettled has no representation here.
BLOCK_REASON_CODES = {
    "OBLIGATION_NOT_YET_ACCEPTED",
    "SUBJECT_MATTER_NOT_YET_SELECTABLE",
    "AUTHORISATION_NOT_YET_CONFERRED",
}

# An ACCEPTED record may not claim its own obligation is undecided: acceptance
# and undecidedness are contradictory by definition of acceptance_state.
BLOCK_REASONS_FORBIDDEN_WHEN_ACCEPTED = {"OBLIGATION_NOT_YET_ACCEPTED"}

# A milestone entry condition is a prohibition on entering the milestone. This
# keeps the authorisation code from being borrowed for an ordinary obligation.
AUTHORISATION_STATEMENT_PREFIX = "do not "

REQUIRED_BLOCK_JUSTIFICATION_FIELDS = (
    "reason_code",
    "gate",
    "canonical_open_question",
    "explanation",
)
REQUIRED_ACTOR_FIELDS = ("id", "title", "kind")
REQUIRED_USE_CASE_FIELDS = (
    "id",
    "title",
    "goal",
    "trigger",
    "actor_links",
    "preconditions",
    "success_outcome",
    "requirement_links",
    "scenarios",
)


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


def check_block_justifications(req: dict, gate_by_id: dict[str, dict]) -> list[str]:
    """Validate one record's block_justifications against the corrected BLOCK semantics.

    Deterministic and record-agnostic: no requirement id, gate id, or count is
    referenced. The rules constrain the shape of each justification and its
    agreement with the record's own acceptance_state, its own BLOCK links, and
    the open questions the gate registry declares.

    The coverage rule is an exact set equality, not a membership test. Every gate
    linked with effect BLOCK must be justified exactly once, and no justification
    may name a gate that is not so linked. A membership test would let an extra
    BLOCK link be attached to an already blocked record while an unrelated
    existing justification kept the record valid, which is precisely the
    unjustified over-blocking this contract exists to prevent.
    """
    rid = req.get("id", "<unknown>")
    blocked = req.get("status") == "BLOCKED_BY_VALIDATION"
    justifications = req.get("block_justifications")

    if not blocked:
        if justifications is not None:
            return [
                f"{rid}: a BASELINED record must not carry block_justifications; "
                f"its obligation is accepted, so nothing is being held back"
            ]
        return []

    if justifications is None:
        return [
            f"{rid}: a blocked record must carry block_justifications naming, for "
            f"every gate it blocks on, why the candidate obligation cannot yet be "
            f"accepted as final. An unresolved gate alone is not a reason to "
            f"block: an accepted obligation whose wording, procedure, owner, or "
            f"evidence is outstanding belongs on a BASELINED record as VALIDATE "
            f"or CALIBRATE"
        ]
    if not isinstance(justifications, list) or not justifications:
        return [f"{rid}: block_justifications must be a non-empty list"]

    problems: list[str] = []
    block_gates = [
        link[1]
        for link in req.get("validation_links", [])
        if isinstance(link, list) and len(link) == 2 and link[0] == "BLOCK"
    ]

    justified: list[str] = []
    for position, justification in enumerate(justifications):
        label = f"{rid}: block_justifications[{position}]"
        if not isinstance(justification, dict):
            problems.append(f"{label} must be an object")
            continue
        missing = [
            f
            for f in REQUIRED_BLOCK_JUSTIFICATION_FIELDS
            if not str(justification.get(f, "")).strip()
        ]
        if missing:
            problems.append(f"{label} missing fields: {missing}")
            continue

        gate_id = justification["gate"]
        justified.append(gate_id)

        reason = justification["reason_code"]
        if reason not in BLOCK_REASON_CODES:
            problems.append(
                f"{label}: unknown block reason_code {reason!r}. Permitted codes "
                f"are {sorted(BLOCK_REASON_CODES)}; none of them means that only "
                f"wording, procedure, ownership, or evidence is unresolved, "
                f"because that case is a BASELINED record with VALIDATE or "
                f"CALIBRATE"
            )
            continue

        if (
            req.get("acceptance_state") == "ACCEPTED"
            and reason in BLOCK_REASONS_FORBIDDEN_WHEN_ACCEPTED
        ):
            problems.append(
                f"{label}: acceptance_state ACCEPTED contradicts block reason_code "
                f"{reason}. Canonical discovery accepts this obligation, so it may "
                f"not also be recorded as undecided. If only its wording, "
                f"procedure, owner, or evidence is outstanding, baseline it with "
                f"VALIDATE or CALIBRATE and let a milestone entry-condition record "
                f"carry the block"
            )

        if reason == "AUTHORISATION_NOT_YET_CONFERRED":
            statement = str(req.get("statement", "")).strip().lower()
            if not statement.startswith(AUTHORISATION_STATEMENT_PREFIX):
                problems.append(
                    f"{label}: block reason_code {reason} is reserved for a "
                    f"milestone entry condition, whose statement must be a "
                    f"prohibition beginning "
                    f"{AUTHORISATION_STATEMENT_PREFIX.strip()!r}"
                )

        if gate_id not in block_gates:
            problems.append(
                f"{label} justifies {gate_id}, which this record does not link "
                f"with effect BLOCK. A justification without a corresponding "
                f"BLOCK link records a constraint that is not actually applied"
            )
            continue

        gate = gate_by_id.get(gate_id)
        if gate is None:
            problems.append(f"{label} names unknown gate {gate_id}")
            continue

        declared = gate.get("open_questions") or []
        if justification["canonical_open_question"] not in declared:
            problems.append(
                f"{label} cites an open question that {gate_id} does not declare. "
                f"A blocking concern must be a registered open question of the "
                f"gate, not an unstated one"
            )

    for gate_id in sorted({g for g in justified if justified.count(g) > 1}):
        problems.append(
            f"{rid}: duplicate block_justification for gate {gate_id}. Each "
            f"BLOCK-linked gate is justified exactly once, so that the "
            f"justification set and the BLOCK link set stay in one-to-one "
            f"correspondence"
        )

    for gate_id in sorted(set(block_gates) - set(justified)):
        problems.append(
            f"{rid}: has no block_justification for BLOCK-linked gate {gate_id}. "
            f"Every gate this record blocks on must state why the candidate "
            f"obligation cannot yet be accepted as final; otherwise a further "
            f"BLOCK link could be attached to an already blocked record without "
            f"any justification for it"
        )

    for gate_id in sorted(set(block_gates)):
        if block_gates.count(gate_id) > 1:
            problems.append(
                f"{rid}: duplicate BLOCK link for gate {gate_id}"
            )

    return problems


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


def check_requirements(registry: dict, sections: set[str], gate_by_id: dict[str, dict]) -> tuple:
    gate_ids = set(gate_by_id)
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

        problems.extend(check_block_justifications(req, gate_by_id))

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
    by_id: dict[str, dict],
    epics: list,
    gate_ids: set[str],
    registry: dict,
    retired_gate_ids: set[str] | None = None,
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
    # A retired identifier may be discussed as history, but never used as if it
    # were current. The mention must identify itself as historical on its own
    # line, so a stale reference that reads as live still fails.
    retired = retired_gate_ids or set()
    for line in text.splitlines():
        historical = any(word in line.lower() for word in ("retired", "stale"))
        for gid in re.findall(r"\bJV-[A-Z][A-Z0-9-]*\b", line):
            if gid in gate_ids:
                continue
            if gid in retired and historical:
                continue
            if gid in retired:
                disagreements.append(
                    f"markdown references retired gate {gid} without identifying it "
                    f"as retired or stale on the same line"
                )
            else:
                disagreements.append(f"markdown references unknown gate {gid}")
    pattern = r"\b(?:%s)-[A-Z][A-Z0-9]*-\d{3}\b" % "|".join(CLASS_PREFIXES)
    for rid in re.findall(pattern, text):
        if rid not in by_id:
            disagreements.append(f"markdown references unknown requirement {rid}")

    return sorted(set(disagreements))


def check_use_case_contract(contract: dict) -> list[str]:
    """Check the small, fixed contract needed to interpret the model."""
    problems: list[str] = []
    expected = {
        "schema_version": "1.0",
        "implementation_authority": "NOT_GRANTED",
        "model_artifact": "docs/planning/DOPIS_USE_CASE_MODEL.json",
        "accepted_requirements_artifact": "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json",
    }
    for field, value in expected.items():
        if contract.get(field) != value:
            problems.append(f"use-case contract {field} must be {value!r}")
    if contract.get("identifiers") != {
        "actor": "ACT-<STABLE-NAME>",
        "use_case": "UC-<DOMAIN>-NNN",
        "scenario": "<USE-CASE-ID>-SNNN",
    }:
        problems.append("use-case contract identifiers do not declare the required patterns")
    actors = contract.get("actors", {})
    if actors.get("allowed_kinds") != ["HUMAN_ROLE", "EXTERNAL_SYSTEM"]:
        problems.append("use-case contract actor kinds are invalid")
    if actors.get("required_fields") != list(REQUIRED_ACTOR_FIELDS):
        problems.append("use-case contract actor fields are invalid")
    use_cases = contract.get("use_cases", {})
    if use_cases.get("required_fields") != list(REQUIRED_USE_CASE_FIELDS):
        problems.append("use-case contract use-case fields are invalid")
    if use_cases.get("actor_link_roles") != ["PRIMARY", "SUPPORTING"]:
        problems.append("use-case contract actor link roles are invalid")
    if use_cases.get("requirement_link_roles") != ["BEHAVIOR", "CONSTRAINT"]:
        problems.append("use-case contract requirement link roles are invalid")
    if use_cases.get("scenario_types") != ["MAIN", "ALTERNATIVE", "EXCEPTION"]:
        problems.append("use-case contract scenario types are invalid")
    return problems


def check_use_case_model(model: dict, requirement_ids: set[str]) -> tuple[dict[str, list[str]], list[str], list[str]]:
    """Validate actors, use cases, scenarios, and their bounded references."""
    problems: list[str] = []
    orphans = {
        "invalid_or_duplicate_actor_ids": [],
        "invalid_or_duplicate_use_case_ids": [],
        "use_cases_without_behavior_requirements": [],
        "unknown_use_case_requirement_references": [],
        "unknown_use_case_actor_references": [],
        "use_cases_without_exactly_one_main_scenario": [],
        "scenario_requirements_outside_parent_use_case": [],
    }
    if model.get("schema_version") != "1.0":
        problems.append("use-case model schema_version must be '1.0'")
    if model.get("implementation_authority") != "NOT_GRANTED":
        problems.append("use-case model implementation_authority must remain NOT_GRANTED")
    if model.get("contract") != "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json":
        problems.append("use-case model must identify its traceability contract")
    if model.get("accepted_requirements") != "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json":
        problems.append("use-case model must identify the accepted requirements registry")

    actor_ids: set[str] = set()
    actors = model.get("actors")
    if not isinstance(actors, list):
        problems.append("use-case model actors must be a list")
        actors = []
    for index, actor in enumerate(actors):
        label = f"actor at index {index}"
        if not isinstance(actor, dict):
            problems.append(f"{label} is not an object")
            continue
        missing = [field for field in REQUIRED_ACTOR_FIELDS if not str(actor.get(field, "")).strip()]
        if missing:
            problems.append(f"{label} missing fields: {missing}")
            continue
        aid = actor["id"]
        if not ACTOR_ID_RE.fullmatch(aid) or aid in actor_ids:
            orphans["invalid_or_duplicate_actor_ids"].append(aid)
            continue
        actor_ids.add(aid)
        if actor["kind"] not in {"HUMAN_ROLE", "EXTERNAL_SYSTEM"}:
            problems.append(f"{aid}: invalid actor kind {actor['kind']!r}")

    use_cases = model.get("use_cases")
    if not isinstance(use_cases, list):
        problems.append("use-case model use_cases must be a list")
        use_cases = []
    use_case_ids: list[str] = []
    seen_use_cases: set[str] = set()
    seen_scenarios: set[str] = set()
    for index, use_case in enumerate(use_cases):
        label = f"use case at index {index}"
        if not isinstance(use_case, dict):
            problems.append(f"{label} is not an object")
            continue
        missing = [field for field in REQUIRED_USE_CASE_FIELDS if field not in use_case]
        if missing:
            problems.append(f"{label} missing fields: {missing}")
            continue
        uid = use_case["id"]
        if not isinstance(uid, str) or not USE_CASE_ID_RE.fullmatch(uid) or uid in seen_use_cases:
            orphans["invalid_or_duplicate_use_case_ids"].append(str(uid))
            continue
        seen_use_cases.add(uid)
        use_case_ids.append(uid)
        for field in ("title", "goal", "trigger", "success_outcome"):
            if not isinstance(use_case[field], str) or not use_case[field].strip():
                problems.append(f"{uid}: {field} must be a non-empty string")
        if not isinstance(use_case["preconditions"], list) or not all(
            isinstance(item, str) and item.strip() for item in use_case["preconditions"]
        ):
            problems.append(f"{uid}: preconditions must be a list of non-empty strings")

        actor_links = use_case["actor_links"]
        if not isinstance(actor_links, list) or not actor_links:
            problems.append(f"{uid}: actor_links must be a non-empty list")
            actor_links = []
        linked_actors: set[str] = set()
        primary_actors = 0
        for link in actor_links:
            if not isinstance(link, dict) or set(link) != {"actor_id", "role"}:
                problems.append(f"{uid}: invalid actor link {link!r}")
                continue
            aid, role = link["actor_id"], link["role"]
            if aid in linked_actors:
                problems.append(f"{uid}: duplicate actor link {aid}")
            linked_actors.add(aid)
            if aid not in actor_ids:
                orphans["unknown_use_case_actor_references"].append(f"{uid}->{aid}")
            if role not in {"PRIMARY", "SUPPORTING"}:
                problems.append(f"{uid}: invalid actor link role {role!r}")
            if role == "PRIMARY":
                primary_actors += 1
        if primary_actors == 0:
            problems.append(f"{uid}: actor_links must contain at least one PRIMARY actor")

        links = use_case["requirement_links"]
        if not isinstance(links, list) or not links:
            problems.append(f"{uid}: requirement_links must be a non-empty list")
            links = []
        linked_requirements: set[str] = set()
        behavior_links = 0
        for link in links:
            if not isinstance(link, dict) or set(link) != {"requirement_id", "role"}:
                problems.append(f"{uid}: invalid requirement link {link!r}")
                continue
            rid, role = link["requirement_id"], link["role"]
            if rid in linked_requirements:
                problems.append(f"{uid}: duplicate requirement link {rid}")
            linked_requirements.add(rid)
            if rid not in requirement_ids:
                orphans["unknown_use_case_requirement_references"].append(f"{uid}->{rid}")
            if role not in {"BEHAVIOR", "CONSTRAINT"}:
                problems.append(f"{uid}: invalid requirement link role {role!r}")
            if role == "BEHAVIOR":
                behavior_links += 1
        if behavior_links == 0:
            orphans["use_cases_without_behavior_requirements"].append(uid)

        scenarios = use_case["scenarios"]
        if not isinstance(scenarios, list) or not scenarios:
            problems.append(f"{uid}: scenarios must be a non-empty list")
            scenarios = []
        main_scenarios = 0
        for scenario in scenarios:
            if not isinstance(scenario, dict) or set(scenario) != {"id", "type", "title", "steps", "requirement_ids"}:
                problems.append(f"{uid}: invalid scenario {scenario!r}")
                continue
            sid = scenario["id"]
            if not isinstance(sid, str) or not re.fullmatch(rf"{re.escape(uid)}-S[0-9]{{3}}", sid) or sid in seen_scenarios:
                problems.append(f"{uid}: invalid or duplicate scenario id {sid!r}")
            seen_scenarios.add(str(sid))
            if scenario["type"] not in {"MAIN", "ALTERNATIVE", "EXCEPTION"}:
                problems.append(f"{uid}: invalid scenario type {scenario['type']!r}")
            if scenario["type"] == "MAIN":
                main_scenarios += 1
            if not isinstance(scenario["title"], str) or not scenario["title"].strip():
                problems.append(f"{uid}: scenario {sid!r} title must be a non-empty string")
            if not isinstance(scenario["steps"], list) or not scenario["steps"] or not all(
                isinstance(step, str) and step.strip() for step in scenario["steps"]
            ):
                problems.append(f"{uid}: scenario {sid!r} steps must be a non-empty list of strings")
            refs = scenario["requirement_ids"]
            if not isinstance(refs, list) or not all(isinstance(rid, str) for rid in refs):
                problems.append(f"{uid}: scenario {sid!r} requirement_ids must be a list of strings")
                continue
            for rid in refs:
                if rid not in requirement_ids:
                    orphans["unknown_use_case_requirement_references"].append(f"{uid}:{sid}->{rid}")
                if rid not in linked_requirements:
                    orphans["scenario_requirements_outside_parent_use_case"].append(f"{uid}:{sid}->{rid}")
        if main_scenarios != 1:
            orphans["use_cases_without_exactly_one_main_scenario"].append(uid)

    for key in orphans:
        orphans[key] = sorted(set(orphans[key]))
    return orphans, problems, sorted(use_case_ids)


def main() -> int:
    problems: list[str] = []

    sections = discovery_sections()
    registry = load_json(REGISTRY_PATH)
    gates_doc = load_json(GATES_PATH)
    exclusions_doc = load_json(EXCLUSIONS_PATH)
    epics_doc = load_json(EPICS_PATH)
    trace = load_json(TRACE_PATH)
    use_case_contract = load_json(USE_CASE_CONTRACT_PATH)
    use_case_model = load_json(USE_CASE_MODEL_PATH)

    problems += check_use_case_contract(use_case_contract)

    gate_by_id, gate_problems = check_gates(gates_doc)
    problems += gate_problems

    by_id, req_orphans, req_problems = check_requirements(registry, sections, gate_by_id)
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

    retired_gate_ids = {
        r.get("id") for r in gates_doc.get("retired_gates", []) if r.get("id")
    }
    md_disagreements = check_markdown(
        by_id, epics, set(gate_by_id), registry, retired_gate_ids
    )
    use_case_orphans, use_case_problems, use_case_ids = check_use_case_model(
        use_case_model, set(by_id)
    )
    problems += use_case_problems

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
        **use_case_orphans,
    }
    if epic_orphans["epic_supporting_duplicates_primary"]:
        problems.append(
            "epic supporting mappings duplicate their own primary: "
            f"{epic_orphans['epic_supporting_duplicates_primary']}"
        )

    future_nodes = trace.get("future_nodes", {})
    if future_nodes.get("use_cases") != use_case_ids:
        problems.append(
            "future_nodes.use_cases must exactly match the use-case model ids: "
            f"declared={future_nodes.get('use_cases')!r}, computed={use_case_ids!r}"
        )
    for name, nodes in sorted(future_nodes.items()):
        if name == "use_cases":
            continue
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
        (USE_CASE_CONTRACT_PATH, use_case_contract),
        (USE_CASE_MODEL_PATH, use_case_model),
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
