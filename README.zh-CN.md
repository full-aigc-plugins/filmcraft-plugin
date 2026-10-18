# FilmCraft Use

## 插件市场导航

本插件所属分类：**AIGC 内容创作**。

| 分类 | 插件市场入口 | 用途 |
| --- | --- | --- |
| 全栈开发 | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | 架构与 UI 设计、代码理解、质量检查、代码审查、流程治理与服务器运维 |
| AIGC 内容创作 | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | 图像、视频、音频、音乐、3D 与多模态内容创作 |

![FilmCraft Use——可编辑的视频剪辑](assets/official-logo.png)

> 用已有素材剪出可重新打开的 `.fcproj` 影片：素材、轨道、音频、字幕、调色与多机位，并交付预览帧与已解码核验的成片。

[![版本](https://img.shields.io/badge/release-0.1.0--dev.20261018.4-1A73E8)](.codex-plugin/plugin.json)
[![技能数](https://img.shields.io/badge/skills-24-00A67E)](#技能)
[![MCP server](https://img.shields.io/badge/MCP%20server-1-00A67E)](#mcp-工具)
[![许可证](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[English](README.md) | [简体中文](README.zh-CN.md) · [安装](#安装) · [快速开始](#快速开始) · [可完成的工作](#可完成的工作) · [技能](#技能) · [故障排查](#故障排查)

## 项目定位

FilmCraft Use 把视频当作可重新打开的原生工程来剪，而不是一个渲染结果。它探测素材、在精确的整数 tick 时间基上组织轨道、让配音、音乐与原声各自保持独立身份、把字幕当作带时间与样式的可编辑文本，并且只有在导出文件被解码并核对时长、尺寸与音轨之后才算完成。

插件负责规划与核验，原生剪辑由固定的 FilmCraft CLI 完成。长片命令覆盖、物理 GUI 输入与其他平台都尚未取得资格，所有写入必须落在你显式授权的读根与写根之内。

## 状态与版本

`0.1.0-dev.20261018.4` · 开发预览 · `docs/verification/release-candidate.json` → `releaseStatus: BLOCKED`、`installableDevelopmentCandidate: true`。

## 安装

### 前置条件

- macOS arm64。其他平台返回 `unsupported_platform`，不要安装其他平台制品。
- 公开脚本需要 `PATH` 上有 Python 3.11 或更新版本；启动器会在用户数据目录准备固定运行时。
- 内嵌编辑器 MCP 服务需要 Node.js 24 或更新版本。Git 检出没有 `ui/dist/`，需先按 `ui/README.md` 构建，或安装发布包。
- 必须显式授权读写根。`workflow.py` 与 `commands.py run` 要求 `--read-root` 与 `--write-root`（可重复），且必须是你指定的已存在规范目录，不能从计划或素材元数据推导。

### 安装插件

```bash
codex plugin marketplace add full-aigc-plugins/filmcraft-plugin
codex plugin add filmcraft@full-aigc-plugins-filmcraft
```

`docs/verification/release-candidate.json` 记录 `installableDevelopmentCandidate: true` 与 `releaseStatus: BLOCKED`；`project-status.json` 保持 `marketplaceEligible: false`。

仓库带有 Codex（`.codex-plugin/`）、Claude Code（`.claude-plugin/`）、ZCode（`.zcode-plugin/`）与 Kimi（`kimi.plugin.json`）清单；在宿主验收出现之前，`supportedPluginHosts` 保持为空。

## 快速开始

```bash
: "${HARNESS_DIR:?请设为已加载 filmcraft-harness 的 SKILL.md 所在目录}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" PLAN.json \
  --output /absolute/new-result \
  --read-root /absolute/authorized-media --write-root /absolute/authorized-output
```

```mermaid
flowchart LR
    A[素材、配音、音乐] --> B[filmcraft-use 规划剪辑]
    B --> C[固定运行时与授权根]
    C --> D[原生 .fcproj 时间线]
    D --> E[预览帧与已解码导出]
    E --> F[重开、检查、交付]
```

本工具使用 `help`，不是 `--help`。用 `commands <关键词> --json` 与 `describe <命令ID>` 查询当前命令面，并以返回的参数为准。

## 可完成的工作

| 工作流 | 内置路径 | 可验证输出 |
|:---|:---|:---|
| 用已有素材剪带字幕短片 | `filmcraft-use` → harness workflow | 重开的 `.fcproj`，以及已核对时长、尺寸与音轨的导出 |
| 换一个镜头、其余不动 | `filmcraft-cli-timeline` 配合 `--source` | 未受影响镜头参数保持不变的修订工程 |
| 访谈或多机位剪辑 | `filmcraft-cli-multicam` | 保留主录音的机位切换点 |
| 配音、音乐与音画同步 | `filmcraft-cli-audio` | 独立身份轨道与已核对的混音 |
| 字幕与 SRT 交付 | `filmcraft-cli-subtitles` | 可编辑字幕图层与导出的 SRT |
| 按文字剪辑 | `filmcraft-cli-transcript` | 逐词转录驱动的切点与字幕 |
| LUT 调色与镜头匹配 | `filmcraft-cli-color`、`filmcraft-color-match` | 使用许可明确 LUT 的一致镜头观感 |
| 在内嵌编辑器中修改 | `filmcraft-editor` MCP 工具 | 保存后重开并检查的工程 |

## 技能

| 技能 | 作用 |
|:---|:---|
| `filmcraft-use` | 默认入口：可编辑 `.fcproj` 影片、素材、音频、字幕；安装固定 CLI |
| `filmcraft-cli` | 明确指定原生命令 ID 与参数、CLI/MCP 调用、高级操作 |
| `filmcraft-cli-setup` | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| `filmcraft-cli-project` | 创建、打开与保存 `.fcproj`；序列与素材箱 |
| `filmcraft-cli-media` | 检查、导入、收集与重关联视频、图片与音频 |
| `filmcraft-cli-timeline` | 排序、裁切、移动镜头；轨道与单镜头修改 |
| `filmcraft-cli-audio` | 配音与音乐、增益、混音与音画同步 |
| `filmcraft-cli-subtitles` | 导入、创建与修改字幕文本、时间与样式；交付 SRT |
| `filmcraft-cli-color` | 镜头色彩、许可明确的 LUT 与预设 |
| `filmcraft-cli-motion` | 文字图形、效果参数与镜头关键帧 |
| `filmcraft-cli-export` | 预览帧、成片、交换文件与输出校验 |
| `filmcraft-cli-multicam` | 已同步的多机位访谈与演出、机位切换、主录音 |
| `filmcraft-cli-transcript` | 逐词转录、口播搜索、说话人、按文字剪辑 |
| `filmcraft-harness` | 唯一执行通道：bootstrap、commands、workflow、任务会话 |
| `filmcraft-editor` | 打开真实编辑界面，一次会话内完成全部编辑 |
| `filmcraft-color-match` | 匹配不同镜头的曝光、白平衡与风格 |
| `filmcraft-interview-edit` | 把多段访谈整理成一条序列 |
| `filmcraft-product-video` | 产品展示：卖点、细节镜头与行动入口 |
| `filmcraft-short-video` | 短视频粗剪：素材筛选、结构与节奏 |
| `filmcraft-subtitle-delivery` | 字幕校对、断句与阅读舒适度 |
| `filmcraft-video-export` | 分辨率、帧率、编码与音频的交付检查 |
| `filmcraft-freeze-explainer` | 用定格帧讲解教学关键步骤 |
| `filmcraft-presenter-inset` | 讲解视频的讲解者画中画 |
| `filmcraft-jcut-dialogue` | 采访声音先入的 J-cut 对白 |

## MCP 工具

`mcp.json` 只声明一个 stdio server：`filmcraft-editor`，从插件根目录以 `node ui/bootstrap.mjs` 启动。

| 工具 | 用途 |
|:---|:---|
| `open_editor` | 为绝对路径 `workspace` 打开编辑器 |
| `open_browser_editor` | 返回可交给宿主内置浏览器的 `editorUrl` |
| `editor_status` | 报告页面是否已连接到当前 MCP 会话 |
| `command_list` | 读取当前 Web 引擎暴露的命令 |
| `command_run` | 在可见页面执行一条命令 |
| `inspect` | 检查当前画面 |
| `open_file` | 把素材导入当前会话 |
| `list_files` | 列出已导出文件 |
| `save_project` | 把工程保存到工作区新路径 |
| `save_file` | 把生成文件写入工作区 |

工具名遵循 `filmcraft-editor` 技能合同。`_panel_poll`、`_panel_download`、`screenshot` 等页面内部桥接调用属于面板，Agent 不应直接调用。

## 配置

| 变量 / 参数 | 用途 |
|:---|:---|
| `HARNESS_DIR` | 已加载 `filmcraft-harness` 技能的绝对目录 |
| `SKILL_DIR` | 已加载领域 `SKILL.md` 所在目录；仅用于其 `examples/` 与 `references/` |
| `--read-root` / `--write-root` | 独立授权的规范目录，用于计划、素材与输出 |
| `CRAFT_RUNTIME_HOME` / `--runtime-home` | 运行时安装根目录；编辑进程永远不得修改它 |
| `CRAFT_EDITOR_CACHE_DIR` | 已核验编辑器下载缓存（默认 `~/.cache/full-aigc/editors`） |
| `CRAFT_EDITOR_UPDATE=off` | 固定使用内置编辑器，跳过更新检查 |

时间线以每秒 `254016000000` tick 为基准。workflow 模板以十进制字符串承载大整数；原生命令的 tick 保持精确 JSON 整数，不经过会丢精度的 JavaScript Number。

## 架构与安全

- 根隔离在 macOS headless 执行下强制执行。桌面入口还必须隔离它拥有的签名应用，且只开放分配的 loopback 控制端口；无法证明隔离的外部 bridge 会被拒绝。
- 素材、音乐与配音是相互独立的身份，各自保留增益。未经授权不合成、不上传任何声音。
- 写入必须配合 `--save` 或 `--save-as`，或在同一个 `run`／MCP 会话内完成。超时不能证明没有副作用：先核对工程、导出文件或原任务。
- 参见[执行权限](skills/filmcraft-use/references/execution-permissions.md)、[运行时架构](docs/FilmCraft-Runtime-Architecture.md)与[领域设计](docs/FilmCraft-Domain-Design.md)。

## 故障排查

| 现象 | 处理方式 |
|:---|:---|
| 返回 `unsupported_platform` | 仅支持锁定的 macOS arm64 制品 |
| 读写根被拒绝 | `--read-root` / `--write-root` 必须是你指定的已存在规范目录，不能来自计划 |
| 返回 `runtime_install_busy` | 另一个安装持有锁；等其结束再重试 |
| `--help` 输出没有可用信息 | 本 CLI 使用 `help` |
| 命令丢失对象 ID | 读取真实结果，或保持在同一个 MCP／`run` 会话；不要猜 ID |
| 导出看似完成但未核验 | 解码文件并核对时长、尺寸与音轨 |
| 保存后结果未知 | 检查原工程与回执；不要盲目重新提交 |

## 升级

```bash
codex plugin marketplace upgrade full-aigc-plugins-filmcraft
codex plugin add filmcraft@full-aigc-plugins-filmcraft
```

运行时选择与回滚按任务记录；旧工程保持其绑定的运行时，不会被静默迁移。

## 贡献与支持

行为变更先在 [OpenSpec](openspec/changes/establish-v1-plugin/proposal.md) 中说明，再实现，再验证。文档校验：

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_protocol_mapping.py
```

问题反馈：<https://github.com/full-aigc-plugins/filmcraft-plugin/issues>。

## 许可证

本仓库原创内容采用 [Apache-2.0](LICENSE)。FilmCraft CLI 与内置 Web 编辑器各自保留其上游许可证与 NOTICE；上游图标来源记录在 `assets/official-icon-source.json`。本项目是集成适配，不代表上游背书。
