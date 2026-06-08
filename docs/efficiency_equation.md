# I2OS Efficiency Equation

## Basic Ratio

```text
I_eff = C_admissible / C_total
```

Where:

```text
I_eff          = intelligence efficiency
C_admissible  = computation contributing to admissible continuity
C_total       = total computation
```

This measures the proportion of computation that contributes to valid continuity.

---

## Inadmissible Computation Penalty

```text
C_inadmissible = C_total - C_admissible
```

```text
I_eff = A_continuity / (C_inadmissible + ε)
```

Where:

```text
A_continuity    = admissible continuity preserved
C_inadmissible  = computation spent on inadmissible trajectories
ε               = small constant preventing division by zero
```

---

## Expanded Model

```text
I_eff =
(A_continuity × H_verify × R_recovery)
/
(C_inference + C_regeneration + C_review + C_recovery + C_external + ε)
```

Where:

```text
H_verify        = human-verifiability
R_recovery      = recoverability
C_inference     = inference cost
C_regeneration  = regeneration cost
C_review        = review cost
C_recovery      = recovery or rollback cost
C_external      = external action cost
```

---

## Interpretation

AI efficiency is not only model-side computation.

It includes downstream correction, review, recovery, and external-action cost.

I2OS improves efficiency by reducing computation spent on inadmissible trajectories.
