# FilmCraft Static Track Gain Architecture and Acceptance

Fixed plugin dev.8 / source dev.7 contain this workflow entry and passed installed-snapshot verification. The plugin OpenSpec FC-DM-003-GAIN is authoritative.

The workflow previously rejected mixer.setStrip even though the audio skill exposed that native command. It now accepts an explicit audio track such as A1 or A2 and a finite volumeDb number only. Bus, recording, routing and automation fields remain rejected.

```mermaid
flowchart LR
    A[Explicit track and decibel gain] --> B[Validate parameters]
    B --> C[Locked native CLI mixer.setStrip]
    C --> D[Save new fcproj and native movie]
    D --> E[Decode audio and check amplitude]
```

Use the skill-owned scripts/workflow.py for creation or revisions. Example operation:

```json
{"command":"mixer.setStrip","params":{"strip":"A1","volumeDb":-6.0}}
```

The candidate first-use test copies only the audio skill into an isolated project .agents/skills and publicly installs the locked CLI into an empty runtime directory. One real test passed in 5.010 seconds. The decoded RMS ratio at -6 dB was 0.5011754631 versus the theoretical 0.5011872336. Original delivery files, video/audio clip identities, captions and skill resource hashes were preserved. The targeted regression first failed with unsupported_command and then passed all eight tests after implementation. [Candidate evidence](evidence/audio-gain-candidate.json).

This does not prove multiple-track mixing, automation, GUI, model dispatch or creative quality. After publication, Codex 0.153.4 isolated installation discovered all 58 skills with zero loading errors. The installed audio skill copied alone publicly cold-installed the CLI and passed one real test in 7.372 seconds. All 58 host skill hashes were preserved. [Installed evidence](evidence/codex-filmcraft8-audio-gain-first-use-20261006.json). ArtCraft still pins the previous FilmCraft source; mixed gain support awaits dependency upgrade and verification.
