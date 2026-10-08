# FilmCraft fixed installed recovery acceptance

[简体中文](FilmCraft-Fixed-Recovery.zh_CN.md). Existing OpenSpec FC-TX-002 remains authoritative. This qualification closes9.16–9.18; broader gates such as3.4–3.6 do not close automatically.

Public plugin dev.48 / `a891fd663667029362a3dd7982e86b88be0cf51f` retains skills dev.42 / `7adfa763b161bc2ff7ef3efae702e285965bf23a`. Isolated Codex0.147.0 on macOS arm64 discovers13 skills without loading errors. Thirty installed execution files and installed test sources match fixed Git objects and remain unchanged after execution. A fresh native runtime passes60 installed tests without skips. Source native tests pass60; Python tests pass45.

| Scenario | Source candidate | Fixed install | Evidence layer |
| :--- | :--- | :--- | :--- |
| `readonly-wal-and-missing-receipts` | PASS | PASS | synthetic receipts; actual SQLite WAL |
| `missing-and-damaged-ledgers` | PASS | PASS | synthetic damaged SQLite bytes |
| `lost-reply-and-old-epoch` | PASS | PASS | synthetic native receipts; actual stopped process |
| `expired-recovery-owner` | PASS | PASS | actual SQLite fences with controlled time |
| `repeat-repair` | PASS | PASS | synthetic native receipts |
| `two-recovery-executors` | PASS | PASS | two actual Node processes; synthetic native receipts |
| `host-exited-child-alive` | PASS | PASS | actual exited Node host and detached controlled Node child; not native editing |
| `schema1-upgrade-rollback` | PASS | PASS | actual SQLite maintenance; synthetic operation records |
| `schema2-upgrade-rollback` | PASS | PASS | actual SQLite maintenance; synthetic operation records |
| `rollback-preserves-new-records` | PASS | PASS | actual SQLite with synthetic new task |
| `inspection-concurrent-write` | PASS | PASS | actual concurrent SQLite commit during isolated observation |
| `actual-native-repair-and-continuation` | PASS | PASS | actual Python/native create, lost reply, repair and continued editing; actual private host grants |
| `actual-previous-version-downgrade-refusal` | PASS | PASS | actual fixed dev45 installed core versus current schema3 SQLite fixture |
| `expired-revoked-authorization` | PASS | PASS | synthetic receipts; actual authorization gates |

Seven read-only windows compare original DB/WAL/SHM, receipt and project inventories/bytes. Supplemental fixture SQL reads occur after the preservation window, preventing SHM read-mark changes from being attributed to diagnosis. Two real repair executors apply only one intent. Actual exited-host/live-controlled-child cases and synthetic receipts are labelled separately.

Actual native continuation binds the current parent project: one child attempt and one continuation intent, while the parent retains one attempt without replay. Repeated API and CLI requests reuse the child. Schema1/2 each pass backed upgrade to3 and compatible rollback, retaining logical task/attempt/receipt/unknown-occupancy digests. New records and actual installed dev.45 downgrade are rejected without changing original files. This qualifies state-schema maintenance, not native binary upgrades/draining.

Three public tasks and26 artifacts validate against the pinned ArtCraft v0.1.0-dev.109 schemas. Release main/tag documentation and implementation workflows all pass (four runs). CI Node units pass58 with2 explicit specialized-environment skips; the separate installed matrix passes60 with0 skips. These evidence layers stay separate.

Failed dev.46 relative-path and dev.47 observation-window collections remain recorded and did not close tasks; original tags/ZIPs are unchanged. Original byte digests and sanitized public projection digests are separate; private ledgers/media/grants are not committed. Complete Harness/public admission, authorization configuration, budgets/cancellation, native runtime upgrades, static type checking, other platforms and quality/user acceptance remain open. V1 has63 open tasks; specs remain unsynced/unarchived.

[Fixed evidence / 固定证据](evidence/filmcraft48-fixed-recovery-20261008.json). [Architecture / 架构](FilmCraft-Recovery-Architecture.md).

dev.58 adds per-scenario recovery evidence gates. Fixed dev.57 passes133 installed tests without skips,47 total matrix rows including14 required recovery rows and all10 FC-TX-002 scenario checks. Missing/duplicate evidence, changed originals, duplicate repair, expired epochs, live-child occupancy and incomplete backups are checked. Synthetic receipts, actual SQLite/controlled processes and actual native continuation are separate layers. New fixed58 qualification is pending;3.4–3.6 and45 full-V1 tasks remain open. [Evidence](evidence/filmcraft58-recovery-candidate-20261009/contract.json).

Fixed dev.58/source46/craft.5 recovery qualification passes133 installed tests without skips,14 required recovery matrix cases and all10 FC-TX-002 scenarios, preserving13 skills and executable identities. Existing target-red evidence and current implementation are verified; OpenSpec3.4–3.6 are complete, with42 full-V1 tasks open. Actual native lost handoff/continuation, SQLite faults, controlled processes and synthetic receipts are separately labelled. Scope is macOS arm64 Codex/headless; other platforms, native binary upgrades, creative and user acceptance remain open. [Evidence](evidence/filmcraft58-fixed-recovery-20261009/acceptance.json).
