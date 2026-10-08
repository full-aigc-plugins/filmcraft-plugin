# FilmCraft HD Sequence Architecture

Date: 2026-10-07. Status: current independent-source candidate. Fixed plugin releases remain unchanged. Specification authority: plugin `openspec/changes/establish-v1-plugin`; scenario FC-DM-001-HD and task 4.44. This component delta uses the runtime and plugin profiles; it does not introduce a second specification or product baseline.

## Driver and implementation

The segmented contract makes a five-second 1080p RGBA sequence possible without raising the 512 MiB v1 sequence limit. Profiling exposed repeated Python PNG reconstruction as a first-use bottleneck. The shared `png_inspection.py` now yields validated RGBA8 rows; Effect `image_sequence.py` and Film `sequence_assets.py` consume these rows to calculate the same pixel hashes and alpha extrema. Every domain skill carries its own synchronized copy, so a single-skill installation requires no sibling.

```mermaid
flowchart LR
    E[Standalone Effect export skill] --> R[Locked native render]
    R --> S[Four bounded segments]
    S --> V[CRC and RGBA pixel verification]
    V --> F[Standalone Film media skill]
    F --> C[Continuous native sequence]
    C --> M[Native project and MP4]
    M --> I[Independent Pillow and full video decode]
```

## Byte semantics and resource boundary

The decoder remains Python standard library code. Existing structure, CRC, bounded decompression and scan-length checks precede row reconstruction. Filter dispatch happens once per row. None copies bytes; Sub reconstructs channels modulo 256; Up adds prior-row values using isolated 16-bit integer slots with no carry between channels; Average and Paeth retain their predictors and tie ordering. Zero-residual shortcuts preserve prior-row dependencies. Independent custom PNG fixtures cover all five filters, wraparound, mixed filters and repeated rows. Pixel hashes and real alpha extrema remain mandatory; filenames or manifest assertions cannot replace actual decoding.

Each segment remains at most 512 MiB decoded. The logical sequence limits remain 64 GiB / 10,000 frames and 2 GiB encoded total. Logical bytes are not simultaneous resident memory. Corrupt pixels, receipt mismatches, invalid ranges and symlinks remain errors; the optimization changes neither budgets nor reuse identity.

## Actual first use and evidence

[HD candidate evidence](evidence/effect-film-segment-hd-candidate-20261007.json) binds the test driver, every copied skill file and both native runtime hashes. The test copies exactly one Effect export skill and one Film media skill into isolated `.agents/skills`, starts with an empty shared runtime, uses public `workflow.py` subprocesses and default public runtime downloads. It checks skill preservation afterward.

| Check | Measured result |
| --- | --- |
| Native output | 1920×1080, 24 fps, five seconds |
| Sequence | Four segments, 120 independently decoded PNG frames |
| Logical RGBA | 995,328,000 bytes, above the old whole-sequence limit |
| Film output | Native `.fcproj`, full 120-frame MP4 decode, 5.000000 seconds |
| Animation | Title pixel changes from transparent to visible; eight composite pixel checks |
| Wall clock | Effect stage 17.047 seconds; full cold candidate 54.839 seconds |
| Default tests | Effect 51 pass / 21 skip; Film 52 pass / 21 skip; two filter tests per domain |

One native 1080p frame reconstructed in 0.046 seconds versus 2.028 seconds before optimization, with identical RGBA hash. This is a single-frame measurement, not a general throughput guarantee. The initial full HD profiling run was intentionally stopped; it is not acceptance evidence. Pillow and ffmpeg/ffprobe are independent test oracles, not new decoder runtime dependencies.

## Failure, release and remaining gates

Public workflow validation must still reject malformed plans before installation. Segment recovery retains the existing project/runtime binding and re-verifies actual pixels before reuse. Failed or incomplete sequences cannot become complete Film inputs. Existing Art candidate regression covers twelve frames, moved text revision, corrupted segment refusal and restoration using current source skills; it does not establish Art HD first use.

Task 4.44 closes only the current-source HD optimization and preservation checks. Immutable domain skill/plugin publication, installed Art HD orchestration, HD text revision/recovery and moved packages remain pending under the existing release tasks. macOS arm64 is the verified native platform. Model dispatch, GUI behavior, creative approval and full V1 acceptance remain open. Historical evidence stays version-bound and is not overwritten.

Tasks4.1-4.3/FC-DM-001 now pass all seven specified scenarios at fixed dev.65/source48/craft.5:current video/image/audio registration and native references;aggregate missing/hash-conflict refusals;24000/1001 transparent sequences;24-frame isolated same-name native collection;pre-output missing-frame/duration refusals;relocated revision with old bytes and non-target tracks preserved. Exact Effect55 Git objects serve only as a real native producer reference,furnishing four30-frame1080p transparent segments. The actual installed Film65 media skill copied alone performs a public cold install and120-frame/995328000-byte logical RGBA consumption/full decode;relocated revision yields121 frames and preserves the source checkpoint. All five PNG filters/wrap/cross-row checks,11 structure/CRC/decompression/resource refusals,8 segment version/range/resource refusals and12 installed-code unit tests pass. Interior animation/revision alignment error is1/255. The unchanged169/169 installed native regression and50 rows are reused,with13 skills and execution files reverified. Index: `docs/evidence/fc-dm-001/index.json`;acceptance: `docs/evidence/filmcraft65-fixed-domain-import-20261009/acceptance.json`. Bounded macOS arm64/Codex/headless scope;Art HD,exhaustive commands/GUI/other platforms,creative/manual review and user acceptance remain separate. Full V1 has23 open tasks;no archive or immutable tag/ZIP rewrite.
