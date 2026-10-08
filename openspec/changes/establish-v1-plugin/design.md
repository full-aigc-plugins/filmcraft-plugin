# FilmCraft V1 Design

## Context

动机和边界见 [proposal.md](proposal.md)。当前已有独立技能源、固定插件快照及有界原生场景验收，具体范围以任务表及其版本绑定证据为准；完整 Harness、质量闭环和完整 V1 验收仍未完成。下文组件表描述完整目标合同，不否定已完成的有界实现。FilmCraft 的代表任务是：使用已有素材制作带字幕和配音的短片；重新打开工程；替换一个镜头后再次导出，未修改的片段参数保持不变。

## Goals / Non-Goals

**Goals:** 独立技能分发、可信运行时、声明式计划编译、可恢复任务、原生工程与导出双重交付，以及可追溯质量结论。

**Non-Goals:** 不重写上游应用，不实现 SaaS，不把原生交付降为只有图片/视频，未通过原生交付与宿主验收前不宣称插件已完成。

## Decisions

1. 独立 `filmcraft-skills` 是知识事实源，插件同步不可变发布副本；替代方案“插件内手工维护一套技能”会形成漂移，予以拒绝。
2. 官方 CLI/MCP 是执行端，适配器编译声明式计划并核对能力；替代方案“LLM 直接拼接任意 shell”无法保证接口和副作用边界。
3. 拟采用 TypeScript/Node.js 24 LTS、SQLite 与内容寻址文件。替代方案云数据库/队列对本地单用户 V1 没有必要，出现跨机器需求后另提变更。
4. 副作用先写意图和幂等键；不明确结果保留工程占用并 reconcile。替代方案超时自动重试会产生重复编辑或重复计费。
5. 公共协议由 ArtCraft 规范持有，领域仓只拥有自己的 payload 与映射。替代方案每个插件独立定义公共 JSON 将导致不兼容。
6. 技术验证与创作评估分离，已有有效用户授权持续生效；只在超范围动作或修改授权约束时要求新的授权。

## Component design

完整中英文运行时设计位于 [中文架构](../../../docs/FilmCraft-Runtime-Architecture.zh_CN.md) 和 [English architecture](../../../docs/FilmCraft-Runtime-Architecture.md)。领域计划对象包括 EditPlan, Sequence, Clip, CaptionTrack, AudioTrack，以下能力逐项编译：

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 素材导入与关联 | 登记视频、图片和音频的哈希、流信息、时长与引用，导入前检查缺失文件；素材移动后以哈希验证重关联。 | 计划中 |
| 精确时间线编排 | 使用整数 ticks 与有理数时间基准记录入出点、轨道和片段顺序；JSON 中的大整数使用十进制字符串；拒绝越界片段。 | 计划中 |
| 音画与配音组织 | 保持配音、音乐、原始音轨的独立身份与增益；验证输出音轨存在及同步；没有授权时不生成或上传声音。 | 计划中 |
| 字幕时间与版式 | 保存字幕文本、语言、起止时间及样式；拒绝时间越界；缺少字体时报告替代影响，不悄悄更换。 | 计划中 |
| 工程保存与局部修订 | 保存 .fcproj、重新打开并核对时间线；根据稳定片段 ID 修改单镜头，保留其他轨道与素材引用。 | 计划中 |
| 预览与正式输出 | 区分代理预览与原生导出；正式输出必须解码验证尺寸、帧率、时长和音轨；不把 FFmpeg 替代输出标为原生导出。 | 计划中 |

## State and recovery

核心状态为 planned、blocked、ready、running、reconciling、verifying、review_ready、completed、failed、cancel_requested、cancelled。同一原生工程单写；状态写入采用 epoch 防止过期执行者提交。原生应用不是账本事务的一部分，需要用检查点、文件核验和 reconciliation 收敛。父编排器不能将 accepted 当 completed，也不重复承担子插件的副作用重试。

## Risks / Trade-offs

| 风险 | 发现方式 | 处理与责任人 |
| :--- | :--- | :--- |
| R1 | 上游命令或格式变化 | Runtime owner：固定版本，比较 schema，重跑 fixture；未通过保持旧版 |
| R2 | 文字、透明或颜色交接损失 | Domain owner：保存源工程，生成 loss report，使用像素与对象检查 |
| R3 | 断线导致重复提交 | Harness owner：持久化意图与幂等键，先 reconcile，再决定重试 |
| R4 | 文档被误读为已实现 | Release owner：功能状态为 planned；无技能和运行时入口不得进市场 |
| R5 | ArtCraft 商标和受限许可代码边界 | Maintainer：独立实现；不复制上游 ArtCraft/Services 代码；品牌授权在发行前核对 |

## Migration Plan

新仓库无历史插件状态迁移。按 M1 运行时与技能 → M2 专业闭环 → M3 跨插件 → M4 宿主发布推进；ArtCraft 公共协议先定义，真实跨插件验收在领域端就绪后执行。升级采用版本目录与排空，保留旧组合；涉及状态 schema 时先备份，禁止不兼容回退。文档基线不进入可安装市场。

## Validation strategy

每条规范通过正向和失败场景验收；任务表关联需求 ID、测试与产物。验收覆盖清洁安装、原生重开、输出解码/像素检查、局部修改、中断恢复、重复调用与宿主加载。元数据检查、MCP 握手与单次调用不能替代完整创作验收。

## Deferred measurements

具体渲染吞吐、峰值内存、macOS x64/Windows/Linux 和各宿主版本兼容性必须通过 M2/M4 测量后填写，不影响当前本地优先架构与任务分解。名称与品牌资源使用由维护者在发行门禁核对。

## 交换报告实施决策

报告生成器属于各独立技能源，插件仅消费不可变快照。报告绑定原生、重开记录与导出摘要；lost/observed/unknown 不互相提升。ArtCraft 严格核验报告结构和实际文件，不允许 nativeSubstitute；历史无报告的交付不补造证据。实现与真实回归已验证，跨编辑器完整保真任务仍待验收。

## CLI 场景技能增量设计

参考 Dreamina 的 use / CLI / setup / 业务场景分层，但按真实命令划分任务。四原生 CLI 保持各自 argv 和工程保存语义；每个技能打包自己的最小运行资源，禁止跨技能文件路径。共有资源在仓库发布脚本中按摘要同步，避免手工维护多份逻辑。上游 ArtCraft 的 scene 保存、生成请求与异步轮询仅作为设计参考，不复制受限代码；本项目 ArtCraft CLI 的事实源为现有 src/cli.ts。原有 use 公开入口保持兼容。插件从新不可变技能源标签同步全部清单，宿主验收锁按新版本单独更新。

## Dreamina 对照优化增量（2026-10-08）

本轮补充既有 7 项能力的场景与任务，不建立新的规格事实源。规范仍为本变更的 specs；[中文优化设计](../../../docs/FilmCraft-Optimization-Architecture.zh_CN.md) 与 [English optimization design](../../../docs/FilmCraft-Optimization-Architecture.md) 说明取舍和实施顺序，追踪见 [任务第 9 节](tasks.md#9-dreamina-对照优化增量2026-10-08)。新增任务按源码候选、固定安装及完整验收分别记录；历史通过记录不覆盖新增验收。实施记录见 [中文进展](../../../docs/FilmCraft-Optimization-Progress.zh_CN.md) 与 [English progress](../../../docs/FilmCraft-Optimization-Progress.md)。

保留既定 Node.js 24/TypeScript + SQLite Harness 方案，用于编排、租约、操作意图与资源账本；已验证的 Python CLI 适配继续负责原生操作，不复制编辑逻辑。公共协议归 ArtCraft，领域侧以兼容映射关联现有回执。借鉴 Dreamina 的路由、持久化尝试记录、独立评审、证据绑定及受限修订；本地编辑预算采用时间、磁盘、输出字节、并发和修订轮数，不直接套用云端积分、授权或 submitId 语义。

依赖顺序为入口一致性及身份/能力快照 → 回执映射 → 恢复与资源边界 → 独立评审和受限修订；技能路由可独立推进，CI 和真实媒体矩阵为各阶段提供验证。只读诊断不改账本、不重放操作；有副作用的状态修复与继续执行另走租约和意图门禁。原授权范围内持续执行，作品变化使旧质量证据失效，授权范围或约束改变才需要新授权。

恢复验收进一步区分“读取状态”“修复账本”“继续原生执行”。SQLite 只读连接仍可能处理 WAL/SHM，因此诊断采用一致的隔离快照并验证原文件保全；读取期间变化返回 unknown。恢复意图先持久化，证据摘要与预期 epoch 在应用前重新检查，并发或过期所有者不能重复提交。已修复尝试的重复请求以新鲜诊断复用原结果，不能提升质量状态。只读不迁移；受支持升级遵循备份策略，未知版本或外来账本不认领。行为以 FC-TX-002 的四项专项场景为准，具体故障矩阵与交付物见 9.16—9.18；本次细化不证明候选实现或固定安装已经通过。

### 参考出处与领域取舍

下表对应本次直接读取的 Dreamina Canvas 插件固定提交 `3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b`；只是设计参考，不是 FilmCraft 验收证据。两个 Dreamina 仓库及 FilmCraft 插件的 CodeGraph 均未初始化，因此本次依据当前文件静态分析，未创建索引。独立 Dreamina 技能源的 `dreamina-canvas-use`、`dreamina-video-evaluator` 和 `dreamina-video-production` 补充了按意图交接、先测量后评审和分阶段制作的参考；技能中声明的工具仍需核对实际可用性。

| 可借鉴设计与固定来源 | FilmCraft 落点 | 不照搬的语义 |
| :--- | :--- | :--- |
| [use 路由](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/skills/dreamina-canvas-use/SKILL.md)：入口唯一、按需加载 | FC-SK-003；9.7—9.9，13 技能主次意图与自身资源 | 不新增没有真实账户接口的 auth 技能，不复制全部技能正文 |
| [operation_ledger.py](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/scripts/operation_ledger.py)：持久身份、未知结果不重提 | FC-AR-001 / FC-TX-002；9.13—9.18，task/attempt 与租约、epoch | 云端 submitId 不等于本地进程、工程或操作尝试身份 |
| [artifact_guard.py](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/scripts/artifact_guard.py)：目录、字节数与摘要校验 | FC-AR-001 / FC-DM-006；9.13—9.15、9.31—9.33，依赖包、原生重开及解码 | 下载摘要正确不等于原生工程完整、音画正确或创作通过 |
| [judge_exchange.py](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/scripts/judge_exchange.py)：独立请求/回执、候选绑定 | FC-QA-001；9.22—9.24，增加时间线、音频与用户接受维度 | 图像单轮控制器不证明视频时序或音频评审，声明 freshContext 不代替实际上下文隔离 |
| [prompt_revision.py](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/scripts/prompt_revision.py)：源版本检查、字段保全 | FC-QA-002；9.25—9.27，时间区间、对象、轨道和依赖差异 | 生成块整块替换规则不套用于 FilmCraft 工程局部编辑 |
| [budget.py](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/scripts/budget.py) 与 [harness](https://github.com/full-aigc-plugins/dreamina-canvas-plugin/blob/3d21ce5e7ddb164a626f18701f9f4ed8ba279f2b/skills/dreamina-canvas-harness/SKILL.md)：保守预留、停滞停止与 draining | FC-TX-003 / FC-QA-002；9.19—9.21、9.25—9.27，本地资源与停止确认 | 积分审批不替代已有本地授权；draining 不等于原生 cancelled |

统一整数校验、运行时参数漂移、当前身份提取、分层 CI 和真实媒体矩阵是 FilmCraft 自身差距补强，不声称 Dreamina 已提供这些领域实现。全部 11 组的规范场景与任务对应关系见 [tasks.md 第 9 节验收索引](tasks.md#验收索引与交付记录)。

能力声明采用既有领域计划的可选 `requires` 扩展，不改变 ArtCraft 公共协议。声明只表达所需模式、身份、参数契约摘要及资源名称，实际状态由执行器探测。无声明的旧计划继续接受必要实时检查；bridge 必须核验桌面身份。资源探测复用同一原生上下文，区分目录发现与实际安装/显示/推理/导出，并在依赖操作前重新确认变化的资源与契约。成功交付和失败阶段均保留能力证据；详细合同见 FC-RT-002-PLAN-REQUIRES 与 FC-RT-002-RESOURCE-PROBE，实施仍由 9.10—9.12 验收。

恢复实施合同增补：继续执行只接受已经独立修复至 verifying 且当前血缘完整的原生工程，以及显式绑定原工程的新计划；新任务/继续意图先持久化，原未知尝试不自动重放。恢复授权由可信宿主查询器或宿主管理的私有本地授权目录核验，引用相等不代表有效授权。当前状态 schema3 增加继续意图，schema1/2 写打开不自动升级；显式维护先排空写租约、独占写入并保全原 DB/WAL 与 SHM 审计，升级前验证备份，回退拒绝会丢弃新操作的情况。此说明不代替9.16—9.18源码与固定安装逐项验收。

资源实施增补（9.19—9.21，在研）：schema4 在同一 SQLite 账本增加 resource_scopes、task_resources、cancel_intents；schema1/2/3 的写打开要求显式备份升级，不静默迁移。根任务的不可变预算和截止时间由可信宿主传入；原生工作流启动前提交时间、磁盘、输出、槽位、修订预留。明确继续执行继承同一预算域并消耗一轮修订，不建立第二份额度；运行时安装/能力预检仍属独立 setup 门禁，不能用此预算声明其受控。

未知尝试保持完整预留；只有已确认结束的任务才结算实际字节/时间并释放槽位，保留的部分产物仍占磁盘额度。并发槽位暂满只拒绝当前调度，硬限/磁盘不足持久停止后续依赖；执行期间监测输出和时间，触限后仍未停止的原生任务不能变成已取消。磁盘预留为保守准入与观察，不能保证其它系统进程不耗尽文件系统，也不是操作系统级磁盘配额。

取消主题绑定根任务、共享预算和截止时间，由可信宿主重新核验；请求先持久化，撤销活动执行者的提交权并阻断新依赖。原生进程身份使用内核出生时间、启动会话、UID、进程组和执行文件；重启后的 PID 相等不足以发送信号。仅对身份一致且声明可停止的本任务 POSIX 进程组发送 SIGTERM；不自动升级 SIGKILL。进程身份不可读、组仍存在或不支持终止时保持 cancel_requested/unknown 与工程占用。只有进程组不存在的停止证据才收敛至 cancelled；不删除部分输出、回执或诊断。Windows 与脱离已受控进程组的运行时不据此声明取消通过。

独立质量实施增补（9.22—9.24，在研）：质量请求只从当前 verifying 任务及重新核验的同尝试交付生成，绑定输入、工程、完整候选文件集合、目标/约束、rubric、执行身份及可信宿主配置的评审者身份。最小上下文只暴露必要作品文件，排除生成器计划解释、聊天、自评及辩护；外部评审进程使用新目录、显式环境和冻结文件副本，进程由宿主实际启动并记录，不能由回执自行声称 freshContext。该边界不冒充操作系统文件沙箱。

回执与请求原字节保存至质量证据 CAS；质量证据不成为第二操作状态账本。读取/应用前重新核验当前任务、候选、目标、rubric 和评审者；变化使旧结论失效。工程、技术、创作、用户接受分别计算，解码失败优先阻断；完整作品的解码/PTS/音频量测与静态帧证据明确区分。字幕时序、可读性、内容音画同步、削波、连续性及节奏按所需证据分别给 PASS/FAIL/NOT_RUN/manual_review，不从容器起始时间对齐推导内容同步，也不从客观量测推导审美或用户接受。

宿主/人工评审导入需要宿主提供独立的可信身份与上下文核验器；记录里的 freshContext、reviewer 字段或生成器身份本身不能授权导入。用户接受默认 NOT_RUN；单独、绑定请求的可信用户决定接口尚待后续实施。当前阶段不自动把任务写成 completed；独立质量证据与后续受限修订闭环另行连接。
