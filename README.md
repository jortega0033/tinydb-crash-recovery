# TinyDB Crash Recovery

A planned offline project. Product implementation has not started. The repository contains the product plan, technical specification, implementation backlog and an empty scaffold (`pyproject.toml`, `tinydb_journal/` stubs, smoke test).

## Program goal

Grow the crash-safe journal into a full embedded document database in Python: transactions, indexes, a query planner, replication and a formally checked storage core, still opening and saving TinyDB documents.

The program is planned ([#30](https://github.com/jortega0033/tinydb-crash-recovery/issues/30)). Phase 1 is the current epic [#1](https://github.com/jortega0033/tinydb-crash-recovery/issues/1) and the only phase with tickets.

**Score.** Faults injected without a lost or half-visible transaction, over every write, sync and rename, plus the share of TinyDB's own test suite that passes unchanged.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 55 to 80 | [#1](https://github.com/jortega0033/tinydb-crash-recovery/issues/1) |
| 2 | Storage engine | 130 to 220 | [#31](https://github.com/jortega0033/tinydb-crash-recovery/issues/31) |
| 3 | Transactions | 110 to 190 | [#32](https://github.com/jortega0033/tinydb-crash-recovery/issues/32) |
| 4 | Queries | 130 to 220 | [#33](https://github.com/jortega0033/tinydb-crash-recovery/issues/33) |
| 5 | Replication | 150 to 260 | [#34](https://github.com/jortega0033/tinydb-crash-recovery/issues/34) |
| 6 | Proof | 100 to 180 | [#35](https://github.com/jortega0033/tinydb-crash-recovery/issues/35) |

About 680 to 1150 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/tinydb-crash-recovery/issues/1)

## Current status

The fixtures describe expected results for future checks. No working baseline or passing implementation tests are claimed; the smoke test only checks imports and CLI help. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.
