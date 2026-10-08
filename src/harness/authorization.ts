import { lstatSync, realpathSync } from 'node:fs';
import { join } from 'node:path';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';

export type AuthorizationRequest = { authorizationRef: string; authorizationScopeSha256: string };
export type AuthorizationSubject = { action: 'repair' | 'continue' | 'upgrade' | 'rollback'; identitySha256: string };
export type AuthorizationDecision = AuthorizationRequest & { subjectSha256: string; expiresAt: number };
/** 宿主提供可信授权查询；每个有副作用门禁重新查询，不能把回执引用当作授权。 */
export type Authorizer = (subject: AuthorizationSubject, request: AuthorizationRequest) => AuthorizationDecision | null;

export function requireAuthorization(authorize: Authorizer | undefined, request: AuthorizationRequest,
  subject: AuthorizationSubject, now = Date.now()) {
  check(typeof request.authorizationRef === 'string' && request.authorizationRef.length > 0
    && request.authorizationRef.length <= 256 && isHash(request.authorizationScopeSha256)
    && ['repair','continue','upgrade','rollback'].includes(subject.action) && isHash(subject.identitySha256), 'invalid_authorization_request');
  check(typeof authorize === 'function', 'authorization_verifier_required');
  const decision = authorize(subject, request);
  check(decision, 'authorization_required');
  check(Number.isSafeInteger(decision.expiresAt) && decision.expiresAt > now, 'authorization_expired');
  check(decision.authorizationRef === request.authorizationRef
    && decision.authorizationScopeSha256 === request.authorizationScopeSha256
    && decision.subjectSha256 === sha256(stableJson(subject)), 'authorization_scope_change_required');
  return decision;
}

/** 本机宿主的私有授权记录；由宿主/用户单独写入，任务计划或回执不能授予权限。 */
export class LocalAuthorizationStore {
  root: string;
  constructor(root: string) { this.root = root; }
  private protected(path: string, directory: boolean) {
    let info;
    try { info = lstatSync(path); } catch (error: any) {
      check(error.code !== 'ENOENT', 'authorization_required'); throw error;
    }
    check(!info.isSymbolicLink() && (directory ? info.isDirectory() : info.isFile())
      && (info.mode & 0o077) === 0 && (process.getuid === undefined || info.uid === process.getuid()), 'authorization_store_unsafe');
  }
  authorize: Authorizer = (subject, request) => {
    this.protected(this.root, true);
    const name = sha256(request.authorizationRef) + '.json';
    const file = join(realpathSync(this.root), name);
    this.protected(file, false);
    const value = parseJson(readBoundFile(realpathSync(this.root), name, 1024 * 1024).toString('utf8'));
    check(isObject(value) && value.schema === 'filmcraft-local-authorization/v1' && value.authorizationRef === request.authorizationRef
      && value.authorizationScopeSha256 === request.authorizationScopeSha256
      && Array.isArray(value.subjects) && value.subjects.length <= 10_000 && value.subjects.every(isHash), 'authorization_required');
    if (value.revoked === true) { return null; }
    check(value.revoked === false && value.subjects.includes(sha256(stableJson(subject))), 'authorization_scope_change_required');
    return { ...request, expiresAt: value.expiresAt, subjectSha256: sha256(stableJson(subject)) };
  };
}
