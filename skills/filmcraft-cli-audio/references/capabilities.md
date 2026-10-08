# 计划能力与失败证据 / Plan capabilities and failure evidence

本文件描述源码候选入口的能力合同；固定发行、宿主与完整命令验收仍须另行记录。命令目录是原生参数原文，不是推导出的 JSON Schema。

## 计划声明 / Plan declarations

`commands.py` 命令计划和 `workflow.py` 领域计划可添加顶层 `requires`。旧计划可省略此字段，仍接受实时命令契约及必要资源检查。声明结构错误在安装与输出写入前拒绝。

```json
{
  "mode": "headless",
  "platform": "darwin-arm64",
  "resources": [
    {"kind": "codec", "name": "h264"},
    {"kind": "font", "name": "Arial"}
  ]
}
```

其余可选字段为 `runtimeVersion`、`runtimeSha256`、`desktopSha256`、`parametersSha256`。摘要须为 64 位小写十六进制，来自实际受验身份与快照；不要猜测或复制其他组合的值。资源仅接受 `{kind, name}`，kind 为 codec、font 或 model，不接受调用者自报 `status`。领域工作流固定 headless；命令入口支持 headless/bridge。

Optional `requires` fields bind mode, platform, runtime version/digest, desktop digest, parameter-documentation digest, and named resources. Existing plans remain valid without declarations but still undergo prerequisite checks. Declarations cannot assert availability. A declaration is not execution acceptance.

## 原生探测 / Native probes

资源在同一执行上下文通过只读 `export.formats`、`fonts.list`、`transcript.models` 探测。目录中的模型只有 installed 为 true 才算已安装。缺失报 capability_missing；无法确认报 capability_unknown；契约变化报 capability_contract_drift；声明身份冲突报 capability_identity_mismatch。依赖编辑停止，既有成功步骤保留，不自动重放或安装资源。

执行器在每次依赖调用前核对当前参数原文。转录模型、字幕 font 和显式导出 format 在引用解析后探测；显式下载模型后的生成请求重新探测，不复用旧缺失状态。领域导出还预先检查 h264。资源发现不证明字形正确、推理成功、输出解码或音画同步。

Read-only native probes run in the editing context and check their current contracts. Missing or uncertain prerequisites block dependent operations. Explicit model installation does not reuse a cached missing result. Font discovery, model listing, and codec listing are separate from rendering, inference, and export qualification.

## Bridge 与记录 / Bridge and records

优先使用本技能 `desktop.py run`，由它核验固定桌面签名与二进制、启动拥有的进程并检查监听者身份。手工连接已运行桌面时，命令入口同时要求 `--mode bridge --connect 127.0.0.1:PORT --desktop-app /absolute/FilmCraft.app`；校验固定应用后记录身份。此手工路径不声称证明监听进程属于该磁盘应用；需要该保证时使用拥有进程的入口，不将手工连接证据升级为 owned-session 验收。

命令 `journal.json`、`success.json` 或 `failure.json` 记录 capabilitySnapshot、逐步 capabilityCheck 和资源阻断。领域成功交付包含由 manifest 绑定的 `capabilities.json`；失败暂存的同名文件由 failure.json 的摘要清单绑定，包含运行快照及后续检查。探测回复仅留摘要和必要状态，不复制模型目录等无关私有路径。

Use the owned `desktop.py run` entry for verified process/listener ownership. Manual bridge connections additionally supply the pinned signed app with `--desktop-app`; the disk app check alone does not prove listener ownership. Receipts retain snapshots and blocked attempts; delivery or failure manifests bind capability files by digest. Execution, negative execution, reopen, and preservation remain separate evidence dimensions.
