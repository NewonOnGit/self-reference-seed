# Closure Certificate for a Minimal Persistence Algebra

**Abstract.** We study the Sylvester self-action L_s(X) = sX + Xs − X on M_2(ℝ), where s is the companion matrix of x² − x − 1. We prove: (1) x² − x − 1 is the unique polynomial x² − ax − b with a, b ∈ ℤ₊ admitting both a nontrivial Sylvester kernel and a rotation N² = −I within that kernel; (2) the sum P = s + N is a rank-1 non-self-adjoint idempotent from which s and N are the symmetric and antisymmetric parts; (3) the block-tower s′ = [[s, N], [0, s]] preserves all identities and produces Cl(3,1) Clifford structure at depth 2 with verified so(3,1) Lie bracket closure; (4) the system is maximally rigid under perturbation; (5) a KL-divergence deficit functional, forced by the tower's product structure via Shore–Johnson uniqueness, produces the dimensionless output α = 1/2 − φ̄² ≈ 0.11803. All computations are publicly reproducible.

---

## 1. Primitive

Let R be the companion matrix of x² − x − 1:

$$R = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$$

and J the swap involution of dimension 2:

$$J = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$

These are the only inputs. R satisfies R² = R + I by construction. J satisfies J² = I. The Cayley–Hamilton theorem applied to any 2×2 non-scalar matrix M satisfying M² = M + I forces tr(M) = 1, det(M) = −1, disc(M) = 5.

**Proof.** M² − tr(M)·M + det(M)·I = 0 by Cayley–Hamilton. Setting M² = M + I gives (1 − tr(M))·M + (1 + det(M))·I = 0. For non-scalar M, both coefficients vanish: tr(M) = 1, det(M) = −1. Then disc(M) = tr² − 4·det = 1 + 4 = 5. ∎

**Proposition 1.1.** Within M_2(ℤ) with entries in {−3,…,3}, there are exactly 8 solutions to M² = M + I, all in one observed GL_2(ℤ)-conjugacy class (all sharing tr = 1, det = −1). Note: the conjugacy class is infinite in M_2(ℤ) — conjugation by any element of GL_2(ℤ) preserves the equation. The claim is that all small-entry solutions are conjugate, not that solutions are finite.

*Exhaustively checked over {−3,…,3}⁴.*

---

## 2. Operation

Define the Sylvester self-action:

$$L_s(X) = sX + Xs - X$$

as a linear operator on M_2(ℝ) ≅ ℝ⁴. This is the only operation applied throughout the paper.

---

## 3. Kernel–Image Decomposition

**Theorem 3.1.** dim ker(L_R) = 2, dim im(L_R) = 2. The kernel fraction ker/A = 1/2.

*Computed via null_space of the 4×4 matrix representation of L_R.*

**Theorem 3.2 (Clifford grading).** ker(L_R) = span{N, NR} is the odd sector of the Clifford algebra Cl(1,1) ≅ M_2(ℝ). im(L_R) = span{I, R_tl} is the even sector. Here R_tl = R − (1/2)I and N is the unique (up to sign) element of ker(L_R) satisfying N² = −I with minimal Frobenius norm.

**Proof.** Direct computation: R_tl² = (5/4)I ∈ even, N² = −I ∈ even, NR·NR = I ∈ even. The grading even × even = even, odd × odd = even, even × odd = odd is verified for all basis products. ∎

**Theorem 3.3 (Scalar channel).** L_R(R_tl) = (disc/2)·I = (5/2)·I.

*Direct computation.*

---

## 4. The Single Generator

**Theorem 4.1.** P = R + N satisfies P² = P, rank(P) = 1, P ≠ Pᵀ, R = (P + Pᵀ)/2, N = (P − Pᵀ)/2.

*Direct computation: P = [[0,0],[2,1]], P² = [[0,0],[2,1]] = P.* ∎

**Theorem 4.2 (Asymmetry necessity).** If P = Pᵀ then N = 0, R = P, R² = P² = P = R, contradicting R² = R + I. Therefore P ≠ Pᵀ is required.

**Theorem 4.3 (Uniqueness).** Among companion matrices of x² − ax − b with a, b ∈ ℤ₊:

(a) P² = P holds only at (a,b) = (1,1).

(b) ker(L_R) ≠ {0} only for a = 1. For a ≥ 2, ker(L_R) = {0}.

(c) L_R(R_tl) is scalar only for a = 1.

*Verified for a, b ∈ {1,…,4} by direct computation (16 cases). (b) and (c) proved algebraically: L(R_tl) = (a−1)R + (2b+a/2)I, so the R-coefficient vanishes iff a = 1.*

**Corollary 4.4.** The polynomial x² − x − 1 is the unique minimal element of the family {x² − ax − b : a, b ∈ ℤ₊} satisfying all three conditions simultaneously. The uniqueness is triple: by scalar channel (4.3c), by kernel existence (4.3b), and by idempotent closure (4.3a).

---

## 5. Seven Identities

For s = R, the following hold in M_2(ℝ):

| # | Identity | |
|---|----------|-|
| 1 | R² = R + I | |
| 2 | N² = −I | |
| 3 | {R, N} = N | |
| 4 | RNR = −N | |
| 5 | NRN = R − I | |
| 6 | (RN)² = I | |
| 7 | [R, N]² = 5I | |

*All verified by direct 2×2 computation. Identity 7 uses {2, 3, 6} but not {1}.*

**Proposition 5.1 (Structure constants).** In sl(2,ℝ) = span{R_tl, N, C} with C = [R, N]: [R_tl, N] = C, [R_tl, C] = 5N, [N, C] = 4R_tl. Structure constants {5, 4} = {disc(R), |V₄|}.

---

## 6. Five Constants

| Constant | Source | Value |
|----------|--------|-------|
| φ = (1+√5)/2 | eigenvalue of R | 1.6180339887… |
| √3 | ‖R‖_F | 1.7320508076… |
| √2 | ‖N‖_F | 1.4142135624… |
| e | exp(h)[0,0] where h = JN | 2.7182818285… |
| π | smallest θ > 0 with exp(θN) = −I | 3.1415926536… |

**Proposition 6.1.** ‖R‖²_F + ‖N‖²_F = 3 + 2 = 5 = disc(R).

**Remark.** φ, √3, √2 are algebraic (from eigenvalues and norms). e and π emerge when the matrix exponential is applied to the algebraically-derived generators h and N. No sixth independent constant exists: the Frobenius sum equals the discriminant.

---

## 7. The Tower

Define the block-tower ascent:

$$s' = \begin{pmatrix} s & N \\ 0 & s \end{pmatrix}, \quad N' = \begin{pmatrix} N & -2h \\ 0 & N \end{pmatrix}, \quad J' = \begin{pmatrix} J & 0 \\ 0 & J \end{pmatrix}$$

**Theorem 7.1.** At every tower depth n tested (n = 0, 1, 2, 3, 4): s'² = s' + I, N'² = −I, {s', N'} = N', and ker(L_{s'})/dim(A) = 1/2.

**Theorem 7.2 (Continuity).** s(t) = [[s, tN], [0, s]] satisfies s(t)² = s(t) + I for all t ∈ [0, 1].

*Verified at t = 0, 0.25, 0.5, 0.75, 1.*

---

## 8. Depth-2 Clifford Structure

**Theorem 8.1.** At tower depth 2 (d_K = 8), there exist exactly 12 anticommuting 4-tuples with signature (3,1) and 18 with signature (2,2) among the 15 non-identity tensor products of {I, J, N, h}.

**Theorem 8.2.** The 6 pairwise commutators of any Cl(3,1) 4-tuple span a 6-dimensional Lie algebra isomorphic to so(3,1). All Lie brackets close within the span.

*Verified: matrix rank of commutator span = 6, and all [L_i, L_j] reconstructed from the span with residual < 10⁻⁸.*

**Remark.** Cl(3,1) requires d_K ≥ 8 (four anticommuting matrices with one timelike and three spacelike). At depth 1 (d_K = 4), no Cl(3,1) embedding exists. The Cl(3,1) structure is a depth-2 phenomenon.

---

## 9. Spectral Properties

**Theorem 9.1.** Eigenvalues of L_R: {−√5, 0, 0, +√5}.

**Theorem 9.2.** Eigenvalues of L_N: {−1, −1, −1+2i, −1−2i}. In particular, ker(L_N) = {0}. N is the unique generator (among R, N, J, h, P, Q) with trivial kernel under self-Sylvester action.

**Theorem 9.3 (Golden invariant).** The restriction of Σ_s(X) = q(sX + Xs) to span{I, s_tl} has matrix [[1, 5/2], [2, 1]] with eigenvalues {1+√5, 1−√5} = {2φ, −2φ̄} at every tower depth tested (n = 0, 1, 2, 3).

**Theorem 9.4 (Commutativity transition).** The projected product X ∗ Y := q(XY) on im(L_s) is commutative at depth 0 and non-commutative at depth ≥ 1.

---

## 10. Generation Direction

**Theorem 10.1.** At depth 0: ker(L_R) × ker(L_R) ⊆ im(L_R). All four products of the ker-basis {N, NR} land in im. im(L_R) × im(L_R) ⊆ im(L_R) (closed). im × ker ⊆ ker and ker × im ⊆ ker. The generating direction is one-way: ker → im.

**Theorem 10.2 (Generation decay).** The rank of ker×ker products projected onto im:

| Depth | im dim | ker²→im rank | Fraction |
|-------|--------|-------------|----------|
| 0 | 2 | 2 | 100% |
| 1 | 8 | 8 | 100% |
| 2 | 32 | 32 | 100% |
| 3 | 128 | 64 | 50% |
| 4 | 512 | 64 | 12.5% |

The generative rank freezes at 64 while im grows exponentially.

---

## 11. Rigidity

**Theorem 11.1 (Perturbation fragility).** For the family R(ε) = companion matrix of x² − x − (1+ε):

| ε | Identities {R,N}=N | P²=P | α |
|---|-------------------|------|---|
| −0.01 | Fail | Fail | 0.124 |
| 0.00 | Pass | Pass | 0.118 |
| +0.01 | Fail | Fail | 0.112 |

**Theorem 11.2 (Alternative seed failure).** Among all (a,b) ∈ {1,…,4}², only (a,b) = (1,1) satisfies ker(L) ≠ 0 ∧ N²=−I ∧ {R,N}=N ∧ P²=P simultaneously.

---

## 12. Deficit Functional

Define δ(ρ) = Err(ρ) + Comp(ρ) where Comp(ρ) = D_KL(ρ ‖ ρ_eq).

**Proposition 12.1 (KL uniqueness).** The tower's product structure (S_{n+1} = S_n × S_n) imposes additivity of Comp over independent subsystems. Combined with continuity and unique minimization at equilibrium, KL-divergence is the unique admissible functional (Shore–Johnson 1980).

**Theorem 12.2.** The partition function Z = Σ_k (φ̄²)^k = 1/(1−φ̄²) = φ. The equilibrium density ρ_eq = 1 − 1/Z = φ̄². The deficit output:

$$\alpha = \frac{1}{2} - \bar\varphi^2 = \frac{\bar\varphi^3}{2} \approx 0.11803398875$$

where 1/2 is the invariant kernel fraction.

**Proposition 12.3.** For the exchange operator P_ex on ℂ² ⊗ ℂ² (eigenspaces Sym² dim 3, Alt² dim 1), the ratio ΣT₃²/ΣQ² over the stabilizer's matter representations equals 3/8.

**Proposition 12.4.** All six anomaly cancellation conditions (SU(3)³, SU(2)²U(1), SU(3)²U(1), U(1)³, U(1)-grav, Witten) are identically satisfied by the exchange-derived matter spectrum.

---

## 13. Summary of Numerical Outputs

| Quantity | Expression | Value |
|----------|-----------|-------|
| α | 1/2 − φ̄² | 0.11803 |
| θ | ΣT₃²/ΣQ² | 3/8 = 0.375 |
| ν | N_c / (‖N‖²/‖R‖²) | 9/2 = 4.500 |
| η | φ̄⁴⁴ | 6.376 × 10⁻¹⁰ |
| so(3,1) | Cl(3,1) Lie closure | dim 6, verified |

These values are presented as computed outputs of the algebraic system, without physical identification.

---

## 14. Reproducibility

```
git clone https://github.com/NewonOnGit/self-reference-seed.git
cd self-reference-seed/modular
python engine.py
```

Dependencies: numpy, scipy. The repository contains the full engine (7 files, ~1400 lines), experiment scripts, and documentation. All theorems in this paper correspond to assertions verified by the engine.

---

## 15. Remarks

### Verification tiers

Every claim in this paper carries one of three verification levels:

| Tier | Meaning | Symbol |
|------|---------|--------|
| **A** | Proved algebraically (from definitions, Cayley–Hamilton, or Clifford grading) | ∎ |
| **E** | Exhaustively checked over a finite family (all (a,b) ∈ {1,…,4}², all entries in {−3,…,3}) | ☐ |
| **N** | Numerically verified to machine tolerance (~10⁻¹⁰) | ≈ |

Summary of claims by tier:

| Claim | Tier |
|-------|------|
| tr=1, det=−1, disc=5 (Cayley–Hamilton) | A |
| 7 identities | A (2×2 computation) |
| P²=P, R=sym(P), N=asym(P) | A |
| Asymmetry necessity (P=Pᵀ → no surplus) | A |
| Scalar channel L(R_tl) = (5/2)I | A |
| Clifford grading ker=odd, im=even | A |
| ker×ker ⊆ im at depth 0 | A (4 products) |
| a=1 forced (R-coefficient vanishes) | A |
| 8 solutions in {−3,…,3}⁴, one conjugacy class | E |
| P²=P only at (1,1) among (a,b) ∈ {1,…,4}² | E |
| ker(L_R)=0 for a≥2, (a,b) ∈ {1,…,4}² | E |
| Tower identities hold at depths 0–4 | N |
| ker/A = 1/2 at depths 0–4 | N |
| Cl(3,1) = 12 at depth 2 | E (combinatorial enumeration) |
| so(3,1) bracket closure | N (rank 6, residual < 10⁻⁸) |
| Golden eigenvalues at depths 0–3 | N |
| Commutativity transition at depth 1 | N (random sampling) |
| Generation decay 100→50→12.5% | N |
| Perturbation fragility at ε=0.01 | N |
| KL uniqueness (Shore–Johnson) | A (external theorem) |
| α = 1/2 − φ̄² | A (algebraic identity) |
| θ = 3/8 | A (arithmetic on matter content) |
| Anomaly cancellation 6/6 | A (arithmetic) |

---

The system generated by the companion matrix of x² − x − 1 under Sylvester self-action produces a closed, rigid, computationally verifiable package of algebraic structures. The closure includes: a rank-1 non-self-adjoint idempotent, a tower preserving all identities with invariant kernel fraction 1/2, Cl(3,1) structure at depth 2 with so(3,1) bracket closure, a commutativity-to-non-commutativity transition at depth 1, a one-directional generation ker → im that decays with depth, a golden eigenvalue invariant, and specific dimensionless numerical outputs.

The system is maximally rigid: perturbation by ε = 0.01 destroys the identity spine, and no alternative integer seed in {1,…,4}² produces the same closure.

The numerical outputs in §13 are stated without interpretation. Their relation to empirical constants, if any, is left to the reader.
