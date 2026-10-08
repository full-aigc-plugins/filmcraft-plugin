# FilmCraft Agent Plugin

四领域RT-001运行时来源与完整性已完成当前全部场景验收，固定技能字节保持不变；运行时升级与完整首版仍开放。[验收架构](docs/Craft-Fixed-Runtime-Integrity-Architecture.zh_CN.md)。

已有素材与剪辑需求进入，交付可重开的 `.fcproj`、素材清单、预览和成片。

当前插件：`0.1.0-dev.41`；技能源：`0.1.0-dev.38`；13 个独立技能。

已验证首次使用平台：macOS arm64、Python 3.11+。固定运行时安装在用户数据目录，技能文件保留在宿主加载目录。当前为开发版本；完整首版验收及通用 Skills CLI 实际安装仍未完成。

固定音频尾部验收：Film 插件 dev.33／源 dev.31、Art 插件 dev.103／源 dev.77 已通过实际安装首用。64 项安装身份核验；23 项有变更技能逐个空运行时安装通过（258.282 秒），另 41 项摘要未变并复用原冷安装证据。音频尾部、增益另存、显式越界拒绝、五子工程配音混合交付、移动包和品牌返工／无关节点复用通过；不关闭通用 Skills CLI、创作审批或完整 V1。[版本绑定证据](docs/evidence/craft-art103-audio-tail-fixed-first-use-20261007.json)。

历史版本证据：当前采样时长修复验收：Film 插件 dev.34／源 dev.32、Art 插件 dev.104／源 dev.78 已通过固定公开标签的实际安装。64 项安装文件身份复核通过；本次 23 项技能分别空运行时安装（Film 13 项、Art 10 项），另 41 项仅在完整摘要一致后复用历史冷安装证据。2.20 秒及 2.211 秒音频尾部、增益另存、显式越界拒绝、序列迁移、带字幕配音短片局部修改、五子工程混合交付、移动包及品牌依赖返工通过。这仅关闭采样时长修复的有界发行门禁，完整 V1、通用 Skills CLI、模型调度和创作验收仍未完成。[当前固定证据](docs/evidence/craft-art104-sample-audio-fixed-first-use-20261007.json)。

历史版本证据：当前 Film 插件 dev.34／源 dev.32／原生 craft.3 的十项独立场景测试通过：工程、素材、时间线、音频、字幕、调色、运动、时间文本、多机位和导出。每项只复制自身技能并从新运行时目录公开安装，断言真实原生另存／重开、渲染帧或解码音频及非目标保全。十项无跳过通过（67.330秒），64项原安装摘要仍匹配固定锁。时间文本使用已提供的带时间词句；自动ASR、实际通用Skills CLI安装、全量命令上下文与完整V1保持未完成。 [证据](docs/evidence/filmcraft34-ten-scene-first-use-20261008.json).

维护者来源校验拒绝符号链接、不完整锁及版本同名分支，并在替换任一管理技能前检查全部声明来源；已发布技能／运行时身份保持。[快照预检架构](docs/Skill-Snapshot-Self-Contained.zh_CN.md)。

## 首次使用

在宿主中调用 **`filmcraft-use`**。直接使用 CLI 时，将 `SKILL_DIR` 设为宿主实际加载的 `SKILL.md` 所在绝对目录；可能位于用户／项目 `.agents/skills`、插件内部或宿主缓存，以实际路径为准。以下入口在调用前安装并核验固定运行时。

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands --json
```
<!-- CRAFT_FIRST_USE_END -->

实际制作、所需输入、原生工程和局部修改参见[可编辑工作流](skills/filmcraft-use/references/workflow.md)。[安装与技能入口](skills/filmcraft-use/SKILL.md) · [版本绑定历史](RELEASE-HISTORY.zh-CN.md)。版本与命令查询验证安装和发现，不代表创作完成。

[首次使用入口证据](docs/evidence/craft-readme-first-use-navigation-20261007.json)。

固定安装路径验收：独立技能及 Art 混合工作流在含中文和空格的路径下，通过原生创建与重开、定点返工及导出；Art 另验证移动交付包。技能与运行时身份保持不变。该结果仅覆盖 macOS arm64 的本次首次使用场景。 [路径验收证据](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

固定发行前的历史源码候选：结构损坏的 runtime／Node 锁在写运行时目录或下载前返回本地恢复诊断。五项候选原生首次使用通过；发布插件快照保持不变，新不可变发行安装需另行验收。 [锁诊断候选](docs/FilmCraft-Lock-Shape-Architecture.zh_CN.md).

---

固定原生首次安装与完整命令恢复验收通过：新版五插件58技能逐项独立冷安装，十个Art技能分别安装四领域；四个原生下载半包SSL EOF恢复、72个原生保存后故障、四个健康命令返工及混合HD返工／恢复／移动包通过，全部安装摘要保全。仅关闭领域2.10／8.11与Art4.10；2639条命令逐项、GUI、模型、通用Skills CLI及完整V1仍开放。 [版本及证据](docs/evidence/codex-native-download-first-use-20261007.json).

历史发行记录：当前插件：`0.1.0-dev.21`；技能源：`0.1.0-dev.19`；固定原生命令网关首用已通过，全量逐命令／GUI／模型／完整V1仍开放。

历史发行记录：当前插件：`0.1.0-dev.21`；技能源：`0.1.0-dev.19`；固定原生命令网关首用已通过，全量逐命令／GUI／模型／完整V1仍开放。

固定发布前的候选记录：原生下载恢复候选：最多三次只读重试并丢弃半包；此前固定版本冷安装遇到SSL EOF失败，修复后的固定安装验收仍开放。

历史插件版本记录 `0.1.0-dev.19`／技能源 `0.1.0-dev.17` 固定完整命令内层JSON修复；实际安装首用复验进行中。

当前固定失败暂存验收：插件 dev.18、独立技能源 dev.16。全部58项独立CLI冷启动、24个原暂存原生故障案例及37原生场景＋6合同检查通过；Art77领域包升级仍开放。[证据](docs/evidence/codex-failed-stage-first-use-20261007.json)。

固定领域客户端首用复验：Film 插件 dev.16／技能源 dev.15，Effect／Photo／Vector 插件 dev.15／技能源 dev.14。隔离 Codex 发现58项零错误；实际安装副本24类保存后故障、四个健康公开工作流和已发布 Art 引擎＋安装后 Vector 客户端六类故障通过，全部58项安装摘要保全。Art dev.75 内置旧领域分发包尚需升级，全量命令／GUI／模型验收仍开放。[版本绑定证据](docs/evidence/codex-public-workflow-session-first-use-20261007.json)。
先前固定版本协议故障首用复验通过：48个独立技能源共288例，实际安装副本24例及四领域健康返工通过；58项安装摘要保持一致。验收范围与固定标签见 [协议故障验收记录](docs/evidence/codex-protocol-fault-first-use-20261007.json)。全量逐命令／GUI验收以及Art领域包升级仍开放。

协议故障修复候选：本领域11项技能逐个单独复制、空运行时公开安装后，原生保存成功再注入六种坏回复全部通过（66例，零跳过）。不重放、未知回执、工程重开与交付／技能保全均已检查。[证据](docs/evidence/protocol-fault-first-use-20261007.json)。固定安装副本与Art领域包升级仍为独立门禁。

固定插件 0.1.0-dev.14／技能源 0.1.0-dev.13 已通过安装后的返工门禁：隔离 Codex 发现全部58项技能零加载错误，本领域安装技能从空运行时直接执行文档创建／返工计划、保存重开与非目标保全。全部58项安装摘要不变，当前固定发行CI通过。[固定返工证据](docs/evidence/codex-complete-command-revision-first-use-20261007.json)。全量命令／GUI／模型验收保持开放。

本领域 11 个技能逐个单独复制、从各自空运行时公开安装后，配套返工计划全部通过（67.161 秒，零跳过）。[返工证据](docs/evidence/complete-command-revision-first-use-20261007.json)。更新快照的真实固定宿主安装另设门禁。

完整命令入口补充了配套的创建／返工 JSON 示例、重新打开后的显式选择前置条件，以及原生保存重开、非目标对象与像素检查。每个独立技能均包含两个可执行计划。[调用指南](skills/filmcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision)。全量逐命令及 GUI 验收保持开放。

先前固定发行首用通过：隔离 Codex 0.153.4 发现全部 58 项技能零加载错误；每项安装技能独立空运行时公开安装（385.234 秒）；安装后的领域新命令入口及 Art 1080p 混合返工／恢复／移动包检查通过。全部安装摘要保全，固定 CI 与五包重建通过。[版本绑定证据](docs/evidence/codex-complete-command-first-use-20261007.json)。通用 Skills CLI、全命令／GUI 与完整创作验收仍开放。

## 完整原生命令入口

全部 11 项独立技能分别从空运行时使用公开锁定 CLI 附件安装，随后完成创建、保存重开、领域参数及渲染检查（72.162 秒，零跳过）。[逐技能冷首用证据](docs/evidence/complete-commands-cold-first-use-20261007.json)。本轮覆盖每项技能的完整命令代表样例；全命令／GUI 和实际宿主安装另行验收。

已发布开发快照：skills dev.12 / plugin dev.13；固定宿主首用代表门禁通过。

666 条命令现在均有逐项参数说明、技能归属与同会话调用入口。运行 `commands.py list / describe / check / run`；原生状态按实时 enabled 校验。旧工作流的 17 项交付合同保留。GUI 命令需显式 bridge，命令目录覆盖不代表全量验收。

[架构与操作指南](docs/FilmCraft-Complete-Commands-Architecture.zh_CN.md) · [逐项参考](skills/filmcraft-use/references/command-reference.md) · [可运行示例](skills/filmcraft-use/examples/commands-advanced.json)

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
| Metadata version | 0.1.0-dev.41 |
| Stage | implementation-in-progress |
| Skills source | filmcraft-skills / v0.1.0-dev.38 |
| Execution | 上游 CLI；ArtCraft 使用子适配器 |
| Host compatibility | Codex dev.35 fixed-tag installation/discovery and standalone real ASR pass; Art105 mixed ASR passes; GUI pending |
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

此前版本绑定的领域场景矩阵：FilmCraft dev.10、EffectCraft dev.9、PhotoCraft dev.10、VectorCraft dev.11 共 37 个原生场景及 6 项合同检查通过，零跳过。每个场景仅复制对应安装技能，从空运行时目录使用默认公开附件安装原生 CLI；核验原生工程、实际像素／音频及局部修改保持，全部 58 项安装身份保持一致。[版本绑定证据](docs/evidence/codex-current-domain-task-matrix-20261006.json)。完整首版、通用 Skills CLI 安装、模型派发、GUI 与创作验收仍开放。

候选运动／LUT 工作流已通过公开运行时首次使用测试：明确关键帧、登记 LUT、原生重开及移动返工；当前不可变插件 dev.10 与 Art 联调尚未包含此映射。 See [architecture](docs/FilmCraft-Motion-LUT-Workflow-Architecture.md) and [evidence](docs/evidence/motion-lut-workflow-candidate-20261006.json).

开发快照 dev.11 固定引用技能源 dev.10，包含声明式运动和 LUT 工作流。公开原生 CLI 保持 0.2.0-craft.2；安装快照与 Art 混合验收分别记录。

固定 Film dev.11／技能源 dev.10 安装后验收通过：隔离 Codex 发现 58 项技能零错误，Film 十一项分别空运行时冷启动通过；安装后的运动／LUT、音轨增益和序列场景三项通过、零跳过。全部 58 安装摘要保全。新 Art LUT 运行时发行与完整首版仍开放。 [Evidence](docs/evidence/codex-filmcraft11-motion-lut-first-use-20261006.json).

工作区分段素材消费候选可校验 Effect 检查点、收集连续帧并保留来源摘要。固定发布、完整 1080p 长片头和 Art 集成仍待完成。[架构](docs/FilmCraft-Segmented-Assets-Architecture.zh_CN.md)。

当前源码 HD 分段候选通过 1080p／24 fps／五秒及动态标题核验；固定安装版与 Art HD 仍待完成。[架构与证据](docs/FilmCraft-HD-Sequence-Architecture.zh_CN.md)。

固定插件发行候选 0.1.0-dev.12 锁定技能源 0.1.0-dev.11，包含 HD 分段工作流与像素校验优化。实际安装版首次使用验收待完成。

公开工作流回复检查已同步领域技能源候选，并通过有界原生／Art 协议验证。新的固定领域和 Art 分发包仍待发行与实际安装验收。[候选架构](docs/FilmCraft-Complete-Commands-Architecture.zh_CN.md) · [证据](docs/evidence/public-workflow-session-candidate-20261007.json)。

失败暂存候选：公开工作流保留原生暂存原路径、依赖摘要、最后提交请求与已完成回执，禁止重放；固定发行与安装副本验收仍开放。[架构](docs/FilmCraft-Failed-Stage-Architecture.zh_CN.md)。

固定领域失败暂存首用门禁已通过：Film插件18／源16，其他领域插件17／源15；五插件58技能发现零错误，全部58项独立空运行时CLI冷启动通过（417.646秒），实际安装副本24个真实保存后故障直接重开产品保留的原工程及依赖，四个健康创作／返工通过。全部安装摘要和16项固定插件CI保持通过；源仓未提供CI运行，仅有本地回归。只关闭领域OpenSpec3.12；Art77内置旧领域源，4.9升级和完整V1仍开放。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

固定安装场景矩阵通过37个原生场景及6个合同检查，零跳过。Photo测试已从安装后的技能锁读取维护版原生版本，CLI与安装技能未修改。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


完整命令内层JSON修复候选：非有限值、溢出和重复键在绑定返回值前记录unknown，真实保存后九类故障与原工程重开通过。这是候选技能源证据，固定发布与实际安装复验尚未完成；逐命令／GUI门禁仍开放。

## 桌面安装组件（候选源码）

每个领域技能自带固定桌面安装、自动启动与完整命令工作流入口。使用当前技能实际目录运行 desktop.py run PLAN --output NEW_DIRECTORY；保留原生工程、命令与生命周期回执。源码48项冷启动已有证据，本次固定版本的实际安装复验仍待完成。见 [桌面使用架构](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

命令计划 JSON 源候选：重复键在安装和创建输出前被拒绝，全部 13 个领域技能的独立副本拒绝测试与有效计划校验通过，3 项专项测试通过。固定插件发布和安装后复验仍为 NOT_RUN。[证据](docs/evidence/command-plan-json-candidate-20261007.json)。

严格计划解析的固定安装复验通过：64 个 CLI 探测、54 个独立安装领域技能的 324 次重复键拒绝、54 次有效计划结构检查，以及四领域空缓存原生保存／重开／渲染实例通过；执行后全部 64 个安装技能摘要不变。仅关闭本次修复的发布门禁；通用 Skills CLI、Art 领域包升级、全部命令上下文和完整首版仍开放。[证据](docs/evidence/command-plan-json-fixed-first-use-20261007.json)。

原生ASR候选：独立单技能空CLI/模型缓存安装与真实识别通过；公开运行时及固定Film／Art升级仍待验收。[证据](docs/evidence/whisper-candidate-inference-20261008.json)。

已发布插件 dev.35 接入源 dev.34／原生 craft.4。源技能与固定标签 Codex 插件首次模型下载、真实 CLI 与工作流识别均通过；Art 分发的 ASR 尚待验收。

Film35固定标签宿主验收：五插件64技能身份与加载通过，错误0；实际安装的转录技能独立冷装、首次模型下载及真实CLI／工作流识别44.833秒通过，源工程和音画保全、重开与SRT均通过。Art105／源79已通过固定宿主混合ASR；完整V1保持开放。 [Evidence](docs/evidence/workflow-model-directory-20261008.json).

场景安装示例已使用实际加载的技能自身目录。源路径／布局检查通过；固定安装运行时验收另行记录。 [Architecture / 架构](docs/Scenario-Own-Path-Architecture.zh_CN.md).

新场景自身目录已通过固定安装复验；64项宿主身份匹配。完整V1仍开放。 [Evidence / 证据](docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

固定独立安装边界验收：全部 64 个当前技能的自身安装器／CLI 共 128 个不可用归档失败案例通过；错误保留本技能 setup 路径，无重试／原生启动，源副本摘要不变。四领域 SK-002 按当前精确锁验收；Art SK-002 和通用 Skills CLI 实际安装仍开放。历史 CLI 红灯为本轮重建，不冒充旧运行。[证据](docs/evidence/craft-fixed-setup-boundary-20261008.json)。

公共协议来源已固定到 ArtCraft v0.1.0-dev.109：[引用与校验说明](docs/Craft-Protocol-Authority.zh_CN.md)。这项检查核对协议来源，完整运行时协议验收仍未完成。

此前已验证的固定协议引用发行矩阵（Film／Effect dev.37、Photo dev.36、Vector dev.34、Art dev.107）已通过隔离 Codex 安装／发现 64 项技能、16 项实际安装所有者文件摘要核对，以及五个全新领域缓存下的 64 项独立公开 CLI 探测。原生场景证据仅对字节一致的技能复用，完整首版仍开放。[固定发行证据](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json)。

本次插件固定协议引用升级至 ArtCraft dev.109；技能快照保持原固定来源，新的实际宿主安装矩阵正在验证。完整首版与运行时协议验收仍开放。

固定发行 Film38／Effect38／Photo37／Vector35／Art109 已通过实际隔离 Codex 安装和发现 64 项技能、16 项安装副本协议文件摘要核对、五个全新领域缓存下的 64 项 CLI 探测。十项 ArtCraft 技能分别从空缓存完成原生 Photo 蒙版调整、源工程返工与迁移打包；另外 54 项技能仅复用整个技能摘要一致的历史原生证据。默认维护验收矩阵已更新；通用 Skills CLI 安装、模型调度、GUI 和完整 V1／协议验收仍开放。[本次固定证据](docs/evidence/craft-archive-prefix-fixed-first-use-20261008.json)。

dev.39 内置不可变独立技能源dev.36，修正小尺寸字幕模板并自含字号换算。源码原生首用通过；新固定插件安装另验。[证据](docs/Caption-Size-First-Use.zh_CN.md)。

固定 Film41/source38 与 Art118/source90 首用通过：64项安装身份一致；Film13和Art10分别独立冷安装，41项未变技能仅复用摘要匹配的历史冷安装证据。新Art安装副本通过1080p／24fps／120帧混合创建、Logo依赖返工、坏帧恢复及五子工程迁移；Film通过移动工程文字返工与关键帧保全。完整V1仍开放。 [Evidence](docs/evidence/craft-art118-segment-guide-fixed-first-use-20261008.json).
