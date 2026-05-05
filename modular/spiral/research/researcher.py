"""
researcher.py -- The orchestrator + mediation slot (merged).

Ties scanner, operations, verifier, derivation engine, ledger,
and knowledge graph into one research loop with LLM mediation.

The LLM sits in a cage: propose, narrate, compare.
NOT certify, promote, or modify status. Promotion = verifier + graph.
The mediation slot is REPLACEABLE: LLM now, framework engine later.

ARCHITECTURE: L9 (reflective cortex). The framework investigating itself.
DEPTH: 9
ORGAN: cortex — O∘B∘S at depth 9
"""
import os
import re
import numpy as np
import sys
sys.path.insert(0, '../..')
from framework_types import ResultType, Tier
from knowledge_graph import KnowledgeGraph
from scanner import Scanner
from operations import probe
from verifier import Verifier
from ledger import Ledger


class Researcher:
    """The research loop orchestrator."""

    def __init__(self, mediate_fn=None, ledger_path=None):
        self.graph = KnowledgeGraph().seed()
        self.scanner = Scanner(mode='PHYSICS', tolerance=0.02, max_complexity=3)
        self.verifier = Verifier()
        self.ledger = Ledger(filepath=ledger_path)
        self.mediate_fn = mediate_fn

    def investigate_number(self, target, name=None):
        """Full pipeline: scan -> verify each -> ledger -> best."""
        if name is None:
            name = f'target={target}'
        matches = self.scanner.scan(target)
        self.ledger.record_scan(target, matches)
        if not matches:
            return {'name': name, 'status': 'NO_MATCHES', 'results': []}
        verified = []
        for match in matches[:10]:
            try:
                vresult = self.verifier.verify_numerical(
                    target=target,
                    expression_fn=self._make_fn(match.expression),
                    expression_str=match.expression
                )
                self.ledger.record_verification(vresult)
                verified.append(vresult)
            except Exception:
                pass
        survivors = [v for v in verified if v.status != ResultType.REFUTED]
        survivors.sort(key=lambda v: (v.tier != Tier.A, not v.details.get('exact'), len(v.checks_failed)))
        return {
            'name': name, 'status': 'FOUND' if survivors else 'ALL_REFUTED',
            'best': survivors[0] if survivors else None,
            'all_verified': verified, 'scan_count': len(matches),
        }

    def investigate_matrix(self, X, name='X'):
        """Probe a matrix using the operations microscope."""
        result = probe(X, name)
        self.ledger.record_probe(name, result)
        return result

    def investigate_frontier(self, n=3):
        """Investigate most promising frontier nodes."""
        frontier = self.graph.frontier()
        open_nodes = [f for f in frontier if f.status == ResultType.OPEN_FRONTIER]
        targets = (open_nodes or frontier)[:n]
        results = []
        for node in targets:
            if node.value is not None and isinstance(node.value, (int, float)):
                results.append(self.investigate_number(node.value, node.name))
        return results

    def report(self):
        gs = self.graph.stats()
        ls = self.ledger.stats()
        return {
            'graph': gs, 'ledger': ls,
            'frontier_size': gs['frontier'],
            'total_investigations': ls['total'],
            'survivors': ls['survivors'],
            'failures': ls['failures'],
        }

    def _make_fn(self, expr):
        def fn(c):
            local = dict(c)
            local['np'] = np
            local['sqrt'] = np.sqrt
            local['ln'] = np.log
            return eval(expr, {"__builtins__": {}}, local)
        return fn


# ================================================================
# MEDIATION SLOT (merged from native_loop.py)
# ================================================================

def load_api_key():
    """Load API key from secret.txt (NOT committed to git)."""
    paths = [
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'secret.txt'),
        os.path.expanduser('~/.anthropic_key'),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                return f.read().strip()
    return os.environ.get('ANTHROPIC_API_KEY')


def make_claude_mediator(api_key, model='claude-haiku-4-5-20251001'):
    """LLM as P2 face. Proposes only. Does not certify."""
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic(api_key=api_key)

    def mediate(context):
        system = (
            "You are a research mediator for the Self-Reference Framework. "
            "Propose ONE specific numerical target or matrix expression to "
            "investigate next. Give the number, a one-line reason, nothing else."
        )
        try:
            response = client.messages.create(
                model=model, max_tokens=150, system=system,
                messages=[{"role": "user", "content": context}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"MEDIATION_FAILED: {e}"
    return mediate


def make_dummy_mediator():
    """Fallback: proposes from a fixed list."""
    targets = [
        (137.036, "1/alpha_EM"), (0.2224, "sin(theta_Cabibbo)"),
        (1836.15, "m_p/m_e"), (0.1181, "alpha_S at m_Z"),
        (23, "chromosome pairs"), (80.379, "m_W GeV"),
    ]
    idx = [0]
    def mediate(context):
        t, reason = targets[idx[0] % len(targets)]
        idx[0] += 1
        return f"Investigate {t}: {reason}"
    return mediate


def run_mediated_cycle(researcher, mediator, n_cycles=3):
    """Run n research cycles with mediation."""
    results = []
    for i in range(n_cycles):
        report = researcher.report()
        frontier_names = [f.name for f in researcher.graph.frontier()[:5]]
        recent = researcher.ledger.entries[-3:] if researcher.ledger.entries else []
        context = (
            f"Research: {report['graph']['nodes']} nodes, "
            f"{report['total_investigations']} investigations. "
            f"Frontier: {frontier_names}. "
            f"What number should I investigate?"
        )
        proposal = mediator(context)
        print(f"\n  Cycle {i+1}: {proposal}")
        target = None
        for num_str in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', proposal):
            try:
                val = float(num_str)
                if 1e-15 < abs(val) < 1e10:
                    target = val
                    break
            except ValueError:
                continue
        if target is not None:
            result = researcher.investigate_number(target, f"mediated_{i}")
            print(f"  Result: {result['status']}")
            if result.get('best'):
                print(f"  Best: {result['best']}")
            results.append(result)
    return results


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("RESEARCHER SELF-TEST")
    print("=" * 55)
    r = Researcher()
    checks = []

    result = r.investigate_number(10.5, 'B-DNA')
    checks.append(("10.5 found", result['status'] == 'FOUND'))

    result12 = r.investigate_number(12, 'semitones')
    checks.append(("12 found", result12['status'] == 'FOUND'))

    R_mat = np.array([[0,1],[1,1]], dtype=float)
    probe_r = r.investigate_matrix(R_mat, 'R')
    checks.append(("R probed", 'PERSISTENCE' in str(probe_r.properties.get('square_law',''))))

    report = r.report()
    checks.append(("has entries", report['total_investigations'] > 0))

    # Dummy mediation
    mediator = make_dummy_mediator()
    results = run_mediated_cycle(r, mediator, n_cycles=2)
    checks.append(("mediated cycles ran", len(results) > 0))

    print(f"\n{'=' * 55}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
