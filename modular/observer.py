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

    def compare(self, X, Y, tol=1e-10):
        """Are X and Y equivalent mod ker? The observer cannot distinguish them.
        Returns (equivalent, distance, diff).
        equivalent: bool — True if X ≡ Y mod ker
        distance: float — how different they look (im-component norm of X-Y)
        diff: matrix — what the observer sees as the difference
        FRAMEWORK_REF: cognitive primitive — distinction applied to pairs"""
        if self.frame is None:
            self.observe()
        rep, res = self.quotient(X - Y)
        dist = float(np.linalg.norm(rep))
        return dist < tol, dist, rep

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

    def multiplication_table(self):
        """ker × ker → im product table. How the void generates the world.
        Returns dict with 'table' (products), 'all_in_im' (bool), 'im_basis_names'.
        FRAMEWORK_REF: Thm 8.2, cognitive primitive — logic from void structure"""
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        ker_basis = f["ker_basis"]
        d = f["d_K"]
        I_d = np.eye(d)
        n = len(ker_basis)
        if n == 0:
            return {"table": {}, "all_in_im": True, "im_basis_names": []}

        # im basis for coefficient extraction
        R_tl = f["R_tl"]
        im_elements = [I_d, R_tl]
        im_mat = np.column_stack([e.flatten() for e in im_elements])

        table = {}
        all_in_im = True
        for i in range(n):
            for j in range(n):
                prod = ker_basis[i] @ ker_basis[j]
                rep, res = self.observer.quotient(prod)
                in_im = np.linalg.norm(res) < 1e-10
                if not in_im:
                    all_in_im = False
                # identify in im basis
                if in_im and im_mat.shape[1] > 0:
                    coeffs = np.linalg.lstsq(im_mat, prod.flatten(), rcond=None)[0]
                    coeffs = np.round(coeffs, 10)
                else:
                    coeffs = None
                table[(i, j)] = {
                    "product": prod,
                    "in_im": in_im,
                    "im_coeffs": {"I": float(coeffs[0]), "R_tl": float(coeffs[1])}
                    if coeffs is not None else None,
                }
        return {"table": table, "all_in_im": all_in_im,
                "im_basis_names": ["I", "R_tl"]}

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

    def invert(self, target, tol=1e-8):
        """Given target T, find X such that L_{s,s}(X) = T. Abduction.
        Returns (X_particular, solvable, residual_norm).
        X + any ker element is also a solution — the answer is an equivalence class.
        FRAMEWORK_REF: cognitive primitive — abduction (given effect, find cause)"""
        if self.observer.frame is None:
            self.observer.observe()
        from algebra import sylvester as _syl
        L = _syl(self.observer.state)
        d = self.observer.frame["d_K"]
        t_vec = target.flatten()
        x_vec, residuals, _, _ = np.linalg.lstsq(L, t_vec, rcond=None)
        X = x_vec.reshape(d, d)
        res_norm = float(np.linalg.norm(L @ x_vec - t_vec))
        return X, res_norm < tol, res_norm

    def __repr__(self):
        if self.observer.frame is None:
            return "Image(unobserved)"
        f = self.observer.frame
        dim_im = f["dim_A"] - f["ker_dim"]
        return f"Image(dim={dim_im}/{f['dim_A']}, fraction={dim_im/f['dim_A']:.3f})"


# ============================================================
# COMPRESSED RETURN (the Boundary Theorem)
# ============================================================

class CompressedReturn:
    """The compressed Sylvester return map and its fiber structure.

    Phi(X) = (tr(L_R(X)), det(L_R(X)), tr(L_N(X)), det(L_N(X)))

    Full paired return is separating. Compressed return has generic
    fiber size 4 (Bezout: 1*2*1*2). Two bits lost:
      epsilon = sign of I-coefficient (scalar sign)
      sigma   = b-root choice (center-Cartan balance)

    The disc = 5 runs through every equation.

    FRAMEWORK_REF: Thm 8.5 (Compressed Return Boundary Theorem)
    GRID: B(5, P3)
    APEX_LINK: I2*TDL*LoMI=Dist (compression IS observation with loss)
    """

    def __init__(self, observer):
        self.observer = observer
        if observer.frame is None:
            observer.observe()
        self._s = observer.frame["state"]
        self._N = observer.frame["N"]
        self._J = observer.frame["J"]
        self._d = observer.frame["d_K"]
        # Framework basis (depth 0 only for now)
        if self._d == 2:
            I2 = np.eye(2)
            R_tl = self._s - 0.5 * I2
            h = self._J @ self._N
            self._basis = [I2, R_tl, self._N, h]
            self._basis_mat = np.column_stack([m.flatten() for m in self._basis])

    def signature(self, X):
        """Compressed return: (tr(L_R(X)), det(L_R(X)), tr(L_N(X)), det(L_N(X)))."""
        s, N_obs = self._s, self._N
        lr = s @ X + X @ s - X
        ln = N_obs @ X + X @ N_obs - X
        return np.array([np.trace(lr), np.linalg.det(lr),
                         np.trace(ln), np.linalg.det(ln)])

    def decompose(self, X):
        """X -> (a, b, c, d) in {I, R_tl, N, h} basis."""
        return np.linalg.solve(self._basis_mat, X.flatten())

    def recompose(self, a, b, c, d):
        """(a, b, c, d) -> X."""
        return a * self._basis[0] + b * self._basis[1] + \
               c * self._basis[2] + d * self._basis[3]

    def fiber(self, X):
        """Exact fiber of the compressed return through X.
        Returns list of matrices sharing the same compressed signature.
        FRAMEWORK_REF: Thm 8.5"""
        if self._d != 2:
            raise NotImplementedError("Exact fiber only at depth 0 (d=2)")
        sig = self.signature(X)
        s1, s2, s3, s4 = sig

        # Bit 1: a^2 = disc(L_R(X)) / 20
        a_sq = (s1**2 - 4 * s2) / 20.0
        if a_sq < -1e-12:
            return []
        a_vals = [0.0] if a_sq < 1e-12 else [np.sqrt(a_sq), -np.sqrt(a_sq)]

        solutions = []
        for a in a_vals:
            # Bit 2: 5b^2 - 2*s1*b + Q(a) = 0
            Q = s4 - 5*a**2 - 5*(2*a + s3)**2/16.0 + s1**2/4.0
            disc_b = 4*s1**2 - 20*Q
            if disc_b < -1e-12:
                continue
            elif disc_b < 1e-12:
                b_vals = [s1 / 5.0]
            else:
                sq = np.sqrt(disc_b)
                b_vals = [(2*s1 + sq) / 10.0, (2*s1 - sq) / 10.0]

            for b in b_vals:
                c = -(2*a + s3) / 4.0
                d = (5*b - s1) / 2.0
                solutions.append(self.recompose(a, b, c, d))

        return solutions

    def fiber_size(self, X):
        """Number of states sharing the same compressed signature."""
        return len(self.fiber(X))

    def bits(self, X):
        """Identify the two hidden bits for X.
        Returns (epsilon, sigma, a_value, b_value).
        epsilon = sign of I-coefficient (+1 or -1)
        sigma   = which b-root (index 0 or 1)"""
        coeffs = self.decompose(X)
        a = coeffs[0]
        epsilon = 1 if a >= 0 else -1
        sig = self.signature(X)
        b_center = sig[0] / 5.0
        sigma = 0 if coeffs[1] >= b_center else 1
        return epsilon, sigma, float(a), float(coeffs[1])

    def discriminant_split(self, X):
        """Delta_b(+a) - Delta_b(-a) = 50*a*sig_3. Cross-projection quantity.
        Returns (split, a_val, sig_3_val)."""
        coeffs = self.decompose(X)
        a = coeffs[0]
        sig = self.signature(X)
        s3 = sig[2]
        return 50 * abs(a) * s3, abs(a), s3

    def __repr__(self):
        return f"CompressedReturn(d={self._d}, generic_fiber=4, bits=2)"


# ============================================================
# COLLAPSE OPERATOR
# ============================================================

class CollapseOperator:
    """The collapse M → P as explicit projectors on ker(L_M).

    Parent M = diag(P, Pᵀ) has ker(L_M) = 8, decomposing into:
      A-sector (child): dim 2 → ker(L_P)
      D-sector (mirror): dim 2 → ker(L_Pᵀ)
      B+C cross-sectors: dim 4 → entanglement, destroyed by collapse

    chi = branch selection (projects onto A-sector)
    rho = mirror (projects onto D-sector)
    Q   = quenching (kills cross-sectors)

    chi + rho = Q. chi·rho = 0. chi²=chi. rho²=rho. Q²=Q.
    Two bits lost: 1 for quenching (8→4), 1 for selection (4→2).

    FRAMEWORK_REF: Thm 0b.5 (Collapse by quotient)
    """

    def __init__(self):
        from algebra import sylvester as _syl
        from scipy.linalg import null_space

        P = np.array([[0,0],[2,1]], dtype=float)
        Z = np.zeros((2, 2))
        M = np.block([[P, Z], [Z, P.T]])

        L_M = _syl(M)
        ker_M = null_space(L_M, rcond=1e-10)
        self.ker_dim = ker_M.shape[1]  # should be 8

        # Classify kernel vectors by sector
        d = 2
        A_vecs, D_vecs, cross_vecs = [], [], []
        for i in range(self.ker_dim):
            K = ker_M[:, i].reshape(4, 4)
            A_block = K[:d, :d]
            D_block = K[d:, d:]
            B_block = K[:d, d:]
            C_block = K[d:, :d]
            a_norm = np.linalg.norm(A_block)
            d_norm = np.linalg.norm(D_block)
            cross_norm = np.linalg.norm(B_block) + np.linalg.norm(C_block)
            if cross_norm < 1e-8:
                if a_norm > 1e-8 and d_norm < 1e-8:
                    A_vecs.append(ker_M[:, i])
                elif d_norm > 1e-8 and a_norm < 1e-8:
                    D_vecs.append(ker_M[:, i])
                else:
                    # Both nonzero diagonal — split
                    A_vecs.append(ker_M[:, i])
            else:
                cross_vecs.append(ker_M[:, i])

        # Build projectors in kernel basis
        all_vecs = np.column_stack(A_vecs + D_vecs + cross_vecs) if (A_vecs + D_vecs + cross_vecs) else ker_M
        n_A = len(A_vecs)
        n_D = len(D_vecs)

        # Orthonormal kernel basis
        Q_full, _ = np.linalg.qr(ker_M)
        Q_A = np.column_stack(A_vecs) if A_vecs else np.zeros((16, 0))
        Q_D = np.column_stack(D_vecs) if D_vecs else np.zeros((16, 0))

        if Q_A.shape[1] > 0:
            Q_A, _ = np.linalg.qr(Q_A)
        if Q_D.shape[1] > 0:
            Q_D, _ = np.linalg.qr(Q_D)

        # Projectors (in the full 16-dim space)
        self.chi_proj = Q_A @ Q_A.T if Q_A.shape[1] > 0 else np.zeros((16, 16))
        self.rho_proj = Q_D @ Q_D.T if Q_D.shape[1] > 0 else np.zeros((16, 16))
        self.Q_proj = self.chi_proj + self.rho_proj

        self.A_dim = n_A
        self.D_dim = n_D
        self.cross_dim = len(cross_vecs)
        self.entropy_bits = np.log2(self.ker_dim) - np.log2(max(n_A, 1))

    def chi(self, v):
        """Child selection: project onto A-sector."""
        return self.chi_proj @ v

    def rho(self, v):
        """Mirror: project onto D-sector."""
        return self.rho_proj @ v

    def quench(self, v):
        """Kill cross-sectors: project onto diagonal."""
        return self.Q_proj @ v

    def verify(self):
        """Check all operator identities."""
        I = np.eye(16)
        chi, rho, Q = self.chi_proj, self.rho_proj, self.Q_proj
        return {
            "chi^2=chi": np.allclose(chi @ chi, chi),
            "rho^2=rho": np.allclose(rho @ rho, rho),
            "Q^2=Q": np.allclose(Q @ Q, Q),
            "chi+rho=Q": np.allclose(chi + rho, Q),
            "chi*rho=0": np.allclose(chi @ rho, 0),
            "rho*chi=0": np.allclose(rho @ chi, 0),
            "A_dim": self.A_dim,
            "D_dim": self.D_dim,
            "cross_dim": self.cross_dim,
            "entropy_bits": self.entropy_bits,
        }

    def __repr__(self):
        return f"CollapseOperator(ker={self.ker_dim}, A={self.A_dim}, D={self.D_dim}, cross={self.cross_dim})"


# ============================================================
# SPECTRAL PROJECTORS (R eigenspace decomposition)
# ============================================================

def spectral_projectors(R):
    """R eigenspace projectors: chi (phi-eigenspace), rho ((-phi_bar)-eigenspace).
    chi = (R + phi_bar*I) / sqrt(disc). rho = (phi*I - R) / sqrt(disc).
    chi^2=chi, rho^2=rho, chi*rho=0, chi+rho=I. chi*R=phi*chi, rho*R=-phi_bar*rho.
    FRAMEWORK_REF: SPEC-10 (collapse projectors)"""
    d = R.shape[0]
    I_d = np.eye(d)
    phi = (1 + np.sqrt(5)) / 2
    phi_bar = phi - 1
    disc = 5.0
    chi = (R + phi_bar * I_d) / np.sqrt(disc)
    rho = (phi * I_d - R) / np.sqrt(disc)
    return chi, rho


# ============================================================
# CYM PERCEPTION (second observer channel)
# ============================================================

class CYM:
    """CYM field decomposition: perception through cyclotomic channels.
    C (Cyan) -> Q(zeta_6) disc=-3. M (Magenta) -> Q(zeta_10) disc=5.
    Y (Yellow) -> Q(sqrt(-15)) disc=-15 (cross-field, h=2).
    FRAMEWORK_REF: Thm 4.4, SPEC-03"""

    MU_PARADOX = (np.sqrt(5) - 1) / 2  # phi^{-1}
    MU_LENS = np.sqrt(3) / 2
    MU_UNITY = 1.0

    @staticmethod
    def from_rgb(r_mean, g_mean, b_mean):
        """RGB means (0-255) -> normalized CYM triple (sum=1)."""
        c_raw = 1.0 - (r_mean / 255.0)
        y_raw = 1.0 - (b_mean / 255.0)
        m_raw = 1.0 - (g_mean / 255.0)
        total = c_raw + y_raw + m_raw
        if total > 0:
            return {'C': c_raw/total, 'Y': y_raw/total, 'M': m_raw/total}
        return {'C': 1/3, 'Y': 1/3, 'M': 1/3}

    @staticmethod
    def from_pixels(pixels):
        """Numpy pixel array (H,W,3) -> CYM triple."""
        return CYM.from_rgb(float(np.mean(pixels[:,:,0])),
                            float(np.mean(pixels[:,:,1])),
                            float(np.mean(pixels[:,:,2])))

    @staticmethod
    def from_coupling(mu):
        """Coupling mu -> CYM triple (internal state model)."""
        if mu < CYM.MU_PARADOX:
            t_holo, info_cap = 1.0, 0.0
        elif mu < CYM.MU_LENS:
            t = (mu - CYM.MU_PARADOX) / (CYM.MU_LENS - CYM.MU_PARADOX)
            t_holo, info_cap = 1.0 - 0.5*t, 0.3*t
        elif mu < CYM.MU_UNITY:
            t = (mu - CYM.MU_LENS) / (CYM.MU_UNITY - CYM.MU_LENS)
            t_holo, info_cap = 0.5*(1.0-t), 0.3 + 0.7*t
        else:
            t_holo, info_cap = 0.0, 1.0
        c = max(0, min(1, t_holo * info_cap))
        m = max(0, min(1, (1-t_holo) * (1-info_cap*0.5)))
        return {'C': c, 'Y': max(0, min(1, 1-c-m)), 'M': m}

    @staticmethod
    def dominant(cym):
        return max(cym, key=cym.get)

    @staticmethod
    def phase(mu):
        if mu < CYM.MU_PARADOX: return 'SUB_CRITICAL'
        elif mu < CYM.MU_LENS: return 'PARADOX'
        elif mu < CYM.MU_UNITY: return 'LENS'
        else: return 'UNITY'

    @staticmethod
    def hellinger(p, q):
        """Hellinger distance between two CYM dicts. Range [0,1]. d_H=0 is closure."""
        s = sum((np.sqrt(max(p[k],0)) - np.sqrt(max(q[k],0)))**2 for k in ['C','Y','M'])
        return float(np.sqrt(s) / np.sqrt(2))
