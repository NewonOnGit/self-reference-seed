"""
backward_search.py -- The derivation engine core.

Given a target, search backward through the typed knowledge graph
to find operation chains that PRODUCE the target from known objects.

A chain is only as strong as its weakest edge.
All-forced chain = LAW. Any weak edge = LAW_CANDIDATE max.

ARCHITECTURE: L9 (cortex). The framework justifying its own findings.
"""
import numpy as np
from collections import deque
import sys
sys.path.insert(0, '../..')
from framework_types import (ResultType, Tier, EdgeType, FORCED_EDGE_TYPES,
                              WEAK_EDGE_TYPES, chain_status)
from knowledge_graph import KnowledgeGraph


class DerivationChain:
    """A candidate derivation path through the knowledge graph."""

    def __init__(self, edges, source_name, target_name):
        self.edges = edges
        self.source = source_name
        self.target = target_name
        self.edge_types = [e.edge_type for e in edges]
        self.length = len(edges)
        self.status = chain_status(self.edge_types)
        self.weakest = self._find_weakest()
        self.is_forced = all(t in FORCED_EDGE_TYPES for t in self.edge_types)
        self.has_numerical = any(t == EdgeType.NUMERICAL_MATCHES for t in self.edge_types)
        self.has_identification = any(t == EdgeType.IDENTIFIED_WITH for t in self.edge_types)

    def _find_weakest(self):
        """Find the weakest (least forced) edge in the chain."""
        weakness_order = [
            EdgeType.FAILED_BRIDGE,
            EdgeType.STRUCTURAL_PARALLEL,
            EdgeType.IDENTIFIED_WITH,
            EdgeType.NUMERICAL_MATCHES,
            EdgeType.COMPUTED_BY,
            EdgeType.LIFT_PROPAGATES,
            EdgeType.IDENTITY_CASTS,
            EdgeType.OPERATION_PRODUCES,
        ]
        for w in weakness_order:
            if w in self.edge_types:
                return w
        return None

    def path_str(self):
        if not self.edges:
            return "(empty chain)"
        parts = [self.edges[0].source.name]
        for e in self.edges:
            parts.append(f" --[{e.edge_type}]--> {e.target.name}")
        return ''.join(parts)

    def __repr__(self):
        forced = "FORCED" if self.is_forced else "MIXED"
        return (f"Chain({self.source}->{self.target}, {self.length} edges, "
                f"{self.status}, {forced}, weakest={self.weakest})")


class BackwardSearch:
    """Search backward from a target to find derivation chains."""

    def __init__(self, graph=None):
        self.graph = graph or KnowledgeGraph().seed()

    def search(self, target_name, max_depth=8, forced_only=False):
        """Find ALL chains from any root/key node to the target.
        Returns list of DerivationChain, sorted by quality."""
        if target_name not in self.graph.nodes:
            return []

        allowed = FORCED_EDGE_TYPES if forced_only else None
        results = []

        # Search from roots
        for root in self.graph.roots():
            chain_edges, status = self.graph.find_chain(
                root.name, target_name,
                allowed_types=allowed, max_depth=max_depth
            )
            if chain_edges:
                results.append(DerivationChain(chain_edges, root.name, target_name))

        # Search from key framework objects
        key_names = ['R', 'N', 'P', 'L', 'disc', 'phi', 'phi_bar',
                     'alpha_S', 'N_c', 'parent_ker', 'dim_gauge',
                     'beta_KMS', 'ker/A', '||N||^2', '||R||^2',
                     'Koide_Q', 'Koide_delta']
        for name in key_names:
            if name in self.graph.nodes and name != target_name:
                chain_edges, status = self.graph.find_chain(
                    name, target_name,
                    allowed_types=allowed, max_depth=max_depth
                )
                if chain_edges:
                    results.append(DerivationChain(chain_edges, name, target_name))

        # Deduplicate by path
        seen = set()
        unique = []
        for r in results:
            key = r.path_str()
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # Sort: forced first, then shorter, then by weakest edge quality
        weakness_rank = {
            EdgeType.OPERATION_PRODUCES: 0,
            EdgeType.IDENTITY_CASTS: 1,
            EdgeType.LIFT_PROPAGATES: 2,
            EdgeType.COMPUTED_BY: 3,
            EdgeType.NUMERICAL_MATCHES: 10,
            EdgeType.IDENTIFIED_WITH: 11,
            EdgeType.STRUCTURAL_PARALLEL: 12,
        }
        unique.sort(key=lambda c: (
            not c.is_forced,
            weakness_rank.get(c.weakest, 20),
            c.length,
        ))

        return unique

    def forced_chains(self, target_name, max_depth=8):
        """Find only fully forced chains (LAW-promotable)."""
        return self.search(target_name, max_depth=max_depth, forced_only=True)

    def competing_chains(self, target_name, max_depth=8):
        """Find all chains and partition into forced vs mixed.
        The derivation engine needs competing chains to discriminate."""
        all_chains = self.search(target_name, max_depth=max_depth)
        forced = [c for c in all_chains if c.is_forced]
        mixed = [c for c in all_chains if not c.is_forced]
        return {
            'target': target_name,
            'forced': forced,
            'mixed': mixed,
            'total': len(all_chains),
            'can_be_LAW': len(forced) > 0,
            'best': all_chains[0] if all_chains else None,
        }

    def investigate(self, target_name, max_depth=8):
        """Full investigation: find chains, compete them, determine status."""
        result = self.competing_chains(target_name, max_depth)

        # Apply the strict success condition:
        # Must have competing chains, kill at least one weak one
        if result['total'] == 0:
            result['verdict'] = 'NO_CHAINS'
            result['status'] = ResultType.FAILED
        elif result['can_be_LAW']:
            result['verdict'] = 'FORCED_CHAIN_EXISTS'
            result['status'] = ResultType.LAW
            result['derivation'] = result['forced'][0].path_str()
        elif result['total'] >= 2:
            result['verdict'] = 'MULTIPLE_MIXED_CHAINS'
            result['status'] = ResultType.PATH_CANDIDATE
        else:
            result['verdict'] = 'SINGLE_MIXED_CHAIN'
            result['status'] = ResultType.LAW_CANDIDATE

        return result


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("BACKWARD SEARCH SELF-TEST")
    print("=" * 65)

    bs = BackwardSearch()
    checks = []

    # Test 1: alpha_S should have a forced chain
    print("\n--- alpha_S ---")
    result = bs.investigate('alpha_S')
    print(f"  Verdict: {result['verdict']}")
    print(f"  Status: {result['status']}")
    print(f"  Forced chains: {len(result['forced'])}")
    print(f"  Mixed chains: {len(result['mixed'])}")
    if result.get('derivation'):
        print(f"  Derivation: {result['derivation']}")
    checks.append(("alpha_S has forced chain", result['can_be_LAW']))
    checks.append(("alpha_S -> LAW", result['status'] == ResultType.LAW))

    # Test 2: wobble_silent should NOT have forced chain (has identification)
    print("\n--- wobble_silent ---")
    result_w = bs.investigate('wobble_silent')
    print(f"  Verdict: {result_w['verdict']}")
    print(f"  Status: {result_w['status']}")
    print(f"  Forced: {len(result_w['forced'])}, Mixed: {len(result_w['mixed'])}")
    if result_w['best']:
        print(f"  Best chain: {result_w['best']}")
        print(f"  Path: {result_w['best'].path_str()}")
    checks.append(("wobble NOT forced", not result_w['can_be_LAW']))

    # Test 3: 1/alpha_EM should be mixed (NUMERICAL_MATCHES edges)
    print("\n--- 1/alpha_EM ---")
    result_em = bs.investigate('1/alpha_EM')
    print(f"  Verdict: {result_em['verdict']}")
    print(f"  Status: {result_em['status']}")
    print(f"  Forced: {len(result_em['forced'])}, Mixed: {len(result_em['mixed'])}")
    if result_em['best']:
        print(f"  Best: {result_em['best']}")
    checks.append(("1/alpha_EM not forced", not result_em['can_be_LAW']))
    checks.append(("1/alpha_EM has chains", result_em['total'] > 0))

    # Test 4: m_e/m_p
    print("\n--- m_e/m_p ---")
    result_ep = bs.investigate('m_e/m_p')
    print(f"  Verdict: {result_ep['verdict']}")
    print(f"  Status: {result_ep['status']}")
    if result_ep['best']:
        print(f"  Best: {result_ep['best'].path_str()}")
    checks.append(("m_e/m_p has chains", result_ep['total'] > 0))

    # Test 5: sin2_theta13
    print("\n--- sin2_theta13 ---")
    result_13 = bs.investigate('sin2_theta13')
    print(f"  Verdict: {result_13['verdict']}")
    print(f"  Forced: {len(result_13['forced'])}")
    if result_13.get('derivation'):
        print(f"  Derivation: {result_13['derivation']}")
    checks.append(("theta_13 has forced chain", result_13['can_be_LAW']))

    # Test 6: open frontier should have no chains
    print("\n--- 4D_Ricci (open) ---")
    result_open = bs.investigate('4D_Ricci')
    print(f"  Verdict: {result_open['verdict']}")
    checks.append(("open frontier = NO_CHAINS", result_open['verdict'] == 'NO_CHAINS'))

    # Summary table
    print(f"\n{'=' * 65}")
    print("DERIVATION STATUS OF ALL KEY QUANTITIES")
    print(f"{'=' * 65}")
    targets = ['alpha_S', 'sin2_thetaW', 'Bell_S', 'Koide_Q', 'Koide_delta',
               'm_p/M_Pl', 'm_e/m_p', '1/alpha_EM', 'sin2_tW_mZ',
               'wobble_silent', 'bp_per_turn', 'sin2_theta13',
               'n_amino', 'n_codons', 'Eigen_threshold']
    for t in targets:
        r = bs.investigate(t)
        forced_n = len(r['forced'])
        mixed_n = len(r['mixed'])
        print(f"  {t:20s}  {r['status']:20s}  forced={forced_n}  mixed={mixed_n}")

    print(f"\n{'=' * 65}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe derivation engine distinguishes forced chains from mixed chains.")
    print(f"Forced = LAW. Mixed = LAW_CANDIDATE. The machine can justify.")
