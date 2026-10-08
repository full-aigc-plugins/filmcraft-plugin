# FilmCraft — Technical-Plan

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81FilmCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81FilmCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/FilmCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Technical decisions and alternatives

| ADR | Decision and rationale | Alternative and reversal condition |
| :--- | :--- | :--- |
| ADR-001 | Independent skills repositories with immutable snapshots inside plugin packages | Reject sibling symlinks; add host dependency resolution only after it is verified |
| ADR-002 | Reuse official Rust CLIs through controlled MCP/argv | Do not rewrite editors; surface missing APIs before adding adapters |
| ADR-003 | Target TypeScript and Node.js 24 LTS for orchestration, matching ecosystem experience | Pin patch versions and dependencies during implementation; design is not compatibility proof |
| ADR-004 | SQLite ledger and content-addressed files for a local single-user workspace | Revisit service storage only when multi-machine collaboration is required |
| ADR-005 | ArtCraft OpenSpec owns shared task and artifact protocols | Domain repositories own mappings and consumer tests, not competing field definitions |
| ADR-006 | Separate technical gates from creative review; preserve valid existing authorization | Do not require approval per call; obtain new authority only when scope changes |

## 2. Independent skill supply chain

`filmcraft-skills` is an independent published knowledge repository. The plugin vendors source tag `v0.1.0-dev.3`, a fixed commit and the full skill digest recorded in `skills.lock.json`. SKILL.md, references and portable scripts remain owned by the skill repository. `python3 scripts/vendor/skill_vendor.py check --offline` verifies the packaged snapshot; a source release does not imply complete host or creative acceptance.

| Stage | Input | Failure rule |
| :--- | :--- | :--- |
| resolve | repository + immutable tag | Stop on unresolved tags or disallowed provenance |
| verify | commit + tree digests | Reject any content drift |
| package | skills inventory | Reject escaping links and duplicate names |
| audit | clean install fixture | Standalone skill installs must resolve public dependencies |

## 3. Domain plan compilation strategy

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Media import and relinking | Register hashes, streams, duration and references for video, images and audio; detect missing files before import and verify hashes when relinking moved assets. | Planned |
| Exact timeline assembly | Represent in/out points, tracks and ordering with integer ticks and rational timebases; serialize large integers as decimal strings and reject out-of-range clips. | Planned |
| Audio and voice-over assembly | Preserve separate identities and gains for voice-over, music and source audio; verify output audio and sync; do not synthesize or upload voices without authorization. | Planned |
| Caption timing and layout | Preserve caption text, language, time ranges and style; reject invalid timing and report font substitution impacts instead of changing fonts silently. | Planned |
| Project round-trip and local revision | Save and reopen .fcproj, inspect the timeline and revise one shot by stable clip ID without changing other tracks or asset references. | Planned |
| Preview and final output | Separate proxy preview from native export; decode final outputs and verify dimensions, frame rate, duration and audio; never label an FFmpeg substitute as native export. | Planned |

The planner emits a declarative plan. The compiler validates command availability, fields, units and bounds, then emits typed operations. Inspect source objects to obtain real IDs first. Compilation records planHash and capabilitySnapshotHash and returns unsupported_mapping for unsupported operations; only verified mappings reach submission.

## 4. Runtime installation and management

Runtime management separates discover, verify, install, probe, activate, upgrade and rollback. Reuse compatible existing installs after verification. Pin download URLs and digests, reject archive traversal and escaping symlinks, and verify before execution. Versioned installs do not overwrite active binaries and preserve prior receipts. An untested platform is unverified; a universal ZIP does not prove every architecture works.

## 5. Submission, recovery and artifact protocol

Use persisted intent, idempotency keys and single-writer leases. Even synchronous CLIs without external task IDs require attempt IDs, process identity, checkpoints and expected outputs. After process failure, inspect projects and files rather than blindly rerunning. Reconciliation handles the gap between file creation and ledger registration. Validate native projects and exports separately; list non-redistributable dependencies and fonts with verifiable acquisition instructions.

## 6. Test plan and acceptance assets

| Layer | Required coverage | Evidence |
| :--- | :--- | :--- |
| contract | Missing/unknown fields, idempotency and revision conflicts | schema + fixture results |
| adapter | Real command discovery, mode differences and error mapping | runtime identity + transcript |
| recovery | Disconnect after submit, late results and unconfirmed cancellation | ledger before/after + duplicate count |
| native | Build a short film from existing footage with captions and voice-over; reopen the project; replace one shot and export again while preserving untouched clip parameters. | project reopen + output inspection |
| host | Clean host install, upgrade and user-data preserving uninstall | host/version/platform + logs |

## 7. Implementation route

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |

Use dependency order without invented dates or effort estimates. Each OpenSpec task carries a requirement ID, owner role, output and validation. Start with failing behavior tests, implement minimally, and leave tasks unchecked until evidence exists.

## 8. Operations, upgrade and release

Plugin, skills, upstream CLI and protocol versions evolve independently. Release matrices pin their combinations; host manifests and marketplace metadata must match verified commits and locks. The documentation baseline ships no installable plugin package; M4 gates the first installable release. Roll back to a previously verified plugin/skills/CLI combination; restore backups when state migrations are incompatible.

---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.

Exchange delivery now includes exchange-loss.json binding native, reopened inspection and exports by digest. Derivatives never substitute for native projects; cross-editor font, effect and mask fidelity remains explicitly unknown until separate acceptance.

## Current host acceptance

Snapshot `0.1.0-dev.2` has scoped installation/discovery and installed-entrypoint evidence. See [verification contracts and exclusions](../../../docs/FilmCraft-Host-Verification-Architecture.md). Full release tasks remain open; target design sections do not constitute implementation evidence.

## CLI skill suite revision

[FilmCraft CLI / setup / task suite](../../../docs/FilmCraft-Skill-Suite-Architecture.md)

Resource implementation update: the schema4 resource architecture in docs/FilmCraft-Resource-Architecture.md defines persistent reservations, shared continuation budgets and identity-bound POSIX cancellation. Source tests pass; fixed dev49 installed acceptance remains pending. Tasks9.19–9.21 and complete V1 remain open.

Fixed dev49/source42 resource acceptance is now complete for tasks9.19–9.21:81 installed tests without skips,32 matrix records and four release CI runs pass. Full V1 remains open with60 tasks.

Independent quality update: minimal context, trusted host/manual verification, version invalidation and per-channel temporal/audio checks have a source candidate. See docs/FilmCraft-Quality-Architecture.md. Fixed dev.50 installed acceptance, tasks9.22–9.24, user acceptance and full V1 remain open.

Fixed dev.50/source42 independent quality acceptance now completes tasks9.22–9.24:107 installed tests without skips,40 matrix records including8 quality cases,13 skills/40 execution files preserved and four release CI runs pass. Creative review remains manual_review, user acceptance NOT_RUN and57 V1 tasks open.

Bounded revision candidate: schema5 ledger, object/track/time/leaf/dependency scope, fresh independent review and round/failure/budget/stagnation gates. See docs/FilmCraft-Revision-Architecture.md. Fixed dev.51 qualification, tasks9.25–9.27 and full V1 remain open.

Fixed dev.51/source42 completes OpenSpec9.25–9.27:126 installed native/state tests without skips,49 matrix records including9 bounded revision cases,13 skills/44 execution files preserved; public protocol validation and all four release CI runs pass. Creative/manual and user acceptance remain open, with54 V1 tasks remaining. docs/evidence/filmcraft51-fixed-revision-20261008.json · docs/evidence/filmcraft51-fixed-revision-20261008.json.


Fixed dev.52/source dev.44 completes OpenSpec9.28–9.30: source CI181 PASS/36 environment NOT_RUN; all four plugin CI runs succeed; installed native/state126/126 with no skips,273 preflight checks and32 bounded headless/bridge cases. Eleven groups/30 scenarios produce180 layer records:28 PASS and152 NOT_RUN. Collection integrity PASS; overall qualification NOT_PROVEN. Real media, other hosts/platforms, exhaustive commands, creative/user acceptance and full V1 remain open with51 tasks.

证据 / Evidence: docs/evidence/filmcraft52-layered-release-20261008/report.json。

OpenSpec9.31 media input preparation is complete:7 cases and18 source/license/hash-bound inputs, measured VFR and181.211333-second audio;64 Python tests pass. Native matrix9.32 and fixed installed9.33 remain NOT_RUN; full V1 has50 open tasks. See docs/FilmCraft-Media-Matrix.md.

First fixed52/source44 real-derived VFR probe for9.32 saves/exports and fully decodes a3.008-second movie, but independent8kHz mono normalized audio correlation is0.49865, below0.98. Window diagnostics also degrade; root cause remains unconfirmed. Tasks9.32/9.33 stay open and thresholds remain unchanged. Evidence: docs/evidence/filmcraft-media-fixtures-20261008/vfr-native-probe.json.

2026-10-09 development dev.53 pins source dev.45, including fixture preparation and failed-probe evidence. The PCM candidate is outside the default craft.4 installer. Tasks9.32/9.33 and50 full-V1 tasks remain open.

2026-10-09 dev.54 pins source dev.46/public craft.5. Seven candidate native media cases, actual Whisper28 words/100% reference coverage and public native first use pass. New fixed-host/media qualification follows publication; tasks9.32/9.33 and50 full-V1 tasks remain open.

Fixed dev.54/source46/public craft.5 passes all seven native media cases in an actual isolated Codex installation, preserving all13 skill and executable identities. OpenSpec9.32 and9.33 are complete;48 full-V1 tasks remain open. Scope is bounded to current macOS arm64, Codex and codecs; creative, user and other-platform acceptance remain open. [Fixed evidence](../../../docs/evidence/filmcraft54-fixed-media-20261009/report.json).
