# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 建立商品镜头分组 | `file.newBin` | `{"name":"Product details"}` |
| 2. 导入实际已授权素材 | `file.import` | `{"paths":["input/product.mp4"]}` |
| 3. 新建匹配平台序列 | `file.newSequence` | `{"name":"Product","width":1920,"height":1080,"fps":25}` |
| 4. 选定素材后按源范围插入 | `source.insert` | `{}` |
| 5. 检查序列结构 | `sequence.inspect` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`command_run`，参数 `{"id": "file.newBin", "params": {"name": "Product details"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

filmcraft-cli --project input.fcproj --save-as output.fcproj run steps.jsonl；每行 {"id":"file.newBin","params":{"name":"Selects"}}。时钟tick与秒/帧参数不得混用。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

型号、真实卖点、规格文字、镜头对应，结尾行动入口完整。

边界：导入返回item后需选定源与入出点；导入+新序列不会自动完成剪辑。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
