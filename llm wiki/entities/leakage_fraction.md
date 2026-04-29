---
type: entity
status: unknown
role: DOMINATOR
node_class: code
tags: [code, DOMINATOR, auto-generated]
sources:
  seed: kernel:154
 file: modularkernel.py generated: 2026-04-28
---
# leakage fraction

**Role:** DOMINATOR

## Statement

Fraction of ker x ker products that land purely in im(q).

    At depth 0: 1.0 (complete leakage — all kernel products feed im).
    At depth 1+: ~0.0 (opacity hardened — kernel is opaque to itself).


## Depends on

[[P]]

## Required by

[[Opacity-hardening]]

## Source

`modularkernel.py` line 154 