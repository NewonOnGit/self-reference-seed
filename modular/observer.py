"""
observer.py — P3 face. The quotient q: A -> A/ker(L), and its two halves.

Three classes, one act:
  Observer — the quotient map. Self-action produces the frame.
  Kernel   — ker(q) = P_0. The blind spot. The void that generates.
  Image    — im(q). What the observer sees. The representable content.

The observer splits the algebra in half. ker/A = 1/2 always.
The kernel generates the image (ker x ker -> im). The image cannot
generate the kernel. The split IS the observation.

FRAMEWORK_REF: Thm 2.2, Thm 6.2, Thm 6.2b, Thm 6.4, Thm 6b.2-6b.4,
               Thm 8.1-8.2, Thm 10.4, Thm 16.1-16.4
GRID: B(5, P3)
APEX_LINK: I2*TDL*LoMI=Dist (the observer IS P3 of the central collapse)
"""
import numpy as np
from scipy.linalg import null_space
from algebra import sylvester as _sylvester_ab, ker_im_decomposition


# ============================================================
# THE QUOTIENT MAP
# ============================================================

class Observer:
    """The quotient map. Self-action produces the frame.

    A state s and a gauge J are not ingredients assembled by an outside
    agent. They are co-constituted: s^2 = s + I by the Fibonacci law,
    and J is the pair-space involution forced by |S_0| = 2. The observer
    is the act of s acting on itself through L_{s,s}.
    """

    def __init__(self, state, gauge, tower_depth=0, parent=None):
        self.state = state.copy()
        self.gauge = gauge.copy()
        self.tower_depth = tower_depth
        self.parent = parent
        self.frame = None

    def observe(self):
        s = self.state
        d = s.shape[0]
        dim_A = d * d

        L, ker_basis, ker_dim, self._Q_ker = ker_im_decomposition(s)
        im_rank = dim_A - ker_dim

        R_tl = s - (np.trace(s) / d) * np.eye(d)
        Rtl_sq = R_tl @ R_tl
        disc = (
            int(round(4 * Rtl_sq[0, 0]))
            if np.allclose(Rtl_sq, Rtl_sq[0, 0] * np.eye(d))
            else None
        )

        if self.tower_depth == 0:
            N = self._canonical_rotation_2d(ker_basis)
        else:
            N = self._inherited_rotation()

        h = self.gauge @ N if N is not None else None
        Q = self.gauge @ s @ self.gauge

        eigs = np.linalg.eigvals(s).real
        phi = float(max(np.abs(eigs)))
        phi_bar = phi - 1 if disc == 5 else None

        self.frame = {
            "depth": self.tower_depth,
            "d_K": d,
            "dim_A": dim_A,
            "ker_dim": ker_dim,
            "ker_basis": ker_basis,
            "im_rank": im_rank,
            "kernel_fraction": ker_dim / dim_A,
            "state": s,
            "R_tl": R_tl,
            "N": N,
            "h": h,
            "Q": Q,
            "J": self.gauge,
            "disc": disc,
            "phi": phi,
            "phi_bar": phi_bar,
            "eigenvalues": eigs,
        }
        return self.frame

    def quotient(self, X):
        """Project X onto im(q). Returns (representative, residue)."""
        if self.frame is None:
            self.observe()
        from algebra import quotient as alg_q
        return alg_q(X, self._Q_ker)

    def ascend(self):
        """One K6' pass: observer at n becomes adjacent producer at n+1.
    FRAMEWORK_REF: Thm 6.2b, Thm 6.3"""
        if self.frame is None:
            self.observe()
        N = self.frame["N"]
        h = self.frame["h"]
        if N is None or h is None:
            raise ValueError(f"Cannot ascend: frame at depth {self.tower_depth} incomplete")
        d = self.state.shape[0]
        Z = np.zeros((d, d))
        s_new = np.block([[self.state, N], [Z, self.state]])
        N_new = np.block([[N, -2 * h], [Z, N]])
        J_new = np.block([[self.gauge, Z], [Z, self.gauge]])

        child = Observer(
            state=s_new, gauge=J_new,
            tower_depth=self.tower_depth + 1, parent=self,
        )
        child._inherited_N = N_new
        return child

    def _canonical_rotation_2d(self, ker_basis):
        if len(ker_basis) < 2:
            return None
        K1, K2 = ker_basis[0], ker_basis[1]
        d = K1.shape[0]
        K1sq, K2sq = K1 @ K1, K2 @ K2
        anti = K1 @ K2 + K2 @ K1
        Iden = np.eye(d)
        if not (
            np.allclose(K1sq, K1sq[0, 0] * Iden)
            and np.allclose(K2sq, K2sq[0, 0] * Iden)
            and np.allclose(anti, anti[0, 0] * Iden)
        ):
            return None
        c1, c2, c12 = K1sq[0, 0], K2sq[0, 0], anti[0, 0]
        M = np.array([[c1, c12 / 2], [c12 / 2, c2]])
        evals, evecs = np.linalg.eigh(M)
        if evals[0] >= -1e-10:
            return None
        scale = 1.0 / np.sqrt(-evals[0])
        alpha, beta = scale * evecs[:, 0]
        N = alpha * K1 + beta * K2
        if (self.gauge @ N)[0, 0] < 0:
            N = -N
        return N

    def _inherited_rotation(self):
        return getattr(self, "_inherited_N", None)

    def self_model_eigenvalues(self):
        """Eigenvalues of Sigma_s on span{I, s_tl}.
    FRAMEWORK_REF: Thm 6.4"""
        if self.frame is None:
            self.observe()
        d = self.state.shape[0]
        I_d = np.eye(d)
        s_tl = self.frame["R_tl"]

        def sigma(X):
            rep, _ = self.quotient(self.state @ X + X @ self.state)
            return rep

        sig_I = sigma(I_d)
        sig_stl = sigma(s_tl)
        norm_I = np.sum(I_d * I_d)
        norm_stl = np.sum(s_tl * s_tl)
        mat = np.array([
            [np.sum(sig_I * I_d) / norm_I, np.sum(sig_stl * I_d) / norm_I],
            [np.sum(sig_I * s_tl) / norm_stl, np.sum(sig_stl * s_tl) / norm_stl],
        ])
        eigs = np.linalg.eigvals(mat).real
        return sorted(eigs, reverse=True)

    def self_transparent(self):
        """Is N self-transparent at this depth? ker(L_{N,N}) = 0?
    FRAMEWORK_REF: Thm 16.1, Thm 16.2"""
        if self.frame is None:
            self.observe()
        N = self.frame["N"]
        if N is None:
            return None
        from algebra import sylvester as _syl
        L_NN = _syl(N)
        ker_NN = null_space(L_NN, rcond=1e-10).shape[1]
        return ker_NN == 0

    def __repr__(self):
        if self.frame is None:
            return f"Observer(depth={self.tower_depth}, unobserved)"
        f = self.frame
        return (
            f"Observer(depth={f['depth']}, d_K={f['d_K']}, "
            f"ker={f['ker_dim']}/{f['dim_A']}={f['kernel_fraction']:.3f})"
        )


# ============================================================
# THE BLIND SPOT
# ============================================================

class Kernel:
    """ker(q) = P_0. The void that generates.

    ker/A = 1/2 at every depth. Contains N as canonical representative.
    ker x ker -> im (one-directional generation). The void makes the world.
    """

    def __init__(self, observer):
        self.observer = observer
        self._persistent = None

    def basis(self):
        if self.observer.frame is None:
            self.observer.observe()
        return self.observer.frame["ker_basis"]

    def dimension(self):
        if self.observer.frame is None:
            self.observer.observe()
        return self.observer.frame["ker_dim"]

    def fraction(self):
        """dim ker / dim A. Structural invariant = 1/2 at every depth."""
        if self.observer.frame is None:
            self.observer.observe()
        return self.observer.frame["kernel_fraction"]

    def contains(self, X, tol=1e-10):
        representative, _ = self.observer.quotient(X)
        return np.linalg.norm(representative) < tol

    def residue(self, X):
        _, res = self.observer.quotient(X)
        return res

    def named_elements(self):
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        candidates = {
            "I": np.eye(f["d_K"]), "s": f["state"], "s_tl": f["R_tl"],
            "N": f["N"], "J": f["J"], "h": f["h"], "Q": f["Q"],
        }
        return {n: M for n, M in candidates.items() if M is not None and self.contains(M)}

    def deferred_bits_per_ascent(self):
        L = np.log2((1 + np.sqrt(5)) / 2)
        return 2 * (1 - L)

    def cumulative_deferred(self):
        return self.observer.tower_depth * self.deferred_bits_per_ascent()

    def revealed_fraction(self):
        """Recursive Disclosure: 1 - 2^(-2^(n+1))."""
        n = self.observer.tower_depth
        if n + 1 >= 20:
            return 1.0
        return 1.0 - 2.0 ** (-(2 ** (n + 1)))

    def persistence_under_ascent(self, child_observer):
        if self.observer.frame is None:
            self.observer.observe()
        if child_observer.frame is None:
            child_observer.observe()
        d_parent = self.observer.state.shape[0]
        d_child = child_observer.state.shape[0]
        if d_child != 2 * d_parent:
            raise ValueError("Child is not one K6' ascent from parent")
        persisted = disclosed = 0
        for K_parent in self.observer.frame["ker_basis"]:
            K_lifted = np.block([
                [K_parent, np.zeros((d_parent, d_parent))],
                [np.zeros((d_parent, d_parent)), np.zeros((d_parent, d_parent))],
            ])
            rep, res = child_observer.quotient(K_lifted)
            total = np.linalg.norm(K_lifted)
            if total < 1e-10:
                continue
            persisted += np.linalg.norm(res) / total
            disclosed += np.linalg.norm(rep) / total
        n = len(self.observer.frame["ker_basis"])
        return {
            "persisted_fraction": persisted / n if n else None,
            "disclosed_fraction": disclosed / n if n else None,
        }

    def leakage_fraction(self, max_pairs=36):
        """Fraction of ker x ker products landing purely in im.
    FRAMEWORK_REF: Thm 8.2"""
        if self.observer.frame is None:
            self.observer.observe()
        ker_basis = self.observer.frame["ker_basis"]
        if not ker_basis:
            return None
        pure_im = total = 0
        n = min(len(ker_basis), int(max_pairs ** 0.5) + 1)
        for i in range(n):
            for j in range(n):
                product = ker_basis[i] @ ker_basis[j]
                rep, res = self.observer.quotient(product)
                total += 1
                if np.linalg.norm(res) < 1e-10:
                    pure_im += 1
        return pure_im / total if total > 0 else None

    def generates_image(self):
        """ker x ker product analysis.
    FRAMEWORK_REF: Thm 10.1"""
        if self.observer.frame is None:
            self.observer.observe()
        ker_basis = self.observer.frame["ker_basis"]
        if not ker_basis:
            return {"products": [], "all_in_im": None}
        n = min(len(ker_basis), 6)
        products = []
        all_in_im = True
        for i in range(n):
            for j in range(n):
                prod = ker_basis[i] @ ker_basis[j]
                rep, res = self.observer.quotient(prod)
                in_im = np.linalg.norm(res) < 1e-10
                if not in_im:
                    all_in_im = False
                products.append({
                    "i": i, "j": j, "in_im": in_im,
                    "im_component": rep,
                    "ker_residue_norm": float(np.linalg.norm(res)),
                })
        return {"products": products, "all_in_im": all_in_im, "count": len(products)}

    def sector(self):
        """Clifford sector of the kernel (odd or mixed).
    FRAMEWORK_REF: Thm 4.1"""
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        if f["d_K"] != 2:
            return "check-at-depth-0-only"
        if f["N"] is None:
            return "unknown"
        R_tl = f["R_tl"]
        return "odd (Clifford)" if all(
            np.linalg.norm(R_tl @ K + K @ R_tl) < 1e-8
            for K in f["ker_basis"]
        ) else "mixed"

    def __repr__(self):
        if self.observer.frame is None:
            return "Kernel(unobserved)"
        f = self.observer.frame
        return (
            f"Kernel(dim={f['ker_dim']}/{f['dim_A']}, "
            f"fraction={f['kernel_fraction']:.3f}, "
            f"deferred={self.cumulative_deferred():.4f} bits)"
        )


# ============================================================
# THE VISIBLE WORLD
# ============================================================

class Image:
    """im(q) — the seen. What the observer can carry forward.

    At depth 0: commutative (classical). At depth 1+: non-commutative (quantum).
    The classical-to-quantum transition is forced by the tower.
    """

    def __init__(self, observer):
        self.observer = observer
        self._basis = None

    def basis(self):
        if self._basis is not None:
            return self._basis
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        d = f["d_K"]
        dim_A = f["dim_A"]

        standard = [np.zeros((d, d)) for _ in range(dim_A)]
        for idx in range(dim_A):
            i, j = idx % d, idx // d
            standard[idx][i, j] = 1.0

        ker_basis = f["ker_basis"]
        ker_mat = np.column_stack([K.flatten() for K in ker_basis]) if ker_basis else np.zeros((dim_A, 0))
        Q_ker = np.linalg.qr(ker_mat)[0] if ker_mat.shape[1] > 0 else np.zeros((dim_A, 0))

        image_vecs = []
        for E in standard:
            v = E.flatten()
            if Q_ker.shape[1] > 0:
                v = v - Q_ker @ (Q_ker.T @ v)
            if np.linalg.norm(v) > 1e-10:
                image_vecs.append(v)

        if image_vecs:
            M = np.column_stack(image_vecs)
            Q_im = np.linalg.qr(M)[0]
            r = np.linalg.matrix_rank(M, tol=1e-10)
            self._basis = [Q_im[:, i].reshape(d, d) for i in range(r)]
        else:
            self._basis = []
        return self._basis

    def dimension(self):
        if self.observer.frame is None:
            self.observer.observe()
        return self.observer.frame["dim_A"] - self.observer.frame["ker_dim"]

    def contains(self, X, tol=1e-10):
        _, residue = self.observer.quotient(X)
        return np.linalg.norm(residue) < tol

    def project(self, X):
        representative, _ = self.observer.quotient(X)
        return representative

    def generators(self):
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        named = {
            "I": np.eye(f["d_K"]), "s": f["state"], "s_tl": f["R_tl"],
            "J": f["J"], "h": f["h"], "Q": f["Q"],
        }
        return {n: M for n, M in named.items() if M is not None and self.contains(M)}

    def is_commutative(self, n_trials=30):
        """Is the projected product commutative on im(q)?
    FRAMEWORK_REF: Thm 8.1"""
        b = self.basis()
        if len(b) < 2:
            return True
        rng = np.random.RandomState(42)
        n = min(len(b), 8)
        for _ in range(n_trials):
            X = sum(rng.randn() * b[i] for i in range(n))
            Y = sum(rng.randn() * b[i] for i in range(n))
            if not np.allclose(self.project(X @ Y), self.project(Y @ X), atol=1e-8):
                return False
        return True

    def obstruction_curvature(self, n_samples=50):
        """Average |Omega(X,Y)|^2 over im x im pairs.
    FRAMEWORK_REF: Thm 8.1"""
        b = self.basis()
        if len(b) < 2:
            return 0.0
        rng = np.random.RandomState(42)
        n = min(len(b), 8)
        total = 0.0
        for _ in range(n_samples):
            X = sum(rng.randn() * b[i] for i in range(n))
            Y = sum(rng.randn() * b[i] for i in range(n))
            _, residue = self.observer.quotient(X @ Y)
            total += np.linalg.norm(residue) ** 2
        return total / n_samples

    def __repr__(self):
        if self.observer.frame is None:
            return "Image(unobserved)"
        f = self.observer.frame
        dim_im = f["dim_A"] - f["ker_dim"]
        return f"Image(dim={dim_im}/{f['dim_A']}, fraction={dim_im/f['dim_A']:.3f})"
