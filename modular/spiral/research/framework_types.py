"""
framework_types.py -- The law table. What can become what. What can't.

Every result the research engine produces carries a type from birth.
Promotion rules are merciless. MYTH cannot become LAW. GAUGE cannot
become LAW. RAW_MATCH cannot become DERIVED without a derivation path.

This is the K1' wall at the research-process level.
"""


# ================================================================
# RESULT TYPES (what a result IS)
# ================================================================

class ResultType:
    """Status of a research result. Ordered by evidential strength."""

    RAW_MATCH = 'RAW_MATCH'
    """Numerical coincidence found by scanner. No interpretation.
    Next required: derivation or ablation."""

    COMPUTED_MATCH = 'COMPUTED_MATCH'
    """Algebraically computed quantity matches a known value.
    Has a computation chain but no structural explanation."""

    DERIVED_CANDIDATE = 'DERIVED_CANDIDATE'
    """Has a derivation path through framework quantities.
    Needs verification (ablation, independence check)."""

    PATH_CANDIDATE = 'PATH_CANDIDATE'
    """Endpoint matches AND at least one legal operation chain reaches it,
    but the final identification remains unforced. Between match and law."""

    LAW_CANDIDATE = 'LAW_CANDIDATE'
    """Passed verification. Candidate for integration into the framework.
    Needs human review or multiple-witness confirmation."""

    LAW = 'LAW'
    """Verified, integrated, tested. Part of the framework.
    Survives gauge flip, tower lift, parent lift, and ablation."""

    FAILED = 'FAILED'
    """Tested and rejected. The relation does not hold.
    Kept in ledger as negative result."""

    REFUTED = 'REFUTED'
    """Was a candidate, then failed verification.
    Stronger than FAILED: it looked right and wasn't."""

    FORBIDDEN = 'FORBIDDEN'
    """Violates a type promotion rule or structural constraint.
    The framework says this CANNOT be true."""

    MYTHIC_RESIDUE = 'MYTHIC_RESIDUE'
    """Suggestive pattern that cannot be promoted to LAW.
    Not wrong — just not provable within the framework.
    Kept for generator-history."""

    GAUGE_RESIDUE = 'GAUGE_RESIDUE'
    """True under one gauge choice, not invariant.
    Not wrong — but not universal. Kept for context."""

    OPEN_FRONTIER = 'OPEN_FRONTIER'
    """Identified as a gap in the knowledge graph.
    Not a result — a question waiting for investigation."""


# ================================================================
# TIER SYSTEM (how certain is the derivation)
# ================================================================

class Tier:
    """Derivation certainty. From TAXONOMY.md."""

    A = 'A'
    """Pure algebra. Zero branching. Survives any mu."""

    B = 'B'
    """Requires identification step. Algebraically sound,
    but one link in the chain is interpretation not computation."""

    N = 'N'
    """Numerically verified to stated precision.
    Not proved algebraically. Could be coincidence."""

    C = 'C'
    """Pattern only. No derivation chain. Suggestive."""

    E = 'E'
    """Exhaustive computational search. Not a proof
    but covers all cases in a bounded domain."""


# ================================================================
# PROMOTION RULES (what can become what)
# ================================================================

# Allowed promotions: (from_type, to_type)
ALLOWED_PROMOTIONS = {
    (ResultType.RAW_MATCH, ResultType.COMPUTED_MATCH),
    (ResultType.RAW_MATCH, ResultType.FAILED),
    (ResultType.COMPUTED_MATCH, ResultType.DERIVED_CANDIDATE),
    (ResultType.COMPUTED_MATCH, ResultType.FAILED),
    (ResultType.DERIVED_CANDIDATE, ResultType.LAW_CANDIDATE),
    (ResultType.DERIVED_CANDIDATE, ResultType.REFUTED),
    (ResultType.LAW_CANDIDATE, ResultType.LAW),
    (ResultType.LAW_CANDIDATE, ResultType.REFUTED),
    (ResultType.OPEN_FRONTIER, ResultType.RAW_MATCH),
    (ResultType.OPEN_FRONTIER, ResultType.COMPUTED_MATCH),
    (ResultType.OPEN_FRONTIER, ResultType.FAILED),
    # Residue paths (can't promote to LAW)
    (ResultType.RAW_MATCH, ResultType.MYTHIC_RESIDUE),
    (ResultType.RAW_MATCH, ResultType.GAUGE_RESIDUE),
    (ResultType.COMPUTED_MATCH, ResultType.MYTHIC_RESIDUE),
    (ResultType.COMPUTED_MATCH, ResultType.GAUGE_RESIDUE),
}

# Blocked promotions: these CANNOT happen
BLOCKED_PROMOTIONS = {
    (ResultType.MYTHIC_RESIDUE, ResultType.LAW),
    (ResultType.MYTHIC_RESIDUE, ResultType.LAW_CANDIDATE),
    (ResultType.GAUGE_RESIDUE, ResultType.LAW),
    (ResultType.GAUGE_RESIDUE, ResultType.LAW_CANDIDATE),
    (ResultType.FAILED, ResultType.LAW),
    (ResultType.FAILED, ResultType.LAW_CANDIDATE),
    (ResultType.REFUTED, ResultType.LAW),
    (ResultType.FORBIDDEN, ResultType.LAW),
    (ResultType.RAW_MATCH, ResultType.LAW),           # skip the chain
    (ResultType.RAW_MATCH, ResultType.LAW_CANDIDATE),  # skip the chain
    (ResultType.RAW_MATCH, ResultType.DERIVED_CANDIDATE),  # skip computed
}


def can_promote(from_type, to_type):
    """Check if promotion is allowed."""
    if (from_type, to_type) in BLOCKED_PROMOTIONS:
        return False
    if (from_type, to_type) in ALLOWED_PROMOTIONS:
        return True
    return False


def promotion_path(from_type, to_type):
    """Find the minimum promotion chain from from_type to to_type.
    Returns list of intermediate types, or None if impossible.
    Each STEP must be in ALLOWED_PROMOTIONS. BLOCKED_PROMOTIONS
    prevents DIRECT shortcuts, not multi-step paths."""
    if from_type == to_type:
        return []

    # BFS over allowed single-step promotions
    from collections import deque
    queue = deque([(from_type, [from_type])])
    visited = {from_type}
    while queue:
        current, path = queue.popleft()
        for (f, t) in ALLOWED_PROMOTIONS:
            if f == current and t not in visited:
                new_path = path + [t]
                if t == to_type:
                    return new_path[1:]  # exclude starting type
                visited.add(t)
                queue.append((t, new_path))
    return None


# ================================================================
# EDGE TYPES (relationships in the knowledge graph)
# ================================================================

# ================================================================
# EDGE TYPES (derivation chain links)
# ================================================================

class EdgeType:
    """Types of edges in the knowledge graph. Ordered by forcing strength.
    A chain is LAW only if ALL edges are FORCED types."""

    # FORCED types (algebraically necessary)
    OPERATION_PRODUCES = 'OPERATION_PRODUCES'
    """Result of applying a framework operation (L, quotient, ker/im, etc.)
    to a known object. This is the strongest edge type."""

    IDENTITY_CASTS = 'IDENTITY_CASTS'
    """A = B by algebraic identity (e.g., phi+phi_bar=1, N^2=-I).
    No computation needed, just recognition."""

    LIFT_PROPAGATES = 'LIFT_PROPAGATES'
    """A at depth n+1 is the K6' lift of B at depth n.
    Tower propagation. Forced by the lift structure."""

    # COMPUTED types (verified but not purely algebraic)
    COMPUTED_BY = 'COMPUTED_BY'
    """Result of numerical computation (eigenvalues, norms, etc.).
    Exact if the computation is symbolic; approximate if numerical."""

    # WEAK types (cannot promote chain to LAW)
    NUMERICAL_MATCHES = 'NUMERICAL_MATCHES'
    """A ~ B numerically within tolerance. NOT forced.
    A chain containing this edge CANNOT become LAW."""

    IDENTIFIED_WITH = 'IDENTIFIED_WITH'
    """A is identified with B by interpretation (physics, biology, etc.).
    The bridge between algebra and the world. Cannot force LAW."""

    STRUCTURAL_PARALLEL = 'STRUCTURAL_PARALLEL'
    """A and B share structural properties (same grid address, same
    algebraic form). Suggestive but not derivative."""

    # NEGATIVE types
    FAILED_BRIDGE = 'FAILED_BRIDGE'
    """Tested connection that was refuted. Kept for the kill ledger."""


# Which edge types are "forced" (can appear in a LAW chain)
FORCED_EDGE_TYPES = {
    EdgeType.OPERATION_PRODUCES,
    EdgeType.IDENTITY_CASTS,
    EdgeType.LIFT_PROPAGATES,
    EdgeType.COMPUTED_BY,
}

# Which edge types block LAW promotion
WEAK_EDGE_TYPES = {
    EdgeType.NUMERICAL_MATCHES,
    EdgeType.IDENTIFIED_WITH,
    EdgeType.STRUCTURAL_PARALLEL,
}


def chain_status(edge_types):
    """Given a list of edge types in a chain, determine max promotable status.
    All forced -> LAW possible. Any weak -> LAW_CANDIDATE max.
    Any failed -> REFUTED."""
    if any(e == EdgeType.FAILED_BRIDGE for e in edge_types):
        return ResultType.REFUTED
    if all(e in FORCED_EDGE_TYPES for e in edge_types):
        return ResultType.LAW
    if any(e in WEAK_EDGE_TYPES for e in edge_types):
        return ResultType.LAW_CANDIDATE
    return ResultType.DERIVED_CANDIDATE


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    checks = []

    # Promotion rules
    checks.append(("RAW->COMPUTED allowed", can_promote(ResultType.RAW_MATCH, ResultType.COMPUTED_MATCH)))
    checks.append(("MYTH->LAW blocked", not can_promote(ResultType.MYTHIC_RESIDUE, ResultType.LAW)))
    checks.append(("GAUGE->LAW blocked", not can_promote(ResultType.GAUGE_RESIDUE, ResultType.LAW)))
    checks.append(("RAW->LAW blocked (skip)", not can_promote(ResultType.RAW_MATCH, ResultType.LAW)))
    checks.append(("FAILED->LAW blocked", not can_promote(ResultType.FAILED, ResultType.LAW)))
    checks.append(("DERIVED->LAW_CAND allowed", can_promote(ResultType.DERIVED_CANDIDATE, ResultType.LAW_CANDIDATE)))
    checks.append(("LAW_CAND->LAW allowed", can_promote(ResultType.LAW_CANDIDATE, ResultType.LAW)))

    # Promotion paths
    path_raw_law = promotion_path(ResultType.RAW_MATCH, ResultType.LAW)
    checks.append(("RAW->LAW path exists", path_raw_law is not None))
    checks.append(("RAW->LAW path length 4",
                    path_raw_law is not None and len(path_raw_law) == 4))
    print(f"  RAW -> LAW path: {path_raw_law}")

    path_myth_law = promotion_path(ResultType.MYTHIC_RESIDUE, ResultType.LAW)
    checks.append(("MYTH->LAW impossible", path_myth_law is None))

    path_frontier = promotion_path(ResultType.OPEN_FRONTIER, ResultType.LAW)
    checks.append(("FRONTIER->LAW path exists", path_frontier is not None))
    print(f"  FRONTIER -> LAW path: {path_frontier}")

    # Summary
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nPromotion chain RAW -> LAW:")
    print(f"  RAW_MATCH -> COMPUTED_MATCH -> DERIVED_CANDIDATE -> LAW_CANDIDATE -> LAW")
    print(f"  4 gates. No shortcuts. MYTH and GAUGE can never reach LAW.")
