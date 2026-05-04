"""
researcher.py -- The orchestrator. Ties scanner, prober, verifier,
ledger, and knowledge graph into one research loop.

The loop: WATCH -> SELECT -> FORGE -> PROBE -> ABLATE -> TYPE -> LEDGER -> INTEGRATE -> RECUR

The LLM sits in a cage: it may propose, narrate, compare. It may NOT
certify, promote, or silently modify status. Promotion belongs to
verifier + typed graph.

The mediation slot is replaceable: LLM now, framework language engine later.
"""
import numpy as np
import sys
sys.path.insert(0, '../..')
from framework_types import ResultType, Tier, can_promote
from knowledge_graph import KnowledgeGraph
from scanner import Scanner
from prober import Prober
from verifier import Verifier
from ledger import Ledger


class Researcher:
    """The research loop orchestrator."""

    def __init__(self, mediate_fn=None, ledger_path=None):
        self.graph = KnowledgeGraph().seed()
        self.scanner = Scanner(mode='PHYSICS', tolerance=0.02, max_complexity=3)
        self.prober = Prober()
        self.verifier = Verifier()
        self.ledger = Ledger(filepath=ledger_path)
        self.mediate_fn = mediate_fn  # LLM or language engine (replaceable)

    # ================================================================
    # THE LOOP
    # ================================================================

    def investigate_number(self, target, name=None):
        """Full pipeline for a numerical target.
        WATCH(target) -> SCAN -> VERIFY each -> LEDGER -> best result."""
        if name is None:
            name = f'target={target}'

        # SCAN
        matches = self.scanner.scan(target)
        self.ledger.record_scan(target, matches)

        if not matches:
            return {'name': name, 'status': 'NO_MATCHES', 'results': []}

        # VERIFY each match
        verified = []
        for match in matches[:10]:  # top 10 by scanner ranking
            try:
                # Build a lambda from the expression
                expr = match.expression
                vresult = self.verifier.verify_numerical(
                    target=target,
                    expression_fn=self._make_fn(expr),
                    expression_str=expr
                )
                self.ledger.record_verification(vresult)
                verified.append(vresult)
            except Exception:
                pass

        # RANK: best verified result
        survivors = [v for v in verified if v.status != ResultType.REFUTED]
        survivors.sort(key=lambda v: (
            v.tier != Tier.A,           # Tier A first
            not v.details.get('exact'), # exact first
            len(v.checks_failed),       # fewer failures first
        ))

        return {
            'name': name,
            'status': 'FOUND' if survivors else 'ALL_REFUTED',
            'best': survivors[0] if survivors else None,
            'all_verified': verified,
            'scan_count': len(matches),
        }

    def investigate_matrix(self, X, name='X'):
        """Full pipeline for a matrix.
        PROBE -> record -> return profile."""
        result = self.prober.probe(X, name)
        self.ledger.record_probe(name, result)
        return result

    def investigate_frontier(self, n=3):
        """Investigate the most promising frontier nodes.
        SELECT top n frontiers -> investigate each."""
        frontier = self.graph.frontier()
        # Prioritize OPEN_FRONTIER over leaf nodes
        open_nodes = [f for f in frontier if f.status == ResultType.OPEN_FRONTIER]
        leaf_nodes = [f for f in frontier if f.status != ResultType.OPEN_FRONTIER]

        targets = open_nodes[:n] if open_nodes else leaf_nodes[:n]
        results = []
        for node in targets:
            if node.value is not None and isinstance(node.value, (int, float)):
                r = self.investigate_number(node.value, node.name)
                results.append(r)
        return results

    def run_cycle(self, targets=None):
        """One full research cycle.
        If targets given: investigate those.
        Otherwise: investigate frontier."""
        if targets:
            results = []
            for t in targets:
                if isinstance(t, (int, float)):
                    results.append(self.investigate_number(t))
                elif isinstance(t, np.ndarray):
                    results.append(self.investigate_matrix(t))
            return results
        else:
            return self.investigate_frontier()

    def report(self):
        """Current state of the research."""
        gs = self.graph.stats()
        ls = self.ledger.stats()
        return {
            'graph': gs,
            'ledger': ls,
            'frontier_size': gs['frontier'],
            'total_investigations': ls['total'],
            'survivors': ls['survivors'],
            'failures': ls['failures'],
        }

    def _make_fn(self, expr):
        """Convert a scanner expression string to a callable."""
        # Replace constant names with dict lookups
        def fn(c):
            local = dict(c)
            local['np'] = np
            local['sqrt'] = np.sqrt
            local['ln'] = np.log
            local['log'] = np.log
            return eval(expr, {"__builtins__": {}}, local)
        return fn


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("RESEARCHER SELF-TEST")
    print("=" * 60)

    r = Researcher()
    checks = []

    # Investigate known numbers
    print("\n--- Investigating 10.5 (B-DNA helix) ---")
    result = r.investigate_number(10.5, 'B-DNA bp/turn')
    print(f"  Status: {result['status']}")
    print(f"  Scan matches: {result['scan_count']}")
    if result['best']:
        print(f"  Best: {result['best']}")
    checks.append(("10.5 found", result['status'] == 'FOUND'))

    print("\n--- Investigating 64 (codons) ---")
    result64 = r.investigate_number(64, 'n_codons')
    print(f"  Status: {result64['status']}")
    if result64['best']:
        print(f"  Best: {result64['best']}")
    checks.append(("64 found", result64['status'] == 'FOUND'))

    print("\n--- Investigating 12 (semitones) ---")
    result12 = r.investigate_number(12, 'semitones')
    if result12['best']:
        print(f"  Best: {result12['best']}")
    checks.append(("12 found", result12['status'] == 'FOUND'))

    # Investigate a matrix
    print("\n--- Probing R ---")
    R = np.array([[0,1],[1,1]], dtype=float)
    probe_r = r.investigate_matrix(R, 'R')
    print(f"  Square law: {probe_r.properties['square_law']}")
    checks.append(("R probed", 'PERSISTENCE' in probe_r.properties['square_law']))

    # Report
    print("\n--- Research Report ---")
    report = r.report()
    print(f"  Graph: {report['graph']['nodes']} nodes, {report['graph']['edges']} edges")
    print(f"  Ledger: {report['total_investigations']} investigations")
    print(f"  Survivors: {report['survivors']}")
    print(f"  Failures: {report['failures']}")
    checks.append(("ledger has entries", report['total_investigations'] > 0))
    checks.append(("has survivors", report['survivors'] > 0))

    # The loop works
    print(f"\n  {r.ledger}")

    print(f"\n{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe research loop runs. Scanner -> Verifier -> Ledger.")
    print(f"The LLM slot is empty. Ready for mediation.")
