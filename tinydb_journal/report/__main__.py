"""python -m tinydb_journal.report is not an entry point; use python -m tinydb_journal report."""

import sys

print("use: python -m tinydb_journal report trials|journal <directory>", file=sys.stderr)
sys.exit(2)
