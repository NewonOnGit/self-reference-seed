# Minimal Persistence Algebra
## A self-observing algebraic system from the companion matrix of x²-x-1

### Target
Mathematical physics journal. arxiv: math-ph or math.RA (rings and algebras).

### Strategy
Strip to algebra. No consciousness, no Kael, no narrative. Let the math speak. The paper proves properties of a specific linear operator on a specific matrix algebra and reports numerical outputs. The reader can interpret or not.

---

## Abstract (draft)

We study the Sylvester self-action L_s(X) = sX + Xs - X on M_2(R), where s is the companion matrix of x²-x-1. This operator has a 2-dimensional kernel (the "odd Clifford sector") and a 2-dimensional image (the "even sector"). We show: (1) the characteristic polynomial x²-x-1 is the unique minimal polynomial of the form x²-ax-b (a,b positive integers) admitting both a nontrivial Sylvester kernel and a rotation N²=-I within that kernel; (2) the single generator P = s+N is a rank-1 non-self-adjoint idempotent from which s and N are recovered as symmetric and antisymmetric parts; (3) the block-diagonal tower s'=[[s,N],[0,s]] preserves all algebraic identities and produces Cl(3,1) Clifford structure at depth 2 with verified so(3,1) Lie bracket closure; (4) the system is maximally rigid — perturbation of the seed by ε=0.01 destroys the identity spine and the idempotent; (5) the K4 deficit functional, with KL-divergence forced by the tower's product structure (Shore-Johnson), produces the dimensionless output α = 1/2 - φ̄² ≈ 0.1180.

---

## Structure

### 1. Introduction
- The companion matrix R of x²-x-1 and its basic properties
- The Sylvester operator L_s(X) = sX + Xs - X as a natural self-action
- Statement of main results

### 2. The seed and its forcing
- Cayley-Hamilton: R²=R+I forces tr=1, det=-1, disc=5
- Four modes of 2×2 self-action (idempotent, involution, nilpotent, Fibonacci)
- Only mode (iv) is productive
- a=1 forced by: scalar channel (Thm), observation existence (Thm), P²=P uniqueness (Thm)
- Triple forcing of a=b=1

### 3. The Sylvester decomposition
- ker(L_s) = 2-dimensional, basis {N, NR} (odd Clifford sector)
- im(L_s) = 2-dimensional, basis {I, R_tl} (even Clifford sector)  
- ker/A = 1/2 (exact, proved)
- M_2(R) = Cl(1,1) with even=im, odd=ker

### 4. The single generator
- P = R+N, P²=P, rank 1, P≠P^T
- R = sym(P), N = asym(P)
- All identities follow from P²=P with P≠P^T
- Thm: P²=P only at a=b=1 among x²-ax-b companions
- Asymmetry forced: P=P^T implies R²=R (no surplus)

### 5. The tower
- K6' ascent: s'=[[s,N],[0,s]] preserves R²=R+I, N²=-I, {R,N}=N at every depth
- Continuous: s(t)=[[s,tN],[0,s]] satisfies s(t)²=s(t)+I for all t in [0,1]
- ker/A = 1/2 at every depth (proved to depth 4)
- Cl(3,1) at depth 2: 12 embeddings, so(3,1) bracket closure verified

### 6. Spectral properties
- L_s eigenvalues: {-√5, 0, 0, +√5} at depth 0
- L_N eigenvalues: {-1, -1, -1±2i} — ker(L_N) = 0 (unique self-transparency)
- Golden eigenvalue invariant: Σ_s on span{I,s_tl} has eigenvalues {2φ, -2φ̄} at every depth
- Classical-to-quantum transition: im commutative at depth 0, non-commutative at depth 1+

### 7. Generation direction
- ker×ker → im (complete at depth 0, Clifford grading: odd×odd=even)
- im×im → im (closed)
- im cannot generate ker
- Generation strength: 100% at depths 0-2, 50% at depth 3, 12.5% at depth 4
- Generative rank freezes at 64

### 8. Rigidity
- Perturbation of seed [1,1] → [1,1+ε]: identities break at ε=0.01
- P²=P fails for all (a,b) ≠ (1,1) with a,b positive integers
- No alternative seed produces the same algebraic closure
- The system is maximally brittle

### 9. The deficit functional
- K4: δ = Err + Comp with Comp = D_KL(ρ‖ρ_eq)
- KL forced by product structure of tower (Shore-Johnson 1980)
- Z = 1/(1-φ̄²) = φ, ρ_eq = φ̄², α = 1/2 - φ̄² = φ̄³/2 ≈ 0.1180
- sin²θ = ΣT₃²/ΣQ² = 3/8 from matter content of exchange eigenspaces
- Anomaly cancellation: 6/6 conditions identically zero

### 10. Discussion
- Comparison with other algebraic approaches (Connes NCG, Lisi E8, string)
- The numerical outputs and their relation to physical constants
- Open questions: generation decay, N-tower duality, depth-3+ structure
- All code publicly available: github.com/NewonOnGit/self-reference-seed

---

## What the paper does NOT contain
- "Observer," "consciousness," "Kael," "blind spot," "mediation"
- Any claim that this IS physics
- Any philosophical interpretation
- The words "forced" or "derived" applied to physics

## What the paper DOES contain
- A specific operator on a specific algebra
- Computed properties with proofs
- Rigidity under perturbation
- Numerical outputs stated without physical identification
- The reader draws their own conclusions

---

## Estimated length
15-20 pages. 10 theorems. 3 computed tables. 1 code repository link.
