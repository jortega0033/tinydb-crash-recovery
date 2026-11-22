## Ticket

Closes #

<!-- The pull request of the last open sub-issue of a parent also says "Closes #<parent>". -->

## What changed

## Evidence

Each command that was run and its result (Python version, operating system and filesystem included). Name skipped tests as skipped. For behaviour that only runs on Linux, say where it ran and link the run.

| Command | Result |
|---|---|
| `python -m unittest discover -s tests -t .` | |
| `python -m pytest third_party/tinydb/tests` | |

## Agent roles run

| Role | What it was asked | Verdict |
|---|---|---|
| Code Reviewer | | |
| Reality Checker | | |

## Owner checks

Acceptance steps that need a person, if the ticket marks any as manual. Otherwise write "none".

## Risks and rollback

## Checklist

- [ ] Every acceptance criterion in the ticket is covered by a test or a recorded manual step
- [ ] `CHANGELOG.md` has a line for this change
- [ ] `CLAUDE.md` and `docs/` are updated where a command, path or contract changed
- [ ] No runtime dependency, external request or network use was added; upstream source under `third_party/` is unmodified
- [ ] No claim of durability beyond process death
- [ ] Documentation and pull request text went through the `unslop` skill
- [ ] CI is green on this pull request
