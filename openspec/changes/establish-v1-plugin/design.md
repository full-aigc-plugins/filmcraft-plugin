# FilmCraft V1 Design

## Context

动机和边界见 [proposal.md](proposal.md)。当前只有文档、元数据与运行时基础证据；专业技能、Harness 和原生交付验收仍待实现。FilmCraft 的代表任务是：使用已有素材制作带字幕和配音的短片；重新打开工程；替换一个镜头后再次导出，未修改的片段参数保持不变。

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
