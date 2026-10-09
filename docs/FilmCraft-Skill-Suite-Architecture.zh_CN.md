# FilmCraft CLI 场景技能架构

> 更新：2026-10-09。当前发行dev.76沿用源dev.57／原生CLI0.2.0-craft.5，共13技能。路由证据保留固定75身份；固定76维护根验收采用所述独立临时目录环境。旧dev.6检查点保留原身份，不替代完整权限、全部命令上下文或宿主发行资格。

## 1. 为什么拆分

原有单个 use 技能提供安装和原生代表流程，但触发范围过宽、场景路由不足。本次借鉴 Dreamina 的 use / CLI / setup / 任务分层，通过源码和实际运行时命令目录决定划分，不制造虚构 auth 或生成接口。本包包含13项技能。

## 2. 职责与路由

| 技能 | 任务边界 |
| :--- | :--- |
| `filmcraft-use` | 组合多个本工具能力并保留可编辑原生交付 |
| `filmcraft-cli` | 查询实际命令参数和能力，调用公开 CLI、MCP 与诊断 |
| `filmcraft-cli-setup` | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| `filmcraft-cli-project` | 创建、打开、保存 fcproj 和组织序列、素材箱 |
| `filmcraft-cli-media` | 检查已有音视频、图片和素材引用，导入并收集或重关联素材 |
| `filmcraft-cli-timeline` | 排序、裁切、移动镜头，组织轨道与单镜头修改 |
| `filmcraft-cli-audio` | 组织已有配音和音乐、增益、混音与音画同步 |
| `filmcraft-cli-subtitles` | 导入、创建、修改字幕文本、时间、样式并交付 SRT |
| `filmcraft-cli-color` | 调整镜头色彩、使用许可明确的 LUT 与颜色预设 |
| `filmcraft-cli-motion` | 创建文字图形、效果参数与镜头关键帧 |
| `filmcraft-cli-export` | 导出预览帧、成片、交换文件与输出验证 |
| `filmcraft-cli-multicam` | 已同步多机位切换与主录音保全 |
| `filmcraft-cli-transcript` | 真实语音识别或逐词文本导入与可编辑字幕 |

```mermaid
flowchart TD
 U[用户任务] --> R[use 路由]
 R --> C[cli 公共操作]
 R --> S[cli-setup 安装诊断]
 R --> T[场景技能]
 T --> B[该技能自己的锁定安装器与 argv 启动器]
 C --> B
 S --> B
 B --> N[原生或编排 CLI]
 N --> D[可编辑工程 / 派生输出 / 证据]
```

## 3. 单技能安装与 CLI 生命周期

每项技能自带必要脚本、运行时锁、工作流参考和实例；不存在兄弟目录读取或符号链接。仓库维护时通过 `scripts/sync_skill_suite.py` 从 use 技能同步共享执行资源，`--check` 拒绝漂移。场景描述与命令证据分别维护。发布资源适度重复以支持按粒度安装，共享代码不手工维护多套实现。

启动器接收 `--` 后的原生 argv，在安装前检查首个子命令，通过固定摘要的可执行文件调用且不使用 shell，保留退出码并有界等待。非法操作、不支持平台与损坏安装明确失败；命令 ID、参数和 enabled 状态运行时重查。超时是结果未知，不能证明写入未发生；先保留检查点、核对工程再决定后续操作。

## 4. 源码证据与工具差异

研究提交：`storytold/filmcraft` 的 `adfd9a66de2bebc764c7f57435ccdf0f1d2e1df6`。CodeGraph 索引 689 文件、20278 节点、97560 边；分别检查 CLI 解析与引擎派发，并读取已安装运行时目录。当前源码与发布二进制可能不同，参见[研究证据](evidence/upstream-codegraph.json)。

FilmCraft 用 ticks 与 save/save-as；EffectCraft 使用 comp/layer 属性路径和渲染通道；PhotoCraft 的 run 参数按顺序绑定并可用 serve 保持会话；VectorCraft 按顺序执行 run/export 且画板/范围索引不同。上游 ArtCraft 是 Tauri 场景与生成应用，含素材保存和异步供应商任务通知。本项目 ArtCraft CLI 为独立实现的本地 DAG/账本运行时，不复制上游 ArtCraft 代码或品牌资源。

## 5. 验证与发布

`tests/test_skill_suite.py` 逐个隔离技能，核对固定 CLI 版本、命令目录子集和非法子命令在安装前被拒绝。既有原生工作流回归验证可编辑交付及修订。单项技能发现成功不代表每条场景命令、创作质量、GUI 或跨编辑器保真均通过。共享资源检查与每项 SKILL.md 校验分别执行；原生/平台和宿主证据分别记录。

在独立技能仓库运行：

```bash
python3 -B scripts/sync_skill_suite.py --check
python3 -B -m unittest discover -s tests -p test_skill_suite.py -v
CRAFT_LIVE_SUITE=1 python3 -B -m unittest discover -s tests -p test_skill_suite.py -v
```

单项安装：`npx skills add full-aigc-skills/filmcraft-skills --skill <skill-name>`，使用其实际绝对路径执行，不读取兄弟技能。插件固定完整技能清单的来源标签、提交和逐项摘要；旧发布标签不可变，原 use/workflow payload 保持兼容。

## 历史dev.6维护版运行时安装场景复验

插件 dev.6／技能源 dev.5 对维护版 CLI 0.2.0-craft.1 的八类工程、素材、时间线、音频、字幕、颜色、动画、导出场景全部通过，耗时 43.688 秒。每项来自实际固定安装快照，单独复制，以自己的全新缓存公开下载安装，子进程仅使用系统 PATH。基础工程由安装的 use 技能在另一个全新缓存生成，原工程保持不变。原生断言覆盖重开、轨道保全、实际音频增益、字幕时间、删除 LUT 源后像素、关键帧像素与成片／交换导出。报告绑定安装技能、测试驱动、合成输入／原工程、原生二进制及输出摘要；全部 58 个安装摘要不变。默认回归 44 项中 32 项通过、12 项门禁跳过，不能代替八项原生用例。旧 0.2.0 证据保留原版本范围。[证据](evidence/maintained-runtime-task-first-use.json)。本 QA 未改变技能字节、原生发行版或插件版本；创作、模型及实际通用安装器门禁仍未完成。


## 固定75路由与业务验收

15个独立只读临时宿主会话全部正确选择并实际读取固定技能说明；模型使用现有登录态和默认配置gpt-6-astra，不由驱动提供预期技能。使用现有客户端0.162.0-alpha.2；旧147客户端因模型要求新版本而拒绝，失败保留，不安装升级工具、不复制凭据。额外根仅本次宿主连接指向实际固定安装技能，验证源技能名称的选择；其他宿主及插件命名空间完整资格属于FC-RL-001，未据此关闭。十三独立原生业务102.290秒通过，232 Markdown／337本地链接限定在自身目录，资源与已发布源57摘要一致。只关闭9.9，余7项；详见[验收](evidence/filmcraft75-fixed-skill-routing-20261009/acceptance.json)。

```mermaid
flowchart LR
    C[15 fixed corpus requests] --> H[Authenticated ephemeral read-only host]
    I[13 fixed installed skill descriptions] --> H
    H --> L[Read selected SKILL.md]
    L --> A[Check expected and rejected skill identities]
    B[13 isolated native business tasks] --> Q[Scenario and preservation assertions]
    M[All skill Markdown and shared bytes] --> R[Standalone links and resource hashes]
    A --> E[Task9.9 evidence]
    Q --> E
    R --> E
    H -->|Incompatible client or failed turn| F[Preserve environment refusal; no route result]
```

可复验脚本：`scripts/verify_host_skill_routing.py --codex CLIENT --installed-plugin FIXED_ROOT --source-repository SOURCE_GIT --output NEW_PRIVATE_DIRECTORY`。语料从安装锁定的技能源Git对象读取；结果与原生业务分别记录。
