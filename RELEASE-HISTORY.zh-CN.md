# 版本绑定的历史发行记录

## 0.1.0-dev.72

dev.72锁定公开source54：完整命令、所属桌面和MCP保留显式只读模型目录。四项目标回归及CLI真实Whisper识别通过（28词，模型摘要不变）；官方签名桌面发现同一缓存，但报告语音能力不可用并正确拒绝推理。完整FC-RL-002、固定72验收及八项V1任务保持开放。 [Evidence](docs/evidence/source54-readonly-model-20261009/report.json).

## 0.1.0-dev.71

dev.71要求运行时维护探测与选择提供独立读写根，规范根摘要进入探测和选择的精确宿主授权；缺少策略及计划／缓存越界在计划读取和授权查询前拒绝，原生能力探测沿用同一沙箱策略。实际公开CLI探测／激活、根扩张拒绝、撤销授权及输入／技能／二进制保全通过候选验证。完整FC-RL-002与八项V1任务保持开放，固定71宿主安装验收为NOT_RUN。

## 0.1.0-dev.70

dev.70将可信执行根绑定到精确宿主授权与原生预检；公开工作流和恢复继续入口接收独立权限文件，根策略变化后旧授权失效。source53隔离原生及所属桌面执行，包含本地桥端口和临时渲染文件。实际候选原生与签名桌面检查通过；完整FC-RL-002、维护权限分离、秘密引用及八项V1任务仍开放，固定70宿主验收为NOT_RUN。

## 0.1.0-dev.69

开发版69锁定独立发布的source52，过滤全部Harness Python子进程环境（含身份探针），补充OpenSpec可信根及子进程环境场景。候选原生／Harness测试通过；公开根授权接入、固定69宿主资格及八项完整任务仍开放。

固定dev.59／源46／公开craft.5在macOS arm64隔离Codex／headless验收FC-AR-001/002全部8场景：13技能／62执行文件保全，10类血缘＋15类产物用例通过，2公共任务／26产物通过固定ArtCraft schema。135项安装回归全部通过、零跳过；源码83项Python／132项Node通过，3项声明环境检查由安装运行补证。OpenSpec5.1—5.3及5.6完成，完整V1剩35项。创作manual_review，用户／其他平台NOT_RUN。[固定证据](docs/evidence/filmcraft59-fixed-artifact-contract-20261009/acceptance.json)。

dev.59先前候选记录（已由上方固定验收补证）：源码候选10类血缘／15类产物用例覆盖FC-AR-001/002全部8场景，包含工程迁移重关联、缺失依赖、独立原生重开及质量回执身份。逐场景门禁拒绝证据缺失或拼接。源46／craft.5技能快照不变；新固定59安装待验收，5.1—5.3／5.6与39项完整V1任务仍开放。[候选证据](docs/evidence/filmcraft59-artifact-candidate-20261009/acceptance.json)。

固定 dev.58 的预算／取消合同补充验收通过：FC-TX-003四个场景、16类必选边界及额外私有CLI场景通过。复用同一固定版本133项无跳过安装回归，重新核验13技能、执行与测试源码身份；本轮未重复运行原生。已完成OpenSpec3.7—3.9，完整V1余39项。未知原生结果保留占用／预留；预算限制后续调度，不作为OS资源配额或其他平台验收。 [Evidence](docs/evidence/filmcraft58-fixed-resource-contract-20261009/report.json).

固定 dev.58／source46／craft.5 的恢复合同验收通过：133项安装测试无跳过、14类恢复必选矩阵及FC-TX-002十个场景全部PASS，13项技能与执行代码保全。复核既有目标失败与当前实现后，OpenSpec3.4—3.6已完成；完整V1余42项。实际原生丢失交接与继续、SQLite故障、受控进程和合成回执分别标明；限macOS arm64、Codex/headless，其他平台、原生二进制升级、创作与用户验收仍开放。 [Evidence](docs/evidence/filmcraft58-fixed-recovery-20261009/acceptance.json).

dev.58 增加恢复合同逐场景证据门禁。固定dev.57的133项安装测试无跳过、47行综合矩阵（含14类恢复必选）及FC-TX-002十个场景校验通过。缺失／重复证据、原文件变化、重复应用、失效epoch、活子进程占用和备份缺失均拒绝；合成回执、实际SQLite／受控进程及实际原生继续分别标记。新dev.58安装复验待执行，不提前关闭3.4—3.6，完整V1仍45项开放。 [Evidence](docs/evidence/filmcraft58-recovery-candidate-20261009/contract.json).

固定 dev.57／source46／公开 craft.5 的真实隔离安装验收通过：FC-TX-001 全部五个场景与七类身份冲突拒绝 PASS，13 项技能及执行代码摘要保全。OpenSpec 3.3 已完成，完整 V1 余45项开放。范围限 macOS arm64、Codex/headless及所属签名桌面桥接；不宣称人工UI点击或其他平台验收。 [Evidence](docs/evidence/filmcraft57-fixed-writer-20261009/report.json).

dev.57 增加版本绑定与单写逐场景QA：固定dev.56的五个规范场景已通过，包括真实工作流同目标竞争、不同目标并行、用户目录保全、真实保存后强杀所有者／拒绝重放／工程重开，以及签名桌面桥接保存后旧计划冲突。新dev.57安装复验待执行，3.3与完整V1继续开放。

固定dev.56／source46／craft.5的7项原生宿主准入验收通过，13项技能与全部执行文件摘要不变。OpenSpec3.1、3.2的测试和最小实现已完成；3.3的完整版本绑定／单写边界、其他调用路径、平台及完整V1仍开放，余46项。dev.55验证器误比较失败保留，不提升旧证据。 [Evidence](docs/evidence/filmcraft56-fixed-admission-20261009/report.json).

dev.56 分别核验适配器原字节树摘要与 vendor 文件摘要树身份，并显式标注算法。固定dev.55的7项原生场景通过，但最终验证器混淆算法而FAIL，失败证据与旧标签保留；dev.56固定验收待执行，未关闭任务。

dev.55 增加首次工作流可信宿主准入：完整任务与资源预算绑定 execute 主体，预检及原生提交前复核授权；缺失、过期、撤销或不匹配拒绝。7项单元、7个真实原生候选场景通过；固定安装验收待执行，完整V1仍开放。

固定 dev.54／source46／公开 craft.5 在真实隔离 Codex 安装完成七类原生媒体矩阵，13项技能与执行代码摘要保持不变；OpenSpec 9.32、9.33 已完成，完整 V1 仍有48项开放。验证仅覆盖当前 macOS arm64、Codex 和编码范围；创意、用户及其他平台验收仍开放。[固定安装证据](docs/evidence/filmcraft54-fixed-media-20261009/report.json)。

## 0.1.0-dev.54

固定源dev.46与公开craft.5；新增七类原生媒体矩阵及固定宿主验收执行器。候选矩阵／真实Whisper／公开原生首用通过，新固定宿主与媒体验收待发布后执行；完整V1继续开放。

## 0.1.0-dev.53

锁定已发布技能源 dev.45；发布真实媒体 fixtures 与原生 VFR 音频失败证据。PCM 修复仅为源码候选，默认 craft.4 不变；9.32/9.33 及完整 V1 未关闭。

dev.49 开发候选：schema4持久资源域、共享继续预算、显式宿主授权与进程身份绑定的POSIX取消，以及schema1/2/3备份迁移。源码原生／状态81/81、Python47/47通过，固定安装待执行。[证据](docs/evidence/filmcraft49-resources-candidate-20261008.json)。

dev.45发布后验收：隔离Codex实际安装后完成9.13—9.15；13技能／26执行文件身份保全、39原生测试与10类回执用例通过，固定公共schema映射通过，质量状态仍NOT_RUN。[证据](docs/evidence/filmcraft45-fixed-lineage-20261008.json)。原标签／ZIP不改写，完整V1仍开放。

开发快照 `0.1.0-dev.45` 固定技能源 dev.42 / `7adfa763b161bc2ff7ef3efae702e285965bf23a`。受控工作流上下文关联任务／尝试／来源；缺失历史字段保持 unknown。集合须具备清单与同尝试执行记录，重核当前身份和文件，冲突不覆盖原字节；部分交接修复不重放。原生39/39、Python42/42与10类候选用例通过；固定公开标签安装在发布后验证。[映射](docs/FilmCraft-Receipt-Lineage.zh_CN.md) · [证据](docs/evidence/filmcraft45-lineage-candidate-20261008.json)。质量、完整授权预算、恢复与完整V1仍开放。

开发快照 `0.1.0-dev.44` 锁定技能源 dev.41 / `f47a2ff6e47e64767d82fd8d88ffa225b204879e`；整体参数引用解析后必须仍为对象，在提交原生命令前拒绝。新增命令分维证据及固定入口验收生产者；新标签实际验收在发布后记录，9.3 完成前保持开放。


以下记录逐字移自 README 前部，描述各自版本，不作为当前安装合同。

开发快照 `0.1.0-dev.43` 锁定源 dev.40 / `2eb9e0f169b3cfea1bf810aa0293c51bdbed4177`，通过实际原生重采集修复目录身份为 MATCH，参数行和已有子集保持不变。新增隔离固定安装验证，复用 ArtCraft 固定辅助函数，支持附注标签及执行文件身份核验。本地 Python 36 项通过，原生 Harness 33 项无跳过通过。dev.43 固定验收在 [身份报告](docs/evidence/filmcraft43-fixed-identity-20261008.json) 单独记录；发布本身不关闭 9.6 或完整宿主/V1 验收。

开发发行 `0.1.0-dev.42` 锁定技能源 `v0.1.0-dev.39` / `6c29e50b5fe85f98a1c5f77977158bb1b00bde5a`，包含 Dreamina 对照优化规范/任务、Node/SQLite 回执血缘、只读诊断及有界同尝试修复。本地插件 Python 28 项通过；独立源和内置快照原生回归各 33 项通过，零跳过。实际导出后回复丢失修复保全文件、不重放原生工作；2 个任务与 13 个产物通过固定公共 schema。见 [绑定报告](docs/evidence/filmcraft-dev42-release-20261008.json)。宿主安装、完整恢复/备份/回退、授权、预算/取消、质量及完整 V1 仍开放，发布不等于验收。

固定Film插件31／源29首用验收通过：宿主发现64技能，加载错误0；13个Film技能各自独立空运行时安装公开原生CLI并查询666命令；7项安装后执行保护及1项实际原生创建／导出／重开／返工通过。公开源ZIP与Git归档逐字节一致，全部64安装摘要保持。Art接入、其他领域保护及完整任务／首版仍开放。 [Evidence / 证据](docs/evidence/filmcraft31-fixed-output-execution-first-use-20261007.json).

插件dev.31固定已发布Film技能源dev.29，收录原生启动前执行登记及规范路径一致性修复，运行时保留0.2.0-craft.2。源原生验收通过，固定安装首用与中断所有者阻断待版本绑定报告通过；完整任务合同仍开放。

Film独立工作流的同目标执行保护源码候选：原生启动前认领规范化目标，中断后保留running／reconciling身份。7项目标回归和1项实际冷原生创建／导出／重开／返工通过；源仓153项中122通过、31条件跳过，候选同步13技能。固定发布／安装、其他领域保护和完整任务合同仍开放。 [Evidence / 证据](docs/evidence/filmcraft-output-execution-candidate-20261007.json).

领域场景验收现为 **43项原生测试通过／全部42个不同场景技能**。固定安装跟踪用例使用受支持H.264 High通过；此前无损输入不受原生解码器支持，失败证据保留。Art角色专项、实际Skills CLI及完整V1仍开放。 [Evidence / 证据](docs/evidence/craft-fixed-tracking-supported-input-20261007.json).

追加专项验收：**累计42项原生测试通过，覆盖41／42个领域场景技能**。多机位、带时间文本转录、滤镜及Puppet补验通过；Effect跟踪视频纹理未出现在预期像素，分析实际关键帧为0，尚未验收。64个安装摘要保持。Art角色专项、自动ASR、实际Skills CLI和完整V1继续开放。[证据](docs/evidence/craft-fixed-additional-task-scenes-20261007.json)。

已安装专项技能首用：**38项原生测试／37个不同领域场景技能通过**，各自使用独立空运行时。Film多机位／转录、Photo滤镜、Effect Puppet／跟踪五项尚未纳入本业务门禁；Art角色专项任务与通用Skills CLI另行验收。全部64安装摘要不变。[证据](docs/evidence/craft-fixed-installed-task-scenes-first-use-20261007.json)。

当前固定版本首版代表任务通过：四领域已安装技能各自使用新公开运行时缓存，验证可编辑原生工程、重开、局部返工及导出。覆盖短片字幕／配音同步与素材移动、片头改字保留动画、海报图层／蒙版／PSD／尺寸变体、矢量布尔／多画板／SVG-PDF-PNG／改色。全部64安装摘要不变。本证据仅覆盖四个代表任务，不等于完整首版或所有专项场景。[证据](docs/evidence/craft-fixed-v1-representative-native-baseline-20261007.json)。

逐技能独立冷启动：**64／64通过**（macOS arm64、Python3.13.5，620.155秒）。每个单技能分别使用独立空运行时与默认公开下载；锁定原生版本和命令发现通过，安装技能摘要不变。通用Skills CLI安装及完整首版仍开放。[证据](docs/evidence/craft-fixed64-every-skill-cold-first-use-20261007.json)。

当前插件：`0.1.0-dev.31`；技能源：`0.1.0-dev.29`。已同步严格命令计划 JSON 的固定快照。源回归与独立副本计划测试通过；固定安装计划拒绝及原生保存／重开／渲染代表场景复验通过，逐命令和完整首版验收仍开放。

固定安装复验：五插件共62技能在隔离Codex宿主中加载成功，加载错误0；62技能完整命令查询与场景资源核对通过，248项安装失败诊断检查通过；四个新增专项技能的空运行时安装、版本与查询通过。原生创作、全量命令和完整V1按各自证据验收。[安装证据](docs/evidence/craft-fixed62-installation-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.28`；技能源：`0.1.0-dev.26`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.27`；技能源：`0.1.0-dev.25`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

固定安装诊断检查：58技能发现通过，184项诊断检查通过；四领域固定副本仍缺失安装脚本本身不存在时的补充修复，当前验收为部分完成。Art插件dev.92锁定技能源dev.66。[证据](docs/evidence/craft-first-use-diagnostics-installed-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.26`；技能源：`0.1.0-dev.24`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次新固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

本次固定版本追加原生验收：Art十项冷启动、四领域四项GUI编辑与保存重开，以及品牌色局部返工、依赖更新和交付打包通过；全量命令、全部GUI和创作质量仍待验收。[证据](docs/evidence/craft-fixed-scene-guidance-20261007.json)。

固定安装场景指引验收：五插件58技能发现与内容摘要、示例引用及完整命令查询通过；四领域运行脚本与锁和示例保持原固定版本身份。Art新分发十项实际冷启动复验通过，全量命令和完整V1仍开放。[证据](docs/evidence/craft-fixed-scene-guidance-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.25`；技能源：`0.1.0-dev.23`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。此前固定版本58技能首次使用通过，当前源码四领域进阶桌面通过；本次固定安装发现、场景资料与代表原生任务复验通过，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.24`；技能源：`0.1.0-dev.22`。完整反射命令入口、独立CLI与桌面安装已提供；固定版本58项独立冷启动、四领域进阶GUI保存／重开／渲染及Art混合返工通过。逐条原生命令执行验收与完整V1保持开放。[固定验收记录](docs/evidence/craft-full-command-fixed-first-use-20261007.json)。

历史发行记录：当前插件：`0.1.0-dev.23`；技能源：`0.1.0-dev.21`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。候选源码48项冷启动通过；本次固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.22`；技能源：`0.1.0-dev.20`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。候选源码48项冷启动通过；本次固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史发行记录：当前插件：`0.1.0-dev.22`；技能源：`0.1.0-dev.20`。独立技能现提供固定桌面与 CLI 安装、自动启动、同会话全命令入口及退出回执。候选源码48项冷启动通过；本次固定发布安装复验待完成，全量命令及完整V1仍开放。[使用指南](docs/Craft-Desktop-First-Use-Architecture.zh_CN.md)。

历史 CLI 验收（原固定版本范围）：当前固定版本的 58 个技能全部通过独立冷启动：单技能目录、空运行环境、公开安装、版本查询及完整命令发现。此证据不代表 2639 条命令全部执行通过或完整场景验收。 [Evidence](docs/evidence/codex-current58-cold-cli-first-use-20261007.json).

历史发行记录：当前首次使用入口：插件 `0.1.0-dev.21`，技能源 `0.1.0-dev.19`。中英文安装与命令指南按当前固定发行核验；历史样例证据保留原版本范围。 [Guide](docs/Craft-Native-Gateway-Usage.zh_CN.md).

固定原生命令网关首用通过：48项领域安装技能与十项 Art85／技能源58 的公开入口独立冷安装、创建／重开／导出、返工并保全原交付。公开 Brief、四领域网关、五子工程、Logo选择性更新／无关图标复用、移动包、真实取消和六类未知回复故障通过；58项安装摘要不变。全2639命令／GUI／模型／通用Skills CLI／完整V1门禁保持开放。[使用指南](docs/Craft-Native-Gateway-Usage.zh_CN.md) · [固定证据](docs/evidence/codex-native-gateway-first-use-20261007.json)。


## 0.1.0-dev.35

插件 dev.35 接入已发布 Film 技能源 dev.34／原生 craft.4，包含真实 Whisper 和工作流模型目录。公开技能源13项独立冷安装通过（40.11秒），源技能真实模型首次使用与 CLI／工作流识别通过（52.497秒）。固定插件宿主及 Art 验收仍待完成。 [Evidence](docs/evidence/workflow-model-directory-20261008.json).

dev49发布后完成9.19—9.21：隔离Codex安装13技能／36执行文件保全，81测试无跳过、32类矩阵记录（16类资源专项）、四次发布CI通过。[证据](docs/evidence/filmcraft49-fixed-resources-20261008.json)。原标签／ZIP不改写，完整V1仍有60项开放。
