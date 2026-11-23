"""python -m tinydb_journal.harness entry point (run --seed <n> --out <directory>)."""

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tinydb_journal.harness", description=__doc__)
    sub = parser.add_subparsers(dest="command", metavar="command", required=True)
    run = sub.add_parser("run", help="run seeded interruption trials")
    run.add_argument("--seed", type=int, required=True)
    run.add_argument("--out", required=True)
    parser.parse_args(argv)
    print("not implemented yet: see #26", file=sys.stderr)
    return 2


sys.exit(main())
