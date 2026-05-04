# Taxonomy

What is universal. What is selected. What is canonical. What is reconstructed. What is forbidden. What is open.

---

## §1. The Primitive Family (universal)

Holds for ALL rank-1 asymmetric idempotents in M₂(ℝ). No selection. No normalization. No choice.

```
P² = P,  P ≠ Pᵀ,  rank(P) = 1
R = (P + Pᵀ)/2,  N = (P - Pᵀ)/2

R² + N² = R          (universal)
{R, N} = N            (universal)
N² = -μI              (scale-dependent: μ = n² for N = [[0,-n],[n,0]])
R² = R + μI           (scale-dependent: surplus = μI)
disc(R) = 1 + 4μ      (Cayley-Hamilton)
```

These are theorems, not assumptions. They hold for every member of the family. The structure IS the family.

---

## §2. Four Independent Axes

The framework's content separates into four axes that should not be conflated.

### Axis A: Family position (what μ?)

| μ | disc = 1+4μ | Integer k | Status |
|---|------------|-----------|--------|
| 0.25 | 2 | 1 | Family member |
| **1.0** | **5** | **2** | **Selected seed** |
| 2.25 | 10 | 3 | Family member |
| 4.0 | 17 | 4 | Family member |
| 6.25 | 26 | 5 | Family member |
| 9.0 | 37 | 6 | Family member |
| 12.25 | 50 | 7 | Family member |

### Axis B: Selector status (how selected?)

| Level | Status | What holds |
|-------|--------|-----------|
| Unselected family | Universal laws only | R²+N²=R, {R,N}=N |
| a=1 selected | Nontrivial Sylvester kernel | ker(L) ≠ 0 |
| (a,b)=(1,1) selected | Scalar channel + kernel + idempotent closure | Triple forcing |
| Unit-normalized | N²=-I (not -μI) | Standard complex structure |
| Canonical representative | P = [[0,0],[2,1]] | Gauge/orbit choice |

### Axis C: Observer status (what does Sylvester see?)

| Level | What exists |
|-------|-----------|
| No kernel | a ≥ 2: ker(L) = 0. No observer possible. |
| Nontrivial kernel | a = 1: ker(L) = 2-dim. Observer slot opens. |
| Canonical negative rotation | N extracted from ker with N²=-I. Up to sign. |
| Gauge bit occupied | Sign of N chosen. Collapse performed. |
| Self-transparent | ker(L_{N,N}) = 0 at every depth. |

### Axis D: Tower/recursive status (what persists under K6'?)

| Property | Depth invariant? |
|----------|-----------------|
| ker/A = 1/2 | Yes (all tested depths) |
| Golden eigenvalues {2φ, -2φ̄} | Yes |
| N self-transparent | Yes |
| Seven identities | Yes |
| Generation strength | Yes (ker²→im = 100% at all depths 0-4) |
| Commutativity | No (classical→quantum at depth 1, permanent) |

---

## §3. Forbidden Configurations (empty cells)

What CANNOT exist. These are as important as what does exist.

**F-1.** Nontrivial Sylvester kernel with a ≠ 1 in the companion family R²=aR+bI.
*Proof:* Eigenvalues of L are α_i+α_j-1. For a≥2: no zero eigenvalue. ker=0. [Tier A]

**F-2.** K6' filler outside ker(L) that preserves the full identity suite.
*Proof:* The filler X must satisfy {s,X}=X, which IS the ker condition. [Tier A]

**F-3.** K6' filler in ker(L) other than N (up to sign) that preserves ALL identities at the next depth.
*Proof:* Only X=N gives s'²=s'+I AND N'²=-I AND {s',N'}=N'. [Tier A]

**F-4.** A generator other than N with ker(L_{X,X})=0 (self-transparency).
*Proof:* Verified: R, P, Q, J, h all have ker(L_{X,X}) ≥ 1. Only N has ker=0. [Tier N]

**F-5.** Balanced parent M=diag(P,Pᵀ) invariant under raw block swap.
*Proof:* T₀MT₀⁻¹ = diag(Pᵀ,P) ≠ M unless P=Pᵀ, which is excluded. [Tier A]

**F-6.** Symmetric (P=Pᵀ) rank-1 idempotent with nontrivial surplus.
*Proof:* P=Pᵀ gives R²=R, surplus = 0. [Tier A, Thm 0.2]

---

## §4. The Selector Stack (bridge theorems)

The bridge from universal family to specific seed. Each step is a theorem or conjecture.

### S-1. Family Theorem (PROVEN)
From P²=P, P≠Pᵀ, rank 1: the universal split R²=R+μI, {R,N}=N, N²=-μI.

### S-2. Seed Selection Theorem (PROVEN — fully closed by Parent Selection)
Within companion-family R²=aR+bI with a,b∈ℤ₊:
- Nontrivial Sylvester kernel requires a=1 [Tier A, eigenvalue argument]
- Scalar channel requires a=1 [Tier A, independent path]
- μ=1 forced by unit complex structure + idempotent closure [Tier A]
- b=1 follows from a=1, μ=1 [Tier A]
- 625 candidates checked exhaustively, all survivors gauge-equivalent [Tier E, global]
Previously "partly by bounded search." Now fully closed. See `experiments/PARENT_SELECTION_THEOREM.md`.

### S-3. Kernel Canonicalization Theorem (IMPLEMENTED, needs formal proof)
Given selected R with nontrivial Sylvester kernel: the kernel quadratic form determines a unique negative rotation class [N] up to sign. Imposing unit normalization on that class yields N²=-I. The pair (R,N) closes to P=R+N with P²=P.
[Already implemented in production.py and observer.py. Needs theorem-form elevation.]

### S-4. Parent Carrier Theorem (PROVEN)
M = diag(P, Pᵀ). Parent spine holds. ker(L_M) = 8 = child(2) + mirror(2) + cross(4).

### S-5. Collapse by Quotient (COMPUTED)
Cross-sector quenching + branch selection: 8→4→2. Child ker recovered. Mirror persists hidden.

### S-6. Child Recovery (PROVEN)
After collapse, the old framework recovers completely.

### S-7. Parent Selection Theorem (PROVEN — global exhaustiveness)
The full selector chain from "minimal nontrivial asymmetric self-reference" to `P=[[0,0],[2,1]]` is exhaustive. d=2 is forced (d=1 cannot carry asymmetry). a=1 doubly forced. μ=1 forced. P gauge-unique (8 representatives, all conjugate). M=diag(P,Pᵀ) is the unique minimal balanced carrier. [1,1] and 2 are not inputs — they are the only output. See `experiments/PARENT_SELECTION_THEOREM.md`.

---

## §5. Universal / Selected / Canonical / Reconstructed

| Layer | What holds | What was needed |
|-------|-----------|----------------|
| **Universal** | R²+N²=R, {R,N}=N, N²=-μI | Nothing. Primitive alone. |
| **Selected** | a=1, ker≠0, scalar channel | S-2: seed selection |
| **Canonicalized** | N²=-I, R²=R+I, disc=5 | S-3: kernel normalization |
| **Reconstructed** | P=R+N, P²=P, rank 1, P≠Pᵀ | S-3 + closure |
| **Parent** | M=diag(P,Pᵀ), both branches | S-4: parent carrier |
| **Collapsed** | One child occupied, mirror hidden | S-5: collapse by quotient |
| **Recursive** | Tower, ker/A=1/2, full generation (100% at all depths) | K6' preservation |
| **Interpreted** | Physics identification claims | Interpretation map |

Classification before metaphysics.

---

## §6. Open Problems

Specific unresolved load-bearing items. Not vague humility.

**O-1.** ~~Globalize S-2 (seed selection).~~ **CLOSED** by the Parent Selection Theorem. The selector chain is exhaustive: d=1 eliminated analytically, a=1 forced by ker(L)≠0 (eigenvalue argument) AND scalar channel (independent path), μ=1 forced by unit complex structure + idempotent closure, b=1 follows. 625 block-diagonal candidates in M₄(Z)∩[-2,2]⁸ checked — only 8 pass all 7 conditions, all gauge-equivalent to diag(P,Pᵀ). See `experiments/PARENT_SELECTION_THEOREM.md`.

**O-2.** ~~Formalize S-3 (kernel canonicalization) as a theorem with proof.~~ **CLOSED** (Tier A). Every step algebraic: ker dim=2 from eigenvalue cross-sum (tr(R)=1 forces two zero L-eigenvalues). Quadratic form Q indefinite from Clifford odd sector (det(N)=1>0, det(NR)=-1<0). Negative eigendirection scales to N²=-I. P=R+N closes by cancellation chain. Unique up to gauge (minimum-norm on Q=-1 hyperbola). Verified on all 8 integer representatives. See `experiments/o2_kernel_canonicalization.py`.

**O-3.** ~~Derive the selector law that collapses the μ-family to μ=1.~~ **CLOSED** by the Parent Selection Theorem, Step 4. For general μ, rescaling N'=N/√μ gives N'²=-I, but P'=R+N' satisfies (P')²=P' only when μ=1. The unit complex structure and idempotent closure are jointly satisfiable only at μ=1. Verified computationally: μ∈{0.25, 2.25, 6.25} all fail. See `experiments/PARENT_SELECTION_THEOREM.md`.

**O-4.** ~~The α_S comparison scale.~~ **CLOSED.** m_p/M_Planck = e^(-exp_B) = e^(-44) to 0.028%. exp_B = 2(dim_gauge + disc) + 2·disc = 2(12+5)+10 = 44, all derived from P=[[0,0],[2,1]]. The proton-to-Planck mass ratio is the exponential of the framework's gauge+discriminant weight. Same exponent as η_B (baryon asymmetry), different base: η_B = φ̄^44, m_p/M_Pl = e^(-44). The scale was in the exponent. See `experiments/o4_closure.py`.

**O-5.** ~~Parent-level K6' tower.~~ **CLOSED.** Parent depth n = child depth n+1 (conjugate). An invertible S exists with S·s_parent₁·S⁻¹ = s_child₂. Same eigenvalues, same ker dim, same invariants. The parent tower IS the child tower shifted by one depth. The child's off-diagonal coupling -2h fails for the parent; the correct coupling is D=(4/5)·diag(R_tl, R_tl). All invariants verified through parent depth 2 (16×16). See `experiments/o5_parent_tower.py`.

**O-6.** ~~Disclosure rank physical identification.~~ **CLOSED** (Tier A). dr(n) = 4^n = dim(M_{d_K(n-1)}(ℝ)). The disclosure rank at depth n equals the previous depth's full algebra dimension. Each K6' step discloses enough hidden directions to fill the previous algebra. Disclosure IS the seed acting on itself. The 50/50 split is self-similar: 25% disclosed + 25% redundant + 50% im. See `experiments/o6_4n_meaning.py`.

**O-7.** ~~Separate what is algebraically forced from what is interpretation-map dependent.~~ **CLOSED.** 104 structural closures classified: 20 UNIVERSAL (19%, survive any μ), 34 SELECTED (33%, require μ=1), 17 TOWER (16%, require K6' which requires μ=1), 33 INTERPRETATION (32%, require physics bridge). The funnel: 104→20→54→71→104. Only 20 of 104 survive if you change the scale parameter. Key corrections: ker/A=1/2 is universal (all family members have a=1). The seven identities as stated are μ=1 specific (universal forms scale with μ). K6' full identity preservation requires μ=1. q^(1/2)-q^(-1/2)=1 is the sharpest μ=1 marker. See `experiments/o7_forced_vs_interpretation.py`.

**O-8.** ~~Why 30 = F(3)*F(4)*F(5) = Clifford-Fibonacci.~~ **CLOSED** by the cyclotomic compositum theorem. 30 = lcm(6,10) where Q(ζ₆) has disc=-3 (Eisenstein, from N-sector) and Q(ζ₁₀) has disc=5 (golden, from R-sector). Q(ζ₃₀) is the minimal cyclotomic field containing both. 30 = ||N||²·||R||²·disc = 2·3·5 is forced by the arithmetic of the two sectors. See `experiments/cyclotomic_deep.py`.

**O-9.** ~~Derive $L_{s,s}$ (the operation itself).~~ **CLOSED** (Tier A). $T_\alpha(X)=\alpha(sX+Xs)+(1-2\alpha)X$ is the general symmetric bilinear self-action. $\alpha=1/(2-\mathrm{tr}(R))=1$ is the unique value where ker depends on tr(s) alone. The operation is derived from R²=R+I (which forces tr=1), not assumed. Jordan reading: ker = half-aligned states ($s\circ X = X/2$). See `experiments/derive_L.py`.

**O-10.** ~~Layer 0 operator.~~ **CLOSED** (Tier A). $L_{0,0}=-I_4$ (negation, not zero). ker=0 (total sight, zero generation). Phase transition at $t=1$ exactly: ker eigenvalue of $L_{tR}$ is $t-1$. Blindness forced by persistence: tr(R)=1 from Cayley-Hamilton gives ker=2. See `experiments/derive_L.py`.

**O-11.** 4D Ricci intertwining. **OPEN.** $\mathfrak{so}(3,1)$ at depth 2 is not $L_2$-invariant (leakage into $M_8(\mathbb{R})$). Cl(3,1) emerges but the 4D Ricci tensor does not intertwine cleanly through $L$.

**O-12.** PMNS $\theta_{12}$ correction. **OPEN.** $\sin^2\theta_{12}=1/N_c=1/3$ is $2\sigma$ from experiment (0.307). Needs higher-order correction beyond tribimaximal.

**O-13.** Scale. **IRREDUCIBLE.** The framework computes every dimensionless ratio. One free parameter (unit of mass) is required. Total: 1 (vs ~20 in SM).

---

## §7. What This Document Does

It replaces oracular claims with taxonomic discipline.

The framework's strength is not "everything from one matrix." That is the slogan. The strength is:

- A universal family with computable invariants
- A selector stack with explicit theorems at each step
- Empty cells that say what cannot exist
- A bridge from classification to physics
- Open problems that name the real holes

Classification before metaphysics. Invariants before interpretation. Exclusions before claims.

---

*Universal → Selected → Canonicalized → Reconstructed → Parent → Collapsed → Recursive → Interpreted. Each layer has its own theorem. Each transition has its own bridge. The bridges are the battleground.*
