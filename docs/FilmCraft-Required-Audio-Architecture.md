# FilmCraft Required Source Audio Architecture and Acceptance

Candidate source dev.8 retains CLI 0.2.0-craft.1 and fixes false audioRequired success. Fixed installed-plugin verification is pending. FC-DM-003-EMPTY is authoritative.

Old fixed plugin dev.8 / source dev.7 exported silent AAC with no native source audio clips. Checking only the exported stream falsely accepted this output; a real failure test failed because no error was raised in 4.514 seconds. The workflow now binds reopened audio clip item IDs to registered media probe.audio, then checks the exported stream, preserving the public export_audio_missing failure code.

```mermaid
flowchart LR
    A[Reopen native project] --> B[Bind audio clips to registered sources]
    B --> C[Native export and stream probe]
    C --> D{Required source and output audio valid}
    D -->|Yes| E[Publish success manifest]
    D -->|No| F[Retain diagnostics and fail]
```

Retain .fcproj, movie, preview, audio-check.json, export-probe.json and failure.json without a success manifest. Never overwrite an existing failed output directory. Explicit audioRequired=false supports video-only delivery; intentional silent WAV source audio remains valid. Successful delivery hashes audio-check.json.

A candidate audio skill copied alone publicly installs into an empty runtime directory. The real public workflow.py exits 1 with export_audio_missing. Independent decoding confirms generated AAC has a zero waveform; diagnostic file hashes survive retries. Explicit optional audio and intentional silent source audio both pass. One real test passed in 6.530 seconds. Default source regression: 36 passes, 16 explicit skips. [Candidate evidence](evidence/required-audio-candidate.json).

This checks source presence, not audibility, speech content or creative quality. Fixed installed-release verification and updated ArtCraft dependency integration remain separate gates.
