# 本场景的 Craft 方法与参数

下列是实际方法与示例参数。capture/$ref是手册记号，先读取返回值，再将整个引用对象替换为真实值；不能将引用对象直接发给CLI/MCP。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 检查序列工作空间 | `color.spaces` | `{}` |
| 2. 按素材来源确认工作空间 | `sequence.colorSettings` | `{"workingSpace":"rec709","wideGamut":false,"autoToneMap":false}` |
| 3. 对明确选中片段匹配参考帧 | `lumetri.applyMatch` | `{"referenceFrame":0,"faceDetection":true,"clip":{"$ref":"clip"}}` |
| 4. 检查序列内容 | `sequence.inspect` | `{}` |

## 返回值和会话

执行前从当前sequence.inspect取得唯一目标片段ID，替换$ref:clip整个对象为实际整数。此记号不是原生参数，不使用预设clip=1。

CLI使用 `filmcraft-cli --project input.fcproj --save-as output.fcproj run steps.jsonl`，每行仅含原生 `{"id":"方法ID","params":{...}}`。本轮新建工程第一次调用省略--project；后续打开已保存的新工程。需要跨批读取返回值时，按batch依次保存中间副本，再生成下一批原生JSONL；source.open、markers.markIn/Out和source.insert必须处于同一run批次，不能靠保存重开恢复源监视器。保持素材路径相对于同一个工作目录，或运行时传入已确认的真实路径。

MCP先等待editor_status就绪，再在同一编辑器会话中使用command_run：`{"id":"方法ID","params":{...}}`；读取实时返回值填入下一步。独立CLI新进程不证明宿主画面同步。

## 参数核对与检查

先读 [命令目录](craft-command-evidence.json) 的当前schema和 [结构化步骤](craft-steps.json)。

相邻镜头反复切换比较肤色、中性物体、黑白点，不能只看一帧。

边界：参考帧需换成实际镜头；HDR素材不得盲设rec709和关闭tone map。 参考帧必须处于另一个镜头，不能位于目标片段内部；先检查sequence.inspect的startFrame/endFrame及源素材，明确clip参数，避免重开工程后的选择丢失。

来源见 [工作流来源](workflow-sources.json)。仅借鉴事实与方法，正文和参数适配原创。
