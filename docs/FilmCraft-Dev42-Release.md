# FilmCraft dev.42 Development Release Verification

Versions: plugin `0.1.0-dev.42`, independent skills `v0.1.0-dev.39` / `6c29e50b5fe85f98a1c5f77977158bb1b00bde5a`. [中文](FilmCraft-Dev42-Release.zh_CN.md). [OpenSpec](../openspec/changes/establish-v1-plugin/specs/) remains the behavioral authority; publication does not complete open implementation tasks.

## Scope

Shared parameter validation, task routing and capability snapshots for 13 independent skills are synchronized from their published immutable tag. The plugin does not maintain another source implementation. The Node.js 24 / SQLite Harness wraps existing Python native workflows and links tasks, attempts and original receipts, adding read-only diagnosis and fenced state repair. Eleven Dreamina comparison groups and 33 tasks retain their individual evidence gates, including recovery preservation, concurrency, repeated repairs and state compatibility.

## Recovery boundaries

Both `inspect` and `reconcile` are read-only: database and WAL copies are checked in an isolated directory without opening the original SHM or creating original-location files. Original digests are compared before and after diagnosis. Inconsistent reads, missing/corrupt evidence or unknown process identity retain unknown and occupancy. Snapshot files currently have a 64 MiB limit; this does not qualify large ledgers or adversarial filesystem races.

`repair` only repairs the state of an original attempt whose completion is established. It checks fresh diagnostic digests, epoch and existing authorization references, persists a recovery intent, and rechecks process/receipt evidence. It enters verifying without replaying native edits or approving quality. Competing or expired owners cannot apply the same intent twice; a fresh repeated repair reuses the existing result. Reference equality does not implement host authorization-scope enforcement.

```bash
node src/cli/recovery.ts inspect --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK"
node src/cli/recovery.ts reconcile --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK"
node src/cli/recovery.ts repair --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK" --expected-epoch "$EPOCH" --inspection-sha256 "$INSPECTION_SHA256" --authorization-ref "$AUTHORIZATION_REF" --authorization-scope-sha256 "$AUTHORIZATION_SCOPE_SHA256"
```

Read-only access supports schema v1/v2 without migration. Writers can upgrade recognized v1 while retaining task/attempt records; foreign or unknown versions are rejected. Complete backup, upgrade, rollback and continuation acceptance remains open; bounded migration tests do not close those requirements.

## Verification and remaining scope

Current commands, file digests, layered results and original logs are recorded in the [dev.42 bound report](evidence/filmcraft-dev42-release-20261008.json). Offline source regression, plugin regression and independent-source/vendored native verification are separate. Running vendored skills is not host installation. Actual fault injection loses receipt transfer after native export and checks read-only preservation and same-attempt repair; synthetic receipt tests are not presented as native acceptance.

The historical Harness report retains its original source digests and cannot verify changed release code. This report does not qualify TypeScript static typechecking, actual CI, host installation, complete headless/bridge or Windows support, authorization enforcement, budgets/cancellation, independent quality, user acceptance, complete media matrices or V1. The reference command catalog/runtime identity mismatch remains visible. There are 72 open tasks; no completed-main-spec synchronization, archival or installable-marketplace entry is claimed.
