---
type: entity
status: unknown
role: DOMINATOR
node_class: code
tags: [code, DOMINATOR, auto-generated]
sources:
  seed: observer:111
 file: modular.py generated: 2026-04-28
---
# ascend

**Role:** DOMINATOR

## Statement

One K6' pass: observer at n becomes adjacent producer at n+1.

    s' = [[s, N], [0, s]]
    N' = [[N, -2h], [0, N]]
    J' = [[J, 0], [0, J]]

    Preserves s² = s + I, N² = −I, {s, N} = N, {h, N} = 

## Depends on

[[P]]

## Required by

[[Filler-uniqueness]], [[Continuity]]

## Source

`modular.py` line 111 