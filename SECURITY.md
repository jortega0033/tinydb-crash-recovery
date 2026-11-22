# Security policy

## Reporting a vulnerability

Report it privately through GitHub: open the repository's Security tab and choose "Report a vulnerability". Do not open a public issue or pull request for a vulnerability.

Include the affected command, the steps to reproduce it, and the Python version, operating system and filesystem you used.

## Supported versions

Only the default branch (`main`) is supported. The project has no tagged release yet.

## Scope worth reporting

The journal reader parses bytes from disk (frames, checkpoints, legacy JSON files). A crafted file that makes the reader allocate beyond the documented caps, accept a frame with a bad checksum, execute code, or write outside its own directory is a vulnerability. So is a way for a second process to write to a journal directory while another process owns it.

Out of scope, as stated in `docs/PRD.md`: power loss, damaged storage hardware, network filesystems and multiple writer processes.
