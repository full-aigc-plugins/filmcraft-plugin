# 预览与成片输出操作指南

## 目标与前置

导出预览帧、成片、交换文件与输出验证。原生 export 等待完成后解码检查尺寸、帧率、时长和音轨，记录交换损失。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `file.exportInterchange` | Export Interchange |
| `file.exportEdl` | EDL… |
| `file.exportSelectionProject` | Selection as FilmCraft Project… |
| `file.exportAle` | Avid Log Exchange… |
| `file.exportOtio` | OpenTimelineIO… |
| `file.exportFcp7Xml` | Final Cut Pro XML… |
| `file.exportFcpxml` | FCPXML… |
| `file.exportAaf` | AAF… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 33 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY --read-root READ_ROOT --write-root WRITE_ROOT --write-root RUNTIME_HOME --runtime-home RUNTIME_HOME` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时先按 `command-usage.md` 检查隔离能力；不具备同等目录隔离的bridge入口拒绝执行。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `export` — 19

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `export.presets.list` | List Export Presets | `describe export.presets.list` |
| `export.presets.get` | Get Export Preset | `describe export.presets.get` |
| `export.presets.save` | Save Export Preset | `describe export.presets.save` |
| `export.presets.delete` | Delete Export Preset | `describe export.presets.delete` |
| `export.presets.favorite` | Favorite Export Preset | `describe export.presets.favorite` |
| `export.presets.import` | Import Export Presets | `describe export.presets.import` |
| `export.presets.export` | Export Export Presets | `describe export.presets.export` |
| `export.formats` | List Export Formats | `describe export.formats` |
| `export.resolve` | Resolve Export Settings | `describe export.resolve` |
| `export.queue.add` | Send to Export Queue | `describe export.queue.add` |
| `export.queue.list` | List Export Queue | `describe export.queue.list` |
| `export.queue.start` | Start Export Queue | `describe export.queue.start` |
| `export.queue.stop` | Stop Export Queue | `describe export.queue.stop` |
| `export.queue.cancel` | Cancel Queued Export | `describe export.queue.cancel` |
| `export.queue.retry` | Retry Queued Export | `describe export.queue.retry` |
| `export.queue.remove` | Remove Queued Export | `describe export.queue.remove` |
| `export.queue.move` | Reorder Queued Export | `describe export.queue.move` |
| `export.queue.clear` | Clear Finished Exports | `describe export.queue.clear` |
| `export.quick` | Quick Export | `describe export.quick` |

### `file` — 12

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.exportInterchange` | Export Interchange | `describe file.exportInterchange` |
| `file.exportEdl` | EDL… | `describe file.exportEdl` |
| `file.exportSelectionProject` | Selection as FilmCraft Project… | `describe file.exportSelectionProject` |
| `file.exportAle` | Avid Log Exchange… | `describe file.exportAle` |
| `file.exportOtio` | OpenTimelineIO… | `describe file.exportOtio` |
| `file.exportFcp7Xml` | Final Cut Pro XML… | `describe file.exportFcp7Xml` |
| `file.exportFcpxml` | FCPXML… | `describe file.exportFcpxml` |
| `file.exportAaf` | AAF… | `describe file.exportAaf` |
| `file.exportOmf` | OMF… | `describe file.exportOmf` |
| `file.exportMedia` | Media… | `describe file.exportMedia` |
| `file.exportGraphicsTemplate` | Motion Graphics Template… | `describe file.exportGraphicsTemplate` |
| `file.exportFrame` | Export Frame | `describe file.exportFrame` |

### `jobs` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `jobs.list` | List Jobs | `describe jobs.list` |
| `jobs.cancel` | Cancel Job | `describe jobs.cancel` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
