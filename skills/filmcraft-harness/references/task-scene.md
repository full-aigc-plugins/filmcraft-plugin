# 执行通道任务模板

## 输入

用户任务、已授权的读写根目录、输出目录与执行模式（commands/workflow/desktop/task_session）。计划文件与示例取自对应领域技能目录；本技能只提供执行脚本与运行时锁。确认当前授权范围及要保留的非目标内容。

## 首次任务

示例请求：安装锁定 CLI 后执行一个原生命令计划。

```bash
: "${HARNESS_DIR:?请先设置为本 SKILL.md 的实际所在目录}"
: "${READ_ROOT:?Set READ_ROOT to an existing independently authorized directory}"
: "${RUNTIME_HOME:?Set RUNTIME_HOME to an existing independently authorized directory}"
: "${WRITE_ROOT:?Set WRITE_ROOT to an existing independently authorized directory}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run PLAN.json --output /absolute/new-result --runtime-home "$RUNTIME_HOME" --read-root "$READ_ROOT" --write-root "$WRITE_ROOT" --write-root "$RUNTIME_HOME"
```

安装参数放 `--` 分隔符前；`--runtime-home` 可隔离缓存。锁定制品摘要失败、损坏安装或不支持平台时停止；不改 PATH、不执行浮动升级。

## 失败

非零退出不算完成；安装失败与原生调用失败分别处理。结果 unknown 时先检查原任务、原工程与回执，不自动重放编辑。超时不证明副作用未发生；保留失败证据与未完成项。

## 局部修订

修订只针对用户指定对象；通过 `--source` 与原工程摘要支持单镜头返工，或在新计划中引用实际返回 ID。核对预期源工程摘要，以新输出目录另存；原目标内复用已有授权，超出范围或授权约束变化才重新确认。

## 核验

重开原生工程核对目标修改与未受影响内容；检查真实导出文件的解码、时长、尺寸和音轨后才能声明成片完成。技术、创作和用户接受分别记录；缺少的维度标 NOT_RUN/manual_review，文件存在或目录检查不能替代验收。
