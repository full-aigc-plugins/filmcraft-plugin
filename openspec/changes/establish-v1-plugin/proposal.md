## Why

FilmCraft 需要将“可编辑视频剪辑与音画组织”落为可独立安装、可追溯、可恢复的 Agent 插件。已安装的上游 CLI 仅证明运行时可用，不能替代技能、Harness 与原生交付验收。

## What Changes

- 建立独立 `filmcraft-skills` 的发布与插件锁定引用规范；本变更不把技能源码改成插件私有内容。
- 定义运行时安装、能力探测、任务执行、工程与素材交付、质量修订和宿主发布门禁。
- 固化代表性验收：使用已有素材制作带字幕和配音的短片；重新打开工程；替换一个镜头后再次导出，未修改的片段参数保持不变。
- 交付中英文产品文档、架构、技术方案与 README；实现按任务与证据逐项推进。
- 补充 Dreamina 对照优化：统一参数校验、当前身份与历史证据分离、技能路由、能力快照、回执血缘、受控恢复、资源预算、独立评审、受限修订、分层验证及真实媒体矩阵。具体合同增量写入既有七项能力，实施细化见 [tasks.md 第 9 节](tasks.md#9-dreamina-对照优化增量2026-10-08)。

## Capabilities

### New Capabilities

- `skills-distribution`: 独立技能与不可变分发。
- `runtime-distribution`: 运行时安装、能力与回退。
- `task-execution`: 任务状态、幂等、授权与恢复。
- `artifact-delivery`: 原生工程、素材和产物证据。
- `quality-review`: 技术门禁与受限创作修订。
- `release-compatibility`: 宿主、权限与发布验收。
- `domain-workflow`: 可编辑视频剪辑与音画组织。

### Modified Capabilities

无。新仓库没有已实现行为或既有主规格。

## Impact

目标模块为未来的 `src/harness/`、`src/adapters/`、`runtime/`、`schemas/` 与独立技能仓库。四款上游应用保留各自工程格式；现有插件通过公开接口适配。ArtCraft Services 仅作为架构参考，不复制其受限许可代码。

优化实施的技能源归独立 `filmcraft-skills`，插件仅同步新发布的不可变快照。沿用 Node.js 24/TypeScript + SQLite 编排方案及已有 Python 原生适配器；公共协议继续由 ArtCraft 持有。候选源码、固定安装、实际宿主与完整产品验收分别记录；规范和任务补充不改变已有任务的完成状态。依赖、责任与验证产物见任务第 9 节，取舍见 [design.md](design.md#dreamina-对照优化增量2026-10-08)。

## Non-goals

用户已授权进入五插件及独立技能实施；本阶段不分发 GUI 应用、不接入真实付费生成，未完成宿主与创作验收前不发布市场条目。协议内容属于目标设计，不能当作现有工具。
