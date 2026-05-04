"""
ledger.py -- Append-only research memory. No deletion.

Every research action produces a ledger entry. The ledger IS the
machine's memory. Without it, the system has vibes instead of history.

Each entry records: timestamp, operation, input, output, status,
dependencies, failure mode (if any), next branch suggested.
"""
import json
import time
import os
from framework_types import ResultType, Tier


class LedgerEntry:
    """One research action recorded."""

    def __init__(self, operation, input_data, output_data, status,
                 tier=None, dependencies=None, failure_mode=None,
                 next_branch=None, notes=None):
        self.timestamp = time.time()
        self.operation = operation       # 'scan', 'probe', 'verify', 'integrate'
        self.input_data = input_data     # what was investigated
        self.output_data = output_data   # what was found
        self.status = status             # ResultType
        self.tier = tier                 # Tier
        self.dependencies = dependencies or []
        self.failure_mode = failure_mode # which check failed (if any)
        self.next_branch = next_branch   # suggested follow-up
        self.notes = notes

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'time_str': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp)),
            'operation': self.operation,
            'input': str(self.input_data),
            'output': str(self.output_data),
            'status': self.status,
            'tier': self.tier,
            'dependencies': self.dependencies,
            'failure_mode': self.failure_mode,
            'next_branch': self.next_branch,
            'notes': self.notes,
        }

    def __repr__(self):
        t = time.strftime('%H:%M:%S', time.localtime(self.timestamp))
        return f"[{t}] {self.operation}: {self.status} | {self.output_data}"


class Ledger:
    """Append-only research memory."""

    def __init__(self, filepath=None):
        self.entries = []
        self.filepath = filepath
        if filepath and os.path.exists(filepath):
            self._load()

    def record(self, operation, input_data, output_data, status,
               tier=None, dependencies=None, failure_mode=None,
               next_branch=None, notes=None):
        """Record a research action. Returns the entry."""
        entry = LedgerEntry(
            operation=operation, input_data=input_data,
            output_data=output_data, status=status, tier=tier,
            dependencies=dependencies, failure_mode=failure_mode,
            next_branch=next_branch, notes=notes
        )
        self.entries.append(entry)
        if self.filepath:
            self._append(entry)
        return entry

    def record_scan(self, target, results):
        """Record a scanner run."""
        n = len(results)
        best = results[0] if results else None
        return self.record(
            operation='scan',
            input_data=f'target={target}',
            output_data=f'{n} matches, best: {best}' if best else 'no matches',
            status=ResultType.RAW_MATCH if n > 0 else ResultType.FAILED,
            notes=f'{n} total matches'
        )

    def record_probe(self, name, result):
        """Record a prober run."""
        props = result.properties if hasattr(result, 'properties') else {}
        return self.record(
            operation='probe',
            input_data=name,
            output_data=props.get('square_law', 'unknown'),
            status=ResultType.COMPUTED_MATCH,
            tier=Tier.A,
            dependencies=[name]
        )

    def record_verification(self, vresult):
        """Record a verification result."""
        return self.record(
            operation='verify',
            input_data=vresult.expression,
            output_data=f'{len(vresult.checks_passed)} passed, {len(vresult.checks_failed)} failed',
            status=vresult.status,
            tier=vresult.tier,
            failure_mode=vresult.checks_failed[0] if vresult.checks_failed else None,
            dependencies=[d[0] for d in vresult.details.get('dependencies', [])]
        )

    def record_integration(self, name, status, tier):
        """Record integration into the knowledge graph."""
        return self.record(
            operation='integrate',
            input_data=name,
            output_data=f'integrated as {status}',
            status=status,
            tier=tier
        )

    def by_operation(self, operation):
        """Filter entries by operation type."""
        return [e for e in self.entries if e.operation == operation]

    def by_status(self, status):
        """Filter entries by result status."""
        return [e for e in self.entries if e.status == status]

    def failures(self):
        """All failed/refuted entries. The kill ledger."""
        return [e for e in self.entries
                if e.status in (ResultType.FAILED, ResultType.REFUTED, ResultType.FORBIDDEN)]

    def survivors(self):
        """All entries that passed verification."""
        return [e for e in self.entries
                if e.status in (ResultType.LAW_CANDIDATE, ResultType.LAW,
                               ResultType.DERIVED_CANDIDATE)]

    def stats(self):
        by_op = {}
        by_status = {}
        for e in self.entries:
            by_op[e.operation] = by_op.get(e.operation, 0) + 1
            by_status[e.status] = by_status.get(e.status, 0) + 1
        return {
            'total': len(self.entries),
            'by_operation': by_op,
            'by_status': by_status,
            'failures': len(self.failures()),
            'survivors': len(self.survivors()),
        }

    def _append(self, entry):
        """Append one entry to file."""
        with open(self.filepath, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')

    def _load(self):
        """Load entries from file."""
        with open(self.filepath) as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    self.entries.append(LedgerEntry(
                        operation=d['operation'], input_data=d['input'],
                        output_data=d['output'], status=d['status'],
                        tier=d.get('tier'), dependencies=d.get('dependencies'),
                        failure_mode=d.get('failure_mode'),
                        next_branch=d.get('next_branch'), notes=d.get('notes')
                    ))

    def __repr__(self):
        s = self.stats()
        return f"Ledger({s['total']} entries, {s['survivors']} survivors, {s['failures']} failures)"


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("LEDGER SELF-TEST")
    print("=" * 60)

    ledger = Ledger()
    checks = []

    # Record some research actions
    ledger.record('scan', 'target=10.5', '3 matches', ResultType.RAW_MATCH)
    ledger.record('probe', 'R', 'PERSISTENCE', ResultType.COMPUTED_MATCH, tier=Tier.A)
    ledger.record('verify', '2*disc+ker/A', '5 passed', ResultType.LAW_CANDIDATE, tier=Tier.A)
    ledger.record('verify', 'disc+3', 'FAILED', ResultType.REFUTED, tier=Tier.C,
                  failure_mode='base_match')
    ledger.record('integrate', 'bp_per_turn', 'LAW', ResultType.LAW, tier=Tier.A)

    s = ledger.stats()
    print(f"  {ledger}")
    print(f"  Stats: {s}")

    checks.append(("5 entries", s['total'] == 5))
    checks.append(("1 failure", s['failures'] == 1))
    checks.append(("2 survivors", s['survivors'] == 2))
    checks.append(("kill ledger works", len(ledger.failures()) == 1))

    # Filter tests
    scans = ledger.by_operation('scan')
    checks.append(("filter by operation", len(scans) == 1))

    refuted = ledger.by_status(ResultType.REFUTED)
    checks.append(("filter by status", len(refuted) == 1))
    checks.append(("refuted has failure_mode", refuted[0].failure_mode == 'base_match'))

    # Append-only: cannot delete
    initial_count = len(ledger.entries)
    # (no delete method exists)
    checks.append(("no delete method", not hasattr(ledger, 'delete')))

    print(f"\n{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe ledger is append-only. No deletion. Every result has a place.")
