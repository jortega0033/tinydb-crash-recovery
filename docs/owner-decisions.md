# Owner decisions

A dated record of the decisions the owner made for this repository. Each entry says what was decided, when, and where it is implemented. Changing any entry needs the owner. An agent that finds a decision blocking a ticket stops and says so.

All entries date from 2026-11-22.

| # | Decision | Implemented in |
|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | `CLAUDE.md`, `.claude/`, `.github/` on `main` |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | `.claude/agents/` ("In this repository" sections, "Use proactively" descriptions), `.claude/skills/implement-ticket/SKILL.md` |
| 3 | Every open ticket is about app implementation. Tooling is installed, not ticketed. | Epic #1 and its child tickets; `.claude/`, `.github/` |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | `CLAUDE.md` ("Git workflow", "Delivery workflow"), `.claude/skills/next-ticket/SKILL.md`, deny rules in `.claude/settings.json`, `docs/RELEASING.md` |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. | `.claude/skills/next-ticket/SKILL.md` (`disable-model-invocation: true`), `LOOP.md` |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles have run after the last code edit. | `.claude/hooks/role_gate.py`, `.claude/settings.json` |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | `LOOP.md`, `loop-constraints.md`, `loop-budget.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | `.github/workflows/ci.yml`; branch protection is set on GitHub by the orchestrator after merge |
| 9 | Documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | `.claude/settings.json` |
| 10 | Open decisions on tickets are settled with the ticket's stated default (list below). | The tickets named below |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed and used for UI work and for copy. | `docs/ui-quality.md`, `.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/` |

Entry 11 (Rust verified in CI only) does not apply: this repository has no Rust.

## Entry 10: decisions settled with the ticket default

| Ref | Decision | Default taken | Ticket |
|---|---|---|---|
| D1 | Runner for the upstream suite | pytest, dev-only, pinned exactly in `requirements-dev.txt`; project tests use `unittest`; nothing is added to runtime | #2 |
| D2 | Staging of upstream TinyDB | Verbatim copy under `third_party/tinydb/` (package, MIT `LICENSE`, upstream tests) plus `UPSTREAM.md` with the commit hash; imported from there, never installed from PyPI | #2 |
| D3 | Project licence | None selected, none added | none |
| D4 | Receipt cap | 1000 receipts; further unique batches are rejected with a clear error | #3 |
| D5 | Frame encoding | Big-endian 4-byte payload length, 4-byte CRC-32 (`zlib.crc32`), UTF-8 JSON payload; file header with magic, format version and 16-byte database ID | #3 |
| D6 | Static HTML report view | Out of this batch (CLI report only); future work | #7 |
| D7 | Non-Linux behaviour | `open_journal` raises `UnsupportedPlatformError`; Linux-only tests skip with a reason | #2 |
| D8 | Filesystem support | Open-time probe of lock, same-directory atomic replace and directory sync; no filesystem-type allowlist; the harness records the filesystem type | #4 |
| D9 | Scan timings | Not measured in this batch; recorded as future work | #7 |

The equality index ticket (plan ID E89-7) is issue #8.

## Program decisions (owner, 2026-11-24)

The owner accepted the goal and each suggestion below. They apply from the phase they name; the rules of `CLAUDE.md` hold for phase 1 as written.

| Decision | Implemented in |
|---|---|
| The repository has a program goal above phase 1: a crash-safe embedded document database, in six phases. | Program issue #30 |
| The plan is a TinyDB extension. Suggested: keep the TinyDB API as the top layer and build the engine below it. | Program issue #30 |
| Replication leaves the local-only rule. Suggested: simulated network and loopback only. | Program issue #30 |
