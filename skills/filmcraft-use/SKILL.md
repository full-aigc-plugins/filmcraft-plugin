---
name: filmcraft-use
description: 使用 FilmCraft 编辑可重新打开的 fcproj 视频工程，编排素材、音频与字幕并导出预览或成片；首次使用时安装并检查锁定 CLI。
license: Apache-2.0
---

# FilmCraft

以原生 `.fcproj` 为编辑事实源，交付工程、依赖素材清单、预览与约定成片。此技能可单独复制安装；所有安装资源位于本技能目录，不读取兄弟技能或插件私有文件。

## 首次使用

1. 定位本 `SKILL.md` 的实际目录。需要 Python 3.11+；使用该目录下的 `scripts/bootstrap.py`，不要假设当前工作目录就是技能目录。
2. 用户已要求安装或完成创作且现有授权涵盖必要依赖时，直接运行安装入口；安装范围是用户数据目录，不需要 sudo。下载固定发布制品并校验摘要，失败即停止，不删除隔离属性、不改 shell 配置。

将 `SKILL_DIR` 设置为宿主实际加载的本 `SKILL.md` 所在目录（绝对路径）。用户级安装可能位于 `~/.agents/skills/filmcraft-use`，项目级可能位于 `.agents/skills/filmcraft-use`，插件可能位于其 `skills/filmcraft-use` 或宿主缓存目录；以实际加载路径为准，不按当前工作目录猜测，也不搜索后随意选择重复版本。技能目录与 CLI 的用户数据安装目录是两个独立位置。

```bash
: "${SKILL_DIR:?请先设置为本 SKILL.md 的实际所在目录}"
python3 -I -B "$SKILL_DIR/scripts/bootstrap.py"
```

安装器返回 JSON `executable`，后续将其作为 argv 的第一个元素。当前锁定平台为 macOS arm64；未支持的平台返回 `unsupported_platform`，不要安装别的平台制品。

安装位置默认 `~/.local/share/craft-runtimes`，可用 `--runtime-home` 或 `CRAFT_RUNTIME_HOME` 指定。重复调用校验并复用同版运行时，不联网升级。`--archive` 接受已下载的锁定 ZIP，但不跳过摘要检查。

3. 执行返回路径的 `--version` 和 `help`。本工具用 `help`，不是 `--help`。根据请求执行 `commands <关键词> --json` 与 `describe <命令ID>`，以当前版本返回的参数为准。

## 可执行剪辑入口

使用 [原生剪辑计划](references/workflow.md) 中的 `scripts/workflow.py`，从已存在的视频和配音制作带字幕短片。入口自动安装 CLI、收集素材、保存并重开工程、导出与解码检查；通过 `--source` 和原工程摘要支持单镜头修订及素材移动后的重关联。

## 编辑流程

- 先核对素材路径、流信息、画幅、帧率、成片时长、配音来源和原生交付要求。`probe <media>` 返回素材信息。
- 修改已有工程前保存独立检查点，使用 `--project <绝对路径.fcproj>` 打开。普通 CLI 调用之间不共享内存，写入命令必须配合 `--save` 或 `--save-as`，或者同一 `run` / MCP 会话完成。
- `run <文件.jsonl>` 接收逐行 `{"id":"命令ID","params":{...}}`。默认遇错停止，不使用 `--keep-going` 掩盖失败。需要上一步创建对象的 ID 时，读取实际结果或保持 MCP 会话；不猜 ID。
- 时间基准为每秒 `254016000000` ticks。计划中的大整数保留十进制字符串；映射到命令时按实测 schema 使用 ticks 或 seconds，不经过 JavaScript Number 丢精度。
- 素材、音乐、配音和字幕分别组织；只在用户授权范围内使用声音。字幕的字体、时间和内容必须可独立修改。
- 使用 `render --seconds <时间> --out <图片>` 检查关键帧。`export <输出> --format <格式>` 等待导出，具体格式和参数以当前 `help`、`describe file.exportMedia` 为准。
- 保存后重新打开工程并 `inspect`，核对轨道、素材引用、字幕和局部修改未影响的内容。检查真实导出文件的解码、时长、尺寸和音轨后才能声明成片完成。

## 修订与失败

仅修改用户指定镜头或参数。记录编辑前后的工程摘要与对象 ID；若用户同时修改工程，重新检查而非覆盖。超时不能证明副作用未发生，先检查原工程、导出文件或原任务，不盲目重新提交。保留原生工程和失败证据，明确未完成项。

本版本正在验证独立技能首次安装后的短片、音画、字幕、素材移动及单镜头修订；完整 Harness 和插件宿主验收仍在开发中。按测试证据陈述通过范围，不能将安装成功当作插件全功能验收。

首次安装或复用遇到其他安装进程时有界等待，超时保持现状并报 runtime_install_busy。参见[安装并发合同](references/installation-concurrency.md)。

开发版本 dev.2 随原生与导出交付[交换损失报告](references/exchange-loss.md)。阅读 lost/observed/unknown 和导出警告；不把扁平导出、SVG 结构或 PSD 图层计数称为无损原生替代。

## 按任务选择独立技能

| 技能 | 触发任务 |
| :--- | :--- |
| **filmcraft-cli** | 查询实际命令参数和能力，调用公开 CLI、MCP 与诊断 |
| **filmcraft-cli-setup** | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| **filmcraft-cli-project** | 创建、打开、保存 fcproj 和组织序列、素材箱 |
| **filmcraft-cli-media** | 检查已有音视频、图片和素材引用，导入并收集或重关联素材 |
| **filmcraft-cli-timeline** | 排序、裁切、移动镜头，组织轨道与单镜头修改 |
| **filmcraft-cli-audio** | 组织已有配音和音乐、增益、混音与音画同步 |
| **filmcraft-cli-subtitles** | 导入、创建、修改字幕文本、时间、样式并交付 SRT |
| **filmcraft-cli-color** | 调整镜头色彩、使用许可明确的 LUT 与颜色预设 |
| **filmcraft-cli-motion** | 创建文字图形、效果参数与镜头关键帧 |
| **filmcraft-cli-export** | 导出预览帧、成片、交换文件与输出验证 |

缺少技能：`npx skills add full-aigc-skills/filmcraft-skills --skill <skill-name>`。每项自带安装与执行资源；直接执行本技能 `scripts/cli.py` 也可查询当前 CLI，不依赖兄弟路径。

工作区分段素材消费候选见 [分段素材](references/segmented-assets.md)。固定发布及 Art 集成仍待验收，不能把候选交接当作完整五插件交付。

## 完整原生命令使用

当前技能自带完整目录的参数说明与同会话入口，不受创作模板白名单限制。读取 [完整使用指南](references/command-usage.md)，按需查询 [命令参考](references/command-reference.md)；每条指令有技能路由、前置观察及验收状态。

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter QUERY
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe COMMAND_ID
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/commands-advanced.json" --output /absolute/new-command-result
```

新入口执行前检查真实注册表与当前可执行状态，保留返回值引用和逐步回执；语义错误或超时不冒充成功。目录覆盖与直接原生使用不等于所有指令、GUI、交付或 Art 编排已验收。

完整工作流命令网关见 [使用说明](references/native-workflow.md)。领域分发固定版本为 0.1.0-dev.21；该版本的独立安装复验与全量逐命令验收分别记录，不以发布替代验收。

GUI任务可先使用本技能自带的 [固定桌面安装](references/desktop-install.md)；安装、启动与实际GUI编辑分别核验。
