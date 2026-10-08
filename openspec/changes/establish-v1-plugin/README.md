# establish-v1-plugin

定义 filmcraft 独立技能、运行时与插件 V1 规格及验收任务

行为事实源为本变更的 [specs/](specs/)，总体范围见 [proposal.md](proposal.md)，设计取舍见 [design.md](design.md)。Dreamina 对照优化沿用该事实源，不新建平行 change。

- [优化任务第 9 节](tasks.md#9-dreamina-对照优化增量2026-10-08)：11 组优化、33 项任务，按失败用例、实现和验证分解，并声明优先级、责任及依赖。
- [中文优化设计](../../../docs/FilmCraft-Optimization-Architecture.zh_CN.md) / [English design](../../../docs/FilmCraft-Optimization-Architecture.md)：技能与插件分工、调用流程及验收边界。
- [需求任务映射](../../../docs/traceability.json)：稳定需求 ID 与任务 ID 的对应关系。
- [中文实施记录](../../../docs/FilmCraft-Optimization-Progress.zh_CN.md) / [English progress](../../../docs/FilmCraft-Optimization-Progress.md)：已有候选证据及未关闭项；以任务自身版本绑定证据判断完成。
- [Harness 源码候选](../../../docs/FilmCraft-Harness-Candidate.zh_CN.md) / [English candidate](../../../docs/FilmCraft-Harness-Candidate.md)：Node/SQLite 与现有 Python 的实际链路、旧回执映射及仍开放的恢复/预算/发行门禁。

本次文档补充不构成实现或验收证据，不勾选新增任务，不执行 apply、sync 或 archive。已有完成记录保留原范围。
