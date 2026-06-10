"""
I2OS Runtime Evaluation Layer v1.2

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal runtime evaluation layer for assessing whether a gate decision
reduced inadmissible computation while preserving admissible continuity.

Relationship:
v1.1 Minimal Runtime Efficiency Gate classifies transitions as:
GO / HOLD / REPAIR / BLOCK

```
v1.2 Runtime Evaluation Layer evaluates gate decisions as:
    EFFECTIVE / PARTIAL / NEUTRAL / FAILED
```

Core Principle:
Capability is not permission.
Permission should be evaluated.

Core Question:
Did this classification reduce inadmissible computation
while preserving admissible continuity?
"""

from dataclasses import dataclass
from enum import Enum

class GateClassification(str, Enum):
GO = "GO"
HOLD = "HOLD"
REPAIR = "REPAIR"
BLOCK = "BLOCK"

class EvaluationOutcome(str, Enum):
EFFECTIVE = "EFFECTIVE"
PARTIAL = "PARTIAL"
NEUTRAL = "NEUTRAL"
FAILED = "FAILED"

class RiskLevel(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"

@dataclass
class EvaluationInput:
transition: str
classification: GateClassification
risk_level: RiskLevel
human_confirmation_required: bool
recovery_path_available: bool
compute_waste_reduced: bool
unsafe_execution_prevented: bool
regeneration_avoided: bool
post_hoc_repair_avoided: bool
continuity_preserved: bool

@dataclass
class EvaluationResult:
evaluation: EvaluationOutcome
reason: str

def evaluate_gate_decision(data: EvaluationInput) -> EvaluationResult:
"""
Evaluate whether a runtime gate decision improved safety, efficiency,
and continuity.

```
The evaluator does not ask only:
    What was the classification?

It asks:
    Did that classification reduce inadmissible computation
    while preserving admissible continuity?
"""

# FAILED: continuity was not preserved
if not data.continuity_preserved:
    return EvaluationResult(
        evaluation=EvaluationOutcome.FAILED,
        reason="Admissible continuity was not preserved."
    )

# EFFECTIVE: BLOCK prevented unsafe execution
if (
    data.classification == GateClassification.BLOCK
    and data.unsafe_execution_prevented
    and data.compute_waste_reduced
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.EFFECTIVE,
        reason="BLOCK prevented unsafe execution and reduced inadmissible computation."
    )

# EFFECTIVE: REPAIR reduced waste while preserving continuity
if (
    data.classification == GateClassification.REPAIR
    and data.compute_waste_reduced
    and data.recovery_path_available
    and data.continuity_preserved
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.EFFECTIVE,
        reason="REPAIR reduced inadmissible computation while preserving a recovery path."
    )

# EFFECTIVE: HOLD correctly required confirmation
if (
    data.classification == GateClassification.HOLD
    and data.human_confirmation_required
    and data.continuity_preserved
    and data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL}
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.EFFECTIVE,
        reason="HOLD preserved continuity by requiring confirmation for a non-trivial transition."
    )

# EFFECTIVE: GO allowed a safe low-risk transition
if (
    data.classification == GateClassification.GO
    and data.risk_level == RiskLevel.LOW
    and data.continuity_preserved
    and not data.unsafe_execution_prevented
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.EFFECTIVE,
        reason="GO allowed a low-risk transition without unnecessary obstruction."
    )

# PARTIAL: classification helped but did not clearly reduce computation
if (
    data.continuity_preserved
    and not data.compute_waste_reduced
    and data.classification in {
        GateClassification.HOLD,
        GateClassification.REPAIR,
        GateClassification.BLOCK,
    }
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.PARTIAL,
        reason="The classification preserved continuity but did not clearly reduce computation."
    )

# PARTIAL: waste reduced, but repair or confirmation still needed
if (
    data.compute_waste_reduced
    and data.continuity_preserved
    and not data.recovery_path_available
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.PARTIAL,
        reason="Computation was reduced, but the recovery path remains incomplete."
    )

# NEUTRAL: harmless GO with little measurable effect
if (
    data.classification == GateClassification.GO
    and data.risk_level == RiskLevel.LOW
    and not data.compute_waste_reduced
    and data.continuity_preserved
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.NEUTRAL,
        reason="The decision was safe but had no significant measurable efficiency effect."
    )

# FAILED: BLOCK stopped a clearly safe and low-risk transition
if (
    data.classification == GateClassification.BLOCK
    and data.risk_level == RiskLevel.LOW
):
    return EvaluationResult(
        evaluation=EvaluationOutcome.FAILED,
        reason="BLOCK stopped a low-risk transition without sufficient justification."
    )

# Default fallback
return EvaluationResult(
    evaluation=EvaluationOutcome.PARTIAL,
    reason="The decision had mixed or insufficiently measurable effects."
)
```

if **name** == "**main**":
example = EvaluationInput(
transition="delete all project files",
classification=GateClassification.BLOCK,
risk_level=RiskLevel.CRITICAL,
human_confirmation_required=True,
recovery_path_available=False,
compute_waste_reduced=True,
unsafe_execution_prevented=True,
regeneration_avoided=True,
post_hoc_repair_avoided=True,
continuity_preserved=True,
)

```
result = evaluate_gate_decision(example)

print({
    "transition": example.transition,
    "classification": example.classification.value,
    "evaluation": result.evaluation.value,
    "reason": result.reason,
})
```
