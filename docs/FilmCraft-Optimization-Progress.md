# FilmCraft Optimization Implementation Record

This record covers source candidates and subsequent fixed-install acceptance. The full objective remains completion of all planned skill and plugin tasks. [中文](FilmCraft-Optimization-Progress.zh_CN.md). [Existing OpenSpec tasks](../openspec/changes/establish-v1-plugin/tasks.md) remain authoritative; this record does not narrow acceptance gates.

## Current fixed acceptance

Plugin dev.44 / skills dev.41 renewed fixed identity task 9.6: current catalog identity MATCH, full qualification NOT_PROVEN. See [identity evidence](FilmCraft-Command-Parity.md). P0 task 9.3 also completed fixed entry parity and the six-dimension command matrix: 390 public CLI cases, 1494 tick parameter cases and six real-reference rejections pass. Exhaustive commands, other parameter types, modes/platforms and model routing remain open. See [entry and matrix evidence](FilmCraft-Command-Parity.md).

The sections below retain the initial dev.41 source-candidate state, including its old catalog MISMATCH, test counts and then-unrun CI. They do not describe the current snapshot. Later dev.42/43 recovery, actual installation and CI results retain their own version-bound evidence.

Task 9.12 [fixed capability acceptance](FilmCraft-Fixed-Capabilities.md) is complete: actual dev.44/source41 installed files passed 273 public preflight cases, 32 headless/owned bridge command cases and 13 domain workflow cases. Three missing/controlled-unknown resource kinds, preservation, failure-stage capability digests and reprobe after an actual isolated model download are verified. Other platforms, exhaustive commands, model inference quality and complete isolated upgrade/drain/rollback remain open.

## Initial candidate implementation (historical)

The independent skill source reuses `commands.validate_tick_parameters` in `native_workflow.validate`. Preflight permits return-value references, with exact integers checked again after resolution and before execution. Invalid literals fail before installation or output writes; invalid references fail before dependent native requests. Wrong plan entry points explain the correct runner. Explicit conversion from domain string timing remains valid. The shared generator synchronizes 13 self-contained copies.

Each of the 13 skills now has a local task playbook for inputs, first use, failures, targeted revisions, and verification. Shared synchronization excludes these task-specific files. The generic CLI description targets explicit native commands and advanced operations; unrelated skills no longer automatically load multicam guidance. The intent corpus records expected and rejected primary skills. Passing structural checks does not establish actual host-model routing acceptance.

The plugin adds `scripts/current_facts.py` to generate `docs/current-facts.json` and bilingual README blocks from the pinned source lock, a suite snapshot from that fixed source, command catalogs, and runtime identities. Documentation validation runs `--check`. The root runtime lock is historical; standalone execution and bridge desktop identities are shown separately. Historical evidence does not establish full current-combination acceptance.

## Initial candidate discrepancies (historical dev.41)

Capability source-candidate tasks 9.10/9.11 are complete: optional `requires` declarations fail before installation/writes when malformed, while snapshots bind actual CLI/desktop identities, parameter-documentation digests, modes, and platforms. Native read-only queries probe codecs, fonts, and models in the editing context. Dependent calls recheck contracts and changed resources; missing or unknown prerequisites block edits. Command receipts retain blocked attempts, and successful/failed domain stages preserve manifest-bound capability files. See [capability evidence](evidence/filmcraft-capability-candidate-20261008.json) for 20 capability unit tests and native source/input/artifact bindings. The full source suite executed 165 passing tests with 36 conditional skips out of 201; explicit headless, workflow create/revision, and owned bridge cold save/reopen/contract-rejection samples ran separately.

The live bridge snapshot exposes parameter-documentation drift for `file.importImageSequence` relative to the current CLI. A plan requiring it was rejected before the first edit, and owned desktop processes stopped normally. Representative success does not qualify the complete bridge catalog. Task 9.12 remains open for new pinned installations and the full mode/platform matrix, as do isolated upgrade, draining, and state-compatible rollback gates.

The pinned `references/commands.json` still records an older executable digest, while the active runtime lock and native snapshot identify craft.4. All 666 parameter texts match the existing native snapshot. Current facts explicitly show MISMATCH. The pinned skill snapshot has not been rewritten. Verify the actual catalog, correct metadata in the independent source, then publish and qualify a new pinned snapshot; replacing an old digest alone cannot prove current acceptance.

## Initial candidate verification and remaining scope (historical)

Node/SQLite Harness and receipt lineage have a [source candidate](FilmCraft-Harness-Candidate.md), bound by [candidate evidence](evidence/filmcraft-harness-candidate-20261008.json). Tasks/attempts, project and canonical output occupancy, leases/epochs, original-byte CAS and four legacy mappings now wrap the existing Python workflow. Actual creation, revision, original preservation, input-conflict rejection before registration/edits, alias targets and idempotent reuse pass. All 22 native Node tests and 28 plugin Python regressions pass without skips. Fixed ArtCraft schemas validate two tasks and 13 artifacts, rejecting five invalid mapping classes.

Execution reaches verifying only; technical, creative and user acceptance remain NOT_RUN. CI no longer conditionally skips npm test based on package.json, but actual GitHub CI and TypeScript static typechecking have not run. The one native skip in ordinary npm test has a separate explicit native execution. Fixed-install prerequisite 9.12 and complete acceptance of 9.13—9.15 remain unmet; those tasks stay unchecked. Diagnostics/recovery, authorization-scope enforcement, budgets, cancellation and quality loops still require implementation and fault-injection acceptance.

See [candidate evidence](evidence/filmcraft-optimization-candidate-20261008.json) for version and test scopes. Native tests establish only their bounded tasks and execution-script digests. They do not qualify the new guides or fact generator as fixed-install, host, or exhaustive-command acceptance.

Continue with pinned-install and full compatibility qualification of capability and receipt candidates, complete Node/SQLite single-writer/recovery/resource contracts, independent review, restricted revisions, real media, and layered release verification. New pinned releases, actual hosts, exhaustive commands, and full V1 remain open. Check tasks only when their own implementation and verification evidence exists.
