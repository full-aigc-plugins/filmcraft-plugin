# 本场景的 Craft 方法与参数

下列是实际方法与示例参数。capture/$ref是手册记号，先读取返回值，再将整个引用对象替换为真实值；不能将引用对象直接发给CLI/MCP。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 建立本任务素材箱并记录返回bin | `file.newBin` | `{"name":"Product details"}` |
| 2. 导入实际素材并记录返回items | `file.import` | `{"paths":["input/product.mp4"],"bin":{"$ref":"bin.bin"}}` |
| 3. 创建目标序列 | `file.newSequence` | `{"name":"Product","width":1920,"height":1080,"fps":25}` |
| 4. 显式打开导入结果中的实际素材ID | `source.open` | `{"item":{"$ref":"media.items.0"}}` |
| 5. 源入点为第0帧 | `markers.markIn` | `{"target":"source","frame":0}` |
| 6. 含出点帧：4秒素材选择0至最后一帧 | `markers.markOut` | `{"target":"source","frame":99}` |
| 7. 在同一源监视器会话中插入 | `source.insert` | `{}` |
| 8. 检查实际序列和时长 | `sequence.inspect` | `{}` |

新增插入后的尺寸适配：用 `clip.fitToFrame`，参数 `{"clips":[实际返回片段ID]}`。它保持画面完整和比例，允许黑边；要求铺满裁切时先确认主体安全区和实际变换能力，不能把适配完整画面称为自动构图。

## 返回值和会话

capture/$ref仅为手册返回值记号，不是原生CLI/MCP参数。先读取对应结果，再以实际整数替换整个$ref对象。相同batch的源打开、入出点与insert必须在同一次CLI run或同一MCP会话执行；工程重开不保留源监视器。示例输入至少4秒，需按源素材实际帧率重算出点。

CLI使用 `filmcraft-cli --project input.fcproj --save-as output.fcproj run steps.jsonl`，每行仅含原生 `{"id":"方法ID","params":{...}}`。本轮新建工程第一次调用省略--project；后续打开已保存的新工程。需要跨批读取返回值时，按batch依次保存中间副本，再生成下一批原生JSONL；source.open、markers.markIn/Out和source.insert必须处于同一run批次，不能靠保存重开恢复源监视器。保持素材路径相对于同一个工作目录，或运行时传入已确认的真实路径。

MCP先等待editor_status就绪，再在同一编辑器会话中使用command_run：`{"id":"方法ID","params":{...}}`；读取实时返回值填入下一步。独立CLI新进程不证明宿主画面同步。

## 参数核对与检查

先读 [命令目录](craft-command-evidence.json) 的当前schema和 [结构化步骤](craft-steps.json)。

型号、真实卖点、规格文字、镜头对应，结尾行动入口完整。

边界：新建示例：先probe素材帧率和时长，4秒范围以源帧率计算含末帧的出点；本例假设源与目标帧率一致。源素材ID、片段ID从返回值取得，不猜测。素材不足4秒、帧率不同或已有序列时先重算范围，不覆盖输入。

来源见 [工作流来源](workflow-sources.json)。仅借鉴事实与方法，正文和参数适配原创。
