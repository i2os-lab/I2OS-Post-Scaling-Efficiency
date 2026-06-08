# I2OS Runtime Gate

## Core Equation

```text
Permit(T)=1[C(S_t,T,S_{t+1})=1]
```

Where:

```text
S_t        = current state
T          = proposed transition
S_{t+1}    = expected next state
C          = admissibility constraint
Permit(T)  = permission function
```

A transition is permitted only if the transition from the current state to the next state satisfies the admissibility constraint.

---

## Admissibility Constraint

```text
C =
C_context
∧ C_safety
∧ C_recovery
∧ C_sync
∧ C_future
∧ C_verify
∧ C_efficiency
```

Where:

```text
C_context     = contextual validity
C_safety      = safety compatibility
C_recovery    = recoverability
C_sync        = synchronization with user/task/system state
C_future      = future compatibility
C_verify      = human-verifiability
C_efficiency  = computation-waste risk acceptability
```

---

## Runtime Classification

| Classification | Meaning | Efficiency Role |
|---|---|---|
| GO | Transition is admissible | Computation contributes to continuity |
| HOLD | More context is needed | Prevents premature waste |
| REPAIR | Transition can be reframed | Reduces regeneration and recovery cost |
| BLOCK | Transition is inadmissible | Prevents high-cost collapse trajectory |

---

## Flow

```text
AI Model
↓
Proposed Transition
↓
State Extraction
↓
Admissibility Check
↓
Efficiency Risk Check
↓
GO / HOLD / REPAIR / BLOCK
↓
Execution or Reframe
```

---

## Core Principle

```text
Capability is not permission.
```
