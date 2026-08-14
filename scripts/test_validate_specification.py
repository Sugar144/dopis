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
import re
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
    "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json",
    "docs/traceability/DOPIS_STORY_ACCEPTANCE_TRACEABILITY_CONTRACT.json",
    "docs/planning/DOPIS_USE_CASE_MODEL.json",
    "docs/backlog/DOPIS_STORIES.json",
    VALIDATOR,
]

REGISTRY = "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json"
GATES = "docs/current/requirements/DOPIS_VALIDATION_GATES.json"
EPICS = "docs/backlog/DOPIS_EPICS.json"
TRACE = "docs/traceability/DOPIS_TRACEABILITY_MATRIX.json"
USE_CASE_MODEL = "docs/planning/DOPIS_USE_CASE_MODEL.json"
STORIES = "docs/backlog/DOPIS_STORIES.json"
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


def populate_valid_use_case_model(tree: Path) -> None:
    """Create a disposable, minimal model using only real requirement IDs."""
    model = read_json(tree, USE_CASE_MODEL)
    model["actors"] = [{
        "id": "ACT-CUSTOMER",
        "title": "Customer",
        "kind": "HUMAN_ROLE",
    }]
    model["use_cases"] = [{
        "id": "UC-ORDERING-001",
        "title": "Browse published menu",
        "goal": "View the currently published menu.",
        "trigger": "The customer wants to review the menu.",
        "actor_links": [{"actor_id": "ACT-CUSTOMER", "role": "PRIMARY"}],
        "preconditions": [],
        "success_outcome": "The customer can view the published menu.",
        "requirement_links": [
            {"requirement_id": "FR-ORDER-001", "role": "BEHAVIOR"},
            {"requirement_id": "FR-ORDER-002", "role": "CONSTRAINT"},
        ],
        "scenarios": [{
            "id": "UC-ORDERING-001-S001",
            "type": "MAIN",
            "title": "Browse the published menu",
            "steps": ["The customer views the currently published menu."],
            "requirement_ids": ["FR-ORDER-001"],
        }],
    }]
    write_json(tree, USE_CASE_MODEL, model)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["use_cases"] = ["UC-ORDERING-001"]
    write_json(tree, TRACE, trace)


def populate_valid_story_backlog(tree: Path) -> None:
    """Create one disposable story and criterion using real model references."""
    backlog = read_json(tree, STORIES)
    backlog["stories"] = [{
        "id": "ST-CATALOG-001",
        "title": "Browse menu information",
        "actor_id": "ACT-CUSTOMER",
        "actor_goal": "Review available menu information.",
        "value_outcome": "The customer can make an informed menu choice.",
        "parent_use_case_id": "UC-CATALOG-001",
        "parent_scenario_ids": ["UC-CATALOG-001-S001"],
        "requirement_links": [{"requirement_id": "FR-ORDER-001", "role": "BEHAVIOR"}],
        "dependencies": [],
        "acceptance_criteria": [{
            "id": "ST-CATALOG-001-AC001",
            "title": "Menu information is observable",
            "context": "A customer is browsing the published menu.",
            "event": "The customer reviews an available item.",
            "expected_outcomes": ["The item information is observable to the customer."],
            "requirement_ids": ["FR-ORDER-001"],
        }],
    }]
    write_json(tree, STORIES, backlog)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["stories"] = ["ST-CATALOG-001"]
    trace["future_nodes"]["acceptance_criteria"] = ["ST-CATALOG-001-AC001"]
    write_json(tree, TRACE, trace)


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
    # Derived from whatever the document currently declares, so the fixture does
    # not hard-code a total that changes with every baseline revision.
    mutated, count = re.subn(
        r"REGISTRY-TOTAL:\s*(\d+)",
        lambda m: f"REGISTRY-TOTAL: {int(m.group(1)) + 1}",
        text,
        count=1,
    )
    assert count == 1, "baseline markdown declares no REGISTRY-TOTAL marker"
    path.write_text(mutated, encoding="utf-8")


def mutate_markdown_uses_retired_gate(tree: Path) -> None:
    """Reference a retired gate identifier as if it were current."""
    gates = read_json(tree, GATES)
    retired = gates["retired_gates"][0]["id"]
    path = tree / BASELINE_MD
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text + f"\nOutstanding wording is confirmed under `{retired}`.\n",
        encoding="utf-8",
    )


def _first_blocked(data: dict) -> dict:
    for req in data["requirements"]:
        if req["status"] == "BLOCKED_BY_VALIDATION":
            return req
    raise AssertionError("registry declares no blocked requirement to mutate")


def _blocked_with_several_gates(data: dict) -> dict:
    """The first blocked record that blocks on more than one gate."""
    for req in data["requirements"]:
        if req["status"] != "BLOCKED_BY_VALIDATION":
            continue
        if len([l for l in req["validation_links"] if l[0] == "BLOCK"]) > 1:
            return req
    raise AssertionError("registry declares no multi-gate blocked requirement")


def _block_gates(req: dict) -> list:
    return [gate for effect, gate in req["validation_links"] if effect == "BLOCK"]


def _unlinked_open_gate(tree: Path, req: dict) -> str:
    """An open gate this record does not already block on.

    Chosen by scanning the gate registry rather than by identifier, and
    restricted to gates whose milestone is not CLOSED so the fixture exercises
    the justification rules rather than the separate closed-gate rule.
    """
    linked = {gate for _, gate in req["validation_links"]}
    for gate in read_json(tree, GATES)["gates"]:
        if gate["id"] not in linked and gate["milestone"] != "CLOSED":
            return gate["id"]
    raise AssertionError("gate registry offers no unlinked open gate")


def mutate_blocked_without_justification(tree: Path) -> None:
    """A blocked record that never says why the obligation cannot be accepted."""
    data = read_json(tree, REGISTRY)
    _first_blocked(data).pop("block_justifications", None)
    write_json(tree, REGISTRY, data)


def mutate_accepted_blocked_as_undecided(tree: Path) -> None:
    """The originally reported defect: an accepted obligation reported as blocked.

    An obligation canonical discovery accepts cannot also be undecided. When only
    its wording, procedure, owner, or evidence is outstanding, the record belongs
    in BASELINED with VALIDATE or CALIBRATE, and the milestone entry-condition
    record carries the block.
    """
    data = read_json(tree, REGISTRY)
    req = _first_blocked(data)
    req["acceptance_state"] = "ACCEPTED"
    req["block_justifications"][0]["reason_code"] = "OBLIGATION_NOT_YET_ACCEPTED"
    write_json(tree, REGISTRY, data)


def mutate_block_justification_unknown_question(tree: Path) -> None:
    """Block on a concern the gate never declared as an open question."""
    data = read_json(tree, REGISTRY)
    req = _first_blocked(data)
    req["block_justifications"][0]["canonical_open_question"] = (
        "an operating concern this gate does not declare"
    )
    write_json(tree, REGISTRY, data)


def mutate_block_justification_foreign_gate(tree: Path) -> None:
    """Repoint an existing justification at a gate the record does not block on."""
    data = read_json(tree, REGISTRY)
    req = _first_blocked(data)
    req["block_justifications"][0]["gate"] = _unlinked_open_gate(tree, req)
    write_json(tree, REGISTRY, data)


def mutate_baselined_with_justification(tree: Path) -> None:
    """A baselined record must not claim anything is holding its obligation back."""
    data = read_json(tree, REGISTRY)
    donor = _first_blocked(data)["block_justifications"]
    for req in data["requirements"]:
        if req["status"] == "BASELINED":
            req["block_justifications"] = [dict(j) for j in donor]
            break
    write_json(tree, REGISTRY, data)


def mutate_extra_block_link_unjustified(tree: Path) -> None:
    """The over-blocking defect this contract exists to prevent.

    Take an already blocked record, add another valid open gate as BLOCK, and
    leave its existing justifications untouched. Under a membership test the
    record would still validate; under the coverage rule it must not.
    """
    data = read_json(tree, REGISTRY)
    req = _first_blocked(data)
    req["validation_links"].append(["BLOCK", _unlinked_open_gate(tree, req)])
    write_json(tree, REGISTRY, data)


def mutate_missing_one_of_several_justifications(tree: Path) -> None:
    """Drop one justification from a record that blocks on several gates."""
    data = read_json(tree, REGISTRY)
    req = _blocked_with_several_gates(data)
    req["block_justifications"] = req["block_justifications"][1:]
    write_json(tree, REGISTRY, data)


def mutate_duplicate_justification_gate(tree: Path) -> None:
    """Justify the same gate twice, so the one-to-one correspondence is broken."""
    data = read_json(tree, REGISTRY)
    req = _blocked_with_several_gates(data)
    req["block_justifications"][1] = dict(req["block_justifications"][0])
    write_json(tree, REGISTRY, data)


def mutate_justification_for_unlinked_gate(tree: Path) -> None:
    """Append a justification for a gate that is not linked with effect BLOCK."""
    data = read_json(tree, REGISTRY)
    req = _first_blocked(data)
    gates = {g["id"]: g for g in read_json(tree, GATES)["gates"]}
    target = _unlinked_open_gate(tree, req)
    req["block_justifications"].append({
        "reason_code": req["block_justifications"][0]["reason_code"],
        "gate": target,
        "canonical_open_question": gates[target]["open_questions"][0],
        "explanation": "A constraint recorded without a corresponding BLOCK link.",
    })
    write_json(tree, REGISTRY, data)


def mutate_implementation_authority(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["implementation_authority"] = "GRANTED"
    write_json(tree, REGISTRY, data)


def mutate_weak_statement(tree: Path) -> None:
    data = read_json(tree, REGISTRY)
    data["requirements"][0]["statement"] = "Should probably show the menu."
    write_json(tree, REGISTRY, data)


def mutate_use_case_without_behavior_requirement(tree: Path) -> None:
    model = read_json(tree, USE_CASE_MODEL)
    model["use_cases"][0]["requirement_links"][0]["role"] = "CONSTRAINT"
    write_json(tree, USE_CASE_MODEL, model)


def mutate_use_case_unknown_requirement(tree: Path) -> None:
    model = read_json(tree, USE_CASE_MODEL)
    model["use_cases"][0]["requirement_links"][0]["requirement_id"] = "FR-NOWHERE-999"
    model["use_cases"][0]["scenarios"][0]["requirement_ids"] = ["FR-NOWHERE-999"]
    write_json(tree, USE_CASE_MODEL, model)


def mutate_use_case_unknown_actor(tree: Path) -> None:
    model = read_json(tree, USE_CASE_MODEL)
    model["use_cases"][0]["actor_links"][0]["actor_id"] = "ACT-NOWHERE"
    write_json(tree, USE_CASE_MODEL, model)


def mutate_scenario_requirement_outside_parent(tree: Path) -> None:
    model = read_json(tree, USE_CASE_MODEL)
    model["use_cases"][0]["scenarios"][0]["requirement_ids"] = ["DATA-ORDER-001"]
    write_json(tree, USE_CASE_MODEL, model)


def mutate_stale_use_case_index(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["use_cases"] = []
    write_json(tree, TRACE, trace)


def mutate_contract_actor_identifier_pattern(tree: Path) -> None:
    contract = read_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json")
    contract["identifiers"]["actor"]["pattern"] = "^ACT-SERVICE-[0-9]{3}$"
    write_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json", contract)


def mutate_contract_actor_kind(tree: Path) -> None:
    contract = read_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json")
    contract["actors"]["allowed_kinds"] = ["EXTERNAL_SYSTEM"]
    write_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json", contract)


def mutate_contract_required_actor_field(tree: Path) -> None:
    contract = read_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json")
    contract["actors"]["required_fields"].append("description")
    write_json(tree, "docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json", contract)


def mutate_matrix_use_case_relation(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    for relation in trace["derived_relations"]:
        if relation.get("derived_from") == "use_cases[].requirement_links with role BEHAVIOR":
            relation["relation"] = "CONSTRAINS"
            break
    write_json(tree, TRACE, trace)


def _story(tree: Path) -> dict:
    return read_json(tree, STORIES)["stories"][0]


def mutate_unknown_story_parent_use_case(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["parent_use_case_id"] = "UC-NOWHERE-001"
    write_json(tree, STORIES, data)


def mutate_story_scenario_outside_parent(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["parent_scenario_ids"] = ["UC-ORDER-001-S001"]
    write_json(tree, STORIES, data)


def mutate_story_actor_outside_parent(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["actor_id"] = "ACT-STAFF-MEMBER"
    write_json(tree, STORIES, data)


def mutate_story_requirement_role_drift(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["requirement_links"][0]["role"] = "CONSTRAINT"
    write_json(tree, STORIES, data)


def mutate_story_without_behavior_requirement(tree: Path) -> None:
    mutate_story_requirement_role_drift(tree)


def mutate_story_without_requirements(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["requirement_links"] = []
    write_json(tree, STORIES, data)


def mutate_story_without_acceptance_criterion(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["acceptance_criteria"] = []
    write_json(tree, STORIES, data)


def mutate_criterion_requirement_outside_story(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["acceptance_criteria"][0]["requirement_ids"] = ["FR-ORDER-002"]
    write_json(tree, STORIES, data)


def mutate_unknown_story_dependency(tree: Path) -> None:
    data = read_json(tree, STORIES)
    data["stories"][0]["dependencies"] = ["ST-NOWHERE-001"]
    write_json(tree, STORIES, data)


def mutate_cyclic_story_dependency(tree: Path) -> None:
    data = read_json(tree, STORIES)
    first = data["stories"][0]
    second = json.loads(json.dumps(first))
    second["id"] = "ST-CATALOG-002"
    second["acceptance_criteria"][0]["id"] = "ST-CATALOG-002-AC001"
    first["dependencies"] = [second["id"]]
    second["dependencies"] = [first["id"]]
    data["stories"].append(second)
    write_json(tree, STORIES, data)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["stories"].append(second["id"])
    trace["future_nodes"]["acceptance_criteria"].append(second["acceptance_criteria"][0]["id"])
    write_json(tree, TRACE, trace)


def mutate_stale_story_index(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["stories"] = []
    write_json(tree, TRACE, trace)


def mutate_stale_criterion_index(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["acceptance_criteria"] = []
    write_json(tree, TRACE, trace)


def mutate_matrix_story_relation(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    for relation in trace["derived_relations"]:
        if relation.get("derived_from") == "stories[].parent_use_case_id":
            relation["relation"] = "CONSTRAINS"
            break
    write_json(tree, TRACE, trace)


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
    ("markdown using a retired gate as current", mutate_markdown_uses_retired_gate,
     "retired gate"),
    ("blocked requirement without a block justification", mutate_blocked_without_justification,
     "must carry block_justifications"),
    ("accepted obligation reported as undecided", mutate_accepted_blocked_as_undecided,
     "contradicts block reason_code"),
    ("block justification citing an undeclared open question",
     mutate_block_justification_unknown_question, "does not declare"),
    ("block justification naming a gate the record does not block on",
     mutate_block_justification_foreign_gate, "does not link with effect BLOCK"),
    ("baselined requirement carrying a block justification",
     mutate_baselined_with_justification, "must not carry block_justifications"),
    ("extra BLOCK link with no corresponding justification",
     mutate_extra_block_link_unjustified, "no block_justification for BLOCK-linked gate"),
    ("missing justification for one of several BLOCK links",
     mutate_missing_one_of_several_justifications,
     "no block_justification for BLOCK-linked gate"),
    ("duplicate justifications for the same gate", mutate_duplicate_justification_gate,
     "duplicate block_justification for gate"),
    ("justification for a gate not linked as BLOCK", mutate_justification_for_unlinked_gate,
     "does not link with effect BLOCK"),
]

USE_CASE_CASES = [
    ("use case without a BEHAVIOR requirement", mutate_use_case_without_behavior_requirement,
     "use_cases_without_behavior_requirements"),
    ("use case with an unknown requirement", mutate_use_case_unknown_requirement,
     "unknown_use_case_requirement_references"),
    ("use case with an unknown actor", mutate_use_case_unknown_actor,
     "unknown_use_case_actor_references"),
    ("scenario requirement outside parent use-case links", mutate_scenario_requirement_outside_parent,
     "scenario_requirements_outside_parent_use_case"),
    ("stale use-case future-node index", mutate_stale_use_case_index,
     "future_nodes.use_cases must exactly match"),
    ("contract actor identifier pattern drift", mutate_contract_actor_identifier_pattern,
     "invalid_or_duplicate_actor_ids"),
    ("contract actor kind drift", mutate_contract_actor_kind,
     "invalid actor kind"),
    ("contract required actor field drift", mutate_contract_required_actor_field,
     "missing fields"),
    ("contract and matrix relation drift", mutate_matrix_use_case_relation,
     "use-case contract traceability relations do not match traceability matrix"),
]

STORY_CASES = [
    ("unknown story parent use case", mutate_unknown_story_parent_use_case,
     "unknown_story_parent_use_cases"),
    ("story scenario outside parent use case", mutate_story_scenario_outside_parent,
     "story_scenarios_outside_parent_use_case"),
    ("story actor outside parent use case", mutate_story_actor_outside_parent,
     "story_actors_outside_parent_use_case"),
    ("story requirement role drift", mutate_story_requirement_role_drift,
     "story_requirements_outside_parent_use_case"),
    ("story without requirement links", mutate_story_without_requirements,
     "stories_without_requirements"),
    ("story without a BEHAVIOR requirement", mutate_story_without_behavior_requirement,
     "stories_without_behavior_requirements"),
    ("story without acceptance criteria", mutate_story_without_acceptance_criterion,
     "stories_without_acceptance_criteria"),
    ("criterion requirement outside parent story", mutate_criterion_requirement_outside_story,
     "acceptance_criterion_requirements_outside_parent_story"),
    ("unknown story dependency", mutate_unknown_story_dependency,
     "unknown_story_dependencies"),
    ("cyclic story dependency", mutate_cyclic_story_dependency,
     "story_dependency_cycles"),
    ("stale story future-node index", mutate_stale_story_index,
     "future_nodes.stories must exactly match"),
    ("stale acceptance-criterion future-node index", mutate_stale_criterion_index,
     "future_nodes.acceptance_criteria must exactly match"),
    ("story contract and matrix relation drift", mutate_matrix_story_relation,
     "story contract traceability relations do not match traceability matrix"),
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
            print("ok   control: real empty PLAN-002A story backlog passes")

        populated = base / "populated-model"
        build_tree(populated)
        populate_valid_use_case_model(populated)
        result = run(populated)
        if result.returncode != 0:
            failures.append(
                "populated model: valid disposable actor/use-case/scenario fixture "
                f"must pass, got exit {result.returncode}\n{result.stderr}"
            )
        else:
            print("ok   populated model: valid disposable model passes")

        populated_story = base / "populated-story"
        build_tree(populated_story)
        populate_valid_story_backlog(populated_story)
        result = run(populated_story)
        if result.returncode != 0:
            failures.append(
                "populated story: valid disposable story and product acceptance "
                f"criterion fixture must pass, got exit {result.returncode}\n{result.stderr}"
            )
        else:
            print("ok   populated story: valid disposable story backlog passes")

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

        for index, (name, mutate, expected) in enumerate(STORY_CASES):
            tree = base / f"story{index:02d}"
            build_tree(tree)
            populate_valid_story_backlog(tree)
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

        for index, (name, mutate, expected) in enumerate(USE_CASE_CASES):
            tree = base / f"use-case{index:02d}"
            build_tree(tree)
            populate_valid_use_case_model(tree)
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
        print(f"NEGATIVE TESTS FAILED: {len(failures)} of {len(CASES) + len(USE_CASE_CASES) + len(STORY_CASES) + 3} cases", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"PASS: {len(CASES) + len(USE_CASE_CASES) + len(STORY_CASES)} defect fixtures rejected, three control fixtures accepted")
    print("      no fixture state written to the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
