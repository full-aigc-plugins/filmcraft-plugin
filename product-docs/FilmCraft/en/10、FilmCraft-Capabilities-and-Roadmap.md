# FilmCraft — Capabilities-and-Roadmap

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81FilmCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81FilmCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/FilmCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Capability entrypoints

| Entry | Purpose | Version |
| :--- | :--- | :--- |
| filmcraft-use | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-setup | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-inspect | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-media | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-timeline | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-audio | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-subtitles | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-preview | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-export | Domain knowledge or workflow entry; currently planned | V1 |
| filmcraft-recover | Domain knowledge or workflow entry; currently planned | V1 |


## 2. Functional scope

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Media import and relinking | Register hashes, streams, duration and references for video, images and audio; detect missing files before import and verify hashes when relinking moved assets. | Planned |
| Exact timeline assembly | Represent in/out points, tracks and ordering with integer ticks and rational timebases; serialize large integers as decimal strings and reject out-of-range clips. | Planned |
| Audio and voice-over assembly | Preserve separate identities and gains for voice-over, music and source audio; verify output audio and sync; do not synthesize or upload voices without authorization. | Planned |
| Caption timing and layout | Preserve caption text, language, time ranges and style; reject invalid timing and report font substitution impacts instead of changing fonts silently. | Planned |
| Project round-trip and local revision | Save and reopen .fcproj, inspect the timeline and revise one shot by stable clip ID without changing other tracks or asset references. | Planned |
| Preview and final output | Separate proxy preview from native export; decode final outputs and verify dimensions, frame rate, duration and audio; never label an FFmpeg substitute as native export. | Planned |


## 3. Navigation and routing

Route single-domain requests directly and mixed scenarios to ArtCraft. Inspect before execution and return bounded availability when capabilities are missing. Choose executors by requested native format, not silent substitution. Lifecycle operations are shared; concrete commands are adapter-specific.

## 4. Release cadence

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |




---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
