# FilmCraft V1 — PRD

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81FilmCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81FilmCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/FilmCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. Release goals and non-goals

Build a short film from existing footage with captions and voice-over; reopen the project; replace one shot and export again while preserving untouched clip parameters.

This PRD is a reading view; linked OpenSpec is the behavioral authority. Unimplemented features remain planned. V1 does not build a new editor or multi-tenant cloud.

## 2. Functional requirements

| ID | Requirement | Behavior summary | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| FC-SK-001 | Canonical independent skills | Only immutable skill snapshots may be packaged. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| FC-SK-002 | Standalone skills and dependencies | Standalone distribution must declare executable dependencies. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| FC-RT-001 | Runtime provenance and integrity | Install verified, versioned runtime artifacts atomically. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| FC-RT-002 | Capabilities and isolated upgrades | Version, commands and execution mode are distinct compatibility gates. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| FC-TX-001 | Revision binding and single writer | Reject stale plans and concurrent native-project writers. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-TX-002 | Idempotency and unknown outcome recovery | An acknowledgement or timeout does not establish completion or failure. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-TX-003 | Cancellation and bounded execution | Cancellation requests require execution-side confirmation. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-AR-001 | Artifact lineage and bundle integrity | Paths alone are insufficient evidence of artifact identity. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| FC-AR-002 | Native editability and interchange loss | Preview success cannot prove native editability. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| FC-QA-001 | Separate technical and creative evidence | Each quality claim must identify its evidence and scope. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| FC-QA-002 | Bounded targeted revision | Revisions must target evidence-backed findings within a bounded budget. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| FC-RL-001 | Host and release evidence | Release readiness requires actual host and task evidence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| FC-RL-002 | Permissions and secret boundaries | Reject path escape, unsafe arguments and secret persistence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| FC-DM-001 | Media import and relinking | Register hashes, streams, duration and references for video, images and audio; detect missing files before import and verify hashes when relinking moved assets. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-002 | Exact timeline assembly | Represent in/out points, tracks and ordering with integer ticks and rational timebases; serialize large integers as decimal strings and reject out-of-range clips. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-003 | Audio and voice-over assembly | Preserve separate identities and gains for voice-over, music and source audio; verify output audio and sync; do not synthesize or upload voices without authorization. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-004 | Caption timing and layout | Preserve caption text, language, time ranges and style; reject invalid timing and report font substitution impacts instead of changing fonts silently. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-005 | Project round-trip and local revision | Save and reopen .fcproj, inspect the timeline and revise one shot by stable clip ID without changing other tracks or asset references. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-006 | Preview and final output | Separate proxy preview from native export; decode final outputs and verify dimensions, frame rate, duration and audio; never label an FFmpeg substitute as native export. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. Non-functional requirements

Enforce one project writer, no added side effects for idempotent duplicates, no secrets in receipts, artifact-bound acceptance and detection of plan/GUI changes. Initial limits of three revision rounds and one render per project are unmeasured defaults, not performance results.

## 4. End-to-end acceptance procedure

1. Install locked runtimes and skills in a clean environment.
2. Register fixture assets and expected outputs.
3. Execute and verify native projects and exports.
4. Close and reopen native projects to inspect editability.
5. Apply the representative local change and compare untouched objects.
6. Inject interruption, recover and check for duplicate side effects.
7. Repeat in the target host and record its version.

## 5. Release gates

Every P0 requirement needs positive and negative evidence; unexecuted cases are NOT_RUN. Technical failures, native corruption, digest drift and duplicate submissions block release.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.

Resource acceptance update: the source candidate implements shared durable budgets and explicit cancellation confirmation. Fixed public-tag installed validation is pending; tasks9.19–9.21 and complete V1 remain open.

Fixed dev49/source42 resources and cancellation pass tasks9.19–9.21. Complete product/V1 acceptance remains incomplete with60 open tasks; creative and user acceptance remain NOT_RUN.

The independent quality candidate separates engineering, technical, creative and user acceptance. Scores cannot override technical failures and stale candidate evidence cannot replay. Built-in measurement retains manual readability, continuity and rhythm review. Fixed dev.50 acceptance, tasks9.22–9.24 and full V1 remain open.

Fixed dev.50 quality qualification completes tasks9.22–9.24; see docs/evidence/filmcraft50-fixed-quality-20261008.json. Independent engineering and bounded technical measurements pass. Creative/manual review and user acceptance remain open; this does not qualify user footage or full V1, with57 tasks remaining.

Bounded revision preserves non-targets and dependencies, never automatically replays unknown attempts, and retains verified best plus unresolved findings on stop; no qualifying best is explicitly null. Goal/rubric changes fence the old loop. Creative and user acceptance remain separate. Fixed dev.51 qualification, tasks9.25–9.27 and full V1 remain open.

Fixed dev.51/source42 completes OpenSpec9.25–9.27:126 installed native/state tests without skips,49 matrix records including9 bounded revision cases,13 skills/44 execution files preserved; public protocol validation and all four release CI runs pass. Creative/manual and user acceptance remain open, with54 V1 tasks remaining. docs/evidence/filmcraft51-fixed-revision-20261008.json · docs/evidence/filmcraft51-fixed-revision-20261008.json.

Layered release results bind current commits, inputs, candidates and original logs. Missing real-media, host or platform scenarios remain NOT_RUN. Dev.52/source44 still requires fixed installation and collection; green CI does not qualify user acceptance or full V1.
