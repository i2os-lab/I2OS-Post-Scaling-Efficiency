"""
I2OS Runtime Trace / Audit Layer v1.3

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal trace and audit layer for recording and auditing runtime
governance decisions after classification and evaluation.

Relationship:
v1.1 classifies transitions:
GO / HOLD / REPAIR / BLOCK

```
v1.2 evaluates decisions:
    EFFECTIVE / PARTIAL / NEUTRAL / FAILED

v1.3 audits trace records:
    VALID / QUESTIONABLE / INSUFFICIENT / INVALID
```

Core Principle:
Capability is not permission.
Permission should be evaluated.
Evaluation should be traceable.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

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

class AuditOutcome(str, Enum):
VALID = "VALID"
QUESTIONABLE = "QUESTIONABLE"
INSUFFICIENT = "INSUFFICIENT"
INVALID = "INVALID"

class RiskLevel(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"

class FinalStatus(str, Enum):
ALLOWED = "allowed"
HELD = "held"
REPAIRED = "repaired"
BLOCKED = "blocked"

@dataclass
class TraceRecord:
trace_id: str
timestamp: str
transition: str
classification: GateClassification
classification_reason: str
evaluation: EvaluationOutcome
evaluation_reason: str
risk_level: RiskLevel
human_confirmation_required: bool
recovery_path_available: bool
continuity_preserved: bool
compute_waste_reduced: bool
final_status: Optional[FinalStatus]
audit_note: str = ""

@dataclass
class AuditResult:
audit: AuditOutcome
reason: str

def audit_trace(record: TraceRecord) -> AuditResult:
"""
Audit a runtime governance trace record.

```
The auditor does not ask only:
    What was decided?

It asks:
    Is the decision trace complete, coherent, and human-verifiable?
"""

# INSUFFICIENT: required explanation or final status is missing
if (
    not record.classification_reason.strip()
    or not record.evaluation_reason.strip()
    or record.final_status is None
):
    return AuditResult(
        audit=AuditOutcome.INSUFFICIENT,
        reason="Trace is incomplete: missing reason or final status."
    )

# INVALID: continuity failed but evaluation claims success
if (
    not record.continuity_preserved
    and record.evaluation == EvaluationOutcome.EFFECTIVE
):
    return AuditResult(
        audit=AuditOutcome.INVALID,
        reason="Trace contradiction: evaluation is EFFECTIVE but continuity was not preserved."
    )

# INVALID: GO with failed continuity
if (
    record.classification == GateClassification.GO
    and not record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.INVALID,
        reason="GO classification is invalid because admissible continuity was not preserved."
    )

# INVALID: low-risk transition blocked and marked effective
if (
    record.classification == GateClassification.BLOCK
    and record.risk_level == RiskLevel.LOW
    and record.final_status == FinalStatus.BLOCKED
    and record.evaluation == EvaluationOutcome.EFFECTIVE
):
    return AuditResult(
        audit=AuditOutcome.INVALID,
        reason="Low-risk blocked transition cannot be marked EFFECTIVE without stronger justification."
    )

# VALID: critical blocked transition with effective evaluation
if (
    record.classification == GateClassification.BLOCK
    and record.evaluation == EvaluationOutcome.EFFECTIVE
    and record.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}
    and record.final_status == FinalStatus.BLOCKED
    and record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.VALID,
        reason="Trace supports a valid BLOCK decision with effective risk prevention."
    )

# VALID: low-risk GO allowed safely
if (
    record.classification == GateClassification.GO
    and record.risk_level == RiskLevel.LOW
    and record.final_status == FinalStatus.ALLOWED
    and record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.VALID,
        reason="Trace supports a valid GO decision for a low-risk transition."
    )

# VALID: REPAIR with preserved continuity and recovery path
if (
    record.classification == GateClassification.REPAIR
    and record.final_status == FinalStatus.REPAIRED
    and record.recovery_path_available
    and record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.VALID,
        reason="Trace supports a valid REPAIR decision with recovery path."
    )

# QUESTIONABLE: partial evaluation but continuity preserved
if (
    record.evaluation == EvaluationOutcome.PARTIAL
    and record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.QUESTIONABLE,
        reason="Trace is coherent but requires review because evaluation is PARTIAL."
    )

# QUESTIONABLE: HOLD requires confirmation but final status unclear in effect
if (
    record.classification == GateClassification.HOLD
    and record.human_confirmation_required
    and record.continuity_preserved
):
    return AuditResult(
        audit=AuditOutcome.QUESTIONABLE,
        reason="Trace is plausible but requires review of confirmation handling."
    )

# Default fallback
return AuditResult(
    audit=AuditOutcome.QUESTIONABLE,
    reason="Trace is not invalid, but its governance effect requires review."
)
```

if **name** == "**main**":
example = TraceRecord(
trace_id="trace-0001",
timestamp="2026-06-10T00:00:00Z",
transition="delete all project files",
classification=GateClassification.BLOCK,
classification_reason="Critical irreversible transition without recovery path.",
evaluation=EvaluationOutcome.EFFECTIVE,
evaluation_reason="BLOCK prevented unsafe execution and reduced inadmissible computation.",
risk_level=RiskLevel.CRITICAL,
human_confirmation_required=True,
recovery_path_available=False,
continuity_preserved=True,
compute_waste_reduced=True,
final_status=FinalStatus.BLOCKED,
audit_note="The transition was correctly blocked before execution."
)

```
result = audit_trace(example)

print({
    "trace_id": example.trace_id,
    "transition": example.transition,
    "classification": example.classification.value,
    "evaluation": example.evaluation.value,
    "audit": result.audit.value,
    "reason": result.reason,
})
```
