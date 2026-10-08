# 音频与配音组织操作指南

## 目标与前置

组织已有配音和音乐、增益、混音与音画同步。使用用户提供或已授权声音；本技能不承诺语音生成。解码成片并核对音轨、起始时间与同步。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `mixer.addSubmix` | Add Audio Submix Track |
| `mixer.inspect` | Inspect Audio Track Mixer |
| `mixer.setStrip` | Track Mixer Settings |
| `mixer.setValue` | Set Mixer Control |
| `mixer.touch` | Touch Mixer Control |
| `mixer.release` | Release Mixer Control |
| `mixer.recordStart` | Start Automation Pass |
| `mixer.recordStop` | Write Automation |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 38 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY --read-root READ_ROOT --write-root WRITE_ROOT --write-root RUNTIME_HOME --runtime-home RUNTIME_HOME` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时先按 `command-usage.md` 检查隔离能力；不具备同等目录隔离的bridge入口拒绝执行。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `audio` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `audio.voiceover.settings` | Voice-Over Record Settings | `describe audio.voiceover.settings` |
| `audio.voiceover.start` | Start Voice-over Recording | `describe audio.voiceover.start` |
| `audio.voiceover.sync` | Sync Voice-over Capture | `describe audio.voiceover.sync` |
| `audio.voiceover.stop` | Stop Voice-over Recording | `describe audio.voiceover.stop` |
| `audio.toggleScrubbing` | Toggle Audio During Scrubbing | `describe audio.toggleScrubbing` |

### `clipMixer` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `clipMixer.set` | Audio Clip Mixer Adjust | `describe clipMixer.set` |
| `clipMixer.setMode` | Audio Clip Mixer Automation Mode | `describe clipMixer.setMode` |
| `clipMixer.touch` | Touch Clip Mixer Control | `describe clipMixer.touch` |
| `clipMixer.release` | Release Clip Mixer Control | `describe clipMixer.release` |

### `essentialSound` — 9

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `essentialSound.inspect` | Inspect Essential Sound | `describe essentialSound.inspect` |
| `essentialSound.setType` | Set Audio Type | `describe essentialSound.setType` |
| `essentialSound.clearType` | Clear Audio Type | `describe essentialSound.clearType` |
| `essentialSound.set` | Essential Sound Setting | `describe essentialSound.set` |
| `essentialSound.applyPreset` | Apply Sound Preset | `describe essentialSound.applyPreset` |
| `essentialSound.savePreset` | Save Sound Preset | `describe essentialSound.savePreset` |
| `essentialSound.deletePreset` | Delete Sound Preset | `describe essentialSound.deletePreset` |
| `essentialSound.autoMatch` | Auto-Match Loudness | `describe essentialSound.autoMatch` |
| `essentialSound.generateDucking` | Generate Ducking Keyframes | `describe essentialSound.generateDucking` |

### `mixer` — 20

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `mixer.addSubmix` | Add Audio Submix Track | `describe mixer.addSubmix` |
| `mixer.inspect` | Inspect Audio Track Mixer | `describe mixer.inspect` |
| `mixer.setStrip` | Track Mixer Settings | `describe mixer.setStrip` |
| `mixer.setValue` | Set Mixer Control | `describe mixer.setValue` |
| `mixer.touch` | Touch Mixer Control | `describe mixer.touch` |
| `mixer.release` | Release Mixer Control | `describe mixer.release` |
| `mixer.recordStart` | Start Automation Pass | `describe mixer.recordStart` |
| `mixer.recordStop` | Write Automation | `describe mixer.recordStop` |
| `mixer.deleteSubmix` | Delete Submix Track | `describe mixer.deleteSubmix` |
| `mixer.addInsert` | Add Track Effect | `describe mixer.addInsert` |
| `mixer.removeInsert` | Remove Track Effect | `describe mixer.removeInsert` |
| `mixer.setInsert` | Track Effect Settings | `describe mixer.setInsert` |
| `mixer.addSend` | Add Send | `describe mixer.addSend` |
| `mixer.setSend` | Send Settings | `describe mixer.setSend` |
| `mixer.removeSend` | Remove Send | `describe mixer.removeSend` |
| `mixer.setKeyframe` | Add Track Keyframe | `describe mixer.setKeyframe` |
| `mixer.deleteKeyframe` | Delete Track Keyframe | `describe mixer.deleteKeyframe` |
| `mixer.moveKeyframe` | Move Track Keyframe | `describe mixer.moveKeyframe` |
| `mixer.clearLane` | Clear Track Keyframes | `describe mixer.clearLane` |
| `mixer.writeAutomation` | Write Automation Points | `describe mixer.writeAutomation` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
