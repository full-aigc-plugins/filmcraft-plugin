# 转录与按文字剪辑 / Transcript and text-based editing

## 输入、前置状态与交付 / Input, state and delivery

输入包括有音轨的媒体、对应逐词转录或自动识别需求、语言与说话人规则、修改范围。导入媒体后使用实际返回的 item ID；转录属于媒体，inspect 展示活动序列中音频片段映射后的词。先创建或打开目标序列并放置媒体；仅导入转录不等于时间线已有可剪辑词。交付 `.fcproj`、媒体清单、必要的字幕与预览；另存修订并保留原工程。

Transcripts belong to media items. Sequence inspection maps words through the active sequence audio clips. Import media, use returned IDs, then place it into the intended sequence before text editing. Preserve editable projects and dependencies.

## 按场景选择命令 / Choose commands by task

| 场景 | 命令 | 使用步骤和验收 |
| --- | --- | --- |
| 已有逐词转录 | `transcript.set` | 指定媒体 item，提供 language、speakers、words；start/end 为有符号64位JSON整数 tick，不能传秒或数字字符串；计划预检及引用解析后的执行前检查均覆盖 words 中的时间字段。核对返回 words 数量，再 inspect 核对媒体与序列映射 |
| 自动语音识别 | `transcript.models`、`transcript.downloadModel`、`transcript.generate` | 先查询实际模型和安装状态；需要时下载指定模型，再对实际 items 识别。运行时若未编译语音能力或模型不存在，报告实际错误；已导入文本不能当作自动识别成功 |
| 查找口播 | `transcript.inspect`、`transcript.search` | inspect 得到当前词的 i、item、clip、start/end；以 query 搜索，核对返回词范围和对应媒体，不猜测词序号 |
| 标记词段 | `transcript.select` | 使用刚查询的 from/to 词索引；核对实际 mark 与播放头。词索引不是秒，也不是 tick |
| 按词剪辑 | `transcript.extract`、`transcript.lift` | extract 与 lift 的后续片段移动行为需分别核验；先记录目标词段和非目标片段，另存后检查时长、位置、音画同步与删除范围 |
| 修改说话人 | `transcript.renameSpeaker` | 明确媒体 item、speaker 名称或索引和新 name；inspect 核对，不以显示名字推断重新完成了声纹分离 |
| 移除停顿 | `transcript.removePauses` | minSeconds/keepSeconds 使用秒；先核对词间停顿和保留量，执行后检查节奏、片段边界和非目标内容 |
| 移除填充词 | `transcript.removeFillers` | 明确 fillers 列表及任务范围；先查词，再编辑，复核实际删去的时间段和后续音画同步 |
| 生成字幕 | `transcript.createCaptions` | 根据目标语言设置 maxChars、lines、minSeconds、maxSeconds、gapFrames；frames 与 seconds 分开。核对返回字幕数量、轨道文本及时间，再导出适用字幕格式 |
| 删除转录 | `transcript.delete` | 提供真实 items，先保存副本；核对这些媒体转录删除，媒体和无关转录保留。删除转录不等于删除字幕轨道 |

Query each current parameter contract with `commands.py describe COMMAND_ID`. Word indices, tick times, seconds and frame counts are distinct. Imported transcripts, ASR, speaker naming, timeline changes and caption delivery each require their own evidence.

## 参数、计划与执行 / Parameters, plan and execution

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter transcript.
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.set
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.createCaptions
python3 -I -B "$SKILL_DIR/scripts/commands.py" check /absolute/transcript-plan.json
python3 -I -B "$SKILL_DIR/scripts/commands.py" run /absolute/transcript-plan.json --output /absolute/new-transcript-result
```

使用本技能 command-usage.md 的计划合同，返回值通过 $ref 连接后续步骤，保存工程必须在同一会话。重新剪辑后旧词索引可能失效，必须再次 inspect。enabled 反映当前状态，不把空会话状态当作完成前置条件。失败、禁用或超时按原生回执处理；未知结果先检查原任务，不能重放删除。

## 核验范围 / Acceptance scope

本指南覆盖14条命令的场景选择与操作要求；目前不宣称全部命令、自动识别质量或按文字剪辑已完成运行验收。源代码证据来自 FilmCraft engine transcript.set/inspect/create_captions；实际固定运行时及交付必须另行验证。

This guide documents all14 assigned commands. It does not prove automatic transcription quality, every command context or delivered creative acceptance.

## 已执行实例 / Executed example

`examples/transcript-import-captions.json` 使用 `--input voice=/absolute/two-second-media.mp4`，示例画幅96×64、12fps，手工提供两个词的整数tick时间；样例媒体并非语音识别基准。步骤导入媒体、放置音视频、导入转录、搜索、改名、生成字幕并保存工程。`examples/transcript-reopen.json` 接收 `--input project=/absolute/project.fcproj`，重开唯一序列、inspect 转录、captions.list 检查字幕并重新导出SRT。实际多序列项目需显式打开目标序列；C1需按实际字幕轨道核对。

候选源码实例已核验重开后的两个词、Narrator说话人和原始/重开SRT字节一致。自动识别、词段删除、停顿处理及全部14条命令验收仍未完成。

The bounded example imports supplied word timings; it is not an ASR benchmark. Reopen and SRT identity passed. Adapt the media duration, active sequence and caption track for real projects.

## 固定 Whisper 首次安装与识别 / Fixed Whisper first use

当前源技能锁定维护运行时 `0.2.0-craft.4`，启用真实CPU Whisper和模型下载。旧的不可变插件快照可能仍锁定craft.3，必须按自身锁和实际 `transcript.models.available` 判断，不能根据本指南推断旧安装已升级。

设定 `MODEL_DATA_DIR` 为任务授权的持久数据目录（绝对路径）；模型不写入技能目录，也不纳入成片/工程交付包。以下调用只使用本技能资源；先检查原生模型目录、来源、许可和体积。tiny多语言模型约154MB，base默认模型更大；按语言、素材和任务选型，不能把一个样例识别率推广为通用准确率。

```bash
: "${SKILL_DIR:?当前技能实际目录}"
: "${MODEL_DATA_DIR:?声明的持久模型数据目录}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- exec transcript.models --data-dir "$MODEL_DATA_DIR"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- exec transcript.downloadModel '{"model":"whisper-tiny"}' --data-dir "$MODEL_DATA_DIR"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- exec transcript.generate '{"model":"whisper-tiny","language":"en"}' --project /absolute/source.fcproj --save-as /absolute/recognized.fcproj --data-dir "$MODEL_DATA_DIR"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- exec transcript.inspect --project /absolute/recognized.fcproj --data-dir "$MODEL_DATA_DIR"
```

下载依当前任务已授权的必要依赖范围执行；未授权且体积/来源会实质影响任务时只询问新增范围。原生下载按固定revision与SHA-256校验；模型查询的installed只反映文件体积，不能作为内容校验的替代。查询available=false时停止自动识别并报告该固定版本不支持，不用transcript.set伪装识别成功。此处省略items仅适用于活动序列已有音轨；明确媒体时传真实items，language按实际语言使用zh/en/auto。不得将参考文本输入识别器。

另存工程重开后核对词句、媒体时间、音视频和原工程摘要，再使用本指南的createCaptions与captions.export流程。同步识别耗时或超时后先查实际进程及产物，不重放写操作。模型缺失、下载摘要不符、语言或音频不可用均按真实非零回执处理。

Source skills pin maintainedcraft.4 with real native CPU Whisper. Immutable older plugin snapshots retain their own locks. Select a declared persistent model directory, inspect source/license/size, download the pinned model and recognize actual audio. Use the language and media IDs appropriate to the project. Preserve the source, reopen the new project, verify media-time words, then create/export captions. Installed state alone checks sizes; actual model checksums and inference are separate evidence. Public/fixed-host acceptance must be stated separately from a local candidate test.

### 公共工作流的模型目录 / Model directory in public workflows

源码工作流 `workflow.py --data-dir "$MODEL_DATA_DIR"`（Python：`execute(..., data_dir=...)`）将同一持久目录传给 MCP、重开、渲染及导出进程。显式参数优先于 `FILMCRAFT_DATA_DIR`；未配置时保持原生默认目录。Art 编排调用可继承此环境变量。预先下载与识别必须指向同一目录；模型位于该目录的 `models/`，不随成片打包。此源码变更尚未进入已发布的 dev.33 或固定 Film34／Art104。

The source workflow forwards `--data-dir` (Python `data_dir`) to MCP and auxiliary native processes. It overrides `FILMCRAFT_DATA_DIR`, while an unconfigured invocation keeps the native default. Use the same persistent directory for model download and recognition. Models remain under `models/` outside the delivery package. This source change is not yet included in published dev.33 or fixed Film34/Art104.

下载若因断网或 `unexpected end of file` 明确失败，可在同一数据目录重新调用 `transcript.downloadModel`，完成文件由原生下载器保留，未完成文件重新校验。不要自动重放已提交的识别／修改命令；先检查回复、工程状态与恢复记录。首次使用网络失败必须作为失败证据保留，不能用复用本地模型冒充首次下载通过。

After an explicit network download failure, retry only `transcript.downloadModel` in the same directory. The native downloader retains completed files and validates new downloads. Do not automatically replay submitted recognition or editing commands; reconcile replies, project state and recovery records first. Retain first-download failures separately from cached-model acceptance.
