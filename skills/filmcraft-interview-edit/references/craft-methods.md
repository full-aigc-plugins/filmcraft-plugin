# 本场景的 Craft 方法与参数

下列是实际方法与示例参数。capture/$ref是手册记号，先读取返回值，再将整个引用对象替换为真实值；不能将引用对象直接发给CLI/MCP。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 按议题建立素材箱 | `file.newBin` | `{"name":"Interview topics"}` |
| 2. 在可靠议题边界添加标记 | `markers.add` | `{"target":"program","time":0,"name":"议题起点","comment":"核对原始上下文"}` |
| 3. 只对明确片段ID修剪示例 | `timeline.trim` | `{"clip":{"$ref":"clip"},"edge":"out","mode":"regular","deltaFrames":-5}` |
| 4. 检查修剪后序列 | `sequence.inspect` | `{}` |

## 返回值和会话

执行前从当前sequence.inspect取得唯一目标片段ID，替换$ref:clip整个对象为实际整数。此记号不是原生参数，不使用预设clip=1。

CLI使用 `filmcraft-cli --project input.fcproj --save-as output.fcproj run steps.jsonl`，每行仅含原生 `{"id":"方法ID","params":{...}}`。本轮新建工程第一次调用省略--project；后续打开已保存的新工程。需要跨批读取返回值时，按batch依次保存中间副本，再生成下一批原生JSONL；source.open、markers.markIn/Out和source.insert必须处于同一run批次，不能靠保存重开恢复源监视器。保持素材路径相对于同一个工作目录，或运行时传入已确认的真实路径。

MCP先等待editor_status就绪，再在同一编辑器会话中使用command_run：`{"id":"方法ID","params":{...}}`；读取实时返回值填入下一步。独立CLI新进程不证明宿主画面同步。

## 参数核对与检查

先读 [命令目录](craft-command-evidence.json) 的当前schema和 [结构化步骤](craft-steps.json)。

首尾词完整、语义忠实、没有截断发音，字幕与说话人一致。

边界：clip=1是示例，必须从序列实际返回ID取得；不靠拼接改变原话含义。

来源见 [工作流来源](workflow-sources.json)。仅借鉴事实与方法，正文和参数适配原创。
