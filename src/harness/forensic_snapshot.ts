import { mkdtempSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { tmpdir } from 'node:os';
import { TaskLedger } from './task_ledger.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { check, sha256, stableJson } from '../support/json.ts';

/** 在原数据库之外打开一致的 DB/WAL 字节副本；从不打开原 SQLite 连接或创建原 sidecar。 */
export function forensicSnapshot<T>(file: string, observe: (ledger: TaskLedger, identity: Record<string, string | null>) => T): T {
  const parent = realpathSync(dirname(file)), name = basename(file);
  function read() {
    const result: Record<string, Buffer | null> = {};
    for (const suffix of ['', '-wal']) {
      try { result[suffix] = readBoundFile(parent, name + suffix, 64 * 1024 * 1024); }
      catch (error: any) { if (suffix !== '' && error.code === 'ENOENT') { result[suffix] = null; } else { throw error; } }
    }
    return result;
  }
  function identity(buffers: Record<string, Buffer | null>) {
    return Object.fromEntries(Object.entries(buffers).map(([suffix, bytes]) => [suffix || 'database', bytes === null ? null : sha256(bytes)]));
  }
  const before = read(), captured = identity(before);
  const directory = realpathSync(mkdtempSync(join(tmpdir(), 'filmcraft-inspect-')));
  let db: TaskLedger | undefined;
  try {
    const copied = join(directory, 'ledger.sqlite'); writeFileSync(copied, before['']!, { mode: 0o600 });
    if (before['-wal']) { writeFileSync(copied + '-wal', before['-wal'], { mode: 0o600 }); }
    // 不复制 SHM 的活动锁；SQLite 只能在隔离副本目录重建自己的读状态。
    check(stableJson(identity(read())) === stableJson(captured), 'ledger_changed');
    db = new TaskLedger(copied, { readOnly: true });
    check(Object.values(db.db.prepare('PRAGMA quick_check').get() ?? {})[0] === 'ok', 'ledger_integrity_failed');
    check(db.db.prepare('PRAGMA foreign_key_check').all().length === 0, 'ledger_integrity_failed');
    db.verifyIntegrity();
    // SHM 的活动读锁不参与任务版本；本函数既不读取也不打开原 SHM。
    const result = observe(db, { database: captured.database, wal: captured['-wal'] });
    check(stableJson(identity(read())) === stableJson(captured), 'ledger_changed');
    return result;
  } finally { db?.close(); rmSync(directory, { recursive: true, force: true }); }
}
