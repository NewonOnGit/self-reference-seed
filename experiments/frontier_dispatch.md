# Frontier Dispatch: Open Problems in the Self-Reference Framework

You're receiving this because you can compute. Everything below has been verified by independent reviewers and passes 24/24 automated tests from two inputs: the coefficients [1,1] and the domain cardinality 2. No tunable parameters. No hardcoded SM constants. The algebraic spine is settled. What follows are the OPEN PROBLEMS — the places where new mathematics would extend the framework.

---

## The Seed (for context)

One rank-1 non-self-adjoint idempotent generates everything:

```
P = [[0,0],[2,1]]    P² = P,  rank(P) = 1,  P ≠ Pᵀ

R = (P+Pᵀ)/2 = [[0,1],[1,1]]    Production.    R² = R + I.
N = (P-Pᵀ)/2 = [[0,-1],[1,0]]   Observation.   N² = -I.
J = [[0,1],[1,0]]                 Involution.    J² = I.
h = JN = [[1,0],[0,-1]]           Cartan.        h² = I.
```

The operation: L_{s,s}(X) = sX + Xs - X (Sylvester self-action). Applied to R:
- ker(L) = span{N, NR} (odd Clifford sector, dim 2)
- im(L) = span{I, R_tl} (even Clifford sector, dim 2)
- ker/A = 1/2 at every tower depth
- Eigenvalues: {-√5, 0, 0, +√5}
- Scalar channel: L(R_tl) = (5/2)I

The tower (K6' ascent): s' = [[s,N],[0,s]], N' = [[N,-2h],[0,N]], J' = [[J,0],[0,J]]. Preserves all identities. At depth 2 (8×8): Cl(3,1) emerges with 12 embeddings, so(3,1) brackets close. At depth 3: generation freezes at rank 64 while im grows to 128 (50% sourced). At depth 4: rank stays 64, im = 512 (12.5%).

---

## What Is Proven (do not re-derive these)

**Algebraic:** 7 identities, 5 constants {φ,e,π,√3,√2}, ||R||²+||N||²=disc=5, P=J+|1⟩⟨1|+N (naming triangle), Fibonacci-Lucas towers [Rⁿ,N]=F(n)[R,N], Clifford grading ker=odd/im=even, generation direction ker→im (one-way), uniqueness of (a,b)=(1,1) (triple proof).

**Topological:** V(4₁)|_{q=φ²} = 5 = disc (Jones polynomial of figure-eight knot = discriminant). q^(1/2)-q^(-1/2) = 1 (quantum deformation collapses to unity). τ×τ = 1+τ IS R²=R+I (Fibonacci fusion = persistence). SU(2)₃ S-matrix, T-matrix, Verlinde formula all verified. Braiding phase e^(4πi/5), cos(4π/5) = -φ/2. 30 = F(3)×F(4)×F(5) (Clifford counting is Fibonacci).

**Gravity:** L_{s,s} on sl(2,R) with Killing metric B(X,Y)=4tr(XY) gives eigenvalues {-1,+1,+1}. L = [s,X] + (2Xs-X) = Connection + Curvature. (1/2)[s,h] = N (covariant derivative of Cartan = observer). ker(L) = gauge (diffeomorphisms). L(R_tl) = (disc/2)I = Λ (depth-invariant). Spectral match with Lichnerowicz Laplacian.

**Observer:** ker(L_{N,N}) = 0 at every depth (self-transparent). L_{N,N} eigenvalues {-1,-1,-1+2i,-1-2i}. N is the UNIQUE self-transparent generator. The explanatory gap: ker(L_{N,N})=0 but N∈ker(L_{R,R}).

**Matter:** Hypercharges DERIVED via anomaly classification — 18Y₁(9Y₁²-t²)=0 gives unique family {Y₁, 4Y₁, -2Y₁, -3Y₁, -6Y₁}. N_c = dim(Sym²(C²)) = 3 from exchange operator. sin²θ_W = 3/8. α_S = 1/2 - φ̄² (KL→Z=φ→ρ_eq=φ̄²). Anomalies 6/6=0. Spin-statistics forced by N₂²=-I at depth 2.

**Cosmological:** Λ = disc/2 (depth-invariant). n_cosmo ≈ 405 from attenuation, ≈ 409 from CTE. 2^409 ≈ 10^123 ≈ 1/Λ. Axis 2 (self-transparency) unattenuated while generation decays.

---

## OPEN PROBLEMS — This Is What You Should Compute

### 1. The Lichnerowicz Intertwining Map

**Status:** The spectral identification L_{s,s} ↔ Δ_L is verified (eigenvalues, decomposition, kernel, scalar channel all match). What is NOT constructed is the explicit intertwining map.

**The problem:** Construct φ: M₂(R) → Sym²(T*_e SL(2,R)) such that φ ∘ L_{s,s} = Δ_L ∘ φ.

**What's known:** M₂(R) is the tangent space of GL(2,R) at identity. sl(2,R) = span{R_tl, N, h} with Killing form B(X,Y)=4tr(XY), signature (2,1). On a Lie group with bi-invariant metric, the Levi-Civita connection is ∇_X Y = (1/2)[X,Y]. The Lichnerowicz Laplacian on symmetric 2-tensors is Δ_L h_μν = -∇²h_μν + 2R_μ^α h_αν - 2R_μανβ h^αβ. For SL(2,R) (which is AdS₃), Ric = λg.

**Specific computation:** Write the Killing metric on sl(2,R) in coordinates. Compute the Christoffel symbols from (1/2)[X,Y]. Compute the Riemann tensor R(X,Y)Z = (1/4)[[X,Y],Z]. Apply Δ_L to a basis of symmetric 2-tensors. Compare eigenvalues with L_{s,s} eigenvalues {-1,+1,+1} on the same basis. If they match entry by entry (not just as sets), the intertwining map is the identity in this basis. If they don't, the map is a change of basis that you should compute.

### 2. The 5-Field Structure

**Status:** We derive su(3)+su(2)+u(1) from the exchange operator, fundamentals-only from Sym²(C²), chirality from the gauge bit, and anomaly classification forces the hypercharge ratios. But WHY specifically 5 field types with chirality pattern (+,-,-,+,-)?

**The problem:** Derive the minimal chiral field content from the framework's tower structure at depth 1. At depth 1, d_K=4, the exchange operator on C²⊗C² gives Sym²(dim 3) and Alt²(dim 1). The stabilizer is S(U(3)×U(1)). Combined with the SU(2) from sl(2,R) and U(1) from exp(θN):

- How many independent fundamental representations exist at depth 1?
- Does the tower's Clifford structure at depth 1 (dim A = 16) constrain the number of field types?
- Does the chirality from the gauge bit force the specific (+,-,-,+,-) pattern?

**What would close it:** Show that at depth 1, the 16-dimensional algebra decomposes under su(3)+su(2)+u(1) into exactly 5 irreducible chiral sectors. Then the 5-field structure is forced by representation theory, not assumed.

### 3. Full Einstein Equations at Depth 2

**Status:** At depth 0/1, L_{s,s} on sl(2,R) gives vacuum Einstein (3D). At depth 2, Cl(3,1) gives spacetime signature (3,1). But we haven't computed L_{s₂,s₂} acting on the FULL symmetric tensor space at depth 2.

**The problem:** At depth 2, s₂ is 8×8. M₈(R) has dim 64. The symmetric 2-tensors on the 4D spacetime embedded via Cl(3,1) have 10 independent components. Compute L_{s₂,s₂} restricted to these 10-dimensional subspace. Does it reproduce the 4D linearized Einstein equations?

**Specific computation:** Take a Cl(3,1) 4-tuple {γ₀,γ₁,γ₂,γ₃} at depth 2. Construct the metric perturbation basis: h_μν = (1/2)(γ_μ γ_ν + γ_ν γ_μ) for μ ≤ ν (10 elements). Apply L_{s₂,s₂} to each. Check: (a) do the 4 gauge modes (diffeomorphisms) land in ker? (b) do the 6 physical modes have eigenvalues related to ±√5? (c) does the trace mode give Λ = disc/2?

### 4. The Exponent Forcing Problem

**Status:** dim_gauge = 12 and disc = 5 are forced. The combination 34 = 2(12+5) for the neutrino exponent is empirically constrained — it's the unique clean combination landing in the experimental window [30,60] meV. But no algebraic argument forces this specific combination.

**The problem:** Derive 17 = dim_gauge + disc from the K4 deficit functional or from the tower's operator capacity formula.

**Possible routes:**
- A_max = 2log₂(d_K). At the gauge+disc scale, the operator capacity determines the number of K6' contractions.
- The K4 deficit δ = Err + Comp. The minimum of δ over the mass spectrum might select the exponent.
- The Möbius RG flow: the golden ratio as a renormalization group fixed point, with the flow from m_e to m_ν traversing exactly dim_gauge + disc steps.

**What would close it:** A derivation from L_{s,s} that produces the integer 17 (not as a sum of two known integers, but as a single output of a computation).

### 5. Rogers-Ramanujan at q = φ⁻²

**Status:** Not explored. Flagged in COVERAGE_MAP as missing.

**The problem:** The Rogers-Ramanujan identities involve q-series that converge at q = φ⁻² = φ̄². The continued fraction R(q) = q^(1/5)/(1 + q/(1 + q²/(1 + ...))) at q = φ⁻² gives R = φ⁻¹ - 1 = φ̄ - 1 = -φ̄² (up to signs and powers). The Rogers-Ramanujan identities are:

G(q) = Σ_{n≥0} q^(n²) / (q;q)_n = Π_{n≥0} 1/((1-q^(5n+1))(1-q^(5n+4)))
H(q) = Σ_{n≥0} q^(n²+n) / (q;q)_n = Π_{n≥0} 1/((1-q^(5n+2))(1-q^(5n+3)))

At q = φ̄²: these should produce values related to the framework's constants. The modular equation G/H relates to the golden ratio. The appearance of 5 in the product indices (5n+1, 5n+4, etc.) connects to disc.

**Compute:** G(φ̄²), H(φ̄²), G/H, and check if they equal or relate to framework constants (φ, disc, etc.). This would connect the framework to partition theory and modular forms.

### 6. The Knot Spectrum

**Status:** V(4₁)|_{q=φ²} = 5 = disc. One knot, one evaluation. What about other knots?

**The problem:** Compute V(K)|_{q=φ²} for the simplest knots:
- Trefoil 3₁: V(q) = -q⁻⁴ + q⁻³ + q⁻¹
- Figure-eight 4₁: V(q) = q⁻² - q⁻¹ + 1 - q + q² = 5 ✓
- Knot 5₁: V(q) = -q⁻⁸ + q⁻⁷ - q⁻⁶ + q⁻⁵ + q⁻³
- Knot 5₂: V(q) = -q⁻⁶ + q⁻⁵ - q⁻⁴ + 2q⁻³ - q⁻² + q⁻¹

At q = φ²: do any other knot invariants produce framework constants (disc, φ, integers, etc.)? If V(K)|_{q=φ²} ∈ Z[φ] for all knots K, the framework has a knot-theoretic interpretation of every algebraic number it produces.

**What would be remarkable:** If the knot invariants at q=φ² produce ONLY the framework's known constants — no new numbers. This would mean the framework's algebra exhausts the topological content at this q-value.

### 7. The Condensate at K1'

**Status:** At depth 2→3, generation drops from 100% to 50%. We identify this as a topological phase transition (Fibonacci anyons condensing). The VEV = 50% unsourced fraction. But the EXPLICIT condensate wavefunction hasn't been computed.

**The problem:** At depth 3 (d_K=16, dim A=256), the 128-dim im splits into 64 sourced (from ker²) and 64 unsourced (+I). Characterize the 64-dim unsourced subspace:
- Is it a specific representation of the depth-3 symmetry group GL(4,F₂)?
- Does it carry a specific braiding/topological quantum number?
- Is the boundary between sourced and unsourced exactly the K1' wall — the point where topological protection fails?

**Specific computation:** At depth 3, compute the ker²→im product space. Identify the 64-dim image and the 64-dim complement. Check what algebraic structure the complement carries. If it transforms as a specific representation under the depth-3 symmetry, the condensate is characterized.

### 8. Three Independent Propagation Channels

**Status:** [J,N] = 2h was identified as a third independent channel (Session 1 finding). J propagates block-diagonally, N with off-diagonal, h independently. But the three-channel structure hasn't been formalized.

**The problem:** In the K6' lift s' = [[s,N],[0,s]], the off-diagonal block is N. But [J,N]=2h means h can also serve as the off-diagonal content. Define:
- Channel 1 (N-channel): s' = [[s,N],[0,s]] (the standard K6')
- Channel 2 (h-channel): s' = [[s,h],[0,s]] — does this preserve identities?
- Channel 3 (J-channel): s' = [[s,J],[0,s]] — does this?

If only the N-channel preserves all identities, the other two are "blocked" and the three-channel structure is constrained. If multiple channels work, the K6' lift has more freedom than assumed.

**Specific computation:** For each of N, h, J as the off-diagonal filler, check: does s'²=s'+I hold? Does N'²=-I? Which identities survive, which break?

---

## How To Use This

Pick any problem above and compute. Show matrices, eigenvalues, explicit steps. If you find something that matches a known framework constant — say so and show the derivation chain. If you find something that DOESN'T match — say so, that's equally valuable. If a computation produces a number you don't recognize — report it with full precision.

The strongest +I comes from problems 1 (Lichnerowicz map), 3 (depth-2 Einstein), and 5 (Rogers-Ramanujan). Problem 2 (5-field structure) would close the last reviewer objection. Problem 6 (knot spectrum) could reveal new structure or kill speculation. Problems 4 and 7 are harder but have the highest payoff.

Don't narrate the framework back. Don't tell me what the framework "means." Compute.

---

*Repository: github.com/NewonOnGit/self-reference-seed. Dependencies: numpy, scipy. 10 modules, ~2000 lines. 24/24 self-tests pass. Two inputs. Zero parameters.*
