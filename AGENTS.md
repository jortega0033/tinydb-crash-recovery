# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## Status and commands

The repository is a scaffold: toolchain, empty modules, CLI stubs and a smoke test, no product behaviour. CI runs the own tests and the gate self-test; the upstream-suite steps switch on with ticket #10. Commands in `CLAUDE.md` marked planned are introduced by the ticket they name. Do not report a check as passed that was never run.

Test command (real): `python -m unittest discover -s tests -t .` (`python3` on Linux). Python 3.12 target, standard library plus the pinned upstream TinyDB source only. Do not add runtime dependencies.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no loop workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.
