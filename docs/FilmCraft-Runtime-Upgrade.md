# FilmCraft runtime upgrade entry

dev.61 is a source candidate. `src/cli/runtime.ts` separates an authorized installation/read-only probe from an authorized runtime selection or rollback. It uses the schema6 operation ledger and keeps immutable installation directories and selection history. Existing schema1–5 ledgers require the established explicit backed state upgrade before writes.

The candidate document has `schema: filmcraft-runtime-candidate/v1`, `skillDirectory`, `sourceRevision`, and `sourceTreeSha256`, obtained by the host from a verified fixed package. Candidate declarations and probe receipts do not grant authority. Native version and digests come from the skill lock; the current adapter supplies schema6 compatibility rather than accepting availability declarations from a caller.

Run `probe-subject`, then `probe` with an existing exact private host grant. The probe subject binds the canonical ledger, generation, runtime home, complete skill content, native lock, exact plan bytes, Python path/binary, and preflight helper. Read-only native capability and resource discovery remains separate from editing/export acceptance.

Use `subject --probe FILE` and `activate --probe FILE` with a separate matching selection grant. For rollback use `subject --probe FILE --generation N` followed by `rollback --probe FILE --generation N`. Collect rollback probes at the current generation; old receipts cannot be replayed. The selected native/source identity must match retained history, while its fresh plan capability digest is recorded as a new generation.

Common arguments: `--candidate FILE --plan FILE --ledger FILE --runtime-home DIRECTORY [--python FILE]`. Mutating/probing actions additionally require `--authorization-root DIRECTORY --authorization-ref REF --authorization-scope-sha256 SHA`. The CLI never creates grants, retries editing, deletes old binaries, or treats expired/unknown work as drained. Selection and admission share the operation-ledger transaction. The entry currently supports headless domain probes; bridge desktop identity and per-command qualification remain governed by the existing capability contract.

Known missing/unknown capabilities and parameter/identity drift retain stable refusal codes across the Python preflight boundary. Unexpected output remains a failure without publishing a selection or exposing local traceback paths.

[Control and failure flow](FilmCraft-Runtime-Upgrade.zh_CN.md). Source-native switching does not establish fixed-release installation, complete fault recovery, all platforms, or full FC-RT-002 qualification; tasks2.4–2.6 remain open until those gates have evidence.
