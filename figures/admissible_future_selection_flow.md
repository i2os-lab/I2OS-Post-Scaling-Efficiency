# Figure 2: Admissible Future Selection Flow

```mermaid
flowchart TD
    A[Current State S_t] --> B[Possible Future Trajectories]

    B --> C1[Trajectory A: Context-valid]
    B --> C2[Trajectory B: Hallucination Risk]
    B --> C3[Trajectory C: Unrecoverable Action]
    B --> C4[Trajectory D: Human-verifiable]
    B --> C5[Trajectory E: Agent Loop Risk]

    C1 --> D[Admissibility Constraint C]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E{Pass C?}

    E -->|Yes| F[Admissible Continuation]
    E -->|No| G[Exclude Before Generation / Execution]

    F --> H[Lower Waste]
    F --> I[Continuity Preserved]

    G --> J[Reduced Inadmissible Computation]
```

## Description

This figure illustrates Admissible Future Selection.

Instead of generating all possible futures and filtering afterward, I2OS evaluates possible trajectories through an admissibility constraint before generation or execution.

Trajectories that are context-invalid, unsafe, unrecoverable, unsynchronized, future-incompatible, human-unverifiable, or computationally wasteful are excluded before they expand into downstream cost.

## Core Message

```text
The most efficient computation is computation that never needed to happen.
```
