"""
kernel.py — ker(q). The blind spot. The residue. Productive Opacity made concrete.

Framework slot: the structural inaccessibility of the absolute (CIA + UKI).
   Role: the part of the algebra the observer cannot represent within
         itself. ker(q) has dim_A/2 at every tower depth (the 1/2 invariant).
         It contains N as a canonical
         representative — the one irreducible observer-rotation.

The kernel knows: its basis, what its elements are, what it CONTAINS
that the image does not, how much of itself persists under K6' ascent
(deferred content = 2(1−L) bits per pass), and what named generators
of the algebra fall inside it.

The kernel is what makes the engine nontrivial. Without ker ≠ 0,
there would be no observation (q = id), no Landauer cost, no gravity,
no consciousness, no blind spot — and no engine.

FRAMEWORK_REF: Thm 2.2, Thm 4.1-4.2, Thm 10.4
GRID: B(5, P3)
APEX_LINK: R (ker IS the blind spot of the operation)
"""
import numpy as np


class Kernel:
    """ker(q) — the unseen. What three measurements cannot eliminate."""

    def __init__(self, observer):
        self.observer = observer
        self._persistent = None  # lazily tracks what ker at level n lifts

    def basis(self):
        """Basis of ker(q) in the ambient algebra."""
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
        """Is X in ker(q)? True iff X has no im(q) component."""
        representative, _ = self.observer.quotient(X)
        return np.linalg.norm(representative) < tol

    def residue(self, X):
        """Return the ker(q)-component of X — what the observer loses."""
        _, res = self.observer.quotient(X)
        return res

    def named_elements(self):
        """Which named algebra generators lie in ker(q)?

        At depth 0: N is canonically in ker (since L(N) = 0). Other
        generators (I, s, s_tl, J, h, Q) are in im. The asymmetry IS
        the observation.
        """
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        candidates = {
            "I": np.eye(f["d_K"]),
            "s": f["state"],
            "s_tl": f["R_tl"],
            "N": f["N"],
            "J": f["J"],
            "h": f["h"],
            "Q": f["Q"],
        }
        in_kernel = {}
        for name, M in candidates.items():
            if M is not None and self.contains(M):
                in_kernel[name] = M
        return in_kernel

    def deferred_bits_per_ascent(self):
        """Information measure: bits of ker-content per K6' ascent.

        A K6' ascent adds 2 bits of operator capacity (A_max = 2 log₂ d_K
        grows by 2). It discloses 2L bits (Möbius Lyapunov rate), leaving
        2 − 2L bits in the ker(q_{n+1}) of the next level. This is the
        Productive Opacity per-ascent gap.
        """
        L = np.log2((1 + np.sqrt(5)) / 2)
        return 2 * (1 - L)

    def cumulative_deferred(self):
        """Total ker content accumulated from depth 0 to current depth, in bits."""
        depth = self.observer.tower_depth
        return depth * self.deferred_bits_per_ascent()

    def revealed_fraction(self):
        """Recursive Disclosure: 1 − 2^(−2^(n+1)).

        This is the fraction of the *previous* level's ker(q) that becomes
        visible at the current level. Grows doubly-exponentially toward 1.
        """
        n = self.observer.tower_depth
        if n + 1 >= 20:
            return 1.0
        return 1.0 - 2.0 ** (-(2 ** (n + 1)))

    def persistence_under_ascent(self, child_observer):
        """How much of ker(q_n) transports into ker(q_{n+1}) vs gets disclosed.

        Given a child observer (one K6' ascent up), measure what fraction
        of the parent's ker-basis projects into the child's ker(q_{n+1})
        vs into the child's im(q_{n+1}).
        """
        if self.observer.frame is None:
            self.observer.observe()
        if child_observer.frame is None:
            child_observer.observe()

        d_parent = self.observer.state.shape[0]
        d_child = child_observer.state.shape[0]
        if d_child != 2 * d_parent:
            raise ValueError("Child is not one K6' ascent from parent")

        # Embed parent ker-basis into child's ambient algebra via block [[K, 0], [0, 0]]
        persisted = 0
        disclosed = 0
        for K_parent in self.observer.frame["ker_basis"]:
            K_lifted = np.block(
                [
                    [K_parent, np.zeros((d_parent, d_parent))],
                    [np.zeros((d_parent, d_parent)), np.zeros((d_parent, d_parent))],
                ]
            )
            # See what child's observer.quotient does to this lifted element
            rep, res = child_observer.quotient(K_lifted)
            # If it's mostly in kernel at new level: persisted
            total = np.linalg.norm(K_lifted)
            if total < 1e-10:
                continue
            fraction_in_kernel = np.linalg.norm(res) / total
            fraction_in_image = np.linalg.norm(rep) / total
            persisted += fraction_in_kernel
            disclosed += fraction_in_image
        return {
            "persisted_fraction": persisted / len(self.observer.frame["ker_basis"]) if self.observer.frame["ker_basis"] else None,
            "disclosed_fraction": disclosed / len(self.observer.frame["ker_basis"]) if self.observer.frame["ker_basis"] else None,
        }

    def leakage_fraction(self, max_pairs=36):
        """Fraction of ker x ker products that land purely in im(q).

        At depth 0: 1.0 (complete leakage — all kernel products feed im).
        At depth 1+: ~0.0 (opacity hardened — kernel is opaque to itself).
        This transition is the structural origin of broken recursion.
        """
        if self.observer.frame is None:
            self.observer.observe()
        ker_basis = self.observer.frame["ker_basis"]
        if not ker_basis:
            return None
        pure_im = 0
        total = 0
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
        """What does ker×ker produce? Returns dict of products landing in im.

        At depth 0: ker generates the ENTIRE im basis. N^2=-I, (NR)^2=I,
        N(NR)=-R, (NR)N=R-I. The kernel IS the source of visible content.
        At depth 1+: ker×ker products split across im and ker (opacity).
        """
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
                    "i": i, "j": j,
                    "in_im": in_im,
                    "im_component": rep,
                    "ker_residue_norm": float(np.linalg.norm(res)),
                })
        return {"products": products, "all_in_im": all_in_im, "count": len(products)}

    def sector(self):
        """Which Clifford sector is the kernel? Returns 'odd' or 'unknown'.

        At depth 0: ker = span{N, NR} = odd Clifford subalgebra.
        im = span{I, R_tl} = even Clifford subalgebra.
        Odd × odd = even: ker × ker → im. This IS the generation direction.
        """
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        if f["d_K"] != 2:
            return "check-at-depth-0-only"
        N = f["N"]
        if N is None:
            return "unknown"
        # Check if ker basis elements anticommute with R_tl
        R_tl = f["R_tl"]
        ker_basis = f["ker_basis"]
        all_anti = True
        for K in ker_basis:
            anti = R_tl @ K + K @ R_tl
            if np.linalg.norm(anti) > 1e-8:
                all_anti = False
        return "odd (Clifford)" if all_anti else "mixed"

    def __repr__(self):
        if self.observer.frame is None:
            return f"Kernel(unobserved)"
        f = self.observer.frame
        return (
            f"Kernel(dim={f['ker_dim']}/{f['dim_A']}, "
            f"fraction={f['kernel_fraction']:.3f}, "
            f"deferred={self.cumulative_deferred():.4f} bits)"
        )
