# 可信执行权限 / Trusted execution permissions

公开工作流和完整命令run入口从独立命令行参数接受读取／写入根；未提供时在计划读取前返回execution_permissions_required。使用已存在、规范真实的目录；不接受软链接或磁盘级根。路径越界在素材摘要读取和安装前拒绝。输出父目录也必须授权，以容纳同父临时工程和执行锁。

Public workflow and full-command run require independent --read-root / --write-root grants before reading the plan. Existing canonical directories only; symlink and disk-wide grants are rejected. Plan and asset paths cannot grant access themselves.

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" "$PLAN" --output "$OUTPUT" \
  --runtime-home "$RUNTIME_HOME" --read-root "$READ_ROOT" \
  --write-root "$PROJECT_ROOT" --write-root "$RUNTIME_HOME"
```

RUNTIME_HOME须事先有独立可信的目录授权。安装维护可写该目录；执行命令的原生进程受macOS系统沙箱限制，缓存／技能／登记输入／源工程仍不可写。普通编辑使用临时本地配置目录；显式本地模型目录须处于读取根并作为只读缓存传递。模型维护需另走setup，不由计划触发扩大权限。根权限扩张需要新的精确宿主授权。桌面入口同时隔离本次拥有的固定签名应用和CLI客户端，仅允许其分配的loopback端口。无法确认同等隔离的手工外部bridge拒绝；不回退无隔离执行。

Installer maintenance and editor access are separate: explicitly authorize the runtime directory for installation, while the editor sandbox denies writes there. Registered input files and source deliveries remain protected. Explicit local model directories are read-only to editing; model maintenance is a separate setup operation. Unsupported bridge isolation refuses execution.

此为在研接入，尚不证明全部权限／秘密合同、固定发行安装或完整GUI上下文通过。旧的低层Python测试API保留兼容调用，不属于带宿主准入的公开入口；仍须完成审计，不能用其无策略调用作为授权路径。
