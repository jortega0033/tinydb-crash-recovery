# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## Status and commands

The repository is planning only: no application code and no tests. CI exists (gate self-test now; test steps switch on with ticket #2). Every command in `CLAUDE.md` is planned and is introduced by the ticket it names. Do not report a check as passed that was never run.

Planned test command (introduced by ticket #2): `python -m unittest discover -s tests -t .` (`python3` on Linux). Python 3.12 target, standard library plus the pinned upstream TinyDB source only. Do not add runtime dependencies.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no loop workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.
