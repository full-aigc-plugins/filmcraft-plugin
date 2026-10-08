# FilmCraft V1 — PRD文档

> **文档说明**：V1 实施阅读视图；规范事实源为 OpenSpec。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](../1%E3%80%81FilmCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../5%E3%80%81FilmCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../../docs/FilmCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../../docs/evidence/runtime-baseline.json)

## 1. 版本目标与非目标

使用已有素材制作带字幕和配音的短片；重新打开工程；替换一个镜头后再次导出，未修改的片段参数保持不变。

本 PRD 是规范阅读视图；行为事实源是链接的 OpenSpec。未实现功能保持 planned。V1 不建设全新编辑器或多租户云平台。

## 2. 功能需求

| ID | 需求 | 行为摘要 | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| FC-SK-001 | 独立技能事实源 | 技能 SHALL 在独立技能仓库维护；插件仅同步固定 tag、commit 和 SHA-256 的发布副本；不得使用 latest、分支浮动引用或包外符号链接。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| FC-SK-002 | 独立安装与依赖声明 | 专业技能 SHALL 通过公开 CLI 接口运行；单独安装时不得依赖插件私有路径；ArtCraft 技能 SHALL 明确声明编排运行时依赖。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| FC-RT-001 | 运行时来源与完整性 | 运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| FC-RT-002 | 运行能力与隔离升级 | 适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| FC-TX-001 | 版本绑定与单写 | 执行 SHALL 绑定 planHash、inputHashes、projectRevision、runtimeIdentity 和有效授权范围；同一工程只有一个写入者，冲突不得覆盖用户修改。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-TX-002 | 幂等与不明确结果恢复 | 任务 SHALL 在副作用前登记幂等键；超时且执行结果未知时进入 reconciling；核对原任务或产物前不得重新提交。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-TX-003 | 取消与预算边界 | 任务 SHALL 区分 cancel_requested 与 cancelled；父子调用共享预算和截止时间；只允许一个层级负责同一副作用的重试。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| FC-AR-001 | 产物血缘与包完整性 | 产物 SHALL 登记逻辑 ID、不可变版本、内容摘要、来源任务、原生工程和依赖；交付前重新校验文件，移动后可按清单重关联。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| FC-AR-002 | 原生工程与交换损失 | 交付 SHALL 同时保留约定的原生工程与导出；工程需重新打开检查，交换中的扁平化、栅格化、字体和效果损失必须显式记录。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| FC-QA-001 | 技术与创作证据分离 | 质量结果 SHALL 分别记录工程、技术、创作和接受状态；证据绑定文件摘要及运行身份，NOT_RUN 不得当作 PASS，视觉评分不得覆盖技术失败。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| FC-QA-002 | 受限局部修订 | 质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；目标变化使旧验收与授权失效。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| FC-RL-001 | 宿主与发布证据 | 发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| FC-RL-002 | 权限与秘密边界 | 运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| FC-DM-001 | 素材导入与关联 | FilmCraft SHALL 登记视频、图片和音频的哈希、流信息、时长与引用，导入前检查缺失文件；素材移动后以哈希验证重关联。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-002 | 精确时间线编排 | FilmCraft SHALL 使用整数 ticks 与有理数时间基准记录入出点、轨道和片段顺序；JSON 中的大整数使用十进制字符串；拒绝越界片段。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-003 | 音画与配音组织 | FilmCraft SHALL 保持配音、音乐、原始音轨的独立身份与增益；验证输出音轨存在及同步；没有授权时不生成或上传声音。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-004 | 字幕时间与版式 | FilmCraft SHALL 保存字幕文本、语言、起止时间及样式；拒绝时间越界；缺少字体时报告替代影响，不悄悄更换。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-005 | 工程保存与局部修订 | FilmCraft SHALL 保存 .fcproj、重新打开并核对时间线；根据稳定片段 ID 修改单镜头，保留其他轨道与素材引用。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| FC-DM-006 | 预览与正式输出 | FilmCraft SHALL 区分代理预览与原生导出；正式输出必须解码验证尺寸、帧率、时长和音轨；不把 FFmpeg 替代输出标为原生导出。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. 非功能要求

工程单写；幂等重复不得增加副作用；秘密不得进入回执；所有验收绑定真实产物哈希；计划变化和 GUI 修改必须检测。初始修订上限 3 轮、单项目渲染并发 1 是待验证默认值，不是性能测量。

## 4. 端到端验收步骤

1. 从干净环境安装锁定运行时与技能。
2. 登记 fixture 素材与预期输出。
3. 执行计划，验证工程与导出。
4. 关闭并重开原生工程，检查对象可编辑性。
5. 执行代表性局部修改，比较不变对象。
6. 注入中断并恢复，核对没有重复副作用。
7. 在目标宿主重新执行并记录宿主版本。

## 5. 发布门禁

每个 P0 需求至少有成功与失败证据；未执行项标为 NOT_RUN。技术失败、原生损坏、摘要漂移或重复提交均阻断发布。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。

资源验收增量：源码候选已实现共享持久预算与明确取消确认；固定公开标签安装验证待执行，9.19—9.21和完整V1保持开放。

固定dev49／源42资源与取消通过9.19—9.21；完整产品／V1余60项开放，创作与用户接受仍NOT_RUN。

独立质量评审候选已区分工程、技术、创作与用户接受。高分不能覆盖技术失败，旧候选证据不可回放；内置测量保留可读性、连续性与节奏人工复核。固定dev.50验收待执行，9.22—9.24和完整V1尚未完成。

固定dev.50质量专项完成9.22—9.24，证据见 docs/evidence/filmcraft50-fixed-quality-20261008.json。独立工程／有界技术量测通过，创作人工复核与用户接受继续开放，不替代真实用户素材或完整V1验收；余57项任务。

受限修订候选保全非目标与依赖，未知结果不自动重放，停止后保留已验证最佳及未解决问题，无合格候选明确null。目标／rubric变化停止旧循环，创作与用户接受不由最佳代替。固定dev.51验收、9.25—9.27及完整V1仍开放。

固定dev.51／源42完成OpenSpec9.25—9.27：126项安装原生／状态测试无跳过、49类矩阵含9类受限修订专项、13技能／44执行文件保全，公共协议与四次发布CI通过。创作人工复核与用户接受仍开放，完整V1余54项。docs/evidence/filmcraft51-fixed-revision-20261008.json · docs/evidence/filmcraft51-fixed-revision-20261008.json。


固定 dev.52／源 dev.44 分层发行验收完成 OpenSpec 9.28—9.30：源真实 CI 181 PASS／36 环境 NOT_RUN；插件四次真实 CI 成功；固定安装原生／状态 126/126、零跳过，273 项前置检查和 32 项 headless／bridge 场景。11 组 30 场景的 180 条分层记录中 28 PASS、152 NOT_RUN；收集完整性 PASS，整体资格仍 NOT_PROVEN。真实媒体、其他宿主／平台、完整命令、创作／用户接受和完整 V1 保持开放，余 51 项。

证据 / Evidence: docs/evidence/filmcraft52-layered-release-20261008/report.json。

媒体矩阵输入准备已完成 OpenSpec9.31：7个场景、18项来源／许可／摘要绑定输入，VFR与181.211333秒长音频已实际测量；64项Python通过。原生矩阵9.32及固定安装9.33仍NOT_RUN，完整V1余50项。详见 docs/FilmCraft-Media-Matrix.zh_CN.md。

9.32首个固定52／源44真实派生VFR探针：原生保存／导出及完整解码通过，3.008秒成片，但独立8kHz单声道音频归一化相关性0.49865，低于0.98预期。分窗相关性也下降，根因待查；不关闭9.32或9.33，不降低验收阈值。证据 docs/evidence/filmcraft-media-fixtures-20261008/vfr-native-probe.json。

2026-10-09 开发版 dev.53 锁定技能源 dev.45，包含真实素材准备及失败探针证据；PCM 修复候选未进入默认 craft.4 安装。9.32/9.33 与50项完整V1任务仍开放。

2026-10-09 dev.54固定技能源dev.46及公开craft.5；七类候选原生矩阵、实际Whisper28词/100%参考词覆盖和公开原生首用通过。新固定宿主与媒体矩阵须发布后实际执行，9.32/9.33与50项完整V1任务暂不关闭。

固定 dev.54／source46／公开 craft.5 在真实隔离 Codex 安装完成七类原生媒体矩阵，13项技能与执行代码摘要保持不变；OpenSpec 9.32、9.33 已完成，完整 V1 仍有48项开放。验证仅覆盖当前 macOS arm64、Codex 和编码范围；创意、用户及其他平台验收仍开放。[固定安装证据](../../../docs/evidence/filmcraft54-fixed-media-20261009/report.json)。

dev.55 增加首次工作流可信宿主准入：完整任务与资源预算绑定 execute 主体，预检及原生提交前复核授权；缺失、过期、撤销或不匹配拒绝。7项单元、7个真实原生候选场景通过；固定安装验收待执行，完整V1仍开放。

固定dev.56／source46／craft.5的7项原生宿主准入验收通过，13项技能与全部执行文件摘要不变。OpenSpec3.1、3.2的测试和最小实现已完成；3.3的完整版本绑定／单写边界、其他调用路径、平台及完整V1仍开放，余46项。dev.55验证器误比较失败保留，不提升旧证据。

dev.57 增加版本绑定与单写逐场景QA：固定dev.56的五个规范场景已通过，包括真实工作流同目标竞争、不同目标并行、用户目录保全、真实保存后强杀所有者／拒绝重放／工程重开，以及签名桌面桥接保存后旧计划冲突。新dev.57安装复验待执行，3.3与完整V1继续开放。

2026-10-09 状态：FC-AR-001/002在固定dev.59的macOS arm64 Codex／headless完成全部8场景验收；仅产物合同任务5.1—5.3及5.6关闭，其他平台、创作／用户接受和完整V1仍开放。事实源仍为OpenSpec；证据见仓库 `docs/evidence/filmcraft59-fixed-artifact-contract-20261009/acceptance.json`。
