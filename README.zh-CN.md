# FilmCraft Agent Plugin

独立技能驱动的可编辑视频剪辑与音画组织.

[English](README.md) | [简体中文](README.zh-CN.md)

## 当前版本与可复现宿主验证

此前完成宿主验证的插件/技能源版本：`0.1.0-dev.3`。Codex 0.147.0 与 0.153.4 均安装五个固定公开发布，发现全部 58 项启用的命名空间技能，加载错误为零，来源摘要一致。五项代表流程已通过 0.147.0 安装后的场景技能入口验证，包括原生工程、局部修订和 ArtCraft 在线混合流程。模型自动派发、桌面 GUI、创作最终评审和完整交换保真尚未验证。

[宿主验证设计](docs/FilmCraft-Host-Verification-Architecture.zh_CN.md) · [绑定版本的证据](docs/evidence/codex-skill-suite.json)。历史里程碑保留原证据范围；当前版本身份以 manifest 和锁文件为准。

> 开发版已通过固定标签的 Codex 安装、技能发现和原生代表工作流；完整产品与创作验收仍未完成。

独立技能包已进入实施，单技能隔离安装已在 macOS arm64 实测；完整创作流程与插件宿主验收仍未完成。[证据](docs/evidence/bootstrap-tests.json)

## 定位

使用已有素材制作带字幕和配音的短片；重新打开工程；替换一个镜头后再次导出，未修改的片段参数保持不变。

面向需要原生可编辑工程、反复修改和可靠自动化的创作者。

## 一眼了解

```text
Intent + assets
  -> independent Skills (pinned development release)
  -> public skill workflow / ArtCraft adapter
  -> verified runtime / child adapter
  -> native project + preview + export + evidence
```
| Property | Value |
| :--- | :--- |
| Plugin ID | filmcraft |
| Metadata version | 0.1.0-dev.9 |
| Stage | implementation-in-progress |
| Skills source | filmcraft-skills / v0.1.0-dev.8 |
| Execution | 上游 CLI；ArtCraft 使用子适配器 |
| Host compatibility | Codex development install/discovery pass; GUI and other hosts pending |
| License | Apache-2.0 (original repository content) |


## 能力与边界

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 素材导入与关联 | 登记视频、图片和音频的哈希、流信息、时长与引用，导入前检查缺失文件；素材移动后以哈希验证重关联。 | 待完整验收 |
| 精确时间线编排 | 使用整数 ticks 与有理数时间基准记录入出点、轨道和片段顺序；JSON 中的大整数使用十进制字符串；拒绝越界片段。 | 待完整验收 |
| 音画与配音组织 | 保持配音、音乐、原始音轨的独立身份与增益；验证输出音轨存在及同步；没有授权时不生成或上传声音。 | 待完整验收 |
| 字幕时间与版式 | 保存字幕文本、语言、起止时间及样式；拒绝时间越界；缺少字体时报告替代影响，不悄悄更换。 | 待完整验收 |
| 工程保存与局部修订 | 保存 .fcproj、重新打开并核对时间线；根据稳定片段 ID 修改单镜头，保留其他轨道与素材引用。 | 待完整验收 |
| 预览与正式输出 | 区分代理预览与原生导出；正式输出必须解码验证尺寸、帧率、时长和音轨；不把 FFmpeg 替代输出标为原生导出。 | 待完整验收 |

不重写上游编辑引擎，不暗中改变原生交付格式，不宣称 GUI 或跨平台验收完成。

## 架构与文档

- [完整运行时架构](docs/FilmCraft-Runtime-Architecture.zh_CN.md)
- [技术方案与路线](product-docs/FilmCraft/5%E3%80%81FilmCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md)
- [V1 PRD 与需求映射](product-docs/FilmCraft/V1/5%E3%80%81FilmCraft-PRD%E6%96%87%E6%A1%A3-V1.md)
- [完整文档导航](docs/README.zh-CN.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [专业领域技术设计](docs/FilmCraft-Domain-Design.zh_CN.md)

## 当前可执行的快速开始

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
以上校验文档和规范，不运行产品工作流。OpenSpec 校验使用 1.13.1；本仓不自动安装工具。

已安装官方 CLI 后可执行基础检查：

```bash
filmcraft-cli --version
```

本次记录结果为 0.2.0。独立技能的 bootstrap 与 workflow 是当前开发版入口；插件安装与技能发现已有证据；完整宿主验收仍待完成。

## 配置与运行时

目标配置包含 CLI 路径、允许读写根目录、运行模式、预算、超时与输出目录；配置 schema 尚待实现。技能锁文件固定已发布的独立技能源提交与内容摘要。运行时锁文件中的摘要来自真实官方制品，只证明已记录平台的基础运行。

## 可靠性与安全

规划要求：单工程写入锁、版本前置条件、持久化意图、幂等键、不明确结果核对、原生工程检查点、产物摘要及受限修订。密钥只通过宿主秘密引用传递；素材元数据不作为执行指令。

## 验证与成熟度

[脱敏 CLI 证据](docs/evidence/runtime-baseline.json)

| 层面 | 状态 |
| :--- | :--- |
| 上游 CLI 与只读 MCP | 已观察，仅 macOS arm64 |
| 独立技能与适配器 | 技术工作流已验证；完整 Harness 待完成 |
| 原生工程与创作验收 | 原生技术用例通过；创作质量待验收 |
| 目标宿主安装 | Codex 受控安装与发现通过；完整宿主验收待完成 |


## 路线与贡献

| 阶段 | 交付 | 进入下一阶段条件 |
| :--- | :--- | :--- |
| D0 | 双语文档与 OpenSpec 基线 | 文档、链接、规范校验通过；实现任务仍未完成 |
| M1 | 独立技能与运行时适配 | 清洁环境安装、摘要检查、真实 MCP 调用 |
| M2 | 专业领域完整闭环 | 代表任务、工程重开、输出解码、局部修改 |
| M3 | ArtCraft 跨插件协作 | 版本传播、局部失效、断线恢复与幂等 |
| M4 | 宿主与发布验收 | 宿主实装与多平台证据；市场清单一致 |

先更新 OpenSpec 再实现行为；每项任务通过实际验收后才能勾选。中英文文档同时维护。参考 CONTRIBUTING.md 与 AGENTS.md。

## 许可与上游

原创内容遵循 [Apache-2.0](LICENSE)。这是第三方集成规划，不代表上游背书。四款应用的代码许可与 ArtCraft/Services 的受限许可分别处理；不复制上游 ArtCraft/Services 代码或品牌资产。

[Upstream FilmCraft](https://github.com/storytold/filmcraft) · [Issues](https://github.com/full-aigc-plugins/filmcraft-plugin/issues)

独立技能已通过原生短片工作流验证：隔离首次安装、工程重开、素材收集、音频与字幕，以及交付目录移动后的单镜头修订（14 项测试）。参见[运行证据](docs/evidence/film-workflow-tests.json)。完整 Harness、插件宿主和创意验收仍未完成。

独立技能现已绑定当前已发布开发标签 `v0.1.0-dev.4`，`skills.lock.json` 固定来源提交与整个技能摘要。使用 `python3 scripts/vendor/skill_vendor.py check` 核对。技能源快照发布不代表宿主验收或生产完成。

## 开发版独立技能安装与使用

安装独立技能：`npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-use`。安装技能后，从其真实目录运行公开入口；插件快照也包含相同技能。

```bash
python3 -I -B skills/filmcraft-use/scripts/bootstrap.py
python3 -I -B skills/filmcraft-use/scripts/workflow.py --help
```

首次入口会安装锁定官方 CLI 到用户数据目录；要求 macOS arm64 与 Python 3.11+。使用技能内示例计划并提供真实素材；交付与修订合同见技能的 SKILL.md。[来源与校验证据](docs/evidence/skill-publication.json)。

## Codex 开发版宿主验证

五个插件已在隔离 Codex 配置中从公开标签安装，app-server 发现带命名空间的技能且无加载错误；安装缓存中的 ArtCraft 入口已交付四种原生工程。[宿主证据](docs/evidence/codex-installation.json)。此为受控开发验收，不代表桌面 GUI、其他宿主、完整创作或正式市场发布通过。

开发版本 `0.1.0-dev.1` 同步独立技能的安装锁等待修复；并行安装和复用按有界互斥协调，原生任务不自动重放。

当前开发里程碑为原生交付增加摘要绑定的交换损失报告，区分 lost、observed、unknown；派生导出不替代原生工程。跨编辑器字体、效果和蒙版保真尚未验证，完整交换验收任务保持未完成。

## CLI 与场景技能体系

技能源包含 11 项可独立安装的技能，分为安装、CLI 公共操作与场景任务。[架构与清单](docs/FilmCraft-Skill-Suite-Architecture.zh_CN.md)。运行时与插件版本分别维护；旧宿主证据保持原版本范围。

## 场景技能的干净首次使用

八项 FilmCraft 场景技能均在 macOS arm64 通过独立首次安装与真实操作：只复制当前技能，从锁定公开地址安装到新运行时目录，核对原生修改、实际音频采样和渲染像素、原工程保留与未知命令拒绝。完整回归 31 项通过、零跳过。[证据](docs/evidence/task-skill-first-use.json)。该结果只覆盖列出的操作，全部命令、GUI 和创作最终验收仍未完成。

```bash
CRAFT_TASK_FIRST_USE=1 CRAFT_LIVE_TEST=1 CRAFT_LIVE_SUITE=1 python3 -B -m unittest discover -s tests -v
```

在独立 `filmcraft-skills` 仓库执行；真实测试另需 ffmpeg、ffprobe 与 Pillow。

历史插件 `0.1.0-dev.5`／技能源 `0.1.0-dev.4` 的路径修正里程碑。命令示例以宿主实际加载的 `SKILL.md` 所在目录调用脚本。全部技能在用户、项目与插件三种含空格布局中通过隔离入口检查。[路径证据](docs/evidence/installed-skill-paths.json)。此前宿主验证仍对应其记录版本，既有安装需更新。

插件 `0.1.0-dev.5` 从固定公开标签重新取快照并修正整个技能摘要，未带入本地 Python 缓存。插件标签 `v0.1.0-dev.4` 的摘要误包含被忽略的开发缓存，已被替代，不可安装该标签。

当前固定发布的宿主核验（2026-10-06）：Codex 0.153.4 安装五个当前固定插件，加载全部 58 技能并逐项核对内容身份。本插件代表性原生工作流从实际安装路径调用，在新的原生运行时中完成创建、重开和修订检查；五工作流调用后，全部 58 个技能摘要保持不变。[证据](docs/evidence/codex-current-release-20261006.json)。显式标签生成器由 ArtCraft 统一持有。模型派发等待授权，GUI、创作与完整宿主验收仍未完成；本次 QA 维护不改变已发布技能/运行时内容或标签。

开发版 dev.6 固定内置 FilmCraft 技能 dev.5（d7773c802a227368e0d0e2c02534bace21bc097f）。维护版原生 CLI 0.2.0-craft.1 修复字幕字体渲染，工作流显式开启成片烧录。公开地址单技能首次安装、中文字幕与真实配音验收通过；源码完整回归 44 项全部通过，无跳过。[证据](docs/evidence/chinese-first-use.json)。当前版本宿主发现、GUI/模型分发及 ArtCraft 新捆绑包仍需另行验收。

当前固定发布矩阵（FilmCraft dev.6、EffectCraft dev.7、PhotoCraft dev.6、VectorCraft dev.6、ArtCraft dev.17）在隔离 Codex 安装后通过 58 技能发现及原生代表工作流；执行后所有技能摘要保持不变。[宿主安装内容的原生验证](docs/evidence/codex-release17-native-20261006.json)。此证据不代表模型调度、GUI 或完整创作验收。

当前实际安装的插件 dev.6／技能 dev.5 使用维护版 CLI 0.2.0-craft.1，八类独立场景冷启动全部通过（43.688 秒）。已记录输入、输出、测试驱动和原生摘要，全部 58 个安装摘要不变；补齐旧 0.2.0 场景证据的版本缺口，发行版字节不变。[证据](docs/evidence/maintained-runtime-task-first-use.json)。

候选安装回执复用校验已实现并验证，固定插件发布与 ArtCraft 同步仍待完成。[架构与证据](docs/FilmCraft-Runtime-Receipt-Architecture.zh_CN.md)。

开发版 dev.7 内置固定技能 dev.6（85866c064c7d91abd8da63b0570d78bee3202bf5）。复用安装前核对回执身份；内置快照的四项测试通过，包括公开地址冷安装、原生重开及 11 个隔离 CLI 入口。[候选证据](docs/evidence/runtime-receipt-candidate.json)。固定 Codex 宿主验收和 ArtCraft 依赖同步仍待完成。

固定 FilmCraft 插件 dev.7／技能源 dev.6 已通过 Codex 0.153.4 实际安装与四项安装快照测试：公开地址冷安装、保存重开、回执异常拒绝／恢复，以及 11 个独立 CLI 入口。执行后全部 58 个安装摘要保持不变。[固定发布证据](docs/evidence/codex-filmcraft7-receipt-first-use-20261006.json)。ArtCraft dev.42 仍锁定技能源 dev.5，其更新待完成。

[时间变化素材的裁切与移动验收](docs/FilmCraft-Temporal-Timeline-Acceptance.zh_CN.md)：实际安装的独立时间线技能空运行时测试 1 项通过；保存重开及原生导出均核对源入点，保留其他镜头、音轨、字幕和原交付。完整时间线／创作验收仍开放。

插件 dev.8 固定技能源 dev.7，补齐原生工作流静态音轨增益（mixer.setStrip）、有限数值校验和隔离候选 -6 dB 解码。固定安装副本真实冷启动增益验收通过，58 项技能发现与执行后摘要保留；[证据](docs/evidence/codex-filmcraft8-audio-gain-first-use-20261006.json)。[范围与架构](docs/FilmCraft-Audio-Gain-Architecture.zh_CN.md)。

固定插件 dev.8 已验证已有配音、音乐、视频原音三个独立音轨、错开起点和仅音乐增益返工，使用实际解码频率幅度核验；全部 58 项安装摘要保持不变。[范围与证据](docs/FilmCraft-Multitrack-Audio-Architecture.zh_CN.md)。

已发布技能源 dev.8 修复必需源音轨缺失却因自动静音 AAC 误成功的问题，保留失败诊断，明确无声视频与有意静音 WAV 仍可交付。[架构与范围](docs/FilmCraft-Required-Audio-Architecture.zh_CN.md)。固定插件 dev.9 安装后 3 项真实验收通过，全部 58 项摘要保留。[证据](docs/evidence/codex-filmcraft9-required-audio-first-use-20261006.json)。

开发快照 dev.10 同步不可变 FilmCraft 技能源 dev.9，锁定公开 CLI craft.2。已有源码冷安装序列与实际 Effect→Film 交接证据；安装后的固定快照和 Art 混合验收仍待完成。[架构与证据](docs/FilmCraft-Public-Sequence-First-Use-Architecture.zh_CN.md)。

固定 Film 插件 dev.10 已通过 Codex 0.153.4 隔离安装后的序列首次使用验收。58 项技能发现且零加载错误，Film 执行后全部摘要保持不变。[有界证据](docs/evidence/codex-filmcraft10-sequence-first-use-20261006.json)；Effect／Art 动态发行联调仍待完成。
