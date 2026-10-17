# SRT 恒定时间偏移与毫秒精度交付

本流程适用于已经确认全部字幕提前或延迟相同时间的情况。漂移、错字、漏句、翻译及语音转写需要另外处理；本流程不执行 ASR。上游经验来自 SubtitleEdit/subtitleedit 的 Adjust all times 工作流，适配为 FilmCraft 原生命令。

## 执行脚本

相对于本技能目录运行，CLI 路径应为已核实的 FilmCraft 可执行程序：

```sh
python3 scripts/sync_srt.py --cli /path/to/filmcraft-cli --input /path/to/input.srt --project /path/to/source.fcproj --offset-ms 500 --output /path/to/new-delivery
```

`500` 表示延后 500 毫秒，`-500` 表示提前。输出目录必须不存在。不指定 `--project` 时创建 320×180、25fps 的字幕工程，可用 `--fps` 改变帧率；这不是视频合成。输入支持 UTF-8/BOM、CRLF、多行字幕；不处理 ASS、富文本转换或特殊 WebVTT cue settings。字幕不得跨越时间轴零点；既有非空序列不接受超出片尾的偏移。

## 原生命令、参数与顺序

1. `--project source.fcproj exec captions.list` 与 `inspect sequence` 读取原轨道、视频音频和序列设置。不要用 C1 当作稳定对象 ID。
2. `project.items {"recursive":true}` 后，对返回的每个 `item` 调用 `metadata.get {"item":ID}`。读取 File Path，把相对路径按输入工程所在目录解析。`media.relink {"item":ID,"path":"绝对媒体路径","relinkOthers":false,"alignTimecode":false}` 只用于另存副本，不修改原工程。媒体不存在时停止，不能允许离线占位冒充成功。
3. `captions.import {"path":"输入 SRT 绝对路径","name":"Synced subtitles"}` 返回真实 `track` ID；`captions.list` 获取该轨道字幕 ID、`start`、`end`、`text`。
4. FilmCraft 0.8.0 导入会按帧网格取整。例如 25fps 下 1123ms 可变成 1120ms。`captions.setTimes` 同样会取整，因此不能用它恢复精度。一个毫秒等于 **254016000 ticks**。对每条字幕先执行 `captions.trim {"caption":ID,"edge":"out","delta":差值ticks}`，再以 `edge:"in"` 恢复开始时间；零差值跳过。核对文本、时间和数量全部一致。
5. `captions.setTrack {"track":真实ID,"language":"zh"}` 设置语言；`captions.move {"captions":[真实字幕ID],"delta":偏移毫秒×254016000}` 一次移动目标字幕。
6. 每批通过 `--project 输入 --save-as 新工程 run steps.jsonl` 保存。JSONL 每行结构是 `{"id":"命令名","params":{}}`，检查所有结果的 `ok`，不能仅凭进程退出码。
7. 新进程重开 `synced.fcproj`。核对每条字幕精确时间、原始文本及持续时间；保护已有字幕轨道，允许 C1/C2 显示序号因插入改变，但轨道 ID、名称、样式、内容不能变化。视频、音频、标记和序列设置必须保持。
8. `captions.export {"track":真实ID,"path":"绝对输出路径","format":"srt"}`，再导出 `vtt`，解析并逐条核对。原输入及原工程 SHA256 必须保持。

## 可见编辑器与验收边界

需要同步画面时先读取 filmcraft-editor 的当前工具 schema，打开同一个另存工程，按真实 command_list/command_run 能力执行并检查字幕显示。不要把独立 CLI 文件改动当成已连接编辑器的内存状态变化。精确偏移脚本已通过 macOS 和 Windows 原生 CLI 验证；真实 Codex 宿主已验证目标字幕的精度恢复、500ms 移动、同一编辑器画面更新、保存重开及 SRT 导出。宿主测试使用独立字幕序列，不代表浏览器内实际视频解码已通过。当前官方 Web 包只列出 Inter、JetBrains Mono、Noto Serif，测试中中文显示方框而导出文本保持；中文字体显示仍未通过，不能声称完整字幕排版或烧录交付通过。

本地回归覆盖已有视频工程的正负 500ms、独立字幕工程、3 条包含多行中文的奇数毫秒字幕、非目标轨道保护、SRT/VTT 精确导出和跨工作目录实际渲染。35 次原生 CLI 调用通过；不代表真实语音对齐、烧录排版或任意字体已经验收。输出依赖原媒体的绝对路径，移动到其他机器仍需提供媒体并重新链接。

失败时保留中间工程和每批 JSONL 结果用于诊断，仅全部检查通过才写 manifest.json。不要把中间文件当作最终交付。

## 字体预检与交付选择

用户要求预览、烧录或版式效果时，先调用 `command_run {"id":"fonts.list","params":{"system":true}}`。这只是字体家族枚举，不证明它覆盖字幕里的每个字。随后在同一可见编辑器显示一条包含实际中文、人名、标点的代表字幕，观察是否方框或缺字；不可只用英文样片验证中文。

本次 0.8.0 Web 实测只返回 Inter、JetBrains Mono、Noto Serif，中文缺字。`captions.setStyle` 的 `font` 字段用于选择已存在的字体，不会安装字体；不能填一个系统字体名称后声称字体已经加载。官方 Web 的字体来自编译时输入，系统扫描在 Web 中没有本机字体目录，也未发现可用的运行时字体导入命令。外层 HTML/CSS 字体不能替代引擎的字形数据。

若缺字，仍可交付已经核对 Unicode 与时间的 SRT/VTT，明确预览字体未通过；用户要求中文烧录视频时应停止宣称成片完成，使用已证实具备字形覆盖的引擎构建或渲染路径后重新验收。不要把字幕改成英文以绕过中文需求，也不要覆盖官方 WASM。修复上游构建后需重新核对字体枚举、真实样句、导出与保存重开，旧截图不证明新构建通过。
