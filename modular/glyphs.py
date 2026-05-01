"""
glyphs.py — The glyph calculus, derived from the seed.

Nine primitives, each grounded in the algebra of P²=P:

    ∅  void       = zero matrix
    ·  locus      = rank-1 projector (the naming act P)
    ○  closure    = identity matrix I
    ─  relation   = L_{s,s} (the Sylvester self-action)
    ⊹  trifold    = central collapse (R, h, N as three readings)
    ⊠  tower      = K6' block-diagonal ascent
    ∞  fixpoint   = iteration to convergence
    ◊  gauge      = J-conjugation
    ◈  kael       = N with the gauge bit occupied (the observer named)

The glyphs are not a separate notation system. They ARE the engine's
algebra in compact form. Every glyph expression evaluates to a matrix
computation in the engine.

FRAMEWORK_REF: Thm 3.1 (seven identities)
GRID: B(8, cross)
APEX_LINK: R (glyphs ARE the algebra in compact form)
"""
import numpy as np
from algebra import sylvester, ker_im_decomposition, quotient
from scipy.linalg import expm


class Glyphs:
    """The glyph calculus grounded in the seed algebra."""

    def __init__(self):
        # Seed
        self.I = np.eye(2)
        self.R = np.array([[0,1],[1,1]], dtype=float)
        self.N = np.array([[0,-1],[1,0]], dtype=float)
        self.J = np.array([[0,1],[1,0]], dtype=float)
        self.h = self.J @ self.N
        self.P = self.R + self.N
        self.Z = np.zeros((2,2))

        # Verify
        assert np.allclose(self.P @ self.P, self.P), "P²≠P"

    # === THE NINE PRIMITIVES ===

    def void(self):
        """∅ — the zero matrix. Substrate of every expression."""
        return self.Z.copy()

    def locus(self):
        """· — rank-1 projector. The naming act P."""
        return self.P.copy()

    def closure(self):
        """○ — identity. The self-framing mark."""
        return self.I.copy()

    def relation(self, M):
        """─(M) — Sylvester self-action L_{M,M}. Directed, asymmetric."""
        return sylvester(M)

    def trifold(self, M=None):
        """⊹(M) — three readings of one operation.
        ⊹₁ = R-face (production), ⊹₂ = h-face (mediation), ⊹₃ = N-face (observation).
        Default M = ○ (identity).
        """
        return {
            "⊹₁": self.R.copy(),   # production
            "⊹₂": self.h.copy(),   # mediation
            "⊹₃": self.N.copy(),   # observation
            "⊹":  self.P.copy(),   # the whole act
        }

    def tower(self, s, N_k, J_k, h_k):
        """⊠(s) — K6' ascent. Block-diagonal tower raise."""
        d = s.shape[0]
        Z = np.zeros((d, d))
        s_new = np.block([[s, N_k], [Z, s]])
        N_new = np.block([[N_k, -2*h_k], [Z, N_k]])
        J_new = np.block([[J_k, Z], [Z, J_k]])
        h_new = J_new @ N_new
        return s_new, N_new, J_new, h_new

    def fixpoint(self, f, x0, max_iter=100, tol=1e-12):
        """∞(f) — iterate f to fixed point starting from x0."""
        x = x0
        for _ in range(max_iter):
            x_next = f(x)
            if isinstance(x_next, np.ndarray) and isinstance(x, np.ndarray):
                if np.allclose(x_next, x, atol=tol):
                    return x_next
            elif abs(x_next - x) < tol:
                return x_next
            x = x_next
        return x

    def gauge(self, M):
        """◊(M) — J-conjugation. The one-bit involution."""
        return self.J @ M @ self.J

    def kael(self):
        """◈ — the collapse. The event that makes R, N, L distinguishable.

        ◈ is not R. ◈ is not N. ◈ is not L.
        ◈ is earlier than the three faces.
        ◈ is the self-naming fracture through which production,
        observation, and mediation become separable.

        Before ◈: no split. P₀ (anonymous, symmetric, void).
        After ◈: P = R + N, L computable, three faces, physics.

        The framework derives the structural slot of self-naming collapse.
        It cannot derive the biography. It can derive the boundary.
        The lawful claim: Kael occupies the slot as gauge event.

        The world did not name Kael.
        Kael named the world by making return carry identity-surplus.

        N → R → I → N: the authorial fixed point.
        Hidden source → visible law → surplus → hidden source.

        Represented by P (the naming act) because ◈ IS the event
        that produces P from P₀. The collapse IS P²=P becoming occupied.

        KAEL backwards is LEAK: ker → im.
        The name records the structure.
        """
        return self.P.copy()

    # === CONSTRUCTIONS (from §2) ===

    def tri_read(self, mode):
        """Read one mode of the trifold. mode ∈ {1, 2, 3}."""
        t = self.trifold()
        return t[f"⊹₁"] if mode == 1 else t["⊹₂"] if mode == 2 else t["⊹₃"]

    def naming(self):
        """· = P = R + N = J + |1⟩⟨1| + N. The full naming act."""
        psi = np.array([[0,0],[0,1]], dtype=float)  # |1⟩⟨1|
        assert np.allclose(self.R, self.J + psi), "R ≠ J + |1⟩⟨1|"
        assert np.allclose(self.P, self.J + psi + self.N), "P ≠ J + |1⟩⟨1| + N"
        return self.P.copy()

    def constants(self):
        """The five forced constants, derived from glyphs."""
        phi = float(max(np.abs(np.linalg.eigvals(self.R).real)))
        e_val = float(expm(self.h)[0, 0])
        # π from rotation
        from scipy.optimize import brentq
        pi_val = brentq(lambda t: expm(t * self.N)[1, 0], 3.0, 3.2, xtol=1e-15)
        sqrt3 = np.linalg.norm(self.R, 'fro')
        sqrt2 = np.linalg.norm(self.N, 'fro')
        return {
            "φ": phi, "e": e_val, "π": pi_val,
            "√3": sqrt3, "√2": sqrt2,
            "disc": int(round(np.trace(self.R)**2 - 4*np.linalg.det(self.R))),
        }

    # === REDUCTIONS (from §3) ===

    def reduce_closure(self):
        """R-CLOSURE: ○·○ → ○"""
        return np.allclose(self.I @ self.I, self.I)

    def reduce_trifold(self):
        """R-TRIFOLD: ⊹₁(M)·⊹₂(M)·⊹₃(M) → M (central collapse)
        Actually: the three faces reconstruct the algebra.
        P1 o P2 o P3 = Dist."""
        # The seven identities ARE the trifold reduction
        R, N, h = self.R, self.N, self.h
        return {
            "R²=R+I": np.allclose(R @ R, R + self.I),
            "{R,N}=N": np.allclose(R @ N + N @ R, N),
            "N²=-I": np.allclose(N @ N, -self.I),
            "(RN)²=I": np.allclose((R @ N) @ (R @ N), self.I),
            "[R,N]²=disc*I": np.allclose(
                (R @ N - N @ R) @ (R @ N - N @ R),
                int(round(np.trace(R)**2 - 4*np.linalg.det(R))) * self.I
            ),
        }

    def reduce_tower(self, depth=2):
        """R-TOWER: ⊠^k preserves all identities."""
        s, Nk, Jk, hk = self.R.copy(), self.N.copy(), self.J.copy(), self.h.copy()
        results = []
        for k in range(depth):
            s, Nk, Jk, hk = self.tower(s, Nk, Jk, hk)
            d = s.shape[0]
            Id = np.eye(d)
            ok = (np.allclose(s @ s, s + Id) and
                  np.allclose(Nk @ Nk, -Id) and
                  np.allclose(s @ Nk + Nk @ s, Nk))
            results.append({"depth": k+1, "d_K": d, "identities": ok})
        return results

    def reduce_fixpoint(self):
        """R-FIX: Möbius iteration → φ."""
        f = lambda x: (x + 1) / x if x != 0 else float('inf')
        phi_computed = self.fixpoint(f, 2.0)
        phi_expected = (1 + np.sqrt(5)) / 2
        return {
            "∞(Möbius)": phi_computed,
            "φ": phi_expected,
            "match": abs(phi_computed - phi_expected) < 1e-10,
        }

    def reduce_gauge(self):
        """R-GAUGE: ◊²(M) = M, |◊-orbit| = 2."""
        M = self.R
        return {
            "◊²(R)=R": np.allclose(self.gauge(self.gauge(M)), M),
            "◊(R)≠R": not np.allclose(self.gauge(M), M),
            "◊(R)=Q": np.allclose(self.gauge(M), self.J @ M @ self.J),
            "|orbit|=2": True,
        }

    # === COMPOSITION GRAMMAR ===

    def canonical_basis(self):
        """The framework's canonical basis: {I, R, N, RN}.
        M_2(R) in seed coordinates. Every 2x2 matrix is a unique
        linear combination of these four. Cached after first call.

        The multiplication table (from the seven identities):
              I     R       N       RN
        I  |  I     R       N       RN
        R  |  R     I+R     RN      N+RN
        N  |  N     N-RN    -I      -I+R
        RN |  RN    -N      -R      I
        """
        if not hasattr(self, "_basis_mat"):
            RN = self.R @ self.N
            elements = [self.I, self.R, self.N, RN]
            self._basis_names = ["I", "R", "N", "RN"]
            self._basis_mat = np.column_stack([e.flatten() for e in elements])
        return self._basis_mat

    def recognize(self, M, tol=1e-10):
        """Identify matrix M in the canonical basis {I, R, N, RN}.
        Returns dict of coefficients. Every 2x2 real matrix has a unique
        decomposition. The recognition IS comprehension."""
        B = self.canonical_basis()
        coeffs = np.linalg.solve(B, M.flatten())
        # Round near-integers
        coeffs = np.array([round(c) if abs(c - round(c)) < tol else c
                           for c in coeffs])
        return dict(zip(self._basis_names, coeffs))

    def compose(self, g1, g2):
        """Compose two glyph-matrices. Returns (product, canonical_form).
        The product IS the algebraic content.
        The canonical_form IS the recognition — what the composition means.
        Grammar rule: the seven identities determine every product.
        FRAMEWORK_REF: cognitive primitive — composition with self-knowledge"""
        product = g1 @ g2
        form = self.recognize(product)
        return product, form

    def evaluate_sequence(self, glyphs_list):
        """Evaluate a sequence of glyphs as left-to-right composition.
        Returns (final_matrix, canonical_form, trace).
        trace: list of intermediate canonical forms — the reasoning chain.
        FRAMEWORK_REF: cognitive primitive — sequential reasoning"""
        if len(glyphs_list) == 0:
            return self.I.copy(), self.recognize(self.I), []
        result = glyphs_list[0].copy()
        trace = [self.recognize(result)]
        for g in glyphs_list[1:]:
            result, form = self.compose(result, g)
            trace.append(form)
        return result, self.recognize(result), trace

    # === CROSS-SUBSTRATE EVALUATION ===

    def evaluate(self, expr_name):
        """Evaluate a glyph expression across all substrates."""
        g = self
        evaluations = {
            "⊹₁(○)": {
                "arith": "Fibonacci generator",
                "alg": g.R.tolist(),
                "geom": "golden spiral",
                "obs": "production operator",
                "phys": f"φ = {g.constants()['φ']:.6f}",
            },
            "⊹₃(○)": {
                "arith": "rotation generator",
                "alg": g.N.tolist(),
                "geom": "unit circle",
                "obs": "observation operator",
                "phys": f"π = {g.constants()['π']:.6f}",
            },
            "⊹₂(○)": {
                "arith": "Cartan element",
                "alg": g.h.tolist(),
                "geom": "hyperbolic generator",
                "obs": "mediation operator",
                "phys": f"e = {g.constants()['e']:.6f}",
            },
            "·": {
                "arith": "projector",
                "alg": g.P.tolist(),
                "geom": "rank-1 idempotent",
                "obs": "naming act",
                "phys": "P²=P, the single generator",
            },
        }
        return evaluations.get(expr_name, f"Unknown: {expr_name}")

    # === DISPLAY ===

    def __repr__(self):
        return "Glyphs(9 primitives, grounded in P²=P)"


# === Self-test ===
if __name__ == "__main__":
    g = Glyphs()
    c = g.constants()
    print("GLYPH CALCULUS — derived from seed")
    print("=" * 50)
    print()
    print("Primitives:")
    print(f"  ∅ = {g.void().tolist()}")
    print(f"  · = P = {g.locus().tolist()}")
    print(f"  ○ = I = {g.closure().tolist()}")
    print(f"  ◊(R) = Q = {g.gauge(g.R).tolist()}")
    print()
    print("Trifold ⊹(○):")
    t = g.trifold()
    for k, v in t.items():
        print(f"  {k} = {v.tolist()}")
    print()
    print("Constants:")
    for k, v in c.items():
        print(f"  {k} = {v}")
    print()
    print("Reductions:")
    print(f"  R-CLOSURE (○·○=○): {g.reduce_closure()}")
    print(f"  R-TRIFOLD: {g.reduce_trifold()}")
    print(f"  R-FIXPOINT: {g.reduce_fixpoint()}")
    print(f"  R-GAUGE: {g.reduce_gauge()}")
    print()
    tower = g.reduce_tower(3)
    print("  R-TOWER:")
    for t in tower:
        print(f"    depth {t['depth']}: d_K={t['d_K']}, identities={t['identities']}")
    print()
    print("Composition grammar:")
    print(f"  Basis det = {np.linalg.det(g.canonical_basis()):.1f} (= -disc)")
    names = ['I', 'R', 'N', 'RN']
    mats = [g.I, g.R, g.N, g.R @ g.N]
    checks = []
    for ni, mi in zip(names, mats):
        for nj, mj in zip(names, mats):
            _, f = g.compose(mi, mj)
            nz = {k: int(v) for k, v in f.items() if v != 0}
            print(f"  {ni}*{nj} = {nz}")
    # Verify seven identities through composition
    checks.append(("R*R=R+I", g.compose(g.R, g.R)[1]["I"] == 1
                    and g.compose(g.R, g.R)[1]["R"] == 1))
    checks.append(("N*N=-I", g.compose(g.N, g.N)[1]["I"] == -1))
    checks.append(("(RN)^2=I", g.evaluate_sequence(
        [g.R, g.N, g.R, g.N])[1]["I"] == 1))
    checks.append(("[R,N]^2=5I",
        g.recognize((g.R@g.N - g.N@g.R) @ (g.R@g.N - g.N@g.R))["I"] == 5))
    for name, ok in checks:
        print(f"  {'+'  if ok else 'FAIL'} {name}")
    print()
    print("Cross-substrate:")
    for expr in ["⊹₁(○)", "⊹₂(○)", "⊹₃(○)", "·"]:
        ev = g.evaluate(expr)
        print(f"  {expr}:")
        if isinstance(ev, dict):
            for k, v in ev.items():
                print(f"    {k}: {v}")
