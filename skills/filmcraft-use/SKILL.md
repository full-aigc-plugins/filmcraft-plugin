---
name: filmcraft-use
description: 使用 FilmCraft 编辑可重新打开的 fcproj 视频工程，编排素材、音频与字幕并导出预览或成片；首次使用时安装并检查官方 CLI。
license: Apache-2.0
---

# FilmCraft

以原生 `.fcproj` 为编辑事实源，交付工程、依赖素材清单、预览与约定成片。此技能可单独复制安装；所有安装资源位于本技能目录，不读取兄弟技能或插件私有文件。

## 首次使用

1. 定位本 `SKILL.md` 的实际目录。需要 Python 3.11+；使用该目录下的 `scripts/bootstrap.py`，不要假设当前工作目录就是技能目录。
2. 用户已要求安装或完成创作且现有授权涵盖必要依赖时，直接运行安装入口；安装范围是用户数据目录，不需要 sudo。下载固定官方制品并校验摘要，失败即停止，不删除隔离属性、不改 shell 配置。

```bash
python3 -I -B /mnt/skills/user/filmcraft-use/scripts/bootstrap.py
```

以上 `/mnt/skills/user/filmcraft-use` 表示宿主挂载的技能根；实际位置不同时，使用已加载技能的真实绝对路径替换。安装器返回 JSON `executable`，后续将其作为 argv 的第一个元素。当前锁定平台为 macOS arm64；未支持的平台返回 `unsupported_platform`，不要安装别的平台制品。

安装位置默认 `~/.local/share/craft-runtimes`，可用 `--runtime-home` 或 `CRAFT_RUNTIME_HOME` 指定。重复调用校验并复用同版运行时，不联网升级。`--archive` 接受已下载的官方 ZIP，但不跳过摘要检查。

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
