# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. The file `loop-verifier.md` in the same folder is not from Agency Agents; it belongs to the Loop Engineering setup described in [`LOOP.md`](../../LOOP.md).

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Reviewer and gate roles have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands. See "Local changes" below for everything else that differs from upstream.

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `engineering-database-reliability-engineer.md` | Database Reliability Engineer | `engineering/engineering-database-reliability-engineer.md` | `0096dc3c1b31e33814c509fda43853cc77cef6252bb94da527b833be13b53a5a` | none |
| `testing-test-automation-engineer.md` | Test Automation Engineer | `testing/testing-test-automation-engineer.md` | `4299d038e88387546d645ccbe767b1dfdb7de10da55eba1ab103149972cd2b9b` | none |
| `engineering-technical-writer.md` | Technical Writer | `engineering/engineering-technical-writer.md` | `bf5c809977e10904b988ab8b218853ce8dfa38b2cbd89a7d2cfadba44ac25761` | none |

## Why these roles

| Role | Use in this repository |
|---|---|
| Code Reviewer (read-only, gate) | Review every ticket diff for correctness, the commit-order and recovery invariants, and scope. |
| Reality Checker (read-only, gate) | Compare claimed evidence with commands that were actually run before a ticket is called done. |
| Software Architect (read-only) | Check a ticket's design against the planned module boundaries and the data contract in `docs/TECHNICAL_SPEC.md`, especially format and layout freezes. |
| Application Security Engineer (read-only) | Review the parts that parse untrusted bytes: frame lengths before allocation, checksums, legacy import validation, path handling in the directory layout. |
| Database Reliability Engineer | Implement and review journaling, checkpoint rotation, recovery and the sync and atomic-replace sequence. |
| Test Automation Engineer | Build the subprocess fault harness, the independent oracle and the deterministic fixtures. |
| Technical Writer | Write the setup, offline commands, limits and verification documentation of the final report ticket. |

Most of these roles are written for larger stacks (cloud databases, replication, browser test tools, CI platforms). In this repository `CLAUDE.md` wins: Python, the standard library plus the pinned upstream TinyDB source, a single local writer, `unittest`, no network.

Roles that were considered and left out: Database Optimizer and Backend Architect (aimed at SQL servers and HTTP services; this project has neither), Codebase Onboarding Engineer (there is no existing code to trace yet), Frontend Developer, UI Designer, UX Architect and Accessibility Auditor (the planned UI is a CLI report; an optional static HTML view is not in the first batch), Performance Benchmarker (scan timings are optional and measured by the report ticket).

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Check that the roles load

From the repository root, in a new session:

```text
claude -p "List the project-level subagents defined in .claude/agents with the tools each one may use."
```

The four reviewer roles and `loop-verifier` must report exactly `Read, Grep, Glob`. Checked-in results of this check, if any, are recorded below under "Verification".

## Updating

Fetch the same paths at a newer revision, re-apply the `tools:` line to the four read-only roles, and update the revision and hashes in this file in the same commit.

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. Nothing else in the role files changed.

A section headed "In this repository" was then inserted directly after the frontmatter of every Agency Agents role (not into `loop-verifier`), before the upstream text. It is project-specific text written for this repository, not upstream text: the planned stack and hard rules that bind the role, the planned files and commands it uses, a checklist of this project's rules with their sources, the parts of the generic text that do not apply here, and what the role hands back. It ends with the sentence "This section and CLAUDE.md override the generic text below wherever they differ." The repository has no code yet, so the sections describe the planned stack, modules and commands from the technical specification and say they are planned; they must be re-checked against the code as tickets land. The upstream text below the section and the rest of the frontmatter are unchanged.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, first remove the "Use proactively" sentence (and, where the upstream description has no final punctuation, the full stop that was added in front of it), the section "In this repository" together with the blank line after it, and the `tools:` line where one was added.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

## Verification

- 2026-11-22: with the three local additions removed (the "Use proactively" sentence, the section "In this repository" with one blank line, and the `tools:` line), all seven Agency Agents files match the upstream SHA-256 values in the table. In Reality Checker the full stop in front of the sentence was removed as well; the other six upstream descriptions already end in a full stop.
- 2026-11-22: the loading check with `claude -p` was not run during this preparation pass (skipped on purpose to spare memory on a shared machine). The roles are therefore installed but their loading in Claude Code is not yet confirmed. Run the command under "Check that the roles load" in a new session to confirm.

## Delivery kit and loading check (2026-11-22)

- The review gate hook (`.claude/hooks/role_gate.py`, gate roles `Code Reviewer` and `Reality Checker`), `.claude/settings.json`, CI, the pull request and issue templates, the `next-ticket` driver and the `ui-ux-pro-max` and `unslop` skills were installed from the SDLC kit. Two small local additions to role files: Code Reviewer names `docs/ui-quality.md` in its checklist, and Reality Checker says that CI is checked by the driver, not by the role. Everything else in the role files is unchanged since the entries above.
- Loading check, run once from the worktree root with Claude Code 2.1.323, model requested `haiku`: `claude -p "List every project subagent in .claude/agents with its name and tools, say whether each starts with a section titled In this repository, and list the project skills." --model haiku`.
  - Reported 8 project subagents. `Software Architect`, `Application Security Engineer`, `Code Reviewer`, `Reality Checker` and `loop-verifier` reported `Read, Grep, Glob`; this matches the files.
  - Reported no tools field for `Database Reliability Engineer`, `Technical Writer` and `Test Automation Engineer`, which matches the files (these three can edit, by design).
  - The haiku answer contained errors that the files contradict: it said `loop-verifier` has an "In this repository" section (it does not, and it corrected itself), and it said the three editing roles have no `name:` field (each has one). Treat the listing of names and tools as confirmed for the five read-only roles and the section check as confirmed from the files, not from the model.
  - Reported the 8 project skills: `implement-ticket`, `next-ticket`, `issue-triage`, `loop-budget`, `loop-constraints`, `loop-intake`, `ui-ux-pro-max`, `unslop`.
  - Claude Code printed that `Write(**/.claude/...)` ask rules are not matched by file permission checks (only `Edit(...)` rules are) and that it ignored `permissions.allow` because the workspace was not trusted. The second is expected for a headless run in an untrusted worktree.
