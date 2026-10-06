# FilmCraft Sequence Workflow and Relinking Architecture

## Authority and current phase

Existing OpenSpec FC-DM-001-SEQUENCE owns the handoff, with independent filmcraft-skills as skill authority. The source workflow now implements sequence registration, native import, complete collection and source-project revision. Plugin snapshots remain unchanged. Public source runtime locks now select craft.2; see [public first-use follow-up](FilmCraft-Public-Sequence-First-Use-Architecture.md). Candidate tests inject the installation result for a checksum-bound maintained binary; this is not public cold installation.

## Three native defects and fixes

Original import used 29.97 fps, Project Manager copied only the first frame, and relinking opened that frame as a five-second still. The combined patch retains caption fixes and adds explicit rational rates, per-frame collection and relinking at the saved media kind/rate. Missing or truncated sequences cannot be relinked even with force. Ordinary forced file relinking retains its existing behavior.

## Workflow contract

Inputs explicitly declare `kind: image-sequence` with manifest SHA-256, or use `--sequence-asset`. The workflow validates the manifest and all frames, imports with native `file.importImageSequence`, checks returned rate/frame count and reads actual native properties to verify type, duration, dimensions and alpha. Source revisions validate packaged manifests and frames, relink from the packaged first frame, and verify native properties again.

```mermaid
flowchart LR
    A[Manifest and all-frame checks] --> I[Native sequence import]
    I --> P[Actual native media properties]
    P --> T[Timeline and native outputs]
    T --> C[Complete native collection]
    C --> H[Manifest and nested hashes]
    H --> M[Packaged relink after relocation]
    M --> R[Local revision and new delivery]
```

## Delivery and failure boundaries

Sequence asset path points to packaged sequence.json, with its original byte digest. sequenceMetadata retains declarations while probe comes from actual native media properties. Delivery files includes every nested frame hash. Collection verifies each path and byte digest. Previous packages/projects stay read-only; bad dependencies or native type/timing conflicts cannot produce a successful delivery.

## Real candidate acceptance

[Evidence](evidence/sequence-workflow-candidate-20261006.json): one copied media skill runs the real candidate CLI through twelve-frame import, complete collection, source removal, relocation and local clip-move revision. Skill bytes and all prior delivery files remain unchanged; corrupted-frame revision fails. Independent native MP4 decoding verifies twelve original frames, thirteen revised frames after a one-frame move, and actual animation color at frame six. The workflow test passes in 1.145 seconds. Ordinary public fixed-runtime audio/caption/revision regression passes in 6.277 seconds. Native engine has 285 passes and three ignored tests; default Python suite has 43 passes and eighteen gated skips.

Public cold installation, fixed source/plugin publication, actual Effect dynamic output integration, Art mixed dependency/revision and creative acceptance remain open. Historical candidate evidence keeps its earlier patch hash and does not prove the current relinking patch.
