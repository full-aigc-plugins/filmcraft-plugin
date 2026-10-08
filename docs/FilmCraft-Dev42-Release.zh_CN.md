# FilmCraft dev.42 开发发行验证

版本：插件 `0.1.0-dev.42`，独立技能源 `v0.1.0-dev.39` / `6c29e50b5fe85f98a1c5f77977158bb1b00bde5a`。[English](FilmCraft-Dev42-Release.md)。正式行为合同仍由 [OpenSpec](../openspec/changes/establish-v1-plugin/specs/) 持有；不因开发发行勾选未完成任务。

## 本次范围

13 项独立技能的共享参数校验、任务路由与能力快照通过已发布标签同步，插件不手工维护另一套技能源。Node.js 24 / SQLite Harness 复用已有 Python 原生工作流，关联任务、尝试与原回执；新增只读诊断及有围栏的状态修复。Dreamina 对照优化的 11 组、33 项任务继续按自身证据推进，恢复验收包含原文件保全、并发、重复修复和状态兼容。

## 恢复边界

`inspect` 和 `reconcile` 均为只读：原数据库及 WAL 在隔离目录复制后检查，不打开原 SHM，不在原位置创建文件。诊断前后核对原文件摘要；读取不一致、缺失、损坏或进程身份无法确认时保留 unknown 和占用。快照当前每文件上限 64 MiB，不证明大型账本或敌对文件系统并发安全。

`repair` 只修复已确认完成的原尝试状态。它核对当前诊断摘要、epoch 及已有授权引用，持久化恢复意图，再复核进程与回执证据；仅进入 verifying，不重放原生编辑、不认定质量通过。竞争者与过期所有者不能应用同一恢复意图；新鲜诊断重复修复复用原结果。授权引用相等不代替宿主授权范围执行器。

```bash
node src/cli/recovery.ts inspect --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK"
node src/cli/recovery.ts reconcile --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK"
node src/cli/recovery.ts repair --ledger "$LEDGER" --blobs "$BLOBS" --task "$TASK" --expected-epoch "$EPOCH" --inspection-sha256 "$INSPECTION_SHA256" --authorization-ref "$AUTHORIZATION_REF" --authorization-scope-sha256 "$AUTHORIZATION_SCOPE_SHA256"
```

只读兼容 schema v1/v2，不迁移；写入者可升级已识别 v1 并保留任务/尝试记录，外来或未知版本拒绝。完整备份、升级、回退及继续执行验收仍开放，局部迁移测试不关闭相关规范。

## 验证与剩余范围

当前命令、文件摘要、逐层结果与原始日志见 [dev.42 绑定报告](evidence/filmcraft-dev42-release-20261008.json)。源仓离线回归、插件回归、独立源与内置快照原生验证分别记录；内置快照执行不等于实际宿主安装。真实故障注入覆盖原生导出完成后回执交接失败，检查只读保全和同尝试修复；合成回执测试不冒充原生验收。

历史 Harness 报告仍对应其初始源码摘要，不能验证本发行改变后的代码。当前报告不证明 TypeScript 静态类型检查、实际 CI、宿主安装、完整 headless/bridge 或 Windows、授权执行、预算/取消、独立质量、用户接受、完整媒体矩阵及 V1。参考命令目录与有效运行时身份差异仍显式保留。当前尚有 72 项未完成任务，不同步或归档为已完成主规格，不加入可安装市场。
