# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取当前输出预设 | `export.presets.list` | `{}` |
| 2. 核对当前序列结构 | `sequence.inspect` | `{}` |
| 3. 以明确路径排队并等待真实完成 | `export.queue.add` | `{"path":"output/review.mp4","start":true,"wait":true}` |
| 4. 检查队列结果 | `export.queue.list` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "export.presets.list", "params": {}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

filmcraft-cli --project input.fcproj --save-as output.fcproj run steps.jsonl；每行 {"id":"file.newBin","params":{"name":"Selects"}}。时钟tick与秒/帧参数不得混用。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

新进程probe输出并实际播放首尾、总时长、帧率、音画同步。

边界：开始前确认实际编码参数与输出范围；队列存在或wait返回不自动证明画质正确。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
