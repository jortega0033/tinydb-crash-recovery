---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Started only by the owner; starting it is the go signal.
disable-model-invocation: true
argument-hint: "[issue number]"
---

# Next ticket

Run one ticket of epic #1 (TinyDB Crash Recovery: complete the offline workflow) from the queue to a ready pull request. The owner starts this with `/next-ticket` or `/next-ticket <issue number>`. That is the go signal: nothing here starts by itself, and there is no scheduler.

One ticket per run. Never merge. Never start another run.

## Steps

1. **Refresh the queue.** `gh issue list --label status:blocked --state open` and read epic #1. A `status:blocked` ticket whose blockers are all closed becomes `status:ready` (`gh issue edit <n> --add-label status:ready --remove-label status:blocked`). A parent whose sub-issues are all closed is closed with a comment.
2. **Pick the ticket.** Work is a leaf ticket: one labelled neither `tracking` nor having open sub-issues. With an argument, use that issue (stop and say so if it is closed, `status:in-progress`, `needs-decision` or still blocked; if it is a `tracking` parent, refuse and list its open sub-issues). Without one, take the first `status:ready` leaf ticket in the epic's dependency order (the order of the table in the epic body, then the order of sub-issues inside a parent) that is neither `status:in-progress` nor `needs-decision`. If none qualifies, report the queue and stop.
3. **Claim it.** Add the label `status:in-progress` and remove `status:ready`.
4. **Branch in a fresh worktree.** `git fetch origin`, then `git worktree add ../tinydb-crash-recovery-<issue-number> -b ticket-<issue-number>-<short-slug> origin/main`. Work only there.
5. **Run the playbook** [`.claude/skills/implement-ticket/SKILL.md`](../implement-ticket/SKILL.md) for that issue, with the rules in `CLAUDE.md`. Order: local checks pass and their output is recorded, Code Reviewer, Reality Checker, `gh pr create --draft`, CI, then ready. Code Reviewer and Reality Checker have no shell: before calling them write the diff and the local evidence to `.claude/state/review/` in the ticket worktree (`git diff --stat origin/main...HEAD`, `git diff origin/main...HEAD`, the check outputs) and name those files in the request. Reality Checker checks that the documented checks ran locally and passed and that CI is configured to run them; it does not need a CI result.
6. **Wait for CI without polling.** After `gh pr create --draft` and `git push`, bind the pull request to the session if the app offers it, and end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When the session wakes (a CI event, or the owner says "continue"), read `gh pr checks <n>` once: green, go to step 7; red, fix, re-run the local checks and both gates, push, and end the turn again; still running, end the turn again with the same line.
7. **Ready.** When CI is green on the draft: `gh pr ready <number>` (the gate hook checks again), then comment on the issue with the pull request link and the CI run link. The pull request of the last open sub-issue of a parent says `Closes #<sub-issue>` and `Closes #<parent>`. Leave the `status:in-progress` label in place; the owner merges and closes.
8. **Stop.** Report the pull request, the evidence, the roles that ran and anything not verified. List acceptance steps the ticket marks as manual under "Owner checks" in the pull request; do as much of such a step as an agent can (a scripted run, with the evidence).

## Stop and say so when

- The ticket names an owner decision with no stated default (`needs-decision`).
- A decision in `docs/owner-decisions.md` blocks the ticket.
- The ticket would need a runtime dependency, an external request or network use, a change to the on-disk format or commit order that the ticket does not authorise, a change to `third_party/tinydb/`, or a claim of durability beyond process death.

Labels used: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking`.
