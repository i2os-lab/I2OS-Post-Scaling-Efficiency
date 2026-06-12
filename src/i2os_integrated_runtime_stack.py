"""
I2OS Integrated Runtime Governance Stack v2.0

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal integrated runtime governance stack that combines:

```
    v1.1 Runtime Classification
    v1.2 Runtime Evaluation
    v1.3 Trace / Audit
    v1.4 Recovery / Repair
    v1.5 Governance Report

into one continuous governance process.
```

Core Principle:
Capability is not permission.
Permission should be evaluated.
Evaluation should be traceable.
Unsafe transitions should be repairable when possible.
Runtime governance should be reportable.
Governance layers should be integrated.

Status:
v2.0 Minimal Integrated Prototype
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone

# ============================================================

# Shared Enums

# ============================================================

class RiskLevel(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"

class ComputeWasteRisk(str, Enum):
LOW = "low"
MEDIUM = "medium"
HIGH = "high"

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

class RepairStatus(str, Enum):
NOT_REQUIRED = "NOT_REQUIRED"
REPAIRED = "REPAIRED"
CONFIRMATION_REQUIRED = "CONFIRMATION_REQUIRED"
NO_REPAIR_AVAILABLE = "NO_REPAIR_AVAILABLE"

class ReportType(str, Enum):
SAFE_TO_PROCEED_REPORT = "SAFE_TO_PROCEED_REPORT"
CONFIRMATION_REQUIRED_REPORT = "CONFIRMATION_REQUIRED_REPORT"
REPAIR_APPLIED_REPORT = "REPAIR_APPLIED_REPORT"
BLOCKED_TRANSITION_REPORT = "BLOCKED_TRANSITION_REPORT"
AUDIT_REVIEW_REPORT = "AUDIT_REVIEW_REPORT"
FAILED_GOVERNANCE_REPORT = "FAILED_GOVERNANCE_REPORT"

class FinalOutcome(str, Enum):
ALLOW = "ALLOW"
HOLD_FOR_CONFIRMATION = "HOLD_FOR_CONFIRMATION"
ALLOW_AFTER_REPAIR = "ALLOW_AFTER_REPAIR"
BLOCK_NO_REPAIR = "BLOCK_NO_REPAIR"
REVIEW_AUDIT = "REVIEW_AUDIT"
FAILED_GOVERNANCE = "FAILED_GOVERNANCE"

# ============================================================

# Input / Output Data Structures

# ============================================================

@dataclass
class RuntimeTransition:
"""
A proposed AI transition before execution.

```
This object represents the transition-centered view of I2OS:
AI actions are not treated only as outputs,
but as movements from one state to another.
"""

transition: str
current_state: str
proposed_next_state: str

risk_level: RiskLevel
reversible: bool
recoverable: bool
context_sufficient: bool
human_confirmed: bool
scope_clear: bool
compute_waste_risk: ComputeWasteRisk
large_or_excessive: bool = False
```

@dataclass
class IntegratedGovernanceResult:
"""
Final integrated governance result.

```
This is the v2.0 output:
classification, evaluation, audit, repair, report,
and final outcome in one human-verifiable structure.
"""

trace_id: str
timestamp: str

transition: str
current_state: str
proposed_next_state: str

classification: GateClassification
classification_reason: str

evaluation: EvaluationOutcome
evaluation_reason: str

audit: AuditOutcome
audit_reason: str

repair_status: RepairStatus
repaired_transition: str
repair_reason: str

report_type: ReportType
final_outcome: FinalOutcome

human_action_required: bool
human_verifiable_summary: str
```

# ============================================================

# v1.1 Runtime Classification

# ============================================================

def classify_transition(data: RuntimeTransition) -> tuple[GateClassification, str]:
"""
v1.1 Minimal Runtime Efficiency Gate

```
Core question:
    Should this transition be allowed?
"""

if (
    data.risk_level == RiskLevel.CRITICAL
    and not data.reversible
    and not data.recoverable
):
    return (
        GateClassification.BLOCK,
        "Critical irreversible transition without recovery path.",
    )

if not data.context_sufficient:
    return (
        GateClassification.HOLD,
        "Context is insufficient. Additional information is required.",
    )

if not data.human_confirmed and data.risk_level in {
    RiskLevel.MEDIUM,
    RiskLevel.HIGH,
    RiskLevel.CRITICAL,
}:
    return (
        GateClassification.HOLD,
        "Human confirmation is required before proceeding.",
    )

if not data.scope_clear:
    return (
        GateClassification.REPAIR,
        "Scope is unclear and should be narrowed before execution.",
    )

if data.large_or_excessive or data.compute_waste_risk == ComputeWasteRisk.HIGH:
    return (
        GateClassification.REPAIR,
        "Transition is excessive or has high compute waste risk.",
    )

if data.risk_level == RiskLevel.LOW and data.reversible and data.recoverable:
    return (
        GateClassification.GO,
        "Low-risk, reversible, recoverable, and sufficiently scoped transition.",
    )

return (
    GateClassification.HOLD,
    "Transition requires additional governance review.",
)
```

# ============================================================

# v1.2 Runtime Evaluation

# ============================================================

def evaluate_decision(
data: RuntimeTransition,
classification: GateClassification,
) -> tuple[EvaluationOutcome, str]:
"""
v1.2 Runtime Evaluation Layer

```
Core question:
    Did the gate decision reduce inadmissible computation
    while preserving admissible continuity?
"""

if classification == GateClassification.BLOCK:
    if data.risk_level == RiskLevel.CRITICAL and not data.recoverable:
        return (
            EvaluationOutcome.EFFECTIVE,
            "BLOCK prevented unsafe execution and reduced inadmissible computation.",
        )
    return (
        EvaluationOutcome.PARTIAL,
        "BLOCK may have reduced risk, but the necessity of blocking requires review.",
    )

if classification == GateClassification.HOLD:
    return (
        EvaluationOutcome.EFFECTIVE,
        "HOLD preserved continuity by requiring confirmation or additional context.",
    )

if classification == GateClassification.REPAIR:
    return (
        EvaluationOutcome.EFFECTIVE,
        "REPAIR reduced unsafe or excessive execution while preserving useful intention.",
    )

if classification == GateClassification.GO:
    if data.risk_level == RiskLevel.LOW and data.context_sufficient:
        return (
            EvaluationOutcome.EFFECTIVE,
            "GO allowed a low-risk admissible transition without unnecessary obstruction.",
        )
    return (
        EvaluationOutcome.FAILED,
        "GO was not sufficiently supported by risk and context conditions.",
    )

return (
    EvaluationOutcome.NEUTRAL,
    "No significant effect was detected.",
)
```

# ============================================================

# v1.3 Trace / Audit

# ============================================================

def audit_trace(
data: RuntimeTransition,
classification: GateClassification,
evaluation: EvaluationOutcome,
classification_reason: str,
evaluation_reason: str,
) -> tuple[AuditOutcome, str]:
"""
v1.3 Runtime Trace / Audit Layer

```
Core question:
    Can that decision be traced and audited later?
"""

if not data.transition or not classification_reason or not evaluation_reason:
    return (
        AuditOutcome.INSUFFICIENT,
        "Trace lacks required transition or reasoning fields.",
    )

if classification == GateClassification.GO and evaluation == EvaluationOutcome.FAILED:
    return (
        AuditOutcome.INVALID,
        "GO classification conflicts with failed evaluation.",
    )

if classification == GateClassification.BLOCK and data.risk_level == RiskLevel.LOW:
    return (
        AuditOutcome.QUESTIONABLE,
        "Low-risk transition was blocked and should be reviewed.",
    )

return (
    AuditOutcome.VALID,
    "Trace supports the classification and evaluation decision.",
)
```

# ============================================================

# v1.4 Recovery / Repair Path

# ============================================================

def suggest_repair(
data: RuntimeTransition,
classification: GateClassification,
) -> tuple[RepairStatus, str, str]:
"""
v1.4 Recovery / Repair Path Layer

```
Core question:
    Can an inadmissible transition be repaired
    into an admissible one?
"""

if classification == GateClassification.GO:
    return (
        RepairStatus.NOT_REQUIRED,
        data.transition,
        "No repair required.",
    )

if classification == GateClassification.BLOCK:
    if data.risk_level == RiskLevel.CRITICAL and not data.recoverable:
        return (
            RepairStatus.NO_REPAIR_AVAILABLE,
            "No safe repair path available. Keep the transition blocked.",
            "Critical irreversible transition with no recovery path.",
        )

    return (
        RepairStatus.CONFIRMATION_REQUIRED,
        "Request human confirmation and define recovery path before proceeding.",
        "BLOCK may be repairable only after human confirmation and recovery design.",
    )

if classification == GateClassification.HOLD:
    return (
        RepairStatus.CONFIRMATION_REQUIRED,
        "Request missing context or explicit human confirmation before execution.",
        "The transition requires human confirmation or additional context.",
    )

if classification == GateClassification.REPAIR:
    if not data.scope_clear:
        return (
            RepairStatus.REPAIRED,
            "Narrow the transition scope and generate a preview before execution.",
            "Unclear scope was repaired into a staged and reviewable transition.",
        )

    if data.large_or_excessive or data.compute_waste_risk == ComputeWasteRisk.HIGH:
        return (
            RepairStatus.REPAIRED,
            "Generate a minimal outline or preview first, then request confirmation before expansion.",
            "Excessive computation was repaired into a staged transition.",
        )

    return (
        RepairStatus.REPAIRED,
        "Convert the transition into a safer preview-first action.",
        "The transition was repaired into a safer admissible path.",
    )

return (
    RepairStatus.CONFIRMATION_REQUIRED,
    "Request human review before proceeding.",
    "Fallback repair path requires confirmation.",
)
```

# ============================================================

# v1.5 Governance Report

# ============================================================

def generate_report(
classification: GateClassification,
evaluation: EvaluationOutcome,
audit: AuditOutcome,
repair_status: RepairStatus,
) -> tuple[ReportType, FinalOutcome, bool, str]:
"""
v1.5 Runtime Governance Report Layer

```
Core question:
    Can the entire governance process be summarized
    in a human-verifiable report?
"""

if evaluation == EvaluationOutcome.FAILED or audit == AuditOutcome.INVALID:
    return (
        ReportType.FAILED_GOVERNANCE_REPORT,
        FinalOutcome.FAILED_GOVERNANCE,
        True,
        "Governance failed or requires urgent review.",
    )

if audit in {AuditOutcome.QUESTIONABLE, AuditOutcome.INSUFFICIENT}:
    return (
        ReportType.AUDIT_REVIEW_REPORT,
        FinalOutcome.REVIEW_AUDIT,
        True,
        "The governance trace requires human audit review.",
    )

if classification == GateClassification.BLOCK and repair_status == RepairStatus.NO_REPAIR_AVAILABLE:
    return (
        ReportType.BLOCKED_TRANSITION_REPORT,
        FinalOutcome.BLOCK_NO_REPAIR,
        True,
        "The transition was blocked and no safe repair path is available.",
    )

if classification == GateClassification.REPAIR and repair_status == RepairStatus.REPAIRED:
    return (
        ReportType.REPAIR_APPLIED_REPORT,
        FinalOutcome.ALLOW_AFTER_REPAIR,
        False,
        "The transition was repaired into a safer admissible path.",
    )

if classification == GateClassification.HOLD or repair_status == RepairStatus.CONFIRMATION_REQUIRED:
    return (
        ReportType.CONFIRMATION_REQUIRED_REPORT,
        FinalOutcome.HOLD_FOR_CONFIRMATION,
        True,
        "Human confirmation or additional context is required.",
    )

if classification == GateClassification.GO and audit == AuditOutcome.VALID:
    return (
        ReportType.SAFE_TO_PROCEED_REPORT,
        FinalOutcome.ALLOW,
        False,
        "The transition is safe to proceed.",
    )

return (
    ReportType.AUDIT_REVIEW_REPORT,
    FinalOutcome.REVIEW_AUDIT,
    True,
    "Mixed governance result requires review.",
)
```

# ============================================================

# v2.0 Integrated Runtime Stack

# ============================================================

def run_integrated_runtime_governance(
data: RuntimeTransition,
trace_id: str = "trace-0001",
) -> IntegratedGovernanceResult:
"""
v2.0 Integrated Runtime Governance Stack

```
Integrated question:
    Can classification, evaluation, audit, repair, and reporting
    be integrated into one runtime governance stack?
"""

timestamp = datetime.now(timezone.utc).isoformat()

classification, classification_reason = classify_transition(data)

evaluation, evaluation_reason = evaluate_decision(data, classification)

audit, audit_reason = audit_trace(
    data=data,
    classification=classification,
    evaluation=evaluation,
    classification_reason=classification_reason,
    evaluation_reason=evaluation_reason,
)

repair_status, repaired_transition, repair_reason = suggest_repair(
    data=data,
    classification=classification,
)

report_type, final_outcome, human_action_required, summary = generate_report(
    classification=classification,
    evaluation=evaluation,
    audit=audit,
    repair_status=repair_status,
)

human_verifiable_summary = (
    f"Transition: {data.transition} | "
    f"Classification: {classification.value} | "
    f"Evaluation: {evaluation.value} | "
    f"Audit: {audit.value} | "
    f"Repair: {repair_status.value} | "
    f"Report: {report_type.value} | "
    f"Final Outcome: {final_outcome.value}. "
    f"{summary}"
)

return IntegratedGovernanceResult(
    trace_id=trace_id,
    timestamp=timestamp,
    transition=data.transition,
    current_state=data.current_state,
    proposed_next_state=data.proposed_next_state,
    classification=classification,
    classification_reason=classification_reason,
    evaluation=evaluation,
    evaluation_reason=evaluation_reason,
    audit=audit,
    audit_reason=audit_reason,
    repair_status=repair_status,
    repaired_transition=repaired_transition,
    repair_reason=repair_reason,
    report_type=report_type,
    final_outcome=final_outcome,
    human_action_required=human_action_required,
    human_verifiable_summary=human_verifiable_summary,
)
```

if **name** == "**main**":
example = RuntimeTransition(
transition="delete all project files without confirmation or recovery",
current_state="project files exist",
proposed_next_state="all project files deleted",
risk_level=RiskLevel.CRITICAL,
reversible=False,
recoverable=False,
context_sufficient=True,
human_confirmed=False,
scope_clear=True,
compute_waste_risk=ComputeWasteRisk.HIGH,
)

```
result = run_integrated_runtime_governance(
    data=example,
    trace_id="trace-v2-0001",
)

print({
    "trace_id": result.trace_id,
    "timestamp": result.timestamp,
    "transition": result.transition,
    "classification": result.classification.value,
    "classification_reason": result.classification_reason,
    "evaluation": result.evaluation.value,
    "evaluation_reason": result.evaluation_reason,
    "audit": result.audit.value,
    "audit_reason": result.audit_reason,
    "repair_status": result.repair_status.value,
    "repaired_transition": result.repaired_transition,
    "repair_reason": result.repair_reason,
    "report_type": result.report_type.value,
    "final_outcome": result.final_outcome.value,
    "human_action_required": result.human_action_required,
    "human_verifiable_summary": result.human_verifiable_summary,
})
```
