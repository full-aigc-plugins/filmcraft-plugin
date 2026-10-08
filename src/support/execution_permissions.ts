import { lstatSync, realpathSync } from 'node:fs';
import { isAbsolute, normalize, relative, sep } from 'node:path';
import { canonicalTarget } from './paths.ts';
import { check, isObject } from './json.ts';

export type ExecutionPermissions = { schema: 'filmcraft-execution-permissions/v1'; readRoots: string[]; writeRoots: string[] };
const broad = new Set(['/', '/Users', '/Volumes', '/System', '/Library', '/private', '/private/tmp', '/private/var', '/private/var/folders', '/System/Volumes', '/System/Volumes/Data', '/opt', '/usr']);
/** 可信调用方独立提供规范真实目录；不从计划或素材推导权限。 */
export function validatePermissions(value: unknown): ExecutionPermissions {
  check(isObject(value) && Object.keys(value).sort().join(',') === 'readRoots,schema,writeRoots'
    && value.schema === 'filmcraft-execution-permissions/v1', 'invalid_execution_permissions');
  const result: ExecutionPermissions = { schema: value.schema, readRoots: [], writeRoots: [] };
  for (const key of ['readRoots', 'writeRoots'] as const) {
    const roots = value[key];
    check(Array.isArray(roots) && roots.length > 0 && roots.length <= 64, 'invalid_execution_permissions');
    for (const root of roots) {
      check(typeof root === 'string' && root.length > 0 && root.length <= 4096
        && isAbsolute(root) && !/[\u0000-\u001f]/u.test(root), 'invalid_execution_permissions');
      let canonical: string, info;
      try { info = lstatSync(root); canonical = realpathSync(root); }
      catch { check(false, 'invalid_execution_permissions'); }
      check(info.isDirectory() && !info.isSymbolicLink() && canonical === normalize(root)
        && canonical === root && !broad.has(canonical), 'invalid_execution_permissions');
      result[key].push(canonical);
    }
    result[key] = [...new Set(result[key])].sort();
  }
  return result;
}
function contained(path: string, root: string) {
  const tail = relative(root, path);
  return tail === '' || (!isAbsolute(tail) && tail !== '..' && !tail.startsWith('..' + sep));
}
function canonical(path: string) {
  try { return realpathSync(path); }
  catch (error: any) { if (error.code !== 'ENOENT') { throw error; } return canonicalTarget(path); }
}
/** 文件打开前检查真实位置，不读取被拒绝目标或回显其位置。 */
export function requireRead(path: string, permissions: ExecutionPermissions) {
  const policy = validatePermissions(permissions), target = canonical(path);
  check([...policy.readRoots, ...policy.writeRoots].some(root => contained(target, root)), 'permission_read_denied');
  return target;
}
/** 输出父目录与目标均受可信写入根约束。 */
export function requireWrite(path: string, permissions: ExecutionPermissions) {
  const policy = validatePermissions(permissions), target = canonical(path);
  check(policy.writeRoots.some(root => contained(target, root)), 'permission_write_denied');
  return target;
}
/** 缺失根策略不能由既有引用或旧授权自动补齐。 */
export function requirePermissions(value: unknown) {
  check(value !== undefined && value !== null, 'execution_permissions_required');
  return validatePermissions(value);
}
