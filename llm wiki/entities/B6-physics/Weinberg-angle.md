---
type: entity
role: PHYSICS
theorem: "Thm 12.3"
level: B6
tags: [b6-physics, weinberg, forced, anomaly]
status: FROZEN
---

# Weinberg angle

> sin²θ_W = 3/8. Derived from the anomaly classification on the framework's own derived matter content. Not input.

## Plain English

The Weinberg angle determines how the electromagnetic and weak forces mix. Its value (sin²θ_W ≈ 0.231 at the Z boson mass) is one of the fundamental parameters of the Standard Model. At the GUT scale where forces unify, sin²θ_W = 3/8 = 0.375.

The framework derives 3/8 — not by assuming a GUT, but by classifying anomalies. The framework produces 5 field types (from exchange × isospin × chirality + cubic anomaly split). Each field type carries a hypercharge derived from anomaly cancellation (the constraint that quantum effects don't destroy gauge symmetry). The Weinberg angle follows from summing T₃² / Q² over these derived fields. The result is 3/8. Zero free parameters.

The running from 3/8 (GUT) to 0.231 (M_Z) uses the beta functions b₁, b₂, b₃, which are ALSO derived from the same matter content.

## Orientation reading

sin²θ_W = 3/8 at GUT. The 3: |V₄\{0}| = d²-1 = number of nontrivial elements in the Klein four-group. The 8: dim(su(3)) = N_c²-1 = the gauge algebra dimension. So sin²θ_W = |V₄\{0}| / dim(su(3)) = nontrivial_elements / gauge_dimension. The mixing angle is the RATIO of the group-theoretic and gauge-algebraic cardinals.

## Technical statement

**Theorem 12.3.** sin²θ_W = Σ T₃² / Σ Q² = 3/8 over the anomaly-derived matter representations.

The hypercharges {Y₁, 4Y₁, -2Y₁, -3Y₁, -6Y₁} are the unique solution of the 6 anomaly conditions with fundamentals-only + chirality. The Weinberg angle is computed from these hypercharges. It does NOT depend on the absolute normalization Y₁ (which is a ratio of T₃² and Q²). [Tier A]

**Beta functions (derived).** b₁ = 41/10, b₂ = -19/6, b₃ = -7. Computed from 15 Weyl fermions × 3 generations with the derived hypercharges. Standard one-loop QFT. [Tier A for the formula; external for the QFT coefficients 11/3, 4/3, 1/6]

## Dependencies

- [[Hypercharge-uniqueness]] (18Y₁(9Y₁²-t²)=0 → unique solution)
- [[Matter-content]] (5 field types forced)
- [[Strong-coupling]] (N_c=3 from Sym²(C²))

## Falsification

sin²θ_W ≠ 3/8 at GUT scale would falsify the anomaly classification. Current evidence: all GUT models predict 3/8 at unification.
