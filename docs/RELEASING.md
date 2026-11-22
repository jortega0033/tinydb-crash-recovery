# Releasing

Only the owner releases. Agents never tag, publish or create a release.

## What a release is here

There is no package on PyPI and no deployment. A release is a Git tag on `main` plus a GitHub release whose notes come from `CHANGELOG.md`. Nothing exists to release until epic #1 is finished. No project licence has been chosen (README, "Licensing"); pick one before the first public release. The staged upstream TinyDB source under `third_party/tinydb/` keeps its own MIT licence and attribution.

## Steps

1. Confirm every ticket of the release is merged and CI is green on `main` (Linux and Windows, Python 3.12 and 3.13).
2. From a clean checkout of `main` on Linux, run `python -m unittest discover -s tests -t .` and `python -m pytest third_party/tinydb/tests` and record the tail of each output.
3. Run the documented demo once: `python -m tinydb_journal scenario run <empty directory>`, then `scenario show <directory>`. (Both commands are planned; ticket #2 makes them real.)
4. Check that `docs/verification.md` records the clean-directory run for the release candidate (ticket #7).
5. In `CHANGELOG.md`, rename `Unreleased` to the version and date, and add a fresh empty `Unreleased` section.
6. Merge that change through a pull request.
7. Tag the merge commit (`vX.Y.Z`) and create the GitHub release from the tag with the changelog section as notes.
