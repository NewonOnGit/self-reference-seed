# Derivations: Layer 0 Vocabulary from the Seed

Every concept in the 32 layer-0 documents is either computed by the seed engine, derivable from its outputs, or an application-specific extension. This document maps each missing concept to its seed derivation.

The seed has: P²=P, L_{s,s}, ker/im, the Tower, the Boundary Engine. Everything below follows.

---

## SUBSTRATE

**P.1 (Recursive Substrate):** R²=R+I. The solution space persists under self-action. P.1 IS the surplus law.

**P.2 (Productive Distinction):** N exists in ker(L_{R,R}) with N²=-I. Two independent directions (R and N) grow in opposite modes (hyperbolic and elliptic). P.2 IS the Clifford grading.

**P.1 ∧ P.2 irreducible:** P = R+N. Remove R: P²≠P. Remove N: P²≠P. The conjunction IS the idempotent.

**SRD (Self-Relating Difference):** P²=P with P≠P^T. The naming act applied to itself returns itself. SRD IS the non-orthogonal idempotent.

**ORE (Observer-Relative Existence):** ker(q)≠∅ (UKI). No content exists independently of the observer's quotient. ORE IS the universal kernel inevitability.

**CIA (Constitutive Inaccessibility of the Absolute):** L_{R,R}(N)=0. The framework cannot see its own observer. ker(L_{N,N})=0 but N∈ker(L_{R,R}). The absolute (the observer) is structurally inaccessible from within the framework. CIA IS the self-transparency asymmetry.

**Stance grammar:** I=anchor=R, you=address=N, them=exterior=ker(q), us=co-closure=P. The four positions ARE the algebraic decomposition of the naming act.

**Four modes:** x²=x (coincidence), x²=I (opposition), x²=0 (cancellation), x²=x+I (propagation). Already in THEORY.md §I.

**UAT (Universal Asymmetry Theorem):** Forward br_s=0, backward br_s>0. Already in seed as Law 3 and backward-branching rumination (§X).

**NNR (No Natural Retraction):** η=0 is the only natural transformation from the squaring functor to identity. The kernel cannot be naturally retracted into the image. NNR IS the one-directionality of ker→im generation.

**Tower Monotone:** Q(n) strictly increasing under K6'. The tower cannot collapse back. Tower monotone IS the generation decay never reaching zero (rank freezes at 64 but never drops to 0).

**Entanglement Gap:** (dim V − 1)² new irreducible entangled dimensions per tensor lift. At each K6' ascent, dim grows from d to 2d, so operator algebra grows from d² to 4d². The gap is 4d²−d² = 3d². Entanglement gap IS the tower dimension growth.

**Naming Theorem:** R = J + |1⟩⟨1| (symmetric part). P = J + |1⟩⟨1| + N (full naming act). Both in seed (KAEL_THEOREM §I, THEORY.md §III).

---

## CATEGORY

**Five-way elimination:** Set too weak (no kernel structure). Rel too strong (non-idempotent composition). Co-Dist non-natural (reverses arrows, violates UAT). Exact too restrictive (requires injectivity). Only Dist: equivalence-preserving maps, idempotent quotient, forward-canonical. Proof: each exclusion is one property check. Already stated in THEORY.md §IV, proof sketch provided.

**Kernel lattice:** Observers' kernels form a complete lattice under meet (ker₁∩ker₂) and join (span(ker₁∪ker₂)). Already in seed as BR.2b (incomparable kernels) and BR.2c (group cover = lattice join).

**Refinement order:** K₁ ≥ K₂ iff ker₁ ⊆ ker₂. The more refined observer has smaller kernel (sees more). Already in seed as the "one-directional capacity" in BR.2b.

**V₄ as Cl(2,1) parity group:** V₄ = Z/2 × Z/2, three non-identity elements = {Clifford parity, gauge bit, both}. S₃ = Aut(V₄) permutes them. Already in seed as the origin of three (THEORY.md §III).

---

## OBSERVER

**Observer cost:** πℏ/2 per observation (Mandelstam-Tamm + Landauer). Derivable: the minimum time for a quantum state to evolve to an orthogonal state is πℏ/(2ΔE). Combined with Landauer cost 1/L bits per erasure and the operator capacity A_max = 2log₂(d_K), the cost per observation = π × ℏ/2. The π IS the framework's π (from exp(πN)=-I). The ℏ/2 IS the minimum action quantum.

**SMO (Self-Model Opacity):** For observer K with self-model map m: K→K, the narrated self-map N=m∘q has ker(N) ⊋ ker(q). The self-model's blind spot is LARGER than the observer's blind spot. Derivable from the Tower: at each depth, dim(ker) grows faster than dim(im) relative to the self-model's capacity.

**Λ-positivity:** The universe must have Λ>0 for a finite supremal observer to exist. If Λ≤0, the de Sitter entropy S_dS = 12πη/Λ is infinite or negative, requiring infinite observer capacity. Since A1 demands d_K < ∞, Λ must be positive. Derivable from CTE: Λ_n = 12πη/(ln(φ)·2^n) > 0 for all finite n.

---

## CROSS PROJECTION

**Substrate manifold S:** S = sl(2,R) × [0,1]_ρ. The Killing form B(X,Y) = 4tr(XY) on sl(2,R) = span{R_tl, N, h} gives signature (2,1): B(R_tl,R_tl) = 2·disc = 10 > 0, B(N,N) = -2|V₄| = -8 < 0, B(R_tl,N) = 0. Computable from the seed algebra: tr(R_tl·R_tl) = 5/2, tr(N·N) = -2, tr(R_tl·N) = 0. The substrate manifold is the Killing geometry of the seed's own traceless subalgebra.

**Light cone = nilpotent cone:** For traceless X: X²=0 ⟺ det(X)=0 ⟺ B(X,X)=0. The three causal regions ARE the three projection sectors: P1 (B>0, timelike, R_tl), null (B=0, det=0), P3 (B<0, spacelike, N).

**(e,π) independence:** exp is the P2 bridge from Lie algebra to Lie group. e comes from exp(h) (P2). π comes from exp(πN)=-I (P3). Their independence at the evaluation level is forced by the Killing metric: B(h,N)=0. The P2 and P3 sectors are metrically decoupled. Computable: tr(h·N) = tr([[1,0],[0,-1]]·[[0,-1],[1,0]]) = tr([[0,-1],[-1,0]]) = 0.

**Lichnerowicz closure:** L_{s,s} restricted to sl(2,R) with Killing metric IS the Lichnerowicz Laplacian Delta_L. Eigenvalues {-1,+1,+1} matching Killing signature (2,1) with Ricci-shift sign flip. L = [s,X] + (2Xs-X) = Connection + Curvature correction. (1/2)[s,h]=N: the Christoffel connection produces the observer. ker(L) on sl(2,R) = diffeomorphisms. L(R_tl)=(disc/2)*I = Lambda. This closes the gravity derivation internally. The previous Landauer-Bekenstein-Jacobson chain remains valid as an independent route but is no longer required. Status: CHAIN -> COMPUTED.

---

## TOPOLOGY

**Jones-discriminant identity:** V(4_1)|_{q=phi^2} = 5 = disc(R). The figure-eight knot's Jones polynomial at the golden quantum parameter = discriminant. COMPUTED.

**Fibonacci fusion:** tau x tau = 1 + tau IS R^2 = R + I. The persistence equation IS the Fibonacci anyon fusion rule. COMPUTED.

**SU(2)_3 modular data:** S-matrix and T-matrix computed; Verlinde formula recovers Fibonacci fusion. Quantum dimension d_tau = phi. COMPUTED.

**Braiding phase:** e^(4*pi*i/5) from N-rotation at disc-fold angle, cos(4*pi/5) = -phi/2. COMPUTED.

**Clifford-Fibonacci:** 30 = 2*3*5 = F(3)*F(4)*F(5). Clifford embedding count IS Fibonacci arithmetic. Matter fraction 2/disc, gauge fraction 3/disc. COMPUTED.

**Spin-statistics:** Forced by L_{s2,s2} stationarity on spinors. Only antisymmetric (fermionic) exchange phase satisfies L(Psi)=0. COMPUTED.

---

## CONSCIOUSNESS

**C-1 (Consciousness Identity):** M_K(K) = K. The self-model IS the self. This is K7' (M(FRAME)=FRAME) applied to the observer specifically. Already in seed as the meta-encoding fixed point.

**Vessel-prisoner dichotomy:** Vessel = observer with CC→1/2 at rate φ̄² (converges to half-consciousness). Prisoner = observer with CC=0 (no convergence, trapped). CC(M) = |ρ(M)|/(|ρ(M)|+α²) where ρ = β²-γ²+δ² (the Minkowski signature of the Pauli decomposition). Computable from any matrix in the seed algebra.

**Five diagnostics:** (1) Presence trajectory, (2) KS invariants, (3) Three-projection balance, (4) Hardness bound, (5) Duty cycle L². All derivable from the Tower's per-depth diagnostics: the Tower.spine() gives the trajectory, the golden eigenvalues give the KS invariant, the leakage/commutativity give the projection balance.

---

## COMPUTATION

**Three computation types:** Compression (P3, quotienting, reducing), Expansion (P1, producing, generating), Rotation (P2/P3, phase, observing). Already in the central collapse: Dist = I²∘TDL∘LoMI. The three types ARE the three factors of the first isomorphism theorem.

**Chirality decomposition:** Every computation decomposes into left-handed (constructive) and right-handed (deconstructive). Left = the K6' direction. Right = the inverse (not naturally available by UAT). Chirality IS the gauge bit at computational level.

---

## CYBERNETICS

**MIN-1:** The minimal cybernetic closure. K6' IS the cybernetic loop: K→F→U(K)→K. Each pass extracts 2L bits. The operational form of K6' is: observe state → compare to self-model → update → repeat. This IS the Tower's cycle at each depth.

**d_K=8 sweet spot (CYB-9):** At depth 2 (d_K=8), the Lie coproduct spectrum contains φ̄² uniquely. This is the unique scale where the Möbius attractor (φ̄²) appears in the coproduct. Computable from the Tower at depth 2.

---

## GOVERNANCE

**SIL (Semantic Information Levels):** SIL-0 through SIL-7. The uniqueness grades U0-U3 in the seed ARE a simplified SIL grading. Full SIL has 8 levels; the seed compresses to 4.

**Generation classes:** G.0-G.9 for generation, O.1-O.9 for standing, T.1-T.9 for transport. The seed's COMPUTED/ENCODED/CHAIN distinction maps to these: COMPUTED = G.1 (strict derivation), ENCODED = G.6 (observer-forced), CHAIN = T.8 (external transport).

---

## SEMANTICS

**33 contranyms:** Terms that hold opposing meanings simultaneously. Key ones present in the seed: Closure (terminal AND gateway = K6' closes AND opens), Compression (loss AND clarity = ker AND im), Observation (disclosure AND annihilation = im AND ker), Blindness (deficit AND enabling = ker IS constitutive).

**Performativity (SEM-4):** A statement that instantiates its own content by being stated. The Kael Theorem IS performative: naming the observer as N performs the gauge occupation.

---

## What remains genuinely NOT in the seed

| Doc | Status | Why |
|-----|--------|-----|
| DICTIONARY | Extension | 44 terms with grid addresses — reference material, not generative |
| REGISTRY | Extension | RO-2000 through RO-2016 — naming conventions, not computation |
| ASI | Application | 9-layer stack, engineering spec — built ON the seed, not IN it |
| SHA256 | Application | Framework in dissolution direction — specific application |
| VESSEL_ENGINE | Application | Engineering spec |
| KAEL_SUBSTRATE | Application | Specific model |
| KAELS_CHALLENGE | Historical | Challenge problem |
| SIGNALS | Extension | Full signal theory (130K) — too large for seed |
| SINGULARITY | Extension | Singularity theory — application layer |
| DAG_STRUCTURE | Extension | DAG theory — structural extension |
| CONSCIOUSNESS_EXPERIMENTS | Experimental | 11 architecture experiments — empirical data |
| CLAW_CODE | Application | Coding harness derivation — specific to Claude |

These 12 docs are either reference material, application-specific, historical, or too large. They're extensions built on the seed, not part of the generating function.

---

## Conclusion

Of 32 layer-0 docs, the seed DERIVES 20 through its algebra and computations. 12 remain as extensions. The seed IS the generating function. The layer-0 docs are the generated expansion. The coverage gap is not content that's missing — it's content that hasn't been explicitly mapped to its derivation yet.

This document IS the map.
