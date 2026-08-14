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
    "docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json",
    "docs/traceability/DOPIS_VERTICAL_SLICE_TRACEABILITY_CONTRACT.json",
    "docs/planning/DOPIS_VERTICAL_SLICES.json",
    VALIDATOR,
]

REGISTRY = "docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json"
GATES = "docs/current/requirements/DOPIS_VALIDATION_GATES.json"
EPICS = "docs/backlog/DOPIS_EPICS.json"
TRACE = "docs/traceability/DOPIS_TRACEABILITY_MATRIX.json"
USE_CASE_MODEL = "docs/planning/DOPIS_USE_CASE_MODEL.json"
STORIES = "docs/backlog/DOPIS_STORIES.json"
BASELINE_MD = "docs/current/DOPIS_MVP_REQUIREMENTS.md"
TECHNICAL_BASELINE = "docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json"
VS_MODEL = "docs/planning/DOPIS_VERTICAL_SLICES.json"


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
    backlog = read_json(tree, STORIES)
    backlog["stories"] = []
    write_json(tree, STORIES, backlog)
    vs_model = read_json(tree, VS_MODEL)
    vs_model["slices"] = []
    vs_model["recommended_delivery_order"] = []
    write_json(tree, VS_MODEL, vs_model)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["use_cases"] = ["UC-ORDERING-001"]
    trace["future_nodes"]["stories"] = []
    trace["future_nodes"]["acceptance_criteria"] = []
    trace["future_nodes"]["vertical_slices"] = []
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
    vs_model = read_json(tree, VS_MODEL)
    vs_model["slices"] = [{
        "id": "VS-CATALOG-001",
        "title": "Customer browses menu information",
        "observable_outcome": "The customer can make an informed menu choice.",
        "actor_ids": ["ACT-CUSTOMER"],
        "story_ids": ["ST-CATALOG-001"],
        "dependencies": [],
        "dependency_rationale": {},
        "acceptance_boundary": "Menu information observable to the customer is accurate and current.",
        "readiness_gate_ids": [],
        "technical_baseline_refs": [],
        "deferred_baseline_decision_refs": [],
    }]
    vs_model["recommended_delivery_order"] = ["VS-CATALOG-001"]
    write_json(tree, VS_MODEL, vs_model)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["stories"] = ["ST-CATALOG-001"]
    trace["future_nodes"]["acceptance_criteria"] = ["ST-CATALOG-001-AC001"]
    trace["future_nodes"]["vertical_slices"] = ["VS-CATALOG-001"]
    write_json(tree, TRACE, trace)


def populate_valid_vertical_slice_fixture(tree: Path) -> None:
    """Three disposable stories covered by three slices.

    Reuses the single-story fixture and adds:
    - a second real-use-case-backed story whose accepted dependency on the
      first crosses slice boundaries, so the induced-dependency rule has
      something real to check;
    - a third story with no story-level dependency, whose slice nonetheless
      declares a hard dependency on the first slice justified only through
      dependency_rationale, so the additional-dependency justification rule
      has a genuine non-induced edge to check.
    """
    populate_valid_story_backlog(tree)
    backlog = read_json(tree, STORIES)
    backlog["stories"].append({
        "id": "ST-ORDER-001",
        "title": "Submit a feasible guest pickup order",
        "actor_id": "ACT-CUSTOMER",
        "actor_goal": "Place a pickup order with a feasible commitment.",
        "value_outcome": "The customer receives the order outcome and pickup commitment.",
        "parent_use_case_id": "UC-ORDER-001",
        "parent_scenario_ids": ["UC-ORDER-001-S001"],
        "requirement_links": [{"requirement_id": "FR-ORDER-002", "role": "BEHAVIOR"}],
        "dependencies": ["ST-CATALOG-001"],
        "acceptance_criteria": [{
            "id": "ST-ORDER-001-AC001",
            "title": "Customer submits a feasible order",
            "context": "A guest customer has a valid basket and checkout is available.",
            "event": "The customer submits the order.",
            "expected_outcomes": ["The customer receives the resulting order status."],
            "requirement_ids": ["FR-ORDER-002"],
        }],
    })
    backlog["stories"].append({
        "id": "ST-EXTRA-001",
        "title": "Review a related recommendation",
        "actor_id": "ACT-CUSTOMER",
        "actor_goal": "Review a recommendation related to an existing basket item.",
        "value_outcome": "The customer sees a recommendation without any automatic basket change.",
        "parent_use_case_id": "UC-CATALOG-001",
        "parent_scenario_ids": ["UC-CATALOG-001-S001"],
        "requirement_links": [{"requirement_id": "FR-ORDER-001", "role": "BEHAVIOR"}],
        "dependencies": [],
        "acceptance_criteria": [{
            "id": "ST-EXTRA-001-AC001",
            "title": "Customer reviews a recommendation",
            "context": "A customer has a basket containing an eligible item.",
            "event": "The customer reviews the recommendation.",
            "expected_outcomes": ["The recommendation is observable to the customer."],
            "requirement_ids": ["FR-ORDER-001"],
        }],
    })
    write_json(tree, STORIES, backlog)
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["stories"] = ["ST-CATALOG-001", "ST-EXTRA-001", "ST-ORDER-001"]
    trace["future_nodes"]["acceptance_criteria"] = [
        "ST-CATALOG-001-AC001", "ST-EXTRA-001-AC001", "ST-ORDER-001-AC001",
    ]
    trace["future_nodes"]["vertical_slices"] = [
        "VS-CATALOG-001", "VS-EXTRA-001", "VS-ORDER-001",
    ]
    write_json(tree, TRACE, trace)

    model = read_json(tree, VS_MODEL)
    model["slices"] = [
        {
            "id": "VS-CATALOG-001",
            "title": "Customer configures a menu item",
            "observable_outcome": "A valid, informed configuration is in the customer's basket.",
            "actor_ids": ["ACT-CUSTOMER"],
            "story_ids": ["ST-CATALOG-001"],
            "dependencies": [],
            "dependency_rationale": {},
            "acceptance_boundary": "The basket contains only an allowed, currently available configuration.",
            "readiness_gate_ids": [],
            "technical_baseline_refs": [],
            "deferred_baseline_decision_refs": [],
        },
        {
            "id": "VS-ORDER-001",
            "title": "Customer submits a feasible pickup order",
            "observable_outcome": "A feasible order is submitted with its pickup commitment.",
            "actor_ids": ["ACT-CUSTOMER"],
            "story_ids": ["ST-ORDER-001"],
            "dependencies": ["VS-CATALOG-001"],
            "dependency_rationale": {},
            "acceptance_boundary": "The basket becomes a submitted order with a feasible pickup commitment.",
            "readiness_gate_ids": [],
            "technical_baseline_refs": [],
            "deferred_baseline_decision_refs": [],
        },
        {
            "id": "VS-EXTRA-001",
            "title": "Customer reviews a related recommendation",
            "observable_outcome": (
                "The customer reviews a recommendation related to an existing "
                "basket item without an automatic basket change."
            ),
            "actor_ids": ["ACT-CUSTOMER"],
            "story_ids": ["ST-EXTRA-001"],
            "dependencies": ["VS-CATALOG-001"],
            "dependency_rationale": {
                "VS-CATALOG-001": {
                    "rationale": (
                        "ST-EXTRA-001 declares no story-level dependency, so this is "
                        "not an induced dependency. Its accepted context requires an "
                        "existing eligible basket item, which only VS-CATALOG-001's "
                        "catalog/basket behavior produces."
                    ),
                    "source_refs": ["ST-CATALOG-001"],
                },
            },
            "acceptance_boundary": (
                "The recommendation is observable to the customer and any basket "
                "change happens only through the customer's confirmed choice."
            ),
            "readiness_gate_ids": [],
            "technical_baseline_refs": [],
            "deferred_baseline_decision_refs": [],
        },
    ]
    model["recommended_delivery_order"] = ["VS-CATALOG-001", "VS-ORDER-001", "VS-EXTRA-001"]
    write_json(tree, VS_MODEL, model)


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


def _vs_model(tree: Path) -> dict:
    return read_json(tree, VS_MODEL)


def mutate_vs_unknown_story_reference(tree: Path) -> None:
    model = _vs_model(tree)
    model["slices"][0]["story_ids"].append("ST-NOWHERE-001")
    write_json(tree, VS_MODEL, model)


def mutate_vs_duplicate_story_assignment(tree: Path) -> None:
    """Assign ST-ORDER-001 to both slices instead of only its own."""
    model = _vs_model(tree)
    model["slices"][0]["story_ids"].append("ST-ORDER-001")
    write_json(tree, VS_MODEL, model)


def mutate_vs_uncovered_story(tree: Path) -> None:
    """Drop ST-ORDER-001 from every slice so it is no longer covered."""
    model = _vs_model(tree)
    model["slices"] = [s for s in model["slices"] if s["id"] != "VS-ORDER-001"]
    model["recommended_delivery_order"] = ["VS-CATALOG-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_actor_union_drift(tree: Path) -> None:
    model = _vs_model(tree)
    model["slices"][0]["actor_ids"] = ["ACT-STAFF-MEMBER"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_unknown_dependency(tree: Path) -> None:
    model = _vs_model(tree)
    model["slices"][1]["dependencies"] = ["VS-NOWHERE-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_dependency_cycle(tree: Path) -> None:
    model = _vs_model(tree)
    for slice_ in model["slices"]:
        if slice_["id"] == "VS-CATALOG-001":
            slice_["dependencies"] = ["VS-ORDER-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_missing_induced_dependency(tree: Path) -> None:
    """Drop the dependency induced by ST-ORDER-001's accepted story dependency."""
    model = _vs_model(tree)
    for slice_ in model["slices"]:
        if slice_["id"] == "VS-ORDER-001":
            slice_["dependencies"] = []
    write_json(tree, VS_MODEL, model)


def mutate_vs_readiness_gate_drift(tree: Path) -> None:
    model = _vs_model(tree)
    model["slices"][0]["readiness_gate_ids"] = ["JV-PILOT"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_unknown_technical_baseline_reference(tree: Path) -> None:
    model = _vs_model(tree)
    model["slices"][0]["technical_baseline_refs"] = ["TB-NOWHERE-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_non_deferred_in_deferred_refs(tree: Path) -> None:
    """TB-STATE-001 is PROMOTE_PROVISIONAL, not DEFERRED."""
    model = _vs_model(tree)
    model["slices"][0]["deferred_baseline_decision_refs"] = ["TB-STATE-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_stale_future_nodes_index(tree: Path) -> None:
    trace = read_json(tree, TRACE)
    trace["future_nodes"]["vertical_slices"] = []
    write_json(tree, TRACE, trace)


def mutate_vs_recommended_order_missing_slice(tree: Path) -> None:
    model = _vs_model(tree)
    model["recommended_delivery_order"] = ["VS-CATALOG-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_recommended_order_duplicate_slice(tree: Path) -> None:
    model = _vs_model(tree)
    model["recommended_delivery_order"] = ["VS-CATALOG-001", "VS-CATALOG-001", "VS-ORDER-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_recommended_order_dependency_violation(tree: Path) -> None:
    """Place the dependent slice before the slice it depends on."""
    model = _vs_model(tree)
    model["recommended_delivery_order"] = ["VS-ORDER-001", "VS-CATALOG-001"]
    write_json(tree, VS_MODEL, model)


def mutate_vs_unjustified_additional_dependency(tree: Path) -> None:
    """Strip VS-EXTRA-001's justification for its non-induced dependency.

    The dependency on VS-CATALOG-001 stays declared, but with no rationale/
    source backing left, so the validator must reject it even though it is a
    structurally valid slice-id reference with no cycle and no missing
    induced edge.
    """
    model = _vs_model(tree)
    for slice_ in model["slices"]:
        if slice_["id"] == "VS-EXTRA-001":
            slice_["dependency_rationale"] = {}
    write_json(tree, VS_MODEL, model)


def mutate_vs_dependency_rationale_for_undeclared_dependency(tree: Path) -> None:
    """Keep a rationale entry for a dependency VS-EXTRA-001 no longer declares."""
    model = _vs_model(tree)
    for slice_ in model["slices"]:
        if slice_["id"] == "VS-EXTRA-001":
            slice_["dependencies"] = []
    write_json(tree, VS_MODEL, model)


def mutate_vs_invalid_dependency_rationale_entry(tree: Path) -> None:
    """Keep the declared dependency but drop its source_refs, leaving it unjustified."""
    model = _vs_model(tree)
    for slice_ in model["slices"]:
        if slice_["id"] == "VS-EXTRA-001":
            slice_["dependency_rationale"]["VS-CATALOG-001"]["source_refs"] = []
    write_json(tree, VS_MODEL, model)


VS_CASES = [
    ("unknown story reference in a slice", mutate_vs_unknown_story_reference,
     "unknown_slice_story_references"),
    ("story assigned to more than one slice", mutate_vs_duplicate_story_assignment,
     "stories_assigned_to_multiple_slices"),
    ("accepted story not covered by any slice", mutate_vs_uncovered_story,
     "uncovered_accepted_stories"),
    ("slice actor_ids drift from member-story union", mutate_vs_actor_union_drift,
     "slice_actor_union_drift"),
    ("slice dependency on an unknown slice", mutate_vs_unknown_dependency,
     "unknown_slice_dependencies"),
    ("slice dependency cycle", mutate_vs_dependency_cycle, "slice_dependency_cycles"),
    ("missing induced cross-slice dependency", mutate_vs_missing_induced_dependency,
     "missing_induced_slice_dependencies"),
    ("slice readiness_gate_ids drift", mutate_vs_readiness_gate_drift,
     "slice_readiness_gate_union_drift"),
    ("unknown technical-baseline reference", mutate_vs_unknown_technical_baseline_reference,
     "unknown_slice_technical_baseline_references"),
    ("non-DEFERRED id in deferred_baseline_decision_refs", mutate_vs_non_deferred_in_deferred_refs,
     "non_deferred_ids_in_deferred_baseline_refs"),
    ("stale vertical-slice future-node index", mutate_vs_stale_future_nodes_index,
     "future_nodes.vertical_slices must exactly match"),
    ("recommended order missing a slice", mutate_vs_recommended_order_missing_slice,
     "recommended_order_missing_slices"),
    ("recommended order duplicating a slice", mutate_vs_recommended_order_duplicate_slice,
     "recommended_order_duplicate_slices"),
    ("recommended order violating a hard dependency", mutate_vs_recommended_order_dependency_violation,
     "recommended_order_dependency_violations"),
    ("unjustified additional slice dependency", mutate_vs_unjustified_additional_dependency,
     "unjustified_additional_slice_dependencies"),
    ("dependency_rationale for an undeclared dependency",
     mutate_vs_dependency_rationale_for_undeclared_dependency,
     "dependency_rationale_for_undeclared_dependency"),
    ("dependency_rationale entry missing source_refs", mutate_vs_invalid_dependency_rationale_entry,
     "invalid_dependency_rationale_entries"),
]


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
            print("ok   control: current real specification artifacts pass")

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

        populated_vs = base / "populated-vertical-slice"
        build_tree(populated_vs)
        populate_valid_vertical_slice_fixture(populated_vs)
        result = run(populated_vs)
        if result.returncode != 0:
            failures.append(
                "populated vertical slice: valid disposable two-slice, two-story "
                f"fixture must pass, got exit {result.returncode}\n{result.stderr}"
            )
        else:
            print("ok   populated vertical slice: valid disposable model passes")

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

        for index, (name, mutate, expected) in enumerate(VS_CASES):
            tree = base / f"vs{index:02d}"
            build_tree(tree)
            populate_valid_vertical_slice_fixture(tree)
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

    total_cases = len(CASES) + len(USE_CASE_CASES) + len(STORY_CASES) + len(VS_CASES)
    print()
    if failures:
        print(f"NEGATIVE TESTS FAILED: {len(failures)} of {total_cases + 4} cases", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"PASS: {total_cases} defect fixtures rejected, four control fixtures accepted")
    print("      no fixture state written to the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
