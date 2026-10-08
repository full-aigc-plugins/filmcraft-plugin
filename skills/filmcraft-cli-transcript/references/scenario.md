# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 14 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY --read-root READ_ROOT --write-root WRITE_ROOT --write-root RUNTIME_HOME --runtime-home RUNTIME_HOME` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时先按 `command-usage.md` 检查隔离能力；不具备同等目录隔离的bridge入口拒绝执行。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `transcript` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `transcript.generate` | Transcribe… | `describe transcript.generate` |
| `transcript.set` | Import Transcript | `describe transcript.set` |
| `transcript.delete` | Delete Transcript | `describe transcript.delete` |
| `transcript.inspect` | Inspect Transcript | `describe transcript.inspect` |
| `transcript.search` | Search Transcript | `describe transcript.search` |
| `transcript.models` | List Speech Models | `describe transcript.models` |
| `transcript.downloadModel` | Download Speech Model | `describe transcript.downloadModel` |
| `transcript.select` | Mark Selected Text | `describe transcript.select` |
| `transcript.extract` | Extract Selected Text | `describe transcript.extract` |
| `transcript.lift` | Lift Selected Text | `describe transcript.lift` |
| `transcript.renameSpeaker` | Rename Speaker… | `describe transcript.renameSpeaker` |
| `transcript.removePauses` | Remove Pauses | `describe transcript.removePauses` |
| `transcript.removeFillers` | Remove Filler Words | `describe transcript.removeFillers` |
| `transcript.createCaptions` | Create Captions from Transcript… | `describe transcript.createCaptions` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
