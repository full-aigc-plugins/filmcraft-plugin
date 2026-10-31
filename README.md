# FilmCraft Use

<!-- FILMCRAFT_CURRENT_FACTS_START -->

Generated current facts: plugin / skill source; skills / discovered commands: `0.1.0-dev.20261018.3` / `filmcraft-skills@v0.1.0-dev.62`; 24 / 666.

Skill inventory: 14 locked source skills + 10 plugin-local skills.

Execution CLI / bridge desktop: `0.2.0-craft.5` / `0.2.0`; root runtime lock is historical only.

Implementation: `in-progress`; full current-combination qualification: `NOT_PROVEN`. Discovery counts and historical reports do not imply current execution or release acceptance. [Machine-readable identities and scope](docs/current-facts.json).

Reference catalog identity: `MATCH`; a mismatch remains visible and does not override the execution runtime lock.

<!-- FILMCRAFT_CURRENT_FACTS_END -->

## Plugin marketplaces

This plugin belongs to **AIGC content creation**.

| Category | Marketplace | Purpose |
| --- | --- | --- |
| Full-stack development | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | Architecture and UI design, code understanding, quality checks, code review, workflow governance, and server operations |
| AIGC content creation | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | Image, video, audio, music, 3D, and multimodal content creation |

![FilmCraft Use — editable video editing](assets/official-logo.png)

> Cut a reopened `.fcproj` film from existing footage: media, tracks, audio, captions, colour and multi-camera, with preview frames and a decoded final export.

[![Version](https://img.shields.io/badge/release-0.1.0--dev.20261018.3-1A73E8)](.codex-plugin/plugin.json)
[![Skills](https://img.shields.io/badge/skills-24-00A67E)](#skills)
[![MCP server](https://img.shields.io/badge/MCP%20server-1-00A67E)](#mcp-tools)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[English](README.md) | [简体中文](README.zh-CN.md) · [Install](#installation) · [Quick start](#quick-start) · [What you can build](#what-you-can-build) · [Skills](#skills) · [Troubleshooting](#troubleshooting)

## Positioning

FilmCraft Use edits video as a native, reopenable project rather than a rendered file. It probes your media, assembles tracks on an exact integer tick base, keeps voice-over, music and source audio separate, treats captions as editable text with timing and style, and finishes only after the exported file has been decoded and checked for duration, size and audio.

The plugin plans and verifies; the pinned FilmCraft CLI performs the native edit. Long-form command coverage, physical GUI input and other platforms are not qualified, and every write must stay inside the read and write roots you explicitly authorize.

## Status and version

`0.1.0-dev.20261018.3` · development preview · `docs/verification/release-candidate.json` → `releaseStatus: BLOCKED`, `installableDevelopmentCandidate: true`.

| Metadata version | 0.1.0-dev.20261018.3 |
| Skills source | filmcraft-skills / 0.1.0-dev.62 |

## Installation

### Prerequisites

- macOS arm64. Other platforms return `unsupported_platform`; do not install a foreign artifact.
- Python 3.11 or newer on `PATH` for the public scripts; the launcher provisions the pinned runtime in the user data directory.
- Node.js 24 or newer for the embedded editor MCP server. A Git checkout has no `ui/dist/`; build it per `ui/README.md` or install a release bundle.
- Explicit authorization roots. `workflow.py` and `commands.py run` require `--read-root` and `--write-root` (repeatable); they must be existing canonical directories named by you, never derived from a plan or from asset metadata.

### Install the plugin

```bash
codex plugin marketplace add full-aigc-plugins/filmcraft-plugin
codex plugin add filmcraft@full-aigc-plugins-filmcraft
```

`docs/verification/release-candidate.json` records `installableDevelopmentCandidate: true` with `releaseStatus: BLOCKED`; `project-status.json` keeps `marketplaceEligible: false`.

Manifests for Codex (`.codex-plugin/`), Claude Code (`.claude-plugin/`), ZCode (`.zcode-plugin/`) and Kimi (`kimi.plugin.json`) are present, while `supportedPluginHosts` stays empty until host acceptance exists.

## Quick start

```bash
: "${HARNESS_DIR:?Set to the directory holding the loaded filmcraft-harness SKILL.md}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" PLAN.json \
  --output /absolute/new-result \
  --read-root /absolute/authorized-media --write-root /absolute/authorized-output
```

```mermaid
flowchart LR
    A[Footage, voice, music] --> B[filmcraft-use plans the cut]
    B --> C[Pinned runtime, authorized roots]
    C --> D[Native .fcproj timeline]
    D --> E[Preview frames and decoded export]
    E --> F[Reopen, inspect, deliver]
```

This tool uses `help`, not `--help`. Query the current command surface with `commands <keyword> --json` and `describe <command-id>`, and treat the returned parameters as authoritative.

## What you can build

| Workflow | Built-in path | Verifiable output |
|:---|:---|:---|
| Captioned short film from existing footage | `filmcraft-use` → harness workflow | Reopened `.fcproj` and an export decoded for duration, size and audio |
| Replace one shot, keep the rest | `filmcraft-cli-timeline` with `--source` | Revised project whose untouched clips keep their parameters |
| Interview or multi-camera edit | `filmcraft-cli-multicam` | Angle switch points with the main recording preserved |
| Voice-over, music and sync | `filmcraft-cli-audio` | Separately identified tracks with a checked mix |
| Captions and SRT delivery | `filmcraft-cli-subtitles` | Editable caption layers plus an exported SRT |
| Text-based editing | `filmcraft-cli-transcript` | Word-level transcript driving cuts and captions |
| Colour matching with LUTs | `filmcraft-cli-color`, `filmcraft-color-match` | Consistent shot look using clearly licensed LUTs |
| Edit in the embedded editor | `filmcraft-editor` MCP tools | Saved project reopened and inspected |

## Skills

| Skill | What it does |
|:---|:---|
| `filmcraft-use` | Default entry: editable `.fcproj` films, media, audio, captions; installs the pinned CLI |
| `filmcraft-cli` | Explicit native command ids and parameters, CLI/MCP calls, advanced operations |
| `filmcraft-cli-setup` | First install, digest checks, version checks, missing-runtime triage |
| `filmcraft-cli-project` | Create, open and save `.fcproj`; sequences and bins |
| `filmcraft-cli-media` | Inspect, import, collect and relink video, images and audio |
| `filmcraft-cli-timeline` | Order, trim and move shots; tracks and single-shot edits |
| `filmcraft-cli-audio` | Voice-over and music, gain, mix and sync |
| `filmcraft-cli-subtitles` | Import, create and edit caption text, timing and style; deliver SRT |
| `filmcraft-cli-color` | Shot colour, clearly licensed LUTs and presets |
| `filmcraft-cli-motion` | Text graphics, effect parameters and shot keyframes |
| `filmcraft-cli-export` | Preview frames, finished films, interchange files and output validation |
| `filmcraft-cli-multicam` | Synced multi-camera interviews, performances, angle switching, main audio |
| `filmcraft-cli-transcript` | Word-level transcripts, speech search, speakers, text-based editing |
| `filmcraft-harness` | The single execution channel: bootstrap, commands, workflow, task sessions |
| `filmcraft-editor` | Open the real editor UI and keep one session for all edits |
| `filmcraft-color-match` | Match exposure, white balance and style across shots |
| `filmcraft-interview-edit` | Assemble several interview segments into one sequence |
| `filmcraft-product-video` | Product showcase: selling points, detail shots, call to action |
| `filmcraft-short-video` | Rough cut of a short video: selection, structure, pacing |
| `filmcraft-subtitle-delivery` | Caption proofreading, line breaking and reading comfort |
| `filmcraft-video-export` | Delivery checks on resolution, frame rate, codec and audio |
| `filmcraft-freeze-explainer` | Freeze frames for teaching steps |
| `filmcraft-presenter-inset` | Picture-in-picture presenter over screen content |
| `filmcraft-jcut-dialogue` | J-cut where interview audio leads the picture |

## MCP tools

`mcp.json` declares one stdio server, `filmcraft-editor`, started as `node ui/bootstrap.mjs` from the plugin root.

| Tool | Purpose |
|:---|:---|
| `open_editor` | Open the editor for an absolute `workspace` path |
| `open_browser_editor` | Return an `editorUrl` for a host built-in browser |
| `editor_status` | Report whether the page has attached to this MCP session |
| `command_list` | Read the commands the current web engine exposes |
| `command_run` | Run one command in the visible page |
| `inspect` | Inspect the current frame |
| `open_file` | Import media into the session |
| `list_files` | List exported files |
| `save_project` | Save the project to a new workspace path |
| `save_file` | Write a generated file into the workspace |

Names follow the `filmcraft-editor` skill contract. Page-internal bridge calls such as `_panel_poll`, `_panel_download` and `screenshot` belong to the panel and must not be called by an agent.

## Configuration

| Variable / flag | Purpose |
|:---|:---|
| `HARNESS_DIR` | Absolute directory of the loaded `filmcraft-harness` skill |
| `SKILL_DIR` | Directory of the loaded domain `SKILL.md`; used only for its `examples/` and `references/` |
| `--read-root` / `--write-root` | Independently authorized canonical directories for plans, assets and outputs |
| `CRAFT_RUNTIME_HOME` / `--runtime-home` | Runtime install root; editing processes may never modify it |
| `CRAFT_EDITOR_CACHE_DIR` | Verified editor download cache (default `~/.cache/full-aigc/editors`) |
| `CRAFT_EDITOR_UPDATE=off` | Stay on the bundled editor and skip the update check |

Timeline positions use `254016000000` ticks per second. Workflow templates carry large integers as decimal strings; native command ticks stay exact JSON integers and never pass through a lossy JavaScript number.

## Architecture and security

- Root isolation is enforced for macOS headless execution. The desktop entry must additionally isolate the signed app it owns and expose only its assigned loopback control port; an external bridge that cannot prove isolation is refused.
- Media, music and voice are separate identities with separate gains. Voices are never synthesized or uploaded without authorization.
- Writes require `--save` or `--save-as`, or one `run`/MCP session. A timeout never proves that no side effect happened: check the project, the export or the task first.
- See [execution permissions](skills/filmcraft-use/references/execution-permissions.md), [runtime architecture](docs/FilmCraft-Runtime-Architecture.md) and [domain design](docs/FilmCraft-Domain-Design.md).

## Troubleshooting

| Symptom | Action |
|:---|:---|
| `unsupported_platform` | Only the locked macOS arm64 artifact is supported |
| Root rejection | `--read-root` / `--write-root` must be existing canonical directories you named; they cannot come from the plan |
| `runtime_install_busy` | Another install holds the lock; wait for it, then retry |
| `--help` prints nothing useful | This CLI uses `help` |
| Command lost an object id | Read the real result or stay in one MCP/`run` session; never guess ids |
| Export looks finished but is not | Decode the file and check duration, dimensions and audio track |
| Unknown result after a save | Inspect the original project and receipts; do not resubmit blindly |

## Upgrade

```bash
codex plugin marketplace upgrade full-aigc-plugins-filmcraft
codex plugin add filmcraft@full-aigc-plugins-filmcraft
```

Runtime selection and rollback are recorded per task; an old project keeps the runtime it was bound to instead of being silently migrated.

## Contributing and support

State behaviour changes in [OpenSpec](openspec/changes/establish-v1-plugin/proposal.md) first, then implement, then verify. Documentation checks:

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_protocol_mapping.py
```

Issues: <https://github.com/full-aigc-plugins/filmcraft-plugin/issues>.

## License

Original repository content is [Apache-2.0](LICENSE). The FilmCraft CLI and bundled web editor keep their own upstream licenses and NOTICE files; upstream icon provenance is recorded in `assets/official-icon-source.json`. This is an integration, not an upstream endorsement.
