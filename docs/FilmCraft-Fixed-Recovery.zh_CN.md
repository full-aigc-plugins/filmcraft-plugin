# FilmCraft 固定恢复专项验收

[English](FilmCraft-Fixed-Recovery.md)。正式合同为现有 OpenSpec FC-TX-002，本次完成9.16—9.18；3.4—3.6等完整门禁未据此整体关闭。

公开插件 dev.48 / `a891fd663667029362a3dd7982e86b88be0cf51f`，技能源 dev.42 / `7adfa763b161bc2ff7ef3efae702e285965bf23a`。隔离 Codex 0.147.0 在 macOS arm64 实际安装发现13技能零错误，30执行文件及测试源码符合固定Git对象，执行后身份保全。全新原生运行时执行60项安装测试无跳过；源码60项原生回归、45项Python测试通过。

| 场景 | 源码候选 | 固定安装 | 证据层 |
| :--- | :--- | :--- | :--- |
| WAL与回执缺失 / `readonly-wal-and-missing-receipts` | PASS | PASS | synthetic receipts; actual SQLite WAL |
| 缺失／损坏账本 / `missing-and-damaged-ledgers` | PASS | PASS | synthetic damaged SQLite bytes |
| 回复丢失及旧epoch / `lost-reply-and-old-epoch` | PASS | PASS | synthetic native receipts; actual stopped process |
| 恢复所有者过期 / `expired-recovery-owner` | PASS | PASS | actual SQLite fences with controlled time |
| 重复修复 / `repeat-repair` | PASS | PASS | synthetic native receipts |
| 双修复执行者 / `two-recovery-executors` | PASS | PASS | two actual Node processes; synthetic native receipts |
| 宿主退出／子进程存活 / `host-exited-child-alive` | PASS | PASS | actual exited Node host and detached controlled Node child; not native editing |
| schema1升级回退 / `schema1-upgrade-rollback` | PASS | PASS | actual SQLite maintenance; synthetic operation records |
| schema2升级回退 / `schema2-upgrade-rollback` | PASS | PASS | actual SQLite maintenance; synthetic operation records |
| 回退保留新记录 / `rollback-preserves-new-records` | PASS | PASS | actual SQLite with synthetic new task |
| 诊断期间并发写 / `inspection-concurrent-write` | PASS | PASS | actual concurrent SQLite commit during isolated observation |
| 真实原生修复继续 / `actual-native-repair-and-continuation` | PASS | PASS | actual Python/native create, lost reply, repair and continued editing; actual private host grants |
| 实际旧版拒绝新schema / `actual-previous-version-downgrade-refusal` | PASS | PASS | actual fixed dev45 installed core versus current schema3 SQLite fixture |
| 到期／撤销授权 / `expired-revoked-authorization` | PASS | PASS | synthetic receipts; actual authorization gates |

7类只读窗口比较原DB/WAL/SHM、回执与业务文件清单及字节摘要；故障用例自身的补充SQL查询在该窗口之后，避免把SHM读标记变化误归因于诊断。两个真实修复执行者仅一方应用；真实退出宿主／存活受控子进程与合成回执分开标注。

真实原生继续绑定当前父工程，新子任务拥有1次尝试／1条继续意图；父任务仍仅1次尝试且未重放，重复API和CLI调用复用子任务。schema1/2分别备份升级至3并兼容回退，旧任务／尝试／回执／未知占用逻辑摘要一致；新增记录和实际旧dev.45代码降级拒绝不修改原文件。该证明属于状态schema升级，不代替运行时二进制升级／排空验收。

3个公共任务／26个产物通过固定ArtCraft v0.1.0-dev.109所有者schema。发布提交main与tag的文档／实施共4次CI成功；CI的Node离线层为58通过／2项明确专项环境跳过，另行安装矩阵为60通过／0跳过，两层不混用。

原dev.46相对路径和dev.47采集窗口汇总失败保留，未据此关闭恢复任务；旧标签及ZIP不改写。原字节摘要与公开脱敏投影摘要分开记录，私有库／媒体／授权记录不提交。完整Harness、公共admission、授权配置、预算取消、运行时升级、类型检查、其他平台与质量／用户接受继续开放；V1余63项未完成，规格未同步或归档。

[Fixed evidence / 固定证据](evidence/filmcraft48-fixed-recovery-20261008.json). [Architecture / 架构](FilmCraft-Recovery-Architecture.zh_CN.md).

dev.58 增加恢复合同逐场景证据门禁。固定dev.57的133项安装测试无跳过、47行综合矩阵（含14类恢复必选）及FC-TX-002十个场景校验通过。缺失／重复证据、原文件变化、重复应用、失效epoch、活子进程占用和备份缺失均拒绝；合成回执、实际SQLite／受控进程及实际原生继续分别标记。新dev.58安装复验待执行，不提前关闭3.4—3.6，完整V1仍45项开放。 [Evidence](evidence/filmcraft58-recovery-candidate-20261009/contract.json).
