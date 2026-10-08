# 可信执行权限 / Trusted execution permissions

公开工作流和完整命令run入口从独立命令行参数接受读取／写入根；未提供时在计划读取前返回execution_permissions_required。使用已存在、规范真实的目录；不接受软链接或磁盘级根。路径越界在素材摘要读取和安装前拒绝。输出父目录也必须授权，以容纳同父临时工程和执行锁。

Public workflow and full-command run require independent --read-root / --write-root grants before reading the plan. Existing canonical directories only; symlink and disk-wide grants are rejected. Plan and asset paths cannot grant access themselves.

```bash
: "${PROJECT_ROOT:?Set PROJECT_ROOT to an existing independently authorized directory}"
: "${READ_ROOT:?Set READ_ROOT to an existing independently authorized directory}"
: "${RUNTIME_HOME:?Set RUNTIME_HOME to an existing independently authorized directory}"
: "${SKILL_DIR:?Set SKILL_DIR to an existing independently authorized directory}"
python3 -I -B "$SKILL_DIR/scripts/workflow.py" "$PLAN" --output "$OUTPUT" \
  --runtime-home "$RUNTIME_HOME" --read-root "$READ_ROOT" \
  --write-root "$PROJECT_ROOT" --write-root "$RUNTIME_HOME"
```

RUNTIME_HOME须事先有独立可信的目录授权。安装维护可写该目录；执行命令的原生进程受macOS系统沙箱限制，缓存／技能／登记输入／源工程仍不可写。普通编辑使用临时本地配置目录；显式本地模型目录须处于读取根并作为只读缓存传递。模型维护需另走setup，不由计划触发扩大权限。根权限扩张需要新的精确宿主授权。桌面入口同时隔离本次拥有的固定签名应用和CLI客户端，仅允许其分配的loopback端口。无法确认同等隔离的手工外部bridge拒绝；不回退无隔离执行。

Installer maintenance and editor access are separate: explicitly authorize the runtime directory for installation, while the editor sandbox denies writes there. Registered input files and source deliveries remain protected. Explicit local model directories are read-only to editing; model maintenance is a separate setup operation. Unsupported bridge isolation refuses execution.

此为在研接入，尚不证明全部权限／秘密合同、固定发行安装或完整GUI上下文通过。旧的低层Python测试API保留兼容调用，不属于带宿主准入的公开入口；仍须完成审计，不能用其无策略调用作为授权路径。

完整命令与所属桌面共用显式 FILMCRAFT_DATA_DIR 的只读缓存；根外／非绝对／控制字符引用在安装前拒绝。截图 TMPDIR 与缓存分离，不扩大模型写入权限。Complete-command and owned desktop use the same explicitly granted read-only cache; temporary screenshots use a separate authorized directory.

## 原生转发与模型维护

`cli.py` 的工程读取、exec/run/render/export/import/MCP 等入口同样要求在 `--` 前提供 `--read-root`、`--write-root` 和 `--runtime-home`；原生进程保护源工程、技能与固定运行时，所有子进程均过滤宿主环境。仅精确 `--version`、`help`、`commands`、`commands --json` 无工程查询保留旧调用方式，附加工程参数不属于豁免。

模型下载必须单独使用 `--model-maintenance -- exec transcript.downloadModel '{"model":"whisper-tiny"}' --data-dir "$MODEL_DATA_DIR"`；该目录须已存在并有独立可信写入授权，不能位于技能、运行时或解释器目录。维护进程的写根缩小为该目录，独立开放网络出站；不允许混合工程参数或其他命令，普通编辑不获得模型维护权限。完整示例见 [转录场景](transcript-scene.md)。
