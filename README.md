# FilmCraft Agent Plugin

Independent-skills-driven Editable video editing and audiovisual assembly.

[English](README.md) | [简体中文](README.zh-CN.md)

## Current release and reproducible host checks

Previously verified plugin/skill suite: `0.1.0-dev.3`. Codex 0.147.0 and 0.153.4 installed five fixed public releases and discovered all 58 enabled namespaced skills with zero loading errors and matching source digests. Five representative workflows passed through installed task-skill entrypoints on 0.147.0, including native projects, targeted revisions and the mixed ArtCraft online workflow. Model dispatch, desktop GUI, final creative review and full interchange fidelity remain unverified.

[Host verification design](docs/FilmCraft-Host-Verification-Architecture.md) · [Version-bound evidence](docs/evidence/codex-skill-suite.json). Historical milestones below retain their original scope; the current manifest and locks own version identity.

> Development release. Fixed-tag Codex installation, skill discovery and representative native workflows have passed; complete product and creative acceptance remain open.

Implementation has started in the independent skills package. The isolated first-use installer is tested on macOS arm64; complete creative workflows and plugin host acceptance remain pending. [Evidence](docs/evidence/bootstrap-tests.json)

## Positioning

Build a short film from existing footage with captions and voice-over; reopen the project; replace one shot and export again while preserving untouched clip parameters.

For creators who need editable native projects, repeatable revisions and reliable automation.

## At a glance

```text
Intent + assets
  -> independent Skills (pinned development release)
  -> public skill workflow / ArtCraft adapter
  -> verified runtime / child adapter
  -> native project + preview + export + evidence
```
| Property | Value |
| :--- | :--- |
| Plugin ID | filmcraft |
| Metadata version | 0.1.0-dev.5 |
| Stage | implementation-in-progress |
| Skills source | filmcraft-skills / v0.1.0-dev.4 |
| Execution | Upstream CLI; ArtCraft uses child adapters |
| Host compatibility | Codex development install/discovery pass; GUI and other hosts pending |
| License | Apache-2.0 (original repository content) |


## Capabilities and boundaries

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Media import and relinking | Register hashes, streams, duration and references for video, images and audio; detect missing files before import and verify hashes when relinking moved assets. | Full scope pending |
| Exact timeline assembly | Represent in/out points, tracks and ordering with integer ticks and rational timebases; serialize large integers as decimal strings and reject out-of-range clips. | Full scope pending |
| Audio and voice-over assembly | Preserve separate identities and gains for voice-over, music and source audio; verify output audio and sync; do not synthesize or upload voices without authorization. | Full scope pending |
| Caption timing and layout | Preserve caption text, language, time ranges and style; reject invalid timing and report font substitution impacts instead of changing fonts silently. | Full scope pending |
| Project round-trip and local revision | Save and reopen .fcproj, inspect the timeline and revise one shot by stable clip ID without changing other tracks or asset references. | Full scope pending |
| Preview and final output | Separate proxy preview from native export; decode final outputs and verify dimensions, frame rate, duration and audio; never label an FFmpeg substitute as native export. | Full scope pending |

Does not rewrite upstream editors, silently change native deliverable formats, or claim GUI/cross-platform acceptance.

## Architecture and documentation

- [Complete runtime architecture](docs/FilmCraft-Runtime-Architecture.md)
- [Technical plan and roadmap](product-docs/FilmCraft/en/5%E3%80%81FilmCraft-Technical-Plan.md)
- [V1 PRD and requirement mapping](product-docs/FilmCraft/en/V1/5%E3%80%81FilmCraft-PRD-V1.md)
- [Complete documentation index](docs/README.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [Domain technical design](docs/FilmCraft-Domain-Design.md)

## Currently executable quick start

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
These commands validate documentation and specifications, not product workflows. OpenSpec validation uses 1.13.1; this repository does not install tools automatically.

After installing the official CLI, perform a basic check:

```bash
filmcraft-cli --version
```

The recorded result is 0.2.0. The public independent-skill bootstrap and workflow are development entry points; plugin-host installation remains unverified.

## Configuration and runtime

Target configuration includes CLI paths, allowed read/write roots, execution mode, budget, timeout and output directory; the configuration schema is not implemented yet. The skills lock pins the published source commit and whole-skill digest. Runtime lock hashes identify real official artifacts and establish only the recorded platform’s smoke evidence.

## Reliability and security

Planned safeguards include project write locks, revision preconditions, persisted intent, idempotency keys, outcome reconciliation, native checkpoints, artifact hashes and bounded revisions. Secrets are host-managed references; asset metadata is never an execution instruction.

## Verification and maturity

[Sanitized CLI evidence](docs/evidence/runtime-baseline.json)

| Layer | Status |
| :--- | :--- |
| Upstream CLI and read-only MCP | Observed on macOS arm64 only |
| Independent skill and adapter | Technical workflow tested; full harness pending |
| Native project and creative acceptance | Native technical cases pass; creative acceptance pending |
| Target host installation | Codex controlled install/discovery pass; full host acceptance pending |


## Roadmap and contribution

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |

Change OpenSpec before behavior; check a task only after actual acceptance. Maintain both document languages. See CONTRIBUTING.md and AGENTS.md.

## License and upstream

Original content uses [Apache-2.0](LICENSE). This is a third-party integration design, not upstream endorsement. Treat the four apps’ code licenses separately from ArtCraft/Services restrictions; do not copy restricted source or brand assets.

[Upstream FilmCraft](https://github.com/storytold/filmcraft) · [Issues](https://github.com/full-aigc-plugins/filmcraft-plugin/issues)

The independent skill now has a native short-film workflow with isolated first-use installation, editable project reopening, media collection, audio/caption verification and one-shot revisions after moving the delivery folder (14 tests). See [runtime evidence](docs/evidence/film-workflow-tests.json). Full Harness, plugin-host and creative acceptance remain pending.

Independent skills are pinned at the current published development tag `v0.1.0-dev.4`, including the exact source commit and whole-skill digest in `skills.lock.json`. Verify using `python3 scripts/vendor/skill_vendor.py check`. These source snapshots do not establish plugin-host acceptance or production readiness.

## Development skill installation and use

Install the independent skill: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-use`. Run the public entry from the actual installed directory; this plugin snapshot includes the same skill.

```bash
python3 -I -B skills/filmcraft-use/scripts/bootstrap.py
python3 -I -B skills/filmcraft-use/scripts/workflow.py --help
```

First use installs the pinned official CLI into user-level storage. Requires macOS arm64 and Python 3.11+. Use the bundled example with real input assets; consult SKILL.md for delivery and revision contracts. [Source verification](docs/evidence/skill-publication.json).

## Codex development host checks

All five plugins installed from public tags into an isolated Codex configuration. App-server discovered their namespaced skills without loading errors; the installed ArtCraft entry produced four native projects. [Host evidence](docs/evidence/codex-installation.json). These controlled development checks do not establish desktop GUI, other hosts, complete creative or production marketplace acceptance.

Development version `0.1.0-dev.1` pins the independent skill install-lock fix: bounded coordination for concurrent installation/reuse, with no native task replay.

The current development milestone adds hash-bound exchange loss reports to native deliveries. lost, observed and unknown are separate; derivatives never substitute for native projects. Font/effect/mask fidelity across editors remains unverified, so full exchange acceptance stays open.

## CLI and task skill suite

The source suite contains 11 independently installable skills with setup, public CLI operations and focused tasks. [Architecture and catalogue](docs/FilmCraft-Skill-Suite-Architecture.md). Runtime and plugin versions are separate; prior host evidence retains its original version scope.

## Focused task skills: clean first use

All eight FilmCraft task skills passed independent first-install operations on macOS arm64, with only that skill copied and a fresh runtime downloaded from its locked public URL. Assertions cover persisted native edits, actual audio samples and rendered pixels, original-project preservation, and rejected unknown commands. The full suite passed 31 tests with no skips. [Evidence](docs/evidence/task-skill-first-use.json). This verifies the listed operations, not every command, GUI or final creative acceptance.

```bash
CRAFT_TASK_FIRST_USE=1 CRAFT_LIVE_TEST=1 CRAFT_LIVE_SUITE=1 python3 -B -m unittest discover -s tests -v
```

Run this command in the independent `filmcraft-skills` repository; live tests require ffmpeg, ffprobe and Pillow.

Current plugin: `0.1.0-dev.5`; skill suite: `0.1.0-dev.4`. The corrected examples resolve scripts from the actual host-loaded `SKILL.md` directory. All skills passed isolated entry-point checks in user, project and plugin layouts with spaces. [Path evidence](docs/evidence/installed-skill-paths.json). Earlier host evidence above covers its recorded release; existing installations require an update.

Plugin `0.1.0-dev.5` corrects the whole-skill digests by fetching the immutable public source tag, without local Python caches. Plugin tag `v0.1.0-dev.4` is superseded and must not be installed because its source digests included ignored development caches.

Current fixed-release host verification (2026-10-06): Codex 0.153.4 installs all five current pinned plugins and discovers all 58 skills with exact content identity. This plugin’s representative native workflow runs from its actual installed skill path with a fresh native runtime; creation/reopening/revision checks pass. All 58 installed skill hashes remain unchanged after the five workflows. [Evidence](docs/evidence/codex-current-release-20261006.json). The shared explicit-tag generator belongs to ArtCraft. Model dispatch awaits authorization; GUI, creative and full host acceptance remain pending. This QA maintenance changes no published skill/runtime content or release tags.
