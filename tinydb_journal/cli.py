"""Command line entry points; every command not built yet exits non-zero and names its ticket."""

import argparse
import sys

from . import __version__

# command words -> ticket that builds it (see CLAUDE.md "Commands")
PLANNED = {
    ("scenario", "run"): 13,
    ("scenario", "show"): 13,
    ("import",): 23,
    ("report", "trials"): 27,
    ("report", "journal"): 28,
}


def not_implemented(ticket: int) -> int:
    print(f"not implemented yet: see #{ticket}", file=sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tinydb_journal", description=__doc__)
    parser.add_argument("--version", action="version", version=f"tinydb_journal {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="command")
    scenario = sub.add_parser("scenario", help="run or show the move-001 demo scenario")
    ssub = scenario.add_subparsers(dest="action", metavar="action", required=True)
    for name in ("run", "show"):
        ssub.add_parser(name, help=f"scenario {name} <directory>").add_argument("directory")
    imp = sub.add_parser("import", help="import <legacy.json> <new-directory>")
    imp.add_argument("legacy")
    imp.add_argument("directory")
    report = sub.add_parser("report", help="read-only reports")
    rsub = report.add_subparsers(dest="action", metavar="action", required=True)
    for name in ("trials", "journal"):
        rsub.add_parser(name, help=f"report {name} <directory>").add_argument("directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    key = (args.command,) if args.command == "import" else (args.command, args.action)
    return not_implemented(PLANNED[key])
