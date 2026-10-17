# 讲解视频画中画的方法和参数

主画面在V1，讲者在V2独立变换，唯一批准讲解声轨在A1。检查讲者窗口不出界、不遮关键内容，背景保护区不变，实际导出保留声音。

## 输入

两视频及narration.wav至少4秒。125%是64×48源得到80×60窗口的样例：实际缩放=目标窗口宽/源宽×100，不能把125当通用比例。位置是序列像素，主画面比例不同允许黑边；真实声画同步和重要区域需按素材重算。

先用`filmcraft-cli probe <素材>`核对类型、真实时长、帧率、音轨与尺寸。技术样例是320×240、25fps，不是通用成片规格；按交付需求重算序列、源范围、窗口和字幕时间。先保存新输出，不覆盖原素材或已有工程。

## 操作表

| 目的 | 方法 | 参数例子 | 批次 |
| --- | --- | --- | --- |
| 1. 导入本任务已检查的素材，核对返回items顺序与类型 | `file.import` | `{"paths": ["input/screen.avi", "input/presenter.avi", "input/narration.wav"]}` | import |
| 2. 建立隔离的320×240、25fps技术样例序列 | `file.newSequence` | `{"name": "PresenterInset", "width": 320, "height": 240, "fps": 25}` | sequence |
| 3. 按已确认时间放入V1 | `timeline.place` | `{"item": {"$ref": "media.items.0"}, "track": "V1", "seconds": 0, "duration": 1016064000000, "sourceIn": 0, "insert": false, "video": true, "audio": false}` | main-place |
| 4. 按已确认时间放入V2 | `timeline.place` | `{"item": {"$ref": "media.items.1"}, "track": "V2", "seconds": 0, "duration": 1016064000000, "sourceIn": 0, "insert": false, "video": true, "audio": false}` | inset-place |
| 5. 按已确认时间放入A1 | `timeline.place` | `{"item": {"$ref": "media.items.2"}, "track": "A1", "seconds": 0, "duration": 1016064000000, "sourceIn": 0, "insert": false, "video": false, "audio": true}` | audio-place |
| 6. 主画面完整适配，保持原始比例 | `clip.fitToFrame` | `{"clips": [{"$ref": "main.clips.0"}]}` | layout |
| 7. 按实际源尺寸计算讲者窗口80×60像素 | `effects.setParam` | `{"clip": {"$ref": "inset.clips.0"}, "effect": "motion", "param": "scale", "value": 125}` | layout |
| 8. 窗口放在右下安全范围，保留16/18像素边距 | `effects.setParam` | `{"clip": {"$ref": "inset.clips.0"}, "effect": "motion", "param": "position", "value": [264, 192]}` | layout |
| 9. 核对所有轨道、源范围与时长 | `sequence.inspect` | `{}` | inspect |
| 10. 保存后另行确认已完成的实际编码文件 | `export.queue.add` | `{"path": "output/review.mp4", "start": true, "wait": true}` | export |

`{"$ref": "media.items.0"}`等对象只是手册占位。第一次file.import返回实际items后，核对数量、路径与媒体类型，再填下一批整数。timeline.place返回clips；不要把素材ID当片段ID。具体计划见[craft-steps.json](craft-steps.json)，参数观察见[craft-command-evidence.json](craft-command-evidence.json)。

## CLI与同会话MCP

CLI逐批将已替换引用的操作写成原生JSONL，每行仅`{"id":"timeline.place","params":{具体参数}}`，不含batch/capture等手册字段。第一批使用`filmcraft-cli --save-as output.fcproj run batch.jsonl`；后续使用`filmcraft-cli --project output.fcproj --save-as output-next.fcproj run batch.jsonl`，使用实际最新检查点继续。以argv调用，避免Windows引号差异。不能将仍有$ref的计划直接运行，也不使用默认demo。

宿主已打开编辑器时，用同一个FilmCraft MCP实例等待editor_status就绪，查当前command_run schema，逐条`command_run {"id":"方法","params":{实际参数}}`并读取实时返回值。遇到禁用或失败先检查当前序列，不能继续下一批。CLI0.8.0与Web候选不同；工具或参数缺失就报告缺口，独立CLI进程不会自动改变另一Web画布。

## 交付检查

主画面在V1，讲者在V2独立变换，唯一批准讲解声轨在A1。检查讲者窗口不出界、不遮关键内容，背景保护区不变，实际导出保留声音。

保存后用新CLI进程`--project output.fcproj inspect sequence`核对轨道、每段起止、sourceIn和时长。`render --seconds <秒> --out frame.png`采样剪辑点前后；最终MP4必须`probe`再重新导入解码首中尾，不将队列返回当成功。需要听声音时另行导出`--project output.fcproj export review.wav --format wav`并播放，检查实际声音、交接与响度；静音或纯音夹具不证明真实采访的语义、音质或口型同步。

定格不能用原本静止的画面验证；需对比被选中的源帧和恢复动作后的帧。画中画应对照关闭叠加层的参考，检查保护区和边界。J-cut应同时核对音频先入的时间与后续源对应关系，不把任意错位都叫J-cut。

人像/屏幕素材、姓名和台词必须来自批准输入；不编造文案事实。[固定来源与许可](workflow-sources.json)只证明阅读和原创适配，样本、真实成片、MCP业务与宿主同步分别验收。
