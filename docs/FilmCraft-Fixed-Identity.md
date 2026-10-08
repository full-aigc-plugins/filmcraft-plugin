# FilmCraft Fixed Snapshot Identity Acceptance

[中文](FilmCraft-Fixed-Identity.zh_CN.md). FC-RL-001-CURRENT-FACTS and [task 9.6](../openspec/changes/establish-v1-plugin/tasks.md) are authoritative. Complete release, host and creative acceptance retain their own gates.

## Source and implementation

The target combination is plugin dev.43, skills dev.40 / `2eb9e0f169b3cfea1bf810aa0293c51bdbed4177`, and CLI craft.4. Skills recapture the catalog from the actual pinned CLI to repair the old reference digest, preserving all 666 parameter rows and existing standalone subsets. Older dev.42 and historical reports retain their original MISMATCH; history is not rewritten.

`scripts/verify_fixed_install.py` orchestrates one FilmCraft installation. It reads manifest, skill lock and executable digests from a local fixed tag, verifies the public tag's peeled commit, then creates a fresh CODEX_HOME, registers a verification-only local catalog and installs the public tag. Daily plugin configuration and official marketplaces are not changed. Annotated tag object hashes are not mistaken for commit identity.

Host discovery and skill verification reuse verify_codex_host.py functions from fixed ArtCraft authority commit `09d4ac5b8ff82f8fe819189e4be487b45ab2472b`, recording the helper's digest without executing its mutable working tree or editing the owner repository. Actual app-server discovery, every skill's content and executable plugin files are checked. Correct names do not permit changed content.

```bash
python3 -I -B scripts/verify_fixed_install.py --codex "$CODEX_CLI" --authority "$ARTCRAFT_REPOSITORY" --ref v0.1.0-dev.43 --output "$NEW_OUTPUT_DIRECTORY"
python3 -I -B scripts/verify_fixed_identity.py --host "$NEW_OUTPUT_DIRECTORY" --authority "$ARTCRAFT_REPOSITORY" --ref v0.1.0-dev.43 --output "$NEW_IDENTITY_REPORT"
python3 -B scripts/current_facts.py --check
```

Existing output directories are rejected. Private installation paths stay in the isolated verification directory and are excluded from public reports. Original installed files remain unchanged; tamper tests operate only on separate copies.

## Acceptance and status

The [fixed identity report](evidence/filmcraft43-fixed-identity-20261008.json) is PASS and task 9.6 is complete: public tag dev.43 was installed in isolated Codex 0.147.0, with 13 discovered skills, zero loading errors and 19 matching executable files. Seven single-field tamper cases on a separate installation copy were rejected. Repeated bilingual document generation produced identical bytes and installed files remained unchanged. Historical dev.42 MISMATCH and current full qualification NOT_PROVEN are preserved.

All 33 native regression tests passed without skips from the installed package, covering actual create, revision, export, idempotency and lost-receipt recovery. Runtime identity was craft.4 / `80dfc579f7639dc1d182c4dc9ab9cd834beaa234e6144e664757d40632f36893`. The native producer report retains its original candidate scope wording; the enclosing evidence identifies the actual Codex-installed execution directory. The identity recheck script and this acceptance record are post-release additions: the published dev.43 tag and ZIP remain unchanged. The script digest is recorded separately and is not claimed to be in the original ZIP.

Source tests, pinned installs, actual host discovery and model routing are separate. Discovery does not prove routing accuracy, matching catalogs do not prove every command executes, and identity MATCH does not promote full qualification from NOT_PROVEN. Complete modes/platforms, upgrade/rollback, budgets/cancellation, quality/user acceptance and V1 remain open.
