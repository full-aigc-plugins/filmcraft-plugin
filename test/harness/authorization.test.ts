import { test } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, mkdirSync, symlinkSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { LocalAuthorizationStore, requireAuthorization } from '../../src/harness/authorization.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { hash, workspace } from './fixtures.ts';

test('private host grant binds the exact operation and is re-read for revocation and expiry', t => {
  const root = workspace(t), storeRoot = join(root, 'grants'); mkdirSync(storeRoot, { mode: 0o700 });
  const subject = { action: 'repair' as const, identitySha256: hash() };
  const request = { authorizationRef: 'local-grant', authorizationScopeSha256: hash('b') };
  const grant = { schema: 'filmcraft-local-authorization/v1', ...request, subjects: [sha256(stableJson(subject))], expiresAt: Date.now()+60_000, revoked: false };
  const file = join(storeRoot, sha256(request.authorizationRef)+'.json');
  const write = () => writeFileSync(file, JSON.stringify(grant), { mode: 0o600 }); write();
  const store = new LocalAuthorizationStore(storeRoot);
  requireAuthorization(store.authorize, request, subject);
  assert.throws(() => requireAuthorization(store.authorize, request, { ...subject, action: 'continue' }), /authorization_scope_change_required/);
  grant.revoked = true; write(); assert.throws(() => requireAuthorization(store.authorize, request, subject), /authorization_required/);
  grant.revoked = false; grant.expiresAt = Date.now()-1; write(); assert.throws(() => requireAuthorization(store.authorize, request, subject), /authorization_expired/);
});

test('host grant files reject shared permissions, symlinks and ambiguous JSON', t => {
  const root = workspace(t), request = { authorizationRef: 'grant', authorizationScopeSha256: hash() };
  const subject = { action: 'repair' as const, identitySha256: hash() }, file = join(root, sha256(request.authorizationRef)+'.json');
  writeFileSync(file, '{}', { mode: 0o644 }); const store = new LocalAuthorizationStore(root);
  assert.throws(() => store.authorize(subject, request), /authorization_store_unsafe/);
  chmodSync(file, 0o600); writeFileSync(file, '{"schema":"x","schema":"y"}');
  assert.throws(() => store.authorize(subject, request), /duplicate_json_key/);
  const other = join(root, 'other'); mkdirSync(other, { mode: 0o700 }); symlinkSync(file, join(other, sha256(request.authorizationRef)+'.json'));
  assert.throws(() => new LocalAuthorizationStore(other).authorize(subject, request), /authorization_store_unsafe/);
});
