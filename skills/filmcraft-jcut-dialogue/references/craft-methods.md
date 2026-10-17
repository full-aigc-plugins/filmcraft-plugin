# 采访声音先入J-cut的方法和参数

A画面0–2秒，B画面2–5秒使用B源1–4秒；A声音0–1秒，B声音1–5秒使用B源0–4秒，使B声音提前1秒进入而露脸后仍声画对齐。

## 输入

A已确认话语在1秒结束，A后1秒是可保留反应镜头；B的音视频必须有相同源时间基准。不能为了J-cut切断词尾或让两句话无意重叠。样例是分离的无声视频与批准音轨；混合AV素材先拆分/检查对应关系和采样率，不盲复制固定时刻。

先用`filmcraft-cli probe <素材>`核对类型、真实时长、帧率、音轨与尺寸。技术样例是320×240、25fps，不是通用成片规格；按交付需求重算序列、源范围、窗口和字幕时间。先保存新输出，不覆盖原素材或已有工程。

## 操作表

| 目的 | 方法 | 参数例子 | 批次 |
| --- | --- | --- | --- |
| 1. 导入本任务已检查的素材，核对返回items顺序与类型 | `file.import` | `{"paths": ["input/shot-a.avi", "input/shot-b.avi", "input/voice-a.wav", "input/voice-b.wav"]}` | import |
| 2. 建立隔离的320×240、25fps技术样例序列 | `file.newSequence` | `{"name": "JCutDialogue", "width": 320, "height": 240, "fps": 25}` | sequence |
| 3. 按已确认时间放入V1 | `timeline.place` | `{"item": {"$ref": "media.items.0"}, "track": "V1", "seconds": 0, "duration": 508032000000, "sourceIn": 0, "insert": false, "video": true, "audio": false}` | shot-a |
| 4. 按已确认时间放入V1 | `timeline.place` | `{"item": {"$ref": "media.items.1"}, "track": "V1", "seconds": 2, "duration": 762048000000, "sourceIn": 254016000000, "insert": false, "video": true, "audio": false}` | shot-b |
| 5. 按已确认时间放入A1 | `timeline.place` | `{"item": {"$ref": "media.items.2"}, "track": "A1", "seconds": 0, "duration": 254016000000, "sourceIn": 0, "insert": false, "video": false, "audio": true}` | voice-a |
| 6. 按已确认时间放入A1 | `timeline.place` | `{"item": {"$ref": "media.items.3"}, "track": "A1", "seconds": 1, "duration": 1016064000000, "sourceIn": 0, "insert": false, "video": false, "audio": true}` | voice-b |
| 7. 两段画面保持完整并统一画幅 | `clip.fitToFrame` | `{"clips": [{"$ref": "aVideo.clips.0"}, {"$ref": "bVideo.clips.0"}]}` | fit |
| 8. 核对所有轨道、源范围与时长 | `sequence.inspect` | `{}` | inspect |
| 9. 保存后另行确认已完成的实际编码文件 | `export.queue.add` | `{"path": "output/review.mp4", "start": true, "wait": true}` | export |

`{"$ref": "media.items.0"}`等对象只是手册占位。第一次file.import返回实际items后，核对数量、路径与媒体类型，再填下一批整数。timeline.place返回clips；不要把素材ID当片段ID。具体计划见[craft-steps.json](craft-steps.json)，参数观察见[craft-command-evidence.json](craft-command-evidence.json)。

## CLI与同会话MCP

CLI逐批将已替换引用的操作写成原生JSONL，每行仅`{"id":"timeline.place","params":{具体参数}}`，不含batch/capture等手册字段。第一批使用`filmcraft-cli --save-as output.fcproj run batch.jsonl`；后续使用`filmcraft-cli --project output.fcproj --save-as output-next.fcproj run batch.jsonl`，使用实际最新检查点继续。以argv调用，避免Windows引号差异。不能将仍有$ref的计划直接运行，也不使用默认demo。

宿主已打开编辑器时，用同一个FilmCraft MCP实例等待editor_status就绪，查当前command_run schema，逐条`command_run {"id":"方法","params":{实际参数}}`并读取实时返回值。遇到禁用或失败先检查当前序列，不能继续下一批。CLI0.8.0与Web候选不同；工具或参数缺失就报告缺口，独立CLI进程不会自动改变另一Web画布。

## 交付检查

A画面0–2秒，B画面2–5秒使用B源1–4秒；A声音0–1秒，B声音1–5秒使用B源0–4秒，使B声音提前1秒进入而露脸后仍声画对齐。

保存后用新CLI进程`--project output.fcproj inspect sequence`核对轨道、每段起止、sourceIn和时长。`render --seconds <秒> --out frame.png`采样剪辑点前后；最终MP4必须`probe`再重新导入解码首中尾，不将队列返回当成功。需要听声音时另行导出`--project output.fcproj export review.wav --format wav`并播放，检查实际声音、交接与响度；静音或纯音夹具不证明真实采访的语义、音质或口型同步。

定格不能用原本静止的画面验证；需对比被选中的源帧和恢复动作后的帧。画中画应对照关闭叠加层的参考，检查保护区和边界。J-cut应同时核对音频先入的时间与后续源对应关系，不把任意错位都叫J-cut。

人像/屏幕素材、姓名和台词必须来自批准输入；不编造文案事实。[固定来源与许可](workflow-sources.json)只证明阅读和原创适配，样本、真实成片、MCP业务与宿主同步分别验收。
