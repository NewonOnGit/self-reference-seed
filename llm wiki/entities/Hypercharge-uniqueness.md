---
type: entity
role: PHYSICS
theorem: "Thm 9.1b"
tags: [physics, forced]
---

# Hypercharge uniqueness

> **Theorem 9.1b.**

Given the framework's constraints — gauge group su(3) + su(2) + u(1) (from exchange operator), fundamental representations only (from exchange representation theory), chirality (from lifted gauge bit), and 5 field types (minimal chiral set: one quark doublet, two quark singlets, one lepton doublet, one lepton singlet) — the anomaly conditions uniquely determine the hypercharge ratios.

## Dependencies

- [[Anomaly-cancellation]]

## Proof

*Proof.* The six anomaly conditions reduce to a system in one free normalization Y_1 and one splitting parameter t (where Y_2 = Y_1 + t, Y_3 = Y_1 - t). The linear conditions (A1, A2, A3, A5) fix Y_4 = -3Y_1, Y_2 + Y_3 = 2Y_1, Y_5 = -6Y_1. The cubic condition (A4 = U(1)^3) gives 18Y_1(9Y_1^2 - t^2) = 0. For Y_1 != 0 (non-trivial): t = +- 3Y_1.

At t = +3Y_1: \{Y_1, Y_2, Y_3, Y_4, Y_5\} = Y_1 * \{1, 4, -2, -3, -6\}. The normalization Y_1 = 1/3 (from the

## Source

`paper/paper_v2.md` line 281
