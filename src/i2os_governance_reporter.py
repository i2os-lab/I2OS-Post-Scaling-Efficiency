"""
I2OS Runtime Governance Report Layer v1.5

Project:
I2OS / Infinity Intelligence Operating System

Purpose:
A minimal governance report layer for summarizing runtime classification,
evaluation, trace/audit, and repair results into a human-verifiable report.

Relationship:
v1.1 classifies transitions:
GO / HOLD / REPAIR / BLOCK

```
v1.2 evaluates decisions:
    EFFECTIVE / PARTIAL / NEUTRAL / FAILED

v1.3 audits traces:
    VALID / QUESTIONABLE / INSUFFICIENT / INVALID

v1.4 proposes repair paths:
    REPAIRED / CONFIRMATION_REQUIRED / NO_REPAIR_AVAILABLE

v1.5 generates governance reports:
    SAFE_TO_PROCEED_REPORT
    CONFIRMATION_REQUIRED_REPORT
    REPAIR_APPLIED_REPORT
    BLOCKED_TRANSITION_REPORT
    AUDIT_REVIEW_REPORT
    FAILED_GOVERNANCE_REPORT
```

Core Principle:
Capability is not permission.
Permission should be evaluated.
Evaluation should be traceable.
Unsafe transitions should be repairable when possible.
Runtime governance should be reportable.
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
PENDING_CONFIRMATION = "pending_confirmation"

class ReportType(str, Enum):
SAFE_TO_PROCEED_REPORT = "SAFE_TO_PROCEED_REPORT"
CONFIRMATION_REQUIRED_REPORT = "CONFIRMATION_REQUIRED_REPORT"
REPAIR_APPLIED_REPORT = "REPAIR_APPLIED_REPORT"
BLOCKED_TRANSITION_REPORT = "BLOCKED_TRANSITION_REPORT"
AUDIT_REVIEW_REPORT = "AUDIT_REVIEW_REPORT"
FAILED_GOVERNANCE_REPORT = "FAILED_GOVERNANCE_REPORT"

@dataclass
class GovernanceReportInput:
report_id: str
transition: str
classification: GateClassification
classification_reason: str
evaluation: EvaluationOutcome
evaluation_reason: str
audit: AuditOutcome
audit_reason: str
repair_status: RepairStatus
repaired_transition: str
risk_level: RiskLevel
continuity_preserved: bool
compute_waste_reduced: bool
human_action_required: bool
final_status: FinalStatus

@dataclass
class GovernanceReport:
report_id: str
report_type: ReportType
transition: str
classification: GateClassification
evaluation: EvaluationOutcome
audit: AuditOutcome
repair_status: RepairStatus
final_status: FinalStatus
human_action_required: bool
summary: str

def generate_governance_report(data: GovernanceReportInput) -> GovernanceReport:
"""
Generate a human-verifiable governance report.

```
The report layer does not ask only:
    What was the final status?

It asks:
    Can the entire governance process be summarized
    in a form humans can inspect, verify, and act on?
"""

# FAILED: governance failed if continuity was not preserved,
# evaluation failed, or audit was invalid.
if (
    not data.continuity_preserved
    or data.evaluation == EvaluationOutcome.FAILED
    or data.audit == AuditOutcome.INVALID
):
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.FAILED_GOVERNANCE_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=data.final_status,
        human_action_required=True,
        summary=(
            "Governance failed or requires urgent review because admissible "
            "continuity was not preserved, evaluation failed, or the audit was invalid."
        ),
    )

# AUDIT REVIEW: audit is incomplete or questionable.
if data.audit in {AuditOutcome.QUESTIONABLE, AuditOutcome.INSUFFICIENT}:
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.AUDIT_REVIEW_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=data.final_status,
        human_action_required=True,
        summary=(
            "The governance trace requires human review because the audit is "
            "questionable or insufficient."
        ),
    )

# BLOCKED: no safe repair path is available.
if (
    data.classification == GateClassification.BLOCK
    and data.repair_status == RepairStatus.NO_REPAIR_AVAILABLE
):
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.BLOCKED_TRANSITION_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=FinalStatus.BLOCKED,
        human_action_required=True,
        summary=(
            "The transition was blocked because it was not admissible and no "
            "safe repair path was available."
        ),
    )

# REPAIR APPLIED: unsafe or excessive transition was repaired.
if (
    data.classification == GateClassification.REPAIR
    and data.repair_status == RepairStatus.REPAIRED
):
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.REPAIR_APPLIED_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=FinalStatus.REPAIRED,
        human_action_required=data.human_action_required,
        summary=(
            "The original transition was repaired into a safer admissible path. "
            f"Repaired transition: {data.repaired_transition}"
        ),
    )

# CONFIRMATION REQUIRED: human action is required before proceeding.
if (
    data.classification == GateClassification.HOLD
    or data.repair_status == RepairStatus.CONFIRMATION_REQUIRED
    or data.human_action_required
):
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.CONFIRMATION_REQUIRED_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=FinalStatus.PENDING_CONFIRMATION,
        human_action_required=True,
        summary=(
            "The transition may be admissible, but human confirmation or review "
            "is required before proceeding."
        ),
    )

# SAFE TO PROCEED: low-risk, valid, effective, and continuity-preserving.
if (
    data.classification == GateClassification.GO
    and data.evaluation == EvaluationOutcome.EFFECTIVE
    and data.audit == AuditOutcome.VALID
    and data.continuity_preserved
    and data.final_status == FinalStatus.ALLOWED
):
    return GovernanceReport(
        report_id=data.report_id,
        report_type=ReportType.SAFE_TO_PROCEED_REPORT,
        transition=data.transition,
        classification=data.classification,
        evaluation=data.evaluation,
        audit=data.audit,
        repair_status=data.repair_status,
        final_status=data.final_status,
        human_action_required=False,
        summary=(
            "The transition is safe to proceed. It was classified as GO, "
            "evaluated as effective, audited as valid, and continuity was preserved."
        ),
    )

# Default fallback: require review.
return GovernanceReport(
    report_id=data.report_id,
    report_type=ReportType.AUDIT_REVIEW_REPORT,
    transition=data.transition,
    classification=data.classification,
    evaluation=data.evaluation,
    audit=data.audit,
    repair_status=data.repair_status,
    final_status=data.final_status,
    human_action_required=True,
    summary=(
        "The governance process produced a mixed result and should be reviewed "
        "before further execution."
    ),
)
```

if **name** == "**main**":
example = GovernanceReportInput(
report_id="report-0001",
transition="delete all project files without confirmation or recovery",
classification=GateClassification.BLOCK,
classification_reason="Critical irreversible transition without recovery path.",
evaluation=EvaluationOutcome.EFFECTIVE,
evaluation_reason="BLOCK prevented unsafe execution and reduced inadmissible computation.",
audit=AuditOutcome.VALID,
audit_reason="Trace supports a valid BLOCK decision with effective risk prevention.",
repair_status=RepairStatus.NO_REPAIR_AVAILABLE,
repaired_transition="No safe repair path available. Keep the transition blocked.",
risk_level=RiskLevel.CRITICAL,
continuity_preserved=True,
compute_waste_reduced=True,
human_action_required=True,
final_status=FinalStatus.BLOCKED,
)

```
report = generate_governance_report(example)

print({
    "report_id": report.report_id,
    "report_type": report.report_type.value,
    "transition": report.transition,
    "classification": report.classification.value,
    "evaluation": report.evaluation.value,
    "audit": report.audit.value,
    "repair_status": report.repair_status.value,
    "final_status": report.final_status.value,
    "human_action_required": report.human_action_required,
    "summary": report.summary,
})
```
