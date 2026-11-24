# TinyDB Crash Recovery

> This document specifies phase 1 of the program in [#30](https://github.com/jortega0033/tinydb-crash-recovery/issues/30). Hour figures in it are early estimates for that phase; its open tickets add up to 55 to 80 hours (2026-11-24). Work that it defers is planned in the later phases only where the program names it.

Engineering plan for an opt-in extension to TinyDB. Six future tickets total **19–30 engineering hours**. The prototype, fault harness, and measurements are planned.

## Product requirements

**User and workflow.** A developer uses TinyDB as a local JSON document store and needs to update several documents together. In the demonstration, a single batch moves two items between fictional bins and records an audit event. The developer interrupts the writer at a known point, reopens the store in a fresh process, and inspects the resulting inventory, transaction receipt, and recovery report.

**First usable slice.** Add a single-writer journal mode that writes one batch, exits, and reopens from a fresh process. One CLI scenario exposes before and after data and the committed generation. The first milestone covers the journal format, atomic visibility, and basic process-stop verification. A later milestone adds checkpoint rotation, a bounded secondary index, an explicit legacy import, and an offline report of fault-test results.

**Compatibility and runtime.** Keep TinyDB v4.8.2’s default JSON storage, existing API, and existing tests intact. Journal mode is opt-in through an explicit entry point with a separate on-disk layout. Target CPython 3.12 on Linux and a supported native local filesystem. Check exclusive lock, same-directory atomic replacement, and directory sync in the target before asserting recovery behavior. Build the data path with the Python standard library and the pinned upstream source staged locally. Process-death testing demonstrates recovery after interruption while the OS keeps running. Power loss, damaged storage hardware, network filesystems, multiple writer processes, and in-place conversion of live legacy files are outside this batch.

**Success criteria.** A fault matrix shows acknowledged batches surviving, unacknowledged batches resolving to one complete state, and repeated recovery producing the same state. A complete but corrupt frame stops recovery with a diagnostic. A legacy snapshot imports into a different directory with unchanged source bytes. The indexed lookup and an independent scan return the same document IDs.

## Upstream and technical design

**Reference.** Use TinyDB v4.8.2 at commit `10644a0e07ad180c5b756aba272ee6b0dbd12df8`. GitHub identifies the license at that tag as MIT. Keep the upstream license and required attribution with any copied source. TinyDB’s `Storage` interface reads and writes the database mapping as a whole. Its default `JSONStorage` rewrites a serialized snapshot using a seek, write, sync, and truncate sequence. Table-level writes update the stored mapping and TinyDB’s table search cache is invalidated on writes. The new journal path needs an explicit batch boundary at the database layer to group updates that would otherwise be separate operations. [Pinned source](https://github.com/msiemens/tinydb/tree/10644a0e07ad180c5b756aba272ee6b0dbd12df8) · [MIT license](https://github.com/msiemens/tinydb/blob/v4.8.2/LICENSE) · [Storage](https://github.com/msiemens/tinydb/blob/v4.8.2/tinydb/storages.py) · [Tables](https://github.com/msiemens/tinydb/blob/v4.8.2/tinydb/table.py)

### Boundaries and data contract

- **API.** An opt-in `open_journal(directory)` opens one database. `apply_batch(batch_id, operations)` stages a bounded list of document inserts, replacements, and removals under that handle. An operation identifies a table and a positive integer document ID. A commit returns the application batch ID and committed generation. Explicit IDs keep the first version’s replay deterministic. Queries on the handle read the current committed view. The initial journal API accepts JSON data and a short caller-generated batch ID. Avoid arbitrary callable predicates or callbacks inside the batch.
- **Visibility and validation.** One exclusive advisory lock guards one app-owned directory from open through close. Acquire it before any read, write, or recovery and return a clear busy error to a second opener. Serialize operations through the owning handle. Check all operations against a candidate snapshot before writing. Stage indexes with the candidate or invalidate them until rebuilt. Copy values in and out so callers cannot mutate the live view through a returned object. Validation failures leave the committed generation and journal unchanged.
- **Layout.** The app directory contains a permanent lock file, a versioned checkpoint, and one write-ahead log. A database ID in the checkpoint and log header prevents mixing files between stores. The checkpoint contains the baseline generation, document mapping, and batch receipts. The log uses a fixed header and bounded frames. Each frame contains payload length, a checksum, and a UTF-8 JSON payload with schema version, batch ID, prior and next generation, and the ordered operations. Freeze the exact byte order and framing in the first ticket and reject malformed lengths before allocation. Start with a 1 MiB frame cap, 100 operations per batch, and a documented cap on stored receipts. Reject further unique batches before reaching the receipt cap until a supported export or policy change is available.
- **Commit and retry.** Append a complete validated frame, flush it, and sync the log file before publishing the new in-memory view or returning a receipt. A batch ID replay with the same canonical payload returns the original receipt and writes no frame. Reusing an ID with a different payload produces a conflict. Persist receipt identity and payload fingerprints through checkpoints. If a write or sync errors after append starts, return an outcome-unknown error, block further mutation on that handle, and require reopen before retry. [Python file sync](https://docs.python.org/3.12/library/os.html#os.fsync) · [Python file locking](https://docs.python.org/3.12/library/fcntl.html#fcntl.flock)

### Recovery and checkpoints

1. Lock the store and load the last complete checkpoint. Check format, database ID and integrity. Inspect the log header and validate each complete frame in order. Apply each batch to a fresh candidate and publish it as a unit. Reject mismatched IDs, generation gaps, conflicting receipts, unknown formats, and complete frames with invalid checksums. A partial final frame at verified EOF can be discarded. Keep evidence and refuse mutation when the boundary is ambiguous.
2. Publish the effective recovered generation and its receipts. Verify that opening twice yields the same canonical data and generation. Report whether recovery replayed a suffix, discarded a partial tail, or stopped on corruption.
3. To checkpoint, write a temporary snapshot in the same directory, flush and sync it, replace the checkpoint atomically, and sync the parent directory before replacing the log with a synced empty segment starting at the new checkpoint generation. Hold the lock during the transition. A crash after checkpoint replacement can leave the old valid log. Verify its header and generation chain. Skip a covered record only when its generation and receipt fingerprint agree with the checkpoint. Reject a new log whose starting generation is ahead of the checkpoint. Temporary artifacts have no authority on restart.

### Indexing and migration

The opt-in mode adds an explicit indexed lookup for equality on selected top-level string fields. Index entries map a field value to stable document IDs. Missing fields stay distinct from empty strings. Perform scans for all other query forms. Use the committed generation to check index validity and rebuild after recovery. Existing TinyDB query semantics remain those of the pinned version. Avoid relying on private query cache internals as the correctness mechanism.

Import reads a closed, valid legacy TinyDB JSON snapshot, checks table names, JSON types, canonical positive decimal document IDs, and collisions after normalization, then initializes a new journal directory headed by a checkpoint. Reject malformed input before publishing the destination. Keep the original file for independent rollback. Provide a read-only report command for the selected journal generation. The report uses generated example files and runs locally.

## Fixture and verification

Use a derived checkable fixture with `bins/F01 = 7` and `bins/F02 = 3` as display labels. Use positive document IDs `1` and `2` in the `bins` table. A single batch with ID `move-001` replaces both counts with `5` and creates movement document `1` in a second table. Before commit, counts are `7, 3` with zero movement rows. After commit, counts are `5, 5` with one movement row. The total is always `10`. The exact same batch ID and payload must retain one movement row and one generation increase.

Record an independent expected state from acknowledged receipts and the fixture operations. Use a controller that launches only its own writer subprocess in a disposable native local directory. The child reports phase boundaries through a dedicated control pipe and waits at a selected test hook. The controller interrupts that child at each boundary, then reads the store in a fresh process. Cover exit before append, partial frame, full frame before sync, durable frame before receipt, received receipt, checkpoint replacement before log rotation, and log rotation followed by restart. Run positive and negative fixtures separately so a genuine corrupt complete frame is never treated like an interrupted tail.

For any interruption before a complete frame exists, expect the old complete tuple. At and after the barrier that confirms the log sync returned successfully, expect the new complete tuple even when no receipt was observed. For a full frame interrupted before that barrier, accept either complete tuple according to the bytes recovery validates. In either unacknowledged case, verify the next retry creates exactly one effective transaction. Report each trial’s seed, interruption phase, receipt observed, recovered tuple and generation, rejection reason if any, and filesystem. Test bounds and scope are planned and must be measured on the host.

## Epic E89 · Recover atomic TinyDB batches after process interruption

A developer can demonstrate safe interruption, reopen, and retry of the synthetic inventory transfer. The epic is done when the existing TinyDB suite passes in the pinned environment, all supported fault cases match the independent oracle, legacy import preserves source bytes, and indexed queries agree with scans after writes and recovery.

| Ticket | Dependency | Remaining estimate |
|---|---|---:|
| E89-1 Opt-in store and legacy seam | — | 3–5 h |
| E89-2 Framed journal and durable batch receipts | E89-1 | 4–6 h |
| E89-3 Recovery and safe checkpoint rotation | E89-2 | 3–5 h |
| E89-4 Explicit import and indexed equality lookup | E89-1, E89-2 | 3–4 h |
| E89-5 Controlled subprocess interruption harness | E89-2, E89-3 | 3–5 h |
| E89-6 Offline report and clean-machine verification | E89-3, E89-4, E89-5 | 3–5 h |

**Batch order.** Freeze the API and directory contract in E89-1. After E89-2 freezes the commit format, E89-3 and E89-4 can proceed in parallel. Keep checkpoint writing with E89-3 and hand E89-4 a checkpoint initialization interface. E89-5 can develop its phase-control test fixtures against the E89-2 contract, then run the full crash matrix after E89-3. E89-6 integrates the checks and documents the findings.

### E89-1 · Opt-in store and legacy seam

Define the transaction facade, error/result states, import boundaries and single-owner locking. Add the synthetic scenario and a reference oracle. Confirm upstream’s tests can run from local inputs. An unmodified legacy client still opens its original JSON. Two processes opening the same journal directory yield one owner and one busy error. A new owner can reopen after the first process exits. Verify with distinct child processes and a clean legacy fixture.

### E89-2 · Framed journal and durable batch receipts

Validate staged batches, serialize a bounded frame, sync before acknowledgement and publish one generation. Include stable receipt lookup and conflicting ID detection. The inventory transfer updates both bin counts and the audit table together. An invalid middle operation produces no change. Retrying the same payload returns the first receipt and an altered payload for that ID fails. Verify the file length and generation after each outcome.

### E89-3 · Recovery and safe checkpoint rotation

Validate frames, replay complete batches, reclaim an unambiguous partial tail and reject corruption. Implement checkpoint publication and covered-generation checks. A truncated last frame preserves the prior complete transaction. A complete frame with a deliberately altered payload but stale checksum causes a diagnostic and leaves evidence intact. An interrupted checkpoint rotation recovers the same generation on two opens. Verify these cases on a native local Linux filesystem.

### E89-4 · Explicit import and indexed equality lookup

Import a validated legacy snapshot into a separate destination and implement bounded string-field equality indexing with a scan fallback. Compare the original legacy file checksum before and after import. Check that same-value documents retain all IDs, an update changes membership exactly once, a removal disappears, and a reopened store matches a full scan. Include missing and empty string fixtures. Run established legacy queries against the imported view where their semantics are supported.

### E89-5 · Controlled subprocess interruption harness

Implement named child-process barriers and the independent crash oracle. Run each documented boundary on owned scratch directories. Prove no mixed inventory tuple, no missing observed receipt, no duplicate movement after retry, and no additional change after a second recovery. Start with one repeatable scenario per boundary before adding a seeded trial set. Report observed trial counts and errors without extrapolating durability guarantees.

### E89-6 · Offline report and clean-machine verification

Create a readable local CLI report for completed trials with failure phase, recovered generation, and reproducible seed, plus an optional static HTML view served locally. Document preparation, setup, offline commands, test scope and limitations. From a clean directory, run the unchanged legacy suite, complete the synthetic scenario, interrupt a fresh run, and read back the recovery evidence. Report indexed scan timings with identical fixtures if measured and leave any unsupported performance target as future work.

## Open implementation checks

Confirm native Linux filesystem support in the target. Stage the licensed upstream code and the pinned test runner before offline work. Measure the fixture on the actual filesystem and record OS, Python version, and interruptions exercised. Keep retention caps and unsupported migration cases visible. Record the engineering estimate separately from actual work.
