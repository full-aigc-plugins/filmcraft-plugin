# FilmCraft Public Runtime Sequence First Use and Effect Handoff

## State and authority

Existing OpenSpec FC-DM-001-SEQUENCE remains authoritative. Maintained native CLI `0.2.0-craft.2` is publicly prereleased. All eleven source skills lock the same archive, binary and provenance digests. Existing immutable releases remain intact. The plugin worktree now vendors immutable skills dev.9. Installed new-plugin acceptance and Art mixed handoff remain pending.

## Installation and execution

```mermaid
flowchart LR
    E[Single Effect export skill] --> R[Public native CLI renders RGBA frames]
    R --> S[Manifest and every frame digest]
    S --> F[Single Film media skill]
    F --> B[Unchanged installer downloads craft.2]
    B --> I[Explicit-rate import and complete collection]
    I --> V[Native MP4 and independent decode]
    V --> M[Relink moved package and revise locally]
```

Tests copy only their respective skills into isolated `.agents/skills`, start with absent runtime directories, preserve real installers and public HTTPS downloads, and check archive, binary, PROVENANCE and version. The single-domain test also checks reuse. The two-domain test consumes actual Effect rendering instead of a still or synthetic sequence. Command references are regenerated from the verified craft.2 native catalogue while retaining each scenario's existing command selection. Catalogue presence is not scenario acceptance.

## Evidence

- [Public native cold installation](evidence/sequence-public-runtime-first-use-20261006.json): twelve frames at 12 fps, one-second duration, complete collection, revision after moving delivery and deleting inputs, unchanged old package and skill bytes, corrupt-frame rejection, and independently decoded MP4 with twelve original frames and thirteen after a one-frame move. One test passed.
- [Effect to Film](evidence/effect-film-sequence-handoff-20261006.json): one copied skill per domain, empty runtime and two public CLI downloads, actual twelve-frame transparent animation consumed by Film, independent frame-count/background/graphic-color checks, Effect text revision, moved Film package and deleted original intro directory, targeted replacement preserving background, initial frame and old delivery. One test passed.
- Updated ordinary audio/caption/single-shot revision regression: one passed. All eight task-skill cold-install regressions passed. Default source tests: 43 passed, 19 environment-gated skips.

## Remaining boundaries

This proves source-skill first use with publicly distributed native runtimes. It does not prove immutable new skill/plugin installation, Art sequence dependencies or selective revision, full creative quality, color fidelity, GUI or all platforms. Task 4.31 remains open and the release remains developmental.
