---
name: filmcraft-harness
description: FilmCraft 内置执行 harness——所有 filmcraft 领域技能（filmcraft-use、filmcraft-cli 及各场景技能）的统一执行通道。执行首次安装、原生命令调用、剪辑 workflow、桌面会话或任务级会话时，经由本技能的入口脚本执行；领域技能只提供场景知识、计划与示例，不自带脚本。
license: Apache-2.0
---

# FilmCraft Harness（内置执行通道）

本技能是 FilmCraft 技能套件的**唯一执行实现**：首次安装、原生命令会话、原生剪辑工作流、桌面会话与任务级会话都收敛在本目录 `scripts/` 内。`filmcraft-use`、`filmcraft-cli` 及各领域技能是薄文档技能——它们提供场景指引、计划示例与参考契约，实际执行一律经由本技能的入口。**执行任何 FilmCraft 命令前，先把 `HARNESS_DIR` 设为本 `SKILL.md` 所在目录（宿主实际加载的绝对路径），不要假设当前工作目录就是技能目录。** 用户级安装可能位于 `~/.agents/skills/filmcraft-harness`，项目级可能位于 `.agents/skills/filmcraft-harness`，插件可能位于其 `skills/filmcraft-harness` 或宿主缓存目录；以宿主实际加载路径为准。

## 六个入口

| 入口 | 用途 |
|---|---|
| `scripts/bootstrap.py` | 首次使用安装器：下载校验锁定 FilmCraft 制品，返回 JSON `executable`；版本与摘要以 `scripts/runtime.lock.json` 为准。 |
| `scripts/cli.py` | 原生转发 CLI：安装校验后直连锁定可执行文件（`--version`、`commands --json`、`describe` 等）；工程读取与编辑须在 `--` 前提供独立根参数。 |
| `scripts/commands.py` | 原生命令入口：`list` / `describe` / `check` / `run` 执行 `craft-command-plan/v1` 计划，输出恒为 JSON。 |
| `scripts/workflow.py` | 原生剪辑计划执行器：从已有素材制作带字幕短片，自动安装、收集、保存重开、导出与解码检查。 |
| `scripts/desktop.py` | 固定桌面安装入口：校验签名应用身份并登记本地 bridge；启动与 GUI 编辑验收单独记录。 |
| `scripts/task_session.py` | 任务级 JSONL 会话入口：启动一次所属编辑器，逐计划检查、保存和返工；任务结束才退出。 |

## 用法

领域技能（`filmcraft-use` 等）提供场景指引与计划示例；执行路径一律换成本目录 `HARNESS_DIR/scripts/`。公开 `workflow.py` 与 `commands.py run` 必须显式提供 `--read-root READ_DIRECTORY --write-root WRITE_DIRECTORY`（可重复）；根须为已存在的规范真实目录，来自用户／宿主授权。安装范围是用户数据目录，不需要 sudo：

```bash
: "${SKILL_DIR:?请先设置为本 SKILL.md 的实际所在目录}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
```

原生命令直连与命令目录查询（输出恒为 JSON）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- --version
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter <关键词>
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe COMMAND_ID
```

原生剪辑计划（计划与示例文件取自对应领域技能目录）：

```bash
: "${READ_ROOT:?Set READ_ROOT to an existing independently authorized directory}"
: "${RUNTIME_HOME:?Set RUNTIME_HOME to an existing independently authorized directory}"
: "${WRITE_ROOT:?Set WRITE_ROOT to an existing independently authorized directory}"
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" --plan PLAN.json --output /absolute/new-result \
  --read-root "$READ_ROOT" --write-root "$WRITE_ROOT" --runtime-home "$RUNTIME_HOME"
```

任务级会话（连续操作共享同一 FilmCraft 实例）与桌面安装分别见 `task_session.py --help` 与 `desktop.py --help`；权限边界由 `scripts/execution_permissions.py` 强制，原生子进程运行在 macOS 系统沙箱内。具体任务先读取本技能 [任务模板](references/task-scene.md)，按对应输入、首次任务、失败边界、局部修订和核验执行。

## 领域技能与本 harness 的关系

- `filmcraft-use`：完整任务路由与交付合同；执行仍走本 harness。
- `filmcraft-cli` 与各场景技能（setup/project/media/timeline/audio/subtitles/color/motion/export/multicam/transcript）：场景知识与参数契约；执行仍走本 harness。
- 领域技能文档中的 `SKILL_DIR` 指领域技能自身目录（用于读取其 `examples/`、`references/`）；脚本执行路径一律换成本目录 `HARNESS_DIR/scripts/`。
- 执行合同（命令目录、参数契约与技能路由）见各领域技能 `references/command-usage.md` 与 `command-reference.md`；本技能 `references/` 内保存执行契约快照（`command-coverage.json`、`native-command-snapshot.json`）。
