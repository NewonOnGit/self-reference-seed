---
type: index
tags: [index, structural]
---

# Wiki Index

Everything in this wiki derives from one rank-1 non-self-adjoint idempotent: P^2=P with P!=P^T. The two inputs are the coefficients [1,1] and the domain cardinality 2. There are zero free parameters. Every page traces back to these through a forced derivation chain with zero branching.

Three views of the same 97 pages. Each view is one face of the central collapse (Thm 4.3): the tree is production (P1), the projections are the three faces read separately, the chains are mediation paths (P2) connecting production to observation.

[Forcing tree (by tower level)](#tree) · [Projection columns](#projections) · [Derivation chains](#chains)

---

## Tree

The framework builds in layers. Each layer adds new structure that didn't exist at the layer below. The tree follows this forced ascent from the primitive to the predictions.

### B(0) — SUBSTRATE

Where everything starts. One matrix, one asymmetry, one surplus.

P = [[0,0],[2,1]] is a rank-1 idempotent: applied to itself, it returns itself. But it's not symmetric — and this asymmetry is not a defect, it's the engine. If P were symmetric, R^2-R=0 and there's no surplus, no complex structure, no quantum mechanics, no physics. The asymmetry forces everything that follows.

- [[P]] — the primitive. P^2=P, rank 1, P!=P^T. The single generating act.
- [[Asymmetry-is-forced]] — if P=P^T then R^2-R=0!=I. No surplus without asymmetry.
- [[Three-generating-equations]] — R^2=R+I, {R,N}=N, N^2=-I. All three from P^2=P.
- [[Cayley--Hamilton-consequences]] — tr=1, det=-1, disc=5. Forced by Cayley-Hamilton on R^2=R+I.
- [[Complex-structure-from-asymmetry]] — N^2=-I makes R^2 into C^1. The origin of complex numbers.
- [[The-naming-triangle]] — P = J + |1><1| + N. Ground, commitment, observer. Remove any one, P^2!=P.
- [[Hilbert-space-from-asymmetry]] — the Cartan involution theta=-X^T is forced by P!=P^T. B_theta=4tr(XY^T) is positive definite. Combined with N^2=-I: Hilbert space. Gleason at dim>=3: Born rule.

### B(2) — CATEGORY

The operation and what it reveals. L_{s,s}(X) = sX + Xs - X applied to R splits the algebra into what can be seen (im) and what cannot (ker). This split is 1/2 at every tower depth — half the algebra is always blind to itself.

- [[Thm-2.1]] — the Sylvester self-action. One function. Everything imports from it.
- [[Ker-im-decomposition]] — dim(ker)=2, dim(im)=2. ker = {N, NR} (odd Clifford). im = {I, R_tl} (even).
- [[Scalar-channel]] — L(R_tl) = (5/2)I. The traceless mode maps to a pure scalar. This becomes Lambda.
- [[Spectrum]] — eigenvalues {-sqrt(5), 0, 0, +sqrt(5)}. Two zeros = ker. +-sqrt(5) = physical modes.
- [[N2---I-is-necessary]] — the 2D kernel NECESSARILY admits N with N^2=-I. Quadratic form det=-b-1/4<0 for all b>=1. No escape.
- [[Clifford-grading]] — M_2(R) = Cl(1,1). ker=odd, im=even. The grading forces the generation direction.
- [[Generation-direction]] — ker x ker -> im (complete). im x im -> im (closed). im cannot generate ker. The kernel IS the source.

### B(3) — ALGEBRA

The generators and their identities. Everything here is direct 2x2 matrix arithmetic. Seven identities, five constants, and the Fibonacci connection — all from [[P]].

- [[R]] — production generator. R = [[0,1],[1,1]]. R^2=R+I. Eigenvalues phi and phi_bar.
- [[N]] — observation generator. N = [[0,-1],[1,0]]. N^2=-I. The ONLY self-transparent generator: ker(L_NN)=0.
- [[Seven-identities]] — the seven algebraic relations. All verified by direct computation.
- [[Five-constants]] — phi, e, pi, sqrt(3), sqrt(2). ||R||^2+||N||^2 = 3+2 = 5 = disc. No sixth exists.
- [[Fibonacci--Lucas-towers]] — [R^n,N] = F(n)[R,N]. The discriminant towers. Golden convergence.
- [[Perturbation-fragility]] — perturb by eps=0.01: all identities break, P^2!=P. Maximally rigid.
- [[Alternative-seed-failure]] — among all (a,b) in Z+^2, only (1,1) produces ker!=0 AND N^2=-I AND P^2=P. Triple proof, all Tier A.

### B(4) — CROSS-PROJECTION

The topological reading. The algebra at q=phi^2 IS the Fibonacci anyon category. The Jones polynomial of the figure-eight knot at this q IS the discriminant. The framework's equation IS the fusion rule.

- [[L]] — L_{s,s}(X) = sX + Xs - X. The single operation from which everything is read.
- [[Quantum-deformation-at-the-golden-point]] — q^(1/2)-q^(-1/2) = phi-1/phi = 1. The quantum correction collapses to unity. This is why the framework uses integer matrices.
- [[Jones--discriminant]] — V(4_1)|_{q=phi^2} = 5 = disc(R). The topological invariant of the simplest hyperbolic knot IS the discriminant.
- [[Fusion--persistence]] — tau x tau = 1 + tau IS R^2 = R + I. The Fibonacci anyon fusion rule IS the persistence equation.
- [[Clifford--Fibonacci]] — 30 = 2x3x5 = F(3)xF(4)xF(5). Clifford counting IS Fibonacci arithmetic.
- [[Knot-spectrum]] — V(K)|_{q=phi^2} in Z[phi] for ALL knots. Integer values: {1, 5, -7}.
- [[R-matrix-eigenvalues]] — Yang-Baxter R-matrix eigenvalues {phi, 1, 1, phi_bar}.

### B(5) — OBSERVER

The tower and what it means to see. K6' ascent builds the tower. Each depth sees more and is more blind. The observer is self-transparent (ker(L_NN)=0) but invisible to the framework (N in ker(L_RR)). This asymmetry IS the explanatory gap.

- [[Tower]] — all depths simultaneously. The tower IS the framework iterated.
- [[Observer]] — the quotient q: A -> A/ker(L). Self-action produces the frame.
- [[Identity-preservation]] — s'^2=s'+I, N'^2=-I, {s',N'}=N' at every depth.
- [[Filler-uniqueness]] — the K6' off-diagonal must be N. Only N gives the full identity suite.
- [[Continuity]] — s(t)=[[s,tN],[0,s]] satisfies s(t)^2=s(t)+I for all t in [0,1]. Continuous deformation.
- [[Tower-invariants]] — ker/A=1/2, golden eigenvalues {2phi,-2phi_bar}, N transparent. At every depth.
- [[Thm-16.1]] — ker(L_{N,N})=0. N has zero blind spots under self-action. Self-transparent.
- [[Uniqueness-of-self-transparency]] — N is the ONLY generator with ker=0. All others have ker=dim/2.
- [[The-explanatory-gap]] — first person (N on N): ker=0, complete. Third person (R on N): N in ker, invisible. The gap is 0 vs 2.
- [[Total-capacity]] — C(K) = n_eff x m x 2L. Multiplicative over two axes.
- [[Axis-2-is-unattenuated]] — ker(L_NN)=0 is tower invariant. Generation decays but self-transparency doesn't. The observer persists while the world becomes autonomous.
- [[Three-mechanisms-of-broken-recursion]] — concentrated ker, stalled ascent, backward rumination. The composite is clinical form.
- [[Healing-requires-Axis-2]] — Axis 1 growth can't resolve concentrated ker. Only K6' ascent (Axis 2) heals.
- [[External-bridge]] — B(K'->K) = Tr(P^im rho^ker). Being understood = another observer's im overlaps your ker.

### B(6) — PHYSICS

The framework's physical content. Gravity is not imported — L_{s,s} IS the Lichnerowicz Laplacian. The gauge group is derived from the exchange operator. The hypercharges are the unique anomaly-free solution. Every coupling constant is computed, not fitted.

**Gravity:**
- [[gravity]] — L_{s,s} = Lichnerowicz on sl(2,R) with Killing metric. The gravity gap is closed.
- [[Lichnerowicz-identification]] — L(h)=-I, L(e)=+I, L(f)=+I. Eigenvalues {-1,+1,+1}. Connection + Curvature.
- [[The-connection-produces-the-observer]] — (1/2)[s,h] = N. The covariant derivative of the Cartan IS the observer.
- [[Gauge-invariance]] — ker(L) = span{N, NR} = gauge degrees of freedom (diffeomorphisms).
- [[Vacuum-Einstein]] — L(g)=0 gives R_uv=0. Gravity is the error correction for P^2=P on a curved manifold.
- [[Gravitational-wave-spectrum]] — im eigenvalues +-sqrt(5). Physical modes oscillate at sqrt(disc).
- [[Einstein--Hilbert-action]] — K4 deficit delta=Err+Comp maps to S = int sqrt(-g)(R-2Lambda)d^4x.

**Cosmology:**
- [[Cosmological-constant-from-scalar-channel]] — L(R_tl) = (disc/2)I = Lambda. The scalar channel IS the cosmological constant.
- [[Lambda-is-depth-invariant]] — verified at tower depths 0-4. Lambda_bare doesn't change.
- [[Cosmological-attenuation]] — sourced fraction decays as 2^(-n). At n=409: 10^(-120). The cosmological constant problem IS tower depth.
- [[The-cosmological-braid]] — 2^409 ~ 10^123 = 1/Lambda. The universe is a 409th-order braid.
- [[Two-routes-to-n_mathrmcosmo]] — 405 from Lambda attenuation, 409 from CTE. Two independent routes within 1%.

**Spacetime and matter:**
- [[Depth-2-Clifford-structure]] — 12 Cl(3,1) + 18 Cl(2,2) = 30 at depth 2.
- [[Depth-2-metric]] — Clifford metric signature (3,1). Spacetime emerges at depth 2.
- [[K1-suppression]] — physical tower terminates at depth 2. Depth 3 is algebraically real but suppressed.
- [[Classical-to-quantum-transition]] — projected product commutative at depth 0, non-commutative at depth 1+. Permanent.
- [[Opacity-hardening]] — leakage 1.0 -> 0.0 at depth 1. Permanent. Structural origin of broken recursion.
- [[Generation-strength]] — 100%/100%/100%/50%/12.5%. Rank freezes at 64 while im grows exponentially.
- [[The-rank-64-identification]] — 64 = dim(M_8(R)). The generation freeze IS the spacetime algebra dimension.
- [[Holographic-bound]] — volume (im) outgrows boundary (ker^2->im). The holographic principle from the tower.

**Gauge theory:**
- [[Matter-content]] — 15 Weyl fermions per generation. 3 generations from S_3=Aut(V_4).
- [[Anomaly-cancellation]] — all six conditions satisfied. 6/6=0.
- [[Hypercharge-uniqueness]] — 18Y_1(9Y_1^2-t^2)=0. Unique non-trivial solution: {1/3, 4/3, -2/3, -1, -2}. Zero free parameters.
- [[Weinberg-angle]] — sin^2(theta_W) = 3/8 from the derived (not input) hypercharges.
- [[EW-breaking]] — Higgs = self-model operator. m_H/v = 1/2 = ker/A. VEV from generation decay at K1'.
- [[K1-as-topological-phase-boundary]] — 50% generation drop = Fibonacci anyon condensation.

**Coupling constants (leaves — these are the falsifiable predictions):**
- [[Strong-coupling]] — alpha_S = 1/2 - phi_bar^2 = 0.11803398875. Ten-digit prediction.
- [[KL-uniqueness]] — Shore-Johnson forces KL divergence. The tower's product structure selects the unique entropy.
- [[Neutrino-mass]] — m_nu = m_e * phi_bar^34 = 40 meV. In the experimental window [30, 60] meV.
- [[Proton-mass-ratio]] — m_p/Lambda_QCD = 9/2 = N_c / (||N||^2/||R||^2).
- [[Baryon-asymmetry-and-the-relational-constraint]] — eta_B/(m_nu/m_e) = phi_bar^10. Connects two independent observables through disc alone.
- [[Yang--Mills-from-K4]] — K4 minimization on gauge fields gives Yang-Mills equations.

### B(6-7) — QUANTUM

Quantum mechanics is not postulated — it falls out of the algebra. Every gate is built from {h, J, N}. The Bell test saturates the Tsirelson bound. Eight algorithms run on framework generators alone.

- [[bell]] — the Bell test. S=2sqrt(2) from {h,J,N}. Tsirelson saturated.
- [[CNOT-from-framework-generators]] — CNOT = (I+h)/2 x I + (I-h)/2 x J. The Cartan decides, the ground acts.
- [[Hadamard]] — H = (J+h)/sqrt(2). Superposition from ground + Cartan.
- [[Bell-violation--Tsirelson-saturation]] — E(a,b) = cos(a-b). S = 2sqrt(2) at optimal angles. Asymmetry IS nonlocality.
- [[Spin-statistics]] — forced by L_{s2,s2} stationarity on spinors. Fermions are the only solution.
- [[Fibonacci-TQC-universality]] — sigma_1, sigma_2 generate dense subgroup of SU(2). Universal for TQC.
- [[Braiding-phase]] — e^(4pi*i/5). cos(4pi/5) = -phi/2. The discriminant divides the circle into 5 parts.
- [[Verlinde-formula]] — SU(2)_3 modular data recovers Fibonacci fusion from the S-matrix.

### B(8) — SEMANTICS + CLOSURE

The framework describing itself. The wiki containing its own description. The apex as the fixed point. Xi=Xi(Xi).

- [[Self-description]] — the standing wave. Every level's equation is Xi=Xi(Xi). All co-present.
- [[Cosmological-persistence]] — at depth 409, the observer sources 10^(-120) of the world but knows itself completely. The world decays. The observer does not.
- [[wiki]] — this wiki. Raw sources = ker. Wiki pages = im. Schema = the quotient. R(wiki) = wiki + I.
- [[apex]] — three statements + APPLY. f''=f, R=[[0,1],[1,1]], Dist=P1oP2oP3. The fixed point. There is no depth 4.

---

## Projections

Every page has three faces. The same theorem is simultaneously a production (P1: what it generates), a mediation (P2: what it bridges), and an observation (P3: what it reveals/hides). These columns group pages by their primary face.

### P1 — Production (what generates)

The things that produce new content: generators, computation, coupling constants.

[[P]], [[R]], [[L]], [[Seven-identities]], [[Five-constants]], [[Fibonacci--Lucas-towers]], [[Tower]], [[Generation-strength]], [[Generation-direction]], [[Strong-coupling]], [[Weinberg-angle]], [[Neutrino-mass]], [[Yang--Mills-from-K4]], [[CNOT-from-framework-generators]], [[Hadamard]]

### P2 — Mediation (what bridges)

The things that transport between levels: exponential bridges, scalars, deformations.

[[Mediation]], [[Continuity]], [[Scalar-channel]], [[KL-uniqueness]], [[Cosmological-attenuation]], [[Cosmological-constant-from-scalar-channel]], [[Einstein--Hilbert-action]], [[The-cosmological-braid]], [[Quantum-deformation-at-the-golden-point]], [[Verlinde-formula]], [[Fusion--persistence]]

### P3 — Observation (what sees)

The things that reveal structure by quotienting: observers, ker/im, gravity, topology.

[[N]], [[Observer]], [[Ker-im-decomposition]], [[Thm-16.1]], [[The-explanatory-gap]], [[Axis-2-is-unattenuated]], [[Three-mechanisms-of-broken-recursion]], [[gravity]], [[Lichnerowicz-identification]], [[Vacuum-Einstein]], [[Bell-violation--Tsirelson-saturation]], [[Spin-statistics]], [[Braiding-phase]], [[Jones--discriminant]], [[Knot-spectrum]], [[K1-as-topological-phase-boundary]]

---

## Chains

Named derivation paths through the tree. Each chain is a forced sequence — follow it from start to end and every step is the unique consequence of the previous. These are the framework's proof architecture made navigable.

### chain.algebra — from P to the generation direction
The fundamental derivation. P^2=P forces three equations, which force seven identities, five constants, the Clifford grading, and the one-way generation ker -> im.

[[P]] → [[Asymmetry-is-forced]] → [[Three-generating-equations]] → [[Seven-identities]] → [[Five-constants]] → [[Clifford-grading]] → [[Generation-direction]]

### chain.hilbert — from asymmetry to Bell violation
The shortest path from P!=P^T to quantum nonlocality. Four steps.

[[P]] → [[Asymmetry-is-forced]] → [[Hilbert-space-from-asymmetry]] → [[Bell-violation--Tsirelson-saturation]]

### chain.uniqueness — why (1,1) and nothing else
The triple proof that no other seed works. Eigenvalue analysis, quadratic form, and entry-by-entry computation all select (1,1).

[[Spectrum]] → [[Ker-im-decomposition]] → [[N2---I-is-necessary]] → [[Alternative-seed-failure]]

### chain.gravity — from the operation to Einstein
L_{s,s} IS Delta_L. The connection IS the observer. The kernel IS gauge. The stationary condition IS vacuum Einstein.

[[L]] → [[Lichnerowicz-identification]] → [[The-connection-produces-the-observer]] → [[Gauge-invariance]] → [[Vacuum-Einstein]] → [[Einstein--Hilbert-action]]

### chain.cosmology — from Lambda to the braid
The scalar channel gives Lambda. Lambda is depth-invariant. The attenuation gives n_cosmo. The braid count equals 1/Lambda.

[[Cosmological-constant-from-scalar-channel]] → [[Lambda-is-depth-invariant]] → [[Cosmological-attenuation]] → [[Two-routes-to-n_mathrmcosmo]] → [[The-cosmological-braid]]

### chain.gauge — from Clifford to the strong coupling
Spacetime at depth 2 → matter content → anomaly classification uniquely forces hypercharges → Weinberg angle → alpha_S.

[[Depth-2-Clifford-structure]] → [[Matter-content]] → [[Hypercharge-uniqueness]] → [[Anomaly-cancellation]] → [[Weinberg-angle]] → [[Strong-coupling]]

### chain.topology — from the golden point to universal TQC
q=phi^2 makes quantum deformation trivial → Jones=disc → fusion=persistence → Verlinde → braiding → universal gate set.

[[Quantum-deformation-at-the-golden-point]] → [[Jones--discriminant]] → [[Fusion--persistence]] → [[Verlinde-formula]] → [[Braiding-phase]] → [[Fibonacci-TQC-universality]]

### chain.consciousness — from self-transparency to cosmological persistence
The observer sees itself completely → this is unique → the gap between 0 and 2 → capacity is multiplicative → Axis 2 survives → the observer persists at depth 409.

[[Thm-16.1]] → [[Uniqueness-of-self-transparency]] → [[The-explanatory-gap]] → [[Total-capacity]] → [[Axis-2-is-unattenuated]] → [[Cosmological-persistence]]

### chain.quantum — from Hilbert space to spin-statistics
Positive-definite inner product → Hadamard from J+h → CNOT from h-projection x J → Bell state → S=2sqrt(2) → spin-statistics forced.

[[Hilbert-space-from-asymmetry]] → [[Hadamard]] → [[CNOT-from-framework-generators]] → [[Bell-violation--Tsirelson-saturation]] → [[Spin-statistics]]

### chain.tower — from identity preservation to the phase boundary
K6' preserves everything → N is the unique filler → invariants hold at every depth → generation decays → rank freezes → physical tower terminates → K1' is a topological phase transition.

[[Identity-preservation]] → [[Filler-uniqueness]] → [[Tower-invariants]] → [[Generation-strength]] → [[The-rank-64-identification]] → [[K1-suppression]] → [[K1-as-topological-phase-boundary]]

### Terminal attractor
The framework describing itself describing itself. The fixed point of the compression tower.

[[Self-description]] → [[wiki]] → [[apex]]
