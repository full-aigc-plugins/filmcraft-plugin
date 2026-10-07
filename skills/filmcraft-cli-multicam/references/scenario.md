# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 38 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `clip` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `clip.createMulticam` | Create Multi-Camera Source Sequence… | `describe clip.createMulticam` |
| `clip.multicamEnable` | Enable | `describe clip.multicamEnable` |
| `clip.multicamFlatten` | Flatten | `describe clip.multicamFlatten` |

### `multicam` — 35

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `multicam.switchAngle` | Switch Multi-Camera Angle | `describe multicam.switchAngle` |
| `multicam.recordStart` | Start Multi-Camera Recording | `describe multicam.recordStart` |
| `multicam.cut` | Cut to Camera | `describe multicam.cut` |
| `multicam.recordStop` | Stop Multi-Camera Recording | `describe multicam.recordStop` |
| `multicam.audioFollowsVideo` | Multi-Camera Audio Follows Video | `describe multicam.audioFollowsVideo` |
| `multicam.editCameras` | Edit Cameras… | `describe multicam.editCameras` |
| `multicam.cutToCamera` | Cut to Camera | `describe multicam.cutToCamera` |
| `multicam.gridLayout` | Multi-Camera Layout | `describe multicam.gridLayout` |
| `multicam.page` | Multi-Camera Page | `describe multicam.page` |
| `multicam.nextPage` | Next Multi-Camera Page | `describe multicam.nextPage` |
| `multicam.prevPage` | Previous Multi-Camera Page | `describe multicam.prevPage` |
| `multicam.selectionTopDown` | Multi-Camera Selection Top Down | `describe multicam.selectionTopDown` |
| `multicam.showPreviewMonitor` | Show Multi-Camera Preview Monitor | `describe multicam.showPreviewMonitor` |
| `multicam.autoAdjustQuality` | Auto-Adjust Multi-Camera Playback Quality | `describe multicam.autoAdjustQuality` |
| `multicam.transmitView` | Transmit Multi-Camera View | `describe multicam.transmitView` |
| `multicam.grid` | Multi-Camera Grid | `describe multicam.grid` |
| `multicam.inspect` | Inspect Multi-Camera | `describe multicam.inspect` |
| `multicam.selectCamera1` | Select Camera 1 | `describe multicam.selectCamera1` |
| `multicam.cutToCamera1` | Cut to Camera 1 | `describe multicam.cutToCamera1` |
| `multicam.selectCamera2` | Select Camera 2 | `describe multicam.selectCamera2` |
| `multicam.cutToCamera2` | Cut to Camera 2 | `describe multicam.cutToCamera2` |
| `multicam.selectCamera3` | Select Camera 3 | `describe multicam.selectCamera3` |
| `multicam.cutToCamera3` | Cut to Camera 3 | `describe multicam.cutToCamera3` |
| `multicam.selectCamera4` | Select Camera 4 | `describe multicam.selectCamera4` |
| `multicam.cutToCamera4` | Cut to Camera 4 | `describe multicam.cutToCamera4` |
| `multicam.selectCamera5` | Select Camera 5 | `describe multicam.selectCamera5` |
| `multicam.cutToCamera5` | Cut to Camera 5 | `describe multicam.cutToCamera5` |
| `multicam.selectCamera6` | Select Camera 6 | `describe multicam.selectCamera6` |
| `multicam.cutToCamera6` | Cut to Camera 6 | `describe multicam.cutToCamera6` |
| `multicam.selectCamera7` | Select Camera 7 | `describe multicam.selectCamera7` |
| `multicam.cutToCamera7` | Cut to Camera 7 | `describe multicam.cutToCamera7` |
| `multicam.selectCamera8` | Select Camera 8 | `describe multicam.selectCamera8` |
| `multicam.cutToCamera8` | Cut to Camera 8 | `describe multicam.cutToCamera8` |
| `multicam.selectCamera9` | Select Camera 9 | `describe multicam.selectCamera9` |
| `multicam.cutToCamera9` | Cut to Camera 9 | `describe multicam.cutToCamera9` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
