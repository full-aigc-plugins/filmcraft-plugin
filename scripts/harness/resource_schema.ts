/** schema4 的资源与取消记录仍属于同一 SQLite 操作账本。 */
export const RESOURCE_TABLES = ['resource_scopes', 'task_resources', 'cancel_intents'];
export const RESOURCE_SCHEMA = `
CREATE TABLE resource_scopes(scope_id TEXT PRIMARY KEY REFERENCES tasks(task_id), limits TEXT NOT NULL,
  deadline INTEGER NOT NULL, state TEXT NOT NULL, reason TEXT, created_at INTEGER NOT NULL) STRICT;
CREATE TABLE task_resources(task_id TEXT PRIMARY KEY REFERENCES tasks(task_id), scope_id TEXT NOT NULL REFERENCES resource_scopes(scope_id),
  allocation TEXT NOT NULL, state TEXT NOT NULL, reserved_at INTEGER NOT NULL, consumed TEXT, process_identity TEXT) STRICT;
CREATE TABLE cancel_intents(task_id TEXT PRIMARY KEY REFERENCES tasks(task_id), scope_id TEXT NOT NULL REFERENCES resource_scopes(scope_id),
  request TEXT NOT NULL, created_at INTEGER NOT NULL, diagnosis TEXT NOT NULL) STRICT;`;
