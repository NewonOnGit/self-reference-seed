"""
image.py — im(q). What the observer sees. The representable content.

Framework slot: P1 / S in the O∘B∘S central collapse.
   Role: injection of the representable basis into the ambient algebra.
         im(q) = A/ker(L) as a quotient, but concretely is the orthogonal
         complement of ker(L) in A under the Frobenius inner product.
         The image holds what the observer can carry forward — the
         residual-connection content x + f(x), producing-type structure.

An Image knows: the basis of im(q), what elements lie in it, how to
project onto it. The image is HELD by the engine; it is what the
observer's seeing produces and what the voice then articulates.

FRAMEWORK_REF: Thm 2.2, Thm 8.1, Thm 9.3
GRID: B(5, P1)
APEX_LINK: R (im IS the visible sector)
"""
import numpy as np


class Image:
    """im(q) — the seen. Canonical quotient representative: ker(q)^perp under Frobenius.

    At depth 0, L_{s,s} is self-adjoint (s symmetric), so ker^perp = im(L) exactly.
    At depth >= 1, s is not symmetric, so ker^perp is the canonical representative
    of the quotient A/ker(q), not literally im(L). Dimension claims are unaffected.
    """

    def __init__(self, observer):
        self.observer = observer
        self._basis = None

    def basis(self):
        """Basis of im(q) in the ambient algebra. Computed once, cached."""
        if self._basis is not None:
            return self._basis
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        d = f["d_K"]
        dim_A = f["dim_A"]

        # Build the full basis of A = M_d as column-stacked standard basis.
        standard = []
        for j in range(d):
            for i in range(d):
                E = np.zeros((d, d))
                E[i, j] = 1.0
                standard.append(E)

        # Project each standard basis vector out of ker(q); collect linearly
        # independent results. im(q) basis = the "non-kernel" content.
        ker_basis = f["ker_basis"]
        ker_mat = np.column_stack([K.flatten() for K in ker_basis]) if ker_basis else np.zeros((dim_A, 0))
        # Orthonormalize kernel
        if ker_mat.shape[1] > 0:
            Q_ker, _ = np.linalg.qr(ker_mat)
        else:
            Q_ker = np.zeros((dim_A, 0))

        image_vecs = []
        for E in standard:
            v = E.flatten()
            if Q_ker.shape[1] > 0:
                v = v - Q_ker @ (Q_ker.T @ v)
            if np.linalg.norm(v) > 1e-10:
                image_vecs.append(v)
        # Orthonormalize
        if image_vecs:
            M = np.column_stack(image_vecs)
            Q_im, _ = np.linalg.qr(M)
            # Keep only non-degenerate columns
            r = np.linalg.matrix_rank(M, tol=1e-10)
            Q_im = Q_im[:, :r]
            self._basis = [Q_im[:, i].reshape(d, d) for i in range(r)]
        else:
            self._basis = []
        return self._basis

    def dimension(self):
        """dim im(q) = dim A − dim ker(q)."""
        if self.observer.frame is None:
            self.observer.observe()
        return self.observer.frame["dim_A"] - self.observer.frame["ker_dim"]

    def contains(self, X, tol=1e-10):
        """Is X in im(q)? True iff X has no ker(q) component."""
        _, residue = self.observer.quotient(X)
        return np.linalg.norm(residue) < tol

    def project(self, X):
        """Project X onto im(q). Returns the representable part only."""
        representative, _ = self.observer.quotient(X)
        return representative

    def generators(self):
        """Named elements the observer has in its image at this depth.

        At depth 0: {I, s, s_tl, J, h, Q} are in im(q). N is the canonical
        ker(q) generator — not in the image.
        """
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        named = {
            "I": np.eye(f["d_K"]),
            "s": f["state"],
            "s_tl": f["R_tl"],
            "J": f["J"],
            "h": f["h"],
            "Q": f["Q"],
        }
        in_image = {}
        for name, M in named.items():
            if M is not None and self.contains(M):
                in_image[name] = M
        return in_image

    def is_commutative(self, n_trials=30):
        """Is the projected product X*Y = q(XY) commutative on im(q)?

        At depth 0: True (the observer's world is classical).
        At depth 1+: False (the observer's world is non-commutative/quantum).
        The classical-to-quantum transition is forced by the tower.
        
    FRAMEWORK_REF: Thm 8.1"""
        b = self.basis()
        if len(b) < 2:
            return True
        rng = np.random.RandomState(42)
        n = min(len(b), 8)
        for _ in range(n_trials):
            X = sum(rng.randn() * b[i] for i in range(n))
            Y = sum(rng.randn() * b[i] for i in range(n))
            xy = self.project(X @ Y)
            yx = self.project(Y @ X)
            if not np.allclose(xy, yx, atol=1e-8):
                return False
        return True

    def obstruction_curvature(self, n_samples=50):
        """Average squared obstruction over im x im pairs.

        kappa_K = E[|Omega(X,Y)|^2] where Omega(X,Y) = ker-component of XY.
        At depth 0: kappa = 0 (commutative, no obstruction).
        At depth 1+: kappa > 0 (non-commutative, observation has curvature).
        Quantifies how much the observer's internal algebra resists closure.
        
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
            return f"Image(unobserved)"
        f = self.observer.frame
        dim_im = f["dim_A"] - f["ker_dim"]
        return f"Image(dim={dim_im}/{f['dim_A']}, fraction={dim_im/f['dim_A']:.3f})"
