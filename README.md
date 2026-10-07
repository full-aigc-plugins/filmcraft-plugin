# FilmCraft Agent Plugin

Edit existing media into a reopenable `.fcproj`, asset inventory, previews and a finished video.

Current plugin: `0.1.0-dev.36`; skill source: `0.1.0-dev.35`; 13 independent skills.

Verified first-use platform: macOS arm64 and Python 3.11+. Pinned runtimes install into the user data directory; skill files stay in their host-loaded directory. These are development releases; complete V1 acceptance and generic Skills CLI installation remain open.

Fixed audio-tail acceptance: Film plugin dev.33 / source dev.31 and Art plugin dev.103 / source dev.77 pass actual installed first use. All 64 installed identities match; 23 changed skills pass fresh independent cold starts (258.282s), while 41 byte-identical skills retain their earlier cold evidence. Native audio-tail/gain/oversized-range checks, five-child spoken mixed delivery, moved package, and brand revision with unrelated reuse pass. This does not close generic Skills CLI, creative approval or full V1. [Version-bound evidence](docs/evidence/craft-art103-audio-tail-fixed-first-use-20261007.json).

Current sample-duration correction: Film plugin dev.34 / source dev.32 and Art plugin dev.104 / source dev.78 pass actual fixed public-tag installation. All 64 installed identities are rechecked; 23 skills pass fresh independent cold starts (13 Film, 10 Art), and 41 historical cold records are reused only after full-tree digest equality. Actual 2.20s and 2.211s audio tails, gain revision, explicit oversized rejection, sequence relocation, captioned/narrated short-film revision, five-child mixed delivery, moved package and selective brand revision pass. Only this bounded sample-duration release gate closes; full V1, generic Skills CLI, model dispatch and creative acceptance remain open. [Current fixed evidence](docs/evidence/craft-art104-sample-audio-fixed-first-use-20261007.json).

Historical: Current Film dev.34 / source dev.32 / native craft.3 passes ten distinct standalone scene tests: project, media, timeline, audio, subtitles, color, motion, transcript, multicam and export. Each scene receives its own copied skill and new public runtime installation; actual native save/reopen, rendered frames or decoded samples and non-target preservation are asserted. All ten pass with no skips (67.330s), and all64 original installed digests still match the fixed lock. Transcript coverage uses provided timed words; automatic ASR, generic Skills CLI installation, every command context and full V1 remain open. [Evidence](docs/evidence/filmcraft34-ten-scene-first-use-20261008.json).

Maintainer source validation rejects symbolic links, incomplete locks and version-named branches, and checks all declared sources before replacing any managed skill. Published skill/runtime identities remain unchanged. [Snapshot preflight architecture](docs/Skill-Snapshot-Self-Contained.md).

## First use

Invoke **`filmcraft-use`** in your host. For direct CLI use, set `SKILL_DIR` to the absolute directory of the `SKILL.md` actually loaded by that host. It may be under user/project `.agents/skills`, the plugin, or a host cache; use the actual path. Each entry below installs/verifies its locked runtime before invoking it.

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands --json
```
<!-- CRAFT_FIRST_USE_END -->

Read the [editable workflow](skills/filmcraft-use/references/workflow.md) for inputs, native projects and targeted revisions. [Setup and skill entry](skills/filmcraft-use/SKILL.md) · [version-bound history](RELEASE-HISTORY.md). Command/version queries verify installation and discovery; they do not constitute creative completion.

[First-use navigation evidence](docs/evidence/craft-readme-first-use-navigation-20261007.json).

Fixed installed path acceptance: standalone skills and Art mixed work pass native creation/reopen, targeted revision and export under Chinese-and-space paths; Art also verifies moved delivery. Skills/runtime identities stay unchanged. This is bounded macOS arm64 first-use evidence. [Path acceptance evidence](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

Historical source candidate before the fixed release: structurally invalid runtime/Node locks now return local setup diagnostics before runtime writes/downloads. Five candidate native first-use checks pass; published plugin snapshots remain unchanged until separate immutable release acceptance. [Lock diagnostics candidate](docs/FilmCraft-Lock-Shape-Architecture.md).

---

Fixed native first-use and complete-command recovery acceptance passed:58 standalone cold installations, ten Art all-domain cold installations, four partial-download SSL EOF recoveries,72 post-save faults, four healthy command revisions and mixed HD revision/recovery/moved delivery. Installed identities remain unchanged. Only domain2.10/8.11 and Art4.10 close; exhaustive2639-command, GUI, model, generic Skills CLI and fullV1 gates remain open. [Version-bound evidence](docs/evidence/codex-native-download-first-use-20261007.json).

Historical release record: Current plugin: `0.1.0-dev.21`; skill source: `0.1.0-dev.19`; bounded fixed native gateway first use passes; full V1 remains open.


Historical candidate observation before fixed acceptance: Native download recovery candidate: up to three read-only attempts discard partial archives. Earlier fixed cold installs failed on SSL EOF; new fixed installed acceptance remains open.

Previous version-bound plugin: `0.1.0-dev.19`; skill source: `0.1.0-dev.17`; complete-command inner JSON fix is published, fixed installed acceptance pending.

Previous version-bound failed-stage acceptance: plugin dev.18, standalone source dev.16. All58 independent CLI cold starts,24 original-stage native fault cases and37 native scene tests plus6 contracts pass. Art77 bundle upgrade remains open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed domain-client first use: Film plugin dev.16 / source dev.15; Effect/Photo/Vector plugin dev.15 / source dev.14. Codex discovers 58 skills without errors. Actual installed copies pass 24 post-save faults and four healthy public workflows; the published Art engine with the installed Vector client passes six faults. All58 installed identities remain unchanged. Art dev.75 still bundles earlier domain sources; exhaustive command/GUI/model acceptance remains open. [Version-bound evidence](docs/evidence/codex-public-workflow-session-first-use-20261007.json).
Previous version-bound protocol recovery acceptance passed: 288 cases across 48 standalone source skills, 24 cases in actual installed copies, four healthy revision cases, and 58 unchanged installed skill identities. See [fixed evidence](docs/evidence/codex-protocol-fault-first-use-20261007.json). Exhaustive command/GUI acceptance and the Art domain-bundle upgrade remain open.

Protocol fault repair candidate: all 11 independently copied skills pass separate empty public-runtime installation and six faulty replies after real native save (66 cases; zero skips). Requests are not replayed; unknown receipts, saved-project reopening and delivery/skill preservation are checked. [Evidence](docs/evidence/protocol-fault-first-use-20261007.json). Fixed installed release and Art bundle upgrade remain separate gates.

Fixed plugin 0.1.0-dev.14 / skills 0.1.0-dev.13 installed revision acceptance passes: isolated Codex discovers all 58 skills without loading errors; this installed domain skill completes the documented cold creation/revision plans, saved-project reopening and non-target preservation. All58 installed digests remain unchanged; current fixed release CI passes. [Fixed revision evidence](docs/evidence/codex-complete-command-revision-first-use-20261007.json). Full command/GUI/model acceptance remains open.

All 11 domain skills pass the paired revision plans when copied alone and installed from separate empty public runtimes (67.161 seconds; zero skips). [Revision evidence](docs/evidence/complete-command-revision-first-use-20261007.json). Fixed installation of the updated snapshot remains a separate gate.

The complete-command entry now includes paired executable creation/revision recipes, explicit selection prerequisites after reopening, and native persisted-state/non-target checks. Each standalone skill includes both JSON plans. [Usage](skills/filmcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision). Full per-command and GUI acceptance remains open.

Previous version-bound release first use passed: isolated Codex 0.153.4 discovers all 58 skills without loading errors; every installed skill independently cold-installs its public locked runtime (385.234 seconds); installed domain command samples and Art 1080p mixed revision/recovery/package checks pass. All installed skill digests remain unchanged; fixed CI and five-bundle rebuild pass. [Version-bound evidence](docs/evidence/codex-complete-command-first-use-20261007.json). Generic Skills CLI installation, full command/GUI and creative acceptance remain open.

## Complete native command entry

All 11 standalone skills now pass separate empty-runtime installation from locked public CLI archives, followed by native creation, save/reopen, domain assertions and rendered image checks (72.162 seconds; zero skips). [Cold-first-use evidence](docs/evidence/complete-commands-cold-first-use-20261007.json). This verifies this complete-command sample in every skill; exhaustive command/GUI and actual host installation remain separate.

Published development snapshot: skills dev.12 / plugin dev.13; bounded fixed-host first use passed.

All 666 commands now have verbatim parameters, skill routing, and same-session invocation through `commands.py list / describe / check / run`. Live enabled state is checked; the existing 17-operation delivery workflow remains bounded. GUI commands require explicit bridge mode. Complete registry coverage does not establish full command acceptance.

[Architecture and usage](docs/FilmCraft-Complete-Commands-Architecture.md) · [Complete reference](skills/filmcraft-use/references/command-reference.md) · [Runnable example](skills/filmcraft-use/examples/commands-advanced.json)

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
| Metadata version | 0.1.0-dev.36 |
| Stage | implementation-in-progress |
| Skills source | filmcraft-skills / v0.1.0-dev.35 |
| Execution | Upstream CLI; ArtCraft uses child adapters |
| Host compatibility | Codex dev.35 fixed-tag installation/discovery and standalone real ASR pass; Art105 mixed ASR passes; GUI pending |
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

Historical plugin `0.1.0-dev.5` / skill suite `0.1.0-dev.4` path milestone. The corrected examples resolve scripts from the actual host-loaded `SKILL.md` directory. All skills passed isolated entry-point checks in user, project and plugin layouts with spaces. [Path evidence](docs/evidence/installed-skill-paths.json). Earlier host evidence above covers its recorded release; existing installations require an update.

Plugin `0.1.0-dev.5` corrects the whole-skill digests by fetching the immutable public source tag, without local Python caches. Plugin tag `v0.1.0-dev.4` is superseded and must not be installed because its source digests included ignored development caches.

Current fixed-release host verification (2026-10-06): Codex 0.153.4 installs all five current pinned plugins and discovers all 58 skills with exact content identity. This plugin’s representative native workflow runs from its actual installed skill path with a fresh native runtime; creation/reopening/revision checks pass. All 58 installed skill hashes remain unchanged after the five workflows. [Evidence](docs/evidence/codex-current-release-20261006.json). The shared explicit-tag generator belongs to ArtCraft. Model dispatch awaits authorization; GUI, creative and full host acceptance remain pending. This QA maintenance changes no published skill/runtime content or release tags.

Development dev.6 vendors FilmCraft skills dev.5 at d7773c802a227368e0d0e2c02534bace21bc097f. Its maintained native CLI 0.2.0-craft.1 fixes caption font rendering and explicit movie burn-in. Cold public single-skill Chinese subtitle and speech acceptance passed; all 44 source regression tests passed with no skips. [Evidence](docs/evidence/chinese-first-use.json). Current-release host discovery, GUI/model dispatch and the updated ArtCraft bundle remain separate pending gates.

The fixed FilmCraft dev.6 / EffectCraft dev.7 / PhotoCraft dev.6 / VectorCraft dev.6 / ArtCraft dev.17 matrix passed isolated Codex discovery of 58 skills and representative native workflows from installed skill content. All installed skill digests remained unchanged afterward. [Installed native evidence](docs/evidence/codex-release17-native-20261006.json). Model dispatch, GUI and complete creative acceptance remain unverified.

Current installed plugin dev.6 / skills dev.5 pass all eight independent task cold starts with maintained CLI 0.2.0-craft.1 (43.688 seconds). Input, output, test-driver and native fingerprints are recorded; all 58 installed hashes remain unchanged. This supplements the older 0.2.0 scene proof without changing release bytes. [Evidence](docs/evidence/maintained-runtime-task-first-use.json).

Candidate installation-receipt reuse validation is implemented and tested; fixed plugin and ArtCraft publication remain pending. [Architecture and evidence](docs/FilmCraft-Runtime-Receipt-Architecture.md).

Development dev.7 vendors immutable skills dev.6 (85866c064c7d91abd8da63b0570d78bee3202bf5). Installation reuse validates receipt identity; four tests from the vendored snapshot pass, including cold public native roundtrip and all 11 isolated CLI entries. [Candidate evidence](docs/evidence/runtime-receipt-candidate.json). Fixed Codex host verification and ArtCraft dependency synchronization remain pending.

Fixed FilmCraft plugin dev.7 / source dev.6 passed actual Codex 0.153.4 installation and four installed-snapshot tests: public cold native install, save/reopen, receipt refusal/restoration, and 11 isolated CLI entries. All 58 installed digests remain unchanged. [Fixed-release evidence](docs/evidence/codex-filmcraft7-receipt-first-use-20261006.json). ArtCraft dev.42 still locks source dev.5; its update remains pending.

[Temporal-source trim and move acceptance](docs/FilmCraft-Temporal-Timeline-Acceptance.md): one installed single-skill empty-runtime case passes, checking source in-points in reopened projects and native exports while preserving other clips, audio, captions and original deliveries. Complete timeline/creative acceptance remains open.

Plugin dev.8 vendors source dev.7: native workflow static audio-track gain (mixer.setStrip), finite-value validation and isolated candidate -6 dB decoding. Fixed Codex installed-snapshot verification passed: one isolated cold audio gain test, 58 discovered skills and preserved hashes; [evidence](docs/evidence/codex-filmcraft8-audio-gain-first-use-20261006.json). [Scope and architecture](docs/FilmCraft-Audio-Gain-Architecture.md).

Installed plugin dev.8 verifies three independent voice/music/original-audio tracks, staggered starts and a music-only gain revision through real decoded frequency amplitudes. All 58 installed hashes remain unchanged. [Scope and evidence](docs/FilmCraft-Multitrack-Audio-Architecture.md).

Published source dev.8 rejects generated silent AAC when required native source audio is absent, retains diagnostic outputs and still accepts explicit video-only or intentional silent WAV delivery. [Architecture and scope](docs/FilmCraft-Required-Audio-Architecture.md). Fixed plugin dev.9 installed verification passed: three real tests and all 58 hashes preserved. [Evidence](docs/evidence/codex-filmcraft9-required-audio-first-use-20261006.json).

Development snapshot dev.10 vendors immutable FilmCraft skills dev.9 and locks public CLI craft.2. Source cold sequence and actual Effect→Film handoff evidence is available; installed snapshot and Art mixed acceptance remain pending. [Architecture](docs/FilmCraft-Public-Sequence-First-Use-Architecture.md).

Fixed Film plugin dev.10 installed-first-use sequence acceptance now passes in isolated Codex 0.153.4. All 58 skills are discovered without loading errors and retain their hashes after Film execution. [Bounded evidence](docs/evidence/codex-filmcraft10-sequence-first-use-20261006.json); Effect/Art dynamic release integration remains pending.

Previous version-bound domain task matrix: 37 native scenarios and 6 contract checks passed with zero skips across FilmCraft dev.10, EffectCraft dev.9, PhotoCraft dev.10 and VectorCraft dev.11. Each task copied only its selected installed skill and installed the native CLI into a fresh runtime directory from the default public archive. Native projects, actual pixels/audio and targeted preservation were checked; all 58 installed skill identities remained unchanged. [Version-bound evidence](docs/evidence/codex-current-domain-task-matrix-20261006.json). This does not close full V1, generic Skills CLI installation, model dispatch, GUI or creative acceptance.

Candidate motion/LUT workflow: explicit keyframes, registered LUTs, native reopening and moved revisions passed a public-runtime first-use test. Immutable plugin dev.10 and Art integration do not yet include this mapping. See [architecture](docs/FilmCraft-Motion-LUT-Workflow-Architecture.md) and [evidence](docs/evidence/motion-lut-workflow-candidate-20261006.json).

Development snapshot dev.11 vendors immutable FilmCraft skills dev.10, including declared motion and LUT workflows. The published native CLI remains 0.2.0-craft.2. Installed snapshot and Art mixed acceptance are separate gates.

Fixed Film dev.11 / source dev.10 installed-first-use verification passed: isolated Codex discovers 58 skills without errors; all 11 Film skills pass separate cold CLI startup; installed motion/LUT, audio-gain and sequence scenarios pass with zero skips. All 58 installed hashes remain intact. New Art LUT runtime publication and full V1 remain pending. [Evidence](docs/evidence/codex-filmcraft11-motion-lut-first-use-20261006.json).

Working-tree segmented asset consumer candidate validates Effect checkpoints, collects continuous frames and preserves source hashes. Fixed release, full HD long render and Art integration remain pending. [Architecture](docs/FilmCraft-Segmented-Assets-Architecture.md).

Current-source HD segmented candidate passes 1080p / 24 fps / five seconds and animated-title checks; immutable installed releases and Art HD remain pending. [Architecture and evidence](docs/FilmCraft-HD-Sequence-Architecture.md).

Immutable plugin release candidate 0.1.0-dev.12 pins skill source 0.1.0-dev.11, including HD segmented workflows and pixel verification optimization. Actual installed first-use acceptance remains pending.

Public-workflow reply validation is synchronized in the domain source candidates and has bounded native/Art protocol evidence. Fixed updated domain and Art distributions are still pending. [Candidate architecture](docs/FilmCraft-Complete-Commands-Architecture.md) · [Evidence](docs/evidence/public-workflow-session-candidate-20261007.json).

Failed-stage candidate: public workflows retain original native staging paths, dependency hashes, last submitted requests and completed receipts; replay is prohibited. Fixed releases and installed-host acceptance remain open. [Architecture](docs/FilmCraft-Failed-Stage-Architecture.md).

Fixed domain failed-stage first use passes: Film plugin18/source16 and other domain plugins17/source15; five plugins/58 skills without loading errors; all58 independent empty-runtime CLI starts (417.646s); actual installed24 post-save faults reopen product-retained original projects and dependencies; four healthy native creation/revision cases pass. All installed identities and16 fixed plugin CI runs pass. Source repositories have no CI runs, only local regression. Only domain OpenSpec3.12 closes; Art77 bundles older domain sources, task4.9 and fullV1 remain open. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

Fixed installed scene matrix passes37 native scenarios and6 contract checks with zero skips. The Photo fixture now resolves the maintained native version from the installed skill lock; the CLI and installed skills are unchanged. [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


Candidate complete-command inner JSON fix: nonfinite values, overflow and duplicate keys now retain unknown receipts before binding results. All nine real post-save fault classes pass with original reopen; this is candidate-source evidence, fixed releases and installed-copy acceptance are pending. Complete per-command/GUI acceptance stays open.

## Desktop installation component (source candidate)

The 48 standalone domain skills now have their own pinned official desktop installers. See the [installation architecture](docs/Craft-Desktop-First-Use-Architecture.md) and [48-skill installation evidence](docs/evidence/craft-desktop-source48-first-use-20261007.json). Existing release-tag skill copies do not yet contain this candidate component. Desktop startup, GUI edits/save/reopen and complete command execution remain open acceptance gates.

Source candidate now includes owned standalone desktop startup: 48/48 single-skill cold GUI save/reopen and cleanup cases passed. See [runtime evidence](docs/evidence/craft-owned-desktop-first-use-20261007.json). Fixed-release installation and complete command execution remain open.

Command-plan JSON source candidate: duplicate keys are rejected before installation and output creation. All 13 domain skills pass standalone-copy rejection and valid-plan checks. Three focused tests pass; fixed-plugin publication and installed acceptance remain NOT_RUN. [Evidence](docs/evidence/command-plan-json-candidate-20261007.json).

Fixed strict-plan installed verification passes: 64 CLI probes, 324 duplicate-key rejections across54 independently copied installed domain skills, 54 unique-plan structure checks and four cold native save/reopen/render samples. All64 installed skill hashes remain unchanged. Only the bounded strict-plan publication gate closes; generic Skills CLI, Art domain-bundle upgrade, exhaustive contexts and fullV1 remain open. [Evidence](docs/evidence/command-plan-json-fixed-first-use-20261007.json).

Native ASR candidate: independent single-skill cold CLI/model installation and real recognition passed; public runtime and fixed Film/Art upgrades remain pending. [Evidence](docs/evidence/whisper-candidate-inference-20261008.json).

Released plugin dev.35 vendors published source dev.34/native craft.4. Source and fixed-tag Codex plugin first-model-download and real CLI/workflow inference pass; Art ASR distribution remains pending.

Fixed Film35 host acceptance: five plugins/all64 skill identities and loading pass with zero errors. The installed transcript skill independently cold-installs, downloads its model and performs real CLI/workflow inference (44.833s), preserving source/audio/video and reopening/exporting SRT. Art105/source79 now passes fixed-host mixed ASR; full V1 remains open. [Evidence](docs/evidence/workflow-model-directory-20261008.json).

Scenario installation examples now name the loaded skill itself. Source paths/layout checks pass; fixed installed runtime acceptance is recorded separately. [Architecture / 架构](docs/Scenario-Own-Path-Architecture.md).

Fixed installed own-directory acceptance passes for the updated scenario skills; 64 host identities match. Complete V1 remains open. [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).
