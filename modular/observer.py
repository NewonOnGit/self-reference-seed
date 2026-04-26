"""
observer.py — the quotient q: A → A/ker(L). The one that sees.

Framework slot: P3 / O in the O∘B∘S central collapse.
   Role: surjection onto im(q). The observer acts by self-action
         L_{s,s}(X) = sX + Xs − X and reads its own structure through
         ker/im decomposition. The observer IS NOT separate from what it
         sees — state s acts on itself; the quotient q IS the act.

Inputs:  state s (satisfying s² = s + I), gauge involution J (J² = I)
Outputs: frame = {ker_basis, im_rank, N, h, R_tl, Q, disc, φ, φ̄}

Primary operation: observe() — one self-observation pass.
Ascent operation: ascend() — K6' lift, observer at n becomes producer at n+1.
                  The single irreducible choice (sign of N) is the RO-2012
                  gauge bit. Everything else is structurally forced.
"""
import numpy as np
from scipy.linalg import null_space


def sylvester(A, B):
    """L_{A,B}(X) = AX + XB − X as a matrix on vec(X)."""
    d = A.shape[0]
    return np.kron(np.eye(d), A) + np.kron(B.T, np.eye(d)) - np.eye(d * d)


class Observer:
    """The quotient map. Self-action produces the frame.

    A state s and a gauge J are not ingredients assembled by an outside
    agent. They are co-constituted: s² = s + I by the Fibonacci law,
    and J is the pair-space involution forced by |S₀| = 2. The observer
    is the act of s acting on itself through L_{s,s}.
    """

    def __init__(self, state, gauge, tower_depth=0, parent=None):
        self.state = state.copy()
        self.gauge = gauge.copy()
        self.tower_depth = tower_depth
        self.parent = parent
        self.frame = None

    # --- the primitive act: observe ---

    def observe(self):
        s = self.state
        d = s.shape[0]
        dim_A = d * d

        # The observer's eye: Sylvester operator. Its kernel is ker(q);
        # its image rank is dim im(q).
        L = sylvester(s, s)
        K = null_space(L, rcond=1e-10)
        ker_dim = K.shape[1]
        ker_basis = [K[:, i].reshape(d, d) for i in range(ker_dim)]
        _, sigma, _ = np.linalg.svd(L)
        im_rank = int(np.sum(sigma > 1e-10))

        # Structural features of the observer's frame.
        # Traceless direct: L(R_tl) = (disc/2)·I (scalar channel).
        R_tl = s - (np.trace(s) / d) * np.eye(d)
        Rtl_sq = R_tl @ R_tl
        disc = (
            int(round(4 * Rtl_sq[0, 0]))
            if np.allclose(Rtl_sq, Rtl_sq[0, 0] * np.eye(d))
            else None
        )

        # N — the minimum-norm observer-rotation in the kernel.
        # At depth 0 this is the Clifford-graded solution to X² = −I.
        # At higher depths, N is inherited from the parent's ascent
        # (specifically, N_new = [[N_prev, −2h_prev], [0, N_prev]]).
        if self.tower_depth == 0:
            N = self._canonical_rotation_2d(ker_basis)
        else:
            N = self._inherited_rotation()

        h = self.gauge @ N if N is not None else None
        Q = self.gauge @ s @ self.gauge  # gauge-conjugate state

        # Fibonacci spectrum
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
        d = self.state.shape[0]
        # Residue is the ker(L) component of X; representative is X − residue.
        # Compute via orthogonal projection in the Frobenius inner product.
        residue = np.zeros_like(X)
        for K in self.frame["ker_basis"]:
            c = np.sum(X * K) / np.sum(K * K)
            residue = residue + c * K
        representative = X - residue
        return representative, residue

    # --- ascent: K6' ---

    def ascend(self):
        """One K6' pass: observer at n becomes adjacent producer at n+1.

        s' = [[s, N], [0, s]]
        N' = [[N, -2h], [0, N]]
        J' = [[J, 0], [0, J]]

        Preserves s² = s + I, N² = −I, {s, N} = N, {h, N} = 0 at every
        depth. The only irreducible choice is
        the sign of N at depth 0 (RO-2012).
        """
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

        # Child: new Observer with the lifted (state, gauge); parent link preserved.
        child = Observer(
            state=s_new,
            gauge=J_new,
            tower_depth=self.tower_depth + 1,
            parent=self,
        )
        # Pre-seed the inherited rotation into the child's frame bookkeeping
        child._inherited_N = N_new
        return child

    # --- helpers ---

    def _canonical_rotation_2d(self, ker_basis):
        """Depth-0 minimum-norm N ∈ ker(L) with N² = −I.

        The kernel at depth 0 is 2-dim with Clifford structure. Parameterize
        N = αK₁ + βK₂, then N² = (α²c₁ + αβc₁₂ + β²c₂)·I. Solve for
        minimum α² + β² with N² = −I. One gauge bit remains (sign of N,
        RO-2012) — we fix it by (J·N)[0,0] > 0.
        """
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
        # RO-2012 gauge bit
        if (self.gauge @ N)[0, 0] < 0:
            N = -N
        return N

    def _inherited_rotation(self):
        """At depth > 0, N is pre-seeded by the parent's ascend() call."""
        return getattr(self, "_inherited_N", None)

    def self_model_eigenvalues(self):
        """Eigenvalues of Sigma_s on span{I, s_tl}.

        Sigma_s(X) = q(sX + Xs) is the observer's self-action restricted
        to the observable sector. On the 2-dim subspace {I, s_tl}, its
        matrix is [[1, 5/2], [2, 1]] at every tower depth, with eigenvalues
        1 +/- sqrt(5) = {2*phi, -2*phi_bar}. The golden ratio is the
        frequency of self-observation.
        """
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
        # Project onto {I, s_tl} basis using Frobenius inner product
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

        N is the ONLY generator with no blind spot under its own
        self-action. L_{N,N} has eigenvalues {-1,-1,-1+2i,-1-2i},
        none zero. The observer sees everything under self-action
        (rotated, not just inverted). Tower invariant: verified at
        every depth tested.
        """
        if self.frame is None:
            self.observe()
        N = self.frame["N"]
        if N is None:
            return None
        d = N.shape[0]
        L_NN = (np.kron(np.eye(d), N) + np.kron(N.T, np.eye(d))
                - np.eye(d * d))
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
