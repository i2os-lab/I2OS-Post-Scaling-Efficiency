# Figure 3: I2OS Runtime Gate Model

```mermaid
flowchart TD
    A[AI Model] --> B[Proposed Transition T]

    B --> C[State Extraction]
    C --> D[Current State S_t]
    C --> E[Expected Next State S_t+1]

    D --> F[Admissibility Constraint C]
    E --> F
    B --> F

    F --> G[C_context]
    F --> H[C_safety]
    F --> I[C_recovery]
    F --> J[C_sync]
    F --> K[C_future]
    F --> L[C_verify]
    F --> M[C_efficiency]

    G --> N{Runtime Decision}
    H --> N
    I --> N
    J --> N
    K --> N
    L --> N
    M --> N

    N -->|Admissible| O[GO]
    N -->|Insufficient Context| P[HOLD]
    N -->|Repairable| Q[REPAIR]
    N -->|Inadmissible| R[BLOCK]

    O --> S[Execute / Generate]
    P --> T1[Request Context]
    Q --> U[Reframe Transition]
    R --> V[Prevent Collapse Trajectory]
```

## Description

This figure shows the I2OS Runtime Gate.

A proposed AI transition is evaluated before generation or execution. The system extracts the current state, estimates the expected next state, and checks the transition against multiple admissibility constraints.

The output is classified as GO, HOLD, REPAIR, or BLOCK.

This allows AI systems to reduce unnecessary computation, prevent unsafe transitions, and preserve continuity.

## Core Equation

```text
Permit(T)=1[C(S_t,T,S_{t+1})=1]
```

## Core Message

```text
Capability is not permission.
```
