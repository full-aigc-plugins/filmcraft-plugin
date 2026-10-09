# 任务级实例复用 / Task-level instance reuse

连续编辑默认使用本技能的 `scripts/task_session.py`。它保持一个前台 Python 进程，在同一所属 FilmCraft MCP 和可选签名桌面内逐步接收计划。不要为每次检查、保存、关闭工程、重开或返工调用单次 `commands.py run`／`desktop.py run`；这些兼容入口仍按单次调用退出。

For continuous editing, keep one foreground task_session.py process and send subsequent plans to that same process. The single-run commands.py and desktop.py interfaces retain their existing lifecycle.

## 启动一次 / Start once

目录必须来自用户或宿主独立授权。`READ_ROOT` 是已有素材／源工程所在根，`WRITE_ROOT` 是新任务输出的父目录，`RUNTIME_HOME` 是已有授权的安装维护根。三者不应因示例而扩大。外部源文件或目录在启动时通过 `--protect-input` 登记为原生进程只读；任务启动后不能追加或扩大保护／授权根。遇到新的外部输入需要新的授权会话时，先保存检查点并正常结束当前会话。

```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
: "${READ_ROOT:?Set to the existing independently authorized source directory}"
: "${WRITE_ROOT:?Set to the existing independently authorized output parent}"
: "${RUNTIME_HOME:?Set to the existing independently authorized runtime directory}"
python3 -I -B -u "$SKILL_DIR/scripts/task_session.py" \
  --output "$WRITE_ROOT/new-task-session" --runtime-home "$RUNTIME_HOME" \
  --read-root "$SKILL_DIR" --read-root "$READ_ROOT" \
  --write-root "$WRITE_ROOT" --write-root "$RUNTIME_HOME" \
  --protect-input "$READ_ROOT" --mode bridge
```

`--output` 必须不存在。bridge 安装校验并拥有一个固定签名桌面；headless 不启动桌面。`READY` 表示任务入口已打开，第一份合法计划才启动原生进程。通过执行工具保持 stdin 打开（终端会话或可继续写入的进程句柄），随后向**同一句柄**写入每行请求，不重新执行启动命令。不要关闭用户已有的 FilmCraft 窗口。

The output must be new. Use bridge for an owned signed desktop or headless without a desktop. READY precedes native startup. Keep stdin open and write to the same terminal/process handle; do not launch the command again for each plan. User-owned applications are untouched.

## 逐步调用 / Send plans incrementally

每行一个严格 JSON 对象，字段为 `name`、`plan` 和可选 `inputs`。`name` 是本任务内新的阶段目录名（字母开头，字母／数字／下划线／短横线，最多64字符）。plan 仍是原 `craft-command-plan/v1` 合同，每阶段实时检查目录、参数、enabled 和权限，保存独立 journal／success／failure 回执。

```json
{"name":"inspect","plan":{"schema":"craft-command-plan/v1","operations":[{"command":"state.inspect","params":{}}]}}
```

收到一行完整回执后再构造下一份计划。返回的原生对象ID直接用于后续参数；`as`／`$ref` 仅在同一计划内有效，禁止猜ID或将先前计划别名作为当前引用。inputs 是 `{"source":"/absolute/source.fcproj"}` 一类名称到文件路径的映射，文件仍逐阶段复制并校验摘要；外部原文件必须位于启动时登记的保护根。任务内生成的工程可作为后续输入，原路径属于本任务写根，不声称它被OS禁止写入。

Each response is one complete JSON receipt. Construct later plans from actual returned IDs; aliases do not silently cross plan boundaries. External inputs must be protected at startup. Files generated within the owned task remain writable task artifacts.

关闭工程使用计划中的 `file.closeAllProjects`，不是结束任务；保存、关闭自有工程再重开可继续共享当前实例。独立进程恢复、启动退出和平台验收另行执行，不能用连续会话代替这些证据。

## 结束与失败 / Finish and failure

```json
{"action":"close"}
```

close、stdin EOF 或中断结束任务，仅清理本次所属进程。保存必须是显式计划步骤；结束任务不自动保存或导出。`task-session.json` 记录实际PID、启动数、各阶段结果和最终清理。正常任务通常为一次MCP启动，bridge另有一次桌面启动。

任何失败、unknown、原生退出、身份／授权／模型目录变化都会停止任务，后续请求不执行；不自动重启、不重放。先读取失败回执和已有原生工程，再决定新的恢复会话。任务会话不是后台常驻服务，不提供跨进程令牌或任意外部应用附着。

Close, EOF and interruption clean only owned processes. Saving is explicit. A failure, unknown outcome, dead process or changed installation/permissions/model identity stops further plans without restart or replay. Inspect receipts and native files before recovery.

Python调用方可从本技能脚本加载 `task_session.py`，以 `with TaskSession(work, runtime_home, permissions, mode, protected_paths) as session` 管理同一任务，调用 `session.execute(plan, stage_name, inputs)`；权限必须是独立提供的可信策略，不能从计划推导。该入口与JSONL入口使用相同的执行和停止逻辑。
