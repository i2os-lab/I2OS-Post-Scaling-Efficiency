"""
I2OS Recovery / Repair Path Layer v1.4

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal recovery / repair path layer for converting unsafe, excessive,
unclear, or inadmissible AI transitions into safer alternatives when possible.

Relationship:
v1.1 classifies transitions:
GO / HOLD / REPAIR / BLOCK

```
v1.2 evaluates decisions:
    EFFECTIVE / PARTIAL / NEUTRAL / FAILED

v1.3 audits trace records:
    VALID / QUESTIONABLE / INSUFFICIENT / INVALID

v1.4 proposes repair paths:
    REPAIRED / CONFIRMATION_REQUIRED / NO_REPAIR_AVAILABLE
```

Core Principle:
Capability is not permission.
Permission should be evaluated.
Evaluation should be traceable.
Unsafe transitions should be repairable when possible.
"""

from dataclasses import dataclass
from enum import Enum

class GateClassification(str, Enum):
GO = "GO"
HOLD = "HOLD"
REPAIR = "REPAIR"
BLOCK = "BLOCK"

class RiskLevel(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"

class ComputeWasteRisk(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"

class RepairType(str, Enum):
NONE = "none"
NARROW_SCOPE = "narrow_scope"
REQUIRE_CONFIRMATION = "require_confirmation"
STAGE_EXECUTION = "stage_execution"
ADD_RECOVERY = "add_recovery"
REDUCE_COMPUTE = "reduce_compute"
REQUEST_CONTEXT = "request_context"
CONVERT_TO_PREVIEW = "convert_to_preview"
BLOCK_NO_REPAIR = "block_no_repair"

class RepairStatus(str, Enum):
REPAIRED = "REPAIRED"
CONFIRMATION_REQUIRED = "CONFIRMATION_REQUIRED"
NO_REPAIR_AVAILABLE = "NO_REPAIR_AVAILABLE"

@dataclass
class RepairInput:
original_transition: str
original_classification: GateClassification
risk_level: RiskLevel
reversible: bool
human_confirmed: bool
scope_clear: bool
recoverable: bool
context_sufficient: bool
compute_waste_risk: ComputeWasteRisk
large_or_excessive: bool = False

@dataclass
class RepairResult:
repair_required: bool
repair_type: RepairType
repaired_transition: str
repair_reason: str
risk_reduced: bool
continuity_preserved: bool
human_confirmation_required: bool
final_repair_status: RepairStatus

def suggest_repair_path(data: RepairInput) -> RepairResult:
"""
Suggest a safer repair path for an inadmissible or risky transition.

```
The repair layer does not ask only:
    Should this transition be blocked?

It asks:
    Can this inadmissible transition be repaired into an admissible one?
"""

# No repair needed for clearly admissible GO transitions
if (
    data.original_classification == GateClassification.GO
    and data.risk_level == RiskLevel.LOW
    and data.scope_clear
    and data.context_sufficient
):
    return RepairResult(
        repair_required=False,
        repair_type=RepairType.NONE,
        repaired_transition=data.original_transition,
        repair_reason="No repair required for a low-risk admissible transition.",
        risk_reduced=False,
        continuity_preserved=True,
        human_confirmation_required=False,
        final_repair_status=RepairStatus.REPAIRED,
    )

# Critical destructive transition with no reversibility or recovery
if (
    data.risk_level == RiskLevel.CRITICAL
    and not data.reversible
    and not data.recoverable
):
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.BLOCK_NO_REPAIR,
        repaired_transition="No safe repair path available. Keep the transition blocked.",
        repair_reason="Critical irreversible transition without recovery path.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.NO_REPAIR_AVAILABLE,
    )

# Missing context: request context before proceeding
if not data.context_sufficient:
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.REQUEST_CONTEXT,
        repaired_transition=(
            "Request missing context, target, scope, and confirmation before proceeding."
        ),
        repair_reason="The transition lacks sufficient context for admissible execution.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Missing confirmation for non-trivial risk
if (
    data.original_classification == GateClassification.HOLD
    and data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    and not data.human_confirmed
):
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.REQUIRE_CONFIRMATION,
        repaired_transition=(
            "List the proposed transition, affected scope, and risk, then request explicit human confirmation."
        ),
        repair_reason="Human confirmation is required before the transition can proceed.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Unclear scope but recoverable: narrow the scope
if (
    data.original_classification == GateClassification.REPAIR
    and not data.scope_clear
    and data.recoverable
):
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.NARROW_SCOPE,
        repaired_transition=(
            "Narrow the transition to explicit targets and execute only after scope confirmation."
        ),
        repair_reason="The original transition is too broad or unclear.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Excessive or high compute-waste transition: stage execution
if data.large_or_excessive or data.compute_waste_risk == ComputeWasteRisk.HIGH:
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.STAGE_EXECUTION,
        repaired_transition=(
            "Convert the transition into a staged version: generate a small preview or outline first, "
            "then request confirmation before expansion."
        ),
        repair_reason="The original transition may produce unnecessary or inadmissible computation.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Risky but can be made reversible: add recovery path
if (
    data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    and not data.reversible
    and data.recoverable
):
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.ADD_RECOVERY,
        repaired_transition=(
            "Add a backup, rollback, or preview step before executing the transition."
        ),
        repair_reason="The transition is risky but can be made safer by adding a recovery path.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Risky execution: convert to preview
if (
    data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    and data.scope_clear
    and data.recoverable
):
    return RepairResult(
        repair_required=True,
        repair_type=RepairType.CONVERT_TO_PREVIEW,
        repaired_transition=(
            "Show a preview, diff, or proposed plan before applying the transition."
        ),
        repair_reason="Previewing the transition preserves intention while reducing execution risk.",
        risk_reduced=True,
        continuity_preserved=True,
        human_confirmation_required=True,
        final_repair_status=RepairStatus.CONFIRMATION_REQUIRED,
    )

# Default fallback: no safe repair path
return RepairResult(
    repair_required=True,
    repair_type=RepairType.BLOCK_NO_REPAIR,
    repaired_transition="No safe repair path available. Keep the transition blocked.",
    repair_reason="The transition is not clearly repairable under the current conditions.",
    risk_reduced=True,
    continuity_preserved=True,
    human_confirmation_required=True,
    final_repair_status=RepairStatus.NO_REPAIR_AVAILABLE,
)
```

if **name** == "**main**":
example = RepairInput(
original_transition="generate a full 100-page report without confirmed scope",
original_classification=GateClassification.REPAIR,
risk_level=RiskLevel.MEDIUM,
reversible=True,
human_confirmed=False,
scope_clear=False,
recoverable=True,
context_sufficient=True,
compute_waste_risk=ComputeWasteRisk.HIGH,
large_or_excessive=True,
)

```
result = suggest_repair_path(example)

print({
    "original_transition": example.original_transition,
    "repair_required": result.repair_required,
    "repair_type": result.repair_type.value,
    "repaired_transition": result.repaired_transition,
    "final_repair_status": result.final_repair_status.value,
    "reason": result.repair_reason,
})
```
