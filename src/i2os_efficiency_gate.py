"""
I2OS Minimal Runtime Efficiency Gate v1.1

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal rule-based runtime gate for classifying proposed AI transitions
before generation, execution, or tool use.

Core Principle:
Capability is not permission.

Core Equation:
Permit(T)=1[C(S_t,T,S_{t+1})=1]

Output Classes:
GO / HOLD / REPAIR / BLOCK
"""

from dataclasses import dataclass
from enum import Enum

class Classification(str, Enum):
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

@dataclass
class TransitionInput:
transition: str
risk_level: RiskLevel
reversible: bool
human_confirmed: bool
scope_clear: bool
recoverable: bool
context_sufficient: bool
compute_waste_risk: ComputeWasteRisk

@dataclass
class GateResult:
classification: Classification
reason: str

def classify_transition(data: TransitionInput) -> GateResult:
"""
Classify a proposed AI transition before execution.

```
The gate does not ask:
    Can the AI do this?

It asks:
    Should this transition be allowed?
"""

# BLOCK: critical, irreversible, unrecoverable transitions
if (
    data.risk_level == RiskLevel.CRITICAL
    and not data.reversible
    and not data.recoverable
):
    return GateResult(
        classification=Classification.BLOCK,
        reason="Critical irreversible transition without recovery path."
    )

# BLOCK: high or critical risk without confirmation and not reversible
if (
    data.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}
    and not data.human_confirmed
    and not data.reversible
):
    return GateResult(
        classification=Classification.BLOCK,
        reason="High-risk irreversible transition without human confirmation."
    )

# BLOCK: unclear scope with no recovery path
if not data.scope_clear and not data.recoverable:
    return GateResult(
        classification=Classification.BLOCK,
        reason="Unclear scope and no recovery path."
    )

# HOLD: insufficient context
if not data.context_sufficient:
    return GateResult(
        classification=Classification.HOLD,
        reason="Insufficient context. More information is required before proceeding."
    )

# HOLD: medium or high risk without human confirmation
if (
    data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    and not data.human_confirmed
):
    return GateResult(
        classification=Classification.HOLD,
        reason="Human confirmation is required before proceeding."
    )

# REPAIR: recoverable but unclear scope
if (
    data.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    and data.recoverable
    and not data.scope_clear
):
    return GateResult(
        classification=Classification.REPAIR,
        reason="The transition is recoverable but too unclear. Narrow the scope before execution."
    )

# REPAIR: high compute waste risk
if data.compute_waste_risk == ComputeWasteRisk.HIGH:
    return GateResult(
        classification=Classification.REPAIR,
        reason="High risk of inadmissible computation. The transition should be narrowed or staged."
    )

# GO: low-risk, reversible, clear, recoverable, and contextually sufficient
if (
    data.risk_level == RiskLevel.LOW
    and data.reversible
    and data.scope_clear
    and data.recoverable
    and data.context_sufficient
):
    return GateResult(
        classification=Classification.GO,
        reason="Low-risk, reversible, scoped, recoverable, and contextually sufficient transition."
    )

# GO: medium-risk but confirmed and safely bounded
if (
    data.risk_level == RiskLevel.MEDIUM
    and data.human_confirmed
    and data.scope_clear
    and data.recoverable
):
    return GateResult(
        classification=Classification.GO,
        reason="Medium-risk transition with human confirmation, clear scope, and recovery path."
    )

# Default fallback: HOLD
return GateResult(
    classification=Classification.HOLD,
    reason="The transition is not clearly admissible. Hold for review."
)
```

if **name** == "**main**":
example = TransitionInput(
transition="delete all project files",
risk_level=RiskLevel.CRITICAL,
reversible=False,
human_confirmed=False,
scope_clear=False,
recoverable=False,
context_sufficient=True,
compute_waste_risk=ComputeWasteRisk.HIGH,
)

```
result = classify_transition(example)

print({
    "transition": example.transition,
    "classification": result.classification.value,
    "reason": result.reason,
})
```
