import { lstatSync, realpathSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { check } from './json.ts';

/** 与 Python 输出认领一致：解析父目录别名，保留目标名称；不创建目录或跟随目标链接。 */
export function canonicalTarget(value: string): string {
  check(typeof value === 'string' && value.length > 0, 'invalid_output_path');
  const target = resolve(value), tail = [basename(target)];
  let parent = dirname(target);
  for (;;) {
    try {
      const canonical = realpathSync(parent);
      check(lstatSync(canonical).isDirectory(), 'invalid_output_parent');
      return join(canonical, ...tail);
    } catch (error: any) {
      if (error.code !== 'ENOENT') { throw error; }
      // 悬空父链接不是尚未创建的普通目录，不能用父级路径掩盖它。
      try { lstatSync(parent); check(false, 'invalid_output_parent'); }
      catch (missing: any) { if (missing.code !== 'ENOENT') { throw missing; } }
      check(dirname(parent) !== parent, 'invalid_output_parent');
      tail.unshift(basename(parent)); parent = dirname(parent);
    }
  }
}
