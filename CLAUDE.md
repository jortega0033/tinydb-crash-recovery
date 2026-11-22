# CLAUDE.md

TinyDB Crash Recovery is an opt-in journal mode for TinyDB: multi-document batches that survive a process stop, with checkpoint rotation, an explicit legacy import, an equality index and a subprocess fault harness. A developer demonstrates it with one scenario: move counts between two bins, record a movement row in a second table, interrupt the writer, reopen in a fresh process and read back the same complete state.

**Status: planning only.** The repository holds the product plan, the technical specification and the backlog. There is no application code and no test yet. CI is installed and runs the review gate self-test now; its test steps are guarded and switch on when ticket [#2](https://github.com/jortega0033/tinydb-crash-recovery/issues/2) adds the tests. Every command below is planned and does not run until the named ticket lands. Do not claim a check passed that was never run.

## Source of truth

- [docs/PRD.md](docs/PRD.md): product requirements, success criteria, epic E89 and its ticket list.
- [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md): data contract, on-disk layout, commit and retry rules, recovery and checkpoint steps, import and index rules, the fault fixture and its expected outcomes.
- Epic [#1](https://github.com/jortega0033/tinydb-crash-recovery/issues/1) and its tickets hold scope, acceptance criteria and estimates. If a ticket and the spec disagree, stop and say so in the issue; do not pick one silently.
- [README.md](README.md): status and licensing. No project licence is selected; do not add one.

## Stack and constraints

- Python, CPython 3.12 target, Linux on a native local filesystem. Windows and macOS are not targets: CI also runs on Windows, so Linux-only code (`fcntl` locking, directory sync) must fail with a clear unsupported-platform error and its tests must skip, never crash the import.
- Build on TinyDB v4.8.2 at commit `10644a0e07ad180c5b756aba272ee6b0dbd12df8` (MIT), staged locally as source. The data path uses the Python standard library plus that pinned upstream source. No PyPI install of `tinydb`, no other runtime dependency, no network use at runtime. Keep the upstream licence and attribution with any copied source.
- Existing TinyDB behaviour stays intact: default `JSONStorage`, the public API and the upstream test suite are unmodified. Journal mode is opt-in through an explicit entry point with a separate on-disk layout.
- Single writer, one process at a time. Out of scope: power loss, damaged storage, network filesystems, multiple writer processes, in-place conversion of live legacy files. Never claim durability beyond process death.
- Deterministic: explicit positive integer document IDs, repeatable recovery, seeded trials.
- Budgets: 1 MiB frame cap, 100 operations per batch, a documented receipt cap. Test bounds are measured on the host and recorded, not assumed.

## Planned module boundaries

Names are the planned defaults; ticket [#2](https://github.com/jortega0033/tinydb-crash-recovery/issues/2) freezes the layout and updates this section. All behaviour comes from [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md).

| Planned path | Responsibility |
|---|---|
| `third_party/tinydb/` | Pinned upstream TinyDB source, its MIT `LICENSE` and the upstream tests. Never edited by hand; the commit hash is recorded next to it. |
| `tinydb_journal/` | The package: `open_journal(directory)` and `apply_batch(batch_id, operations)`, error and result types. |
| `tinydb_journal/` lock | One exclusive advisory lock per app-owned directory, taken before any read, write or recovery; a second opener gets a clear busy error. |
| `tinydb_journal/` frame and log | Fixed header, bounded frames (length, checksum, UTF-8 JSON payload), append then flush then sync before acknowledgement, receipts and payload fingerprints. |
| `tinydb_journal/` recovery and checkpoint | Load the last complete checkpoint, validate and replay complete frames, discard only an unambiguous partial tail, stop on corruption with a diagnostic; checkpoint rotation in the same directory. |
| `tinydb_journal/` import and index | Explicit legacy import into a new directory; equality index on top-level string fields with scan fallback, valid only for the committed generation. |
| `tinydb_journal/harness/` | Controller, writer child with a control pipe and named barriers, independent oracle, seeded trials. |
| `tinydb_journal/report/` | Read-only CLI report for trial results and a selected generation. |
| `tests/` | The project's own `unittest` suite and fixtures. |

Invariants every change must keep (from the spec): validation failures leave the generation and journal unchanged; a frame is synced before any receipt is returned or the in-memory view is published; an identical batch replay returns the original receipt and writes nothing; a reused batch ID with a different payload is a conflict; a write or sync error after append starts is outcome-unknown and blocks the handle until reopen; a complete frame with a bad checksum is corruption, never a partial tail; opening twice yields identical data and generation.

## Commands

Local Python is `python` (3.13 on the owner's PC; `python3` on Linux). The fault and lock tests only run on Linux, so Linux CI is the verification for them.

| Purpose | Command | Status |
|---|---|---|
| Setup | `python -m venv .venv`, then install the pinned dev requirement file | planned: introduced by ticket #2 (only for the upstream suite runner) |
| Own tests | `python -m unittest discover -s tests -t .` | planned: introduced by ticket #2 |
| Upstream suite | `python -m pytest third_party/tinydb/tests` | planned: introduced by ticket #2 (runner choice is an open decision) |
| Demo scenario | `python -m tinydb_journal scenario run <directory>`, then `scenario show <directory>` | planned: introduced by ticket #2 |
| Legacy import | `python -m tinydb_journal import <legacy.json> <new-directory>` | planned: introduced by ticket #5 |
| Fault harness | `python -m tinydb_journal.harness run --seed <n> --out <directory>` | planned: introduced by ticket #6 |
| Report | `python -m tinydb_journal report <trials-directory>` | planned: introduced by ticket #7 |

The ticket that introduces a command makes it real and replaces "planned" here in the same pull request.

## Git workflow

- One branch per ticket, named `ticket-<number>-<short-slug>`, from an up-to-date `main`. One pull request per ticket, opened against `main` with `Closes #<number>`.
- Small commits with a clear message. Never push to `main`, never force-push, never merge. Only the owner merges.
- Work stays inside the ticket's scope. A finding outside it becomes a comment on the issue, not a drive-by change.
- `.env` files and journal data directories are never committed.

## Evidence before a ticket is called done

Quote, in the pull request, each command that was run and its actual result. For this project that means:

1. The ticket's own verification commands, with output (tests that were skipped on this platform are named as skipped, not counted as passed).
2. The own test suite and, once ticket #2 has landed, the upstream TinyDB suite, both passing.
3. For any on-disk, recovery or ordering change: a test that fails without the change, run for the interruption case it covers, and the effect on file length and generation.
4. For behaviour that only runs on Linux: say where it ran (CI job or Linux host) and link the run. A Windows-only local pass proves nothing for it.
5. CI green on the draft pull request, with the run link. Order of the gates: local checks pass and their output is recorded; Code Reviewer, then Reality Checker, on the diff and that evidence (Reality Checker checks that the documented checks ran locally and that CI is configured to run them, and does not need a CI result); only then `gh pr create --draft`; CI runs on the draft; when it is green, `gh pr ready` and a comment on the issue with the CI run link.
6. A statement of what was not verified.

A criterion without evidence is not met.

## Agent roles and Loop

Loop Engineering is installed at L1, report-only and unscheduled: see [LOOP.md](LOOP.md), [loop-constraints.md](loop-constraints.md) and [loop-budget.md](loop-budget.md).

The project subagents live in `.claude/agents/` and come from Agency Agents at a pinned revision; provenance and local changes are in [.claude/agency-agents/README.md](.claude/agency-agents/README.md). Each role file starts with an "In this repository" section written for this project; it and this file override the generic upstream text below it. Reviewer and gate roles are read-only (`tools: Read, Grep, Glob`), so the caller gives them the diff and the recorded command output.

When asked to implement, continue or finish a GitHub issue, follow the playbook [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand. Delegate to the roles without waiting to be asked:

- **Before coding:** Software Architect, for a ticket that changes a module boundary, the on-disk format or the data contract.
- **While coding:** the implementing role that matches the files: Database Reliability Engineer for journal, recovery and checkpoint code, Test Automation Engineer for tests and the fault harness, Technical Writer for documentation.
- **After coding:** Application Security Engineer when the change parses untrusted bytes (frames, checkpoints, legacy import).
- **On every ticket, before it is called done:** Code Reviewer, then Reality Checker.
- The session that wrote a change does not count as its reviewer.
- List the roles that ran and their verdicts in the pull request description under "Agent roles run".

Each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate to it without being told.

## Delivery workflow

- **Driver and playbook.** The owner starts a ticket with `/next-ticket` ([`.claude/skills/next-ticket/SKILL.md`](.claude/skills/next-ticket/SKILL.md)); it runs the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Starting it is the go signal; there is no scheduler. Agents take a ticket up to a ready pull request and never merge or release. A ticket with open sub-issues or the label `tracking` is a container and is never picked.
- **Review gate hook.** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py), wired in [`.claude/settings.json`](.claude/settings.json), blocks `gh pr create` and `gh pr ready` until Code Reviewer and Reality Checker have run after the last code edit; documentation-only changes pass. `ROLE_GATE=off` in the environment Claude Code is started from switches it off for that session.
- **Permissions.** `.claude/settings.json` allows the documented commands and git and gh read operations, asks before edits to CI, agent configuration, skills, hooks and Loop files, and denies force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env`.
- **CI.** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs the gate self-test, the own tests and the upstream suite on Linux and Windows with Python 3.12; the test steps are guarded until ticket #2 lands and that ticket removes the guards. Every job must be green before a pull request is marked ready.
- **Pull request.** Use [`.github/pull_request_template.md`](.github/pull_request_template.md). Add a line to [`CHANGELOG.md`](CHANGELOG.md) under `Unreleased` in every ticket pull request.
- **Labels.** `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking`.
- **UI and copy.** [`docs/ui-quality.md`](docs/ui-quality.md) holds the ten binding rules for any screen and for user-facing text; the product has a CLI only today. A ticket that adds a screen starts with the `ui-ux-pro-max` skill and ends with a check against that file. User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- **Decisions.** [`docs/owner-decisions.md`](docs/owner-decisions.md) records what the owner decided and where it is implemented. A decision that blocks a ticket stops the ticket.
- **Releases and security.** [`docs/RELEASING.md`](docs/RELEASING.md), [`SECURITY.md`](SECURITY.md).
- **Only the owner merges and releases.**
