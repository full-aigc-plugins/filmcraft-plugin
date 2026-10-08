import type { DatabaseSync } from 'node:sqlite';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';

/** schema5 中的循环及轮次仍归唯一操作账本，不能通过重启重新开始计数。 */
export const REVISION_TABLES=['revision_loops','revision_rounds'];
export const REVISION_SCHEMA=`
CREATE TABLE revision_loops(loop_id TEXT PRIMARY KEY, root_task_id TEXT NOT NULL UNIQUE REFERENCES tasks(task_id),
  policy_sha256 TEXT NOT NULL, definition TEXT NOT NULL, state TEXT NOT NULL, reason TEXT,
  generation INTEGER NOT NULL, created_at INTEGER NOT NULL) STRICT;
CREATE TABLE revision_rounds(loop_id TEXT NOT NULL REFERENCES revision_loops(loop_id), round_no INTEGER NOT NULL,
  child_task_id TEXT NOT NULL UNIQUE REFERENCES tasks(task_id), intent_sha256 TEXT NOT NULL, intent TEXT NOT NULL,
  state TEXT NOT NULL, result TEXT, result_sha256 TEXT, PRIMARY KEY(loop_id,round_no)) STRICT;`;

/** 隔离取证时也核验循环原文摘要、连续轮次及任务绑定，禁止篡改后重置停止状态。 */
export function verifyRevisionIntegrity(db:DatabaseSync){
  for(const loop of db.prepare('SELECT * FROM revision_loops').all() as any[]){
    const definition=parseJson(loop.definition);
    check(isObject(definition)&&definition.rootTaskId===loop.root_task_id&&isHash(loop.policy_sha256)
      &&sha256(stableJson(definition))===loop.policy_sha256&&['active','stopped'].includes(loop.state)
      &&Number.isSafeInteger(loop.generation)&&loop.generation>0&&Number.isSafeInteger(loop.created_at)
      &&(loop.state==='active'?loop.reason===null:typeof loop.reason==='string'&&loop.reason.length>0),'ledger_revision_corrupt');
    const rounds=db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? ORDER BY round_no').all(loop.loop_id) as any[];
    check(rounds.filter(row=>['pending','unknown'].includes(row.state)).length<=1,'ledger_revision_corrupt');
    for(const [index,row] of rounds.entries()){
      const intent=parseJson(row.intent),binding=db.prepare('SELECT binding FROM tasks WHERE task_id=?').get(row.child_task_id) as any;
      check(row.round_no===index+1&&isObject(intent)&&intent.child?.taskId===row.child_task_id
        &&binding?.binding===stableJson(intent.child)&&isHash(row.intent_sha256)&&sha256(stableJson(intent))===row.intent_sha256
        &&['pending','unknown','reviewed','rejected','failed'].includes(row.state),'ledger_revision_corrupt');
      check(row.result===null?row.result_sha256===null&&['pending','unknown'].includes(row.state)
        :isObject(parseJson(row.result))&&isHash(row.result_sha256)&&sha256(row.result)===row.result_sha256,'ledger_revision_corrupt');
    }
  }
}
