# 时间线剪辑操作指南

## 目标与前置

排序、裁切、移动镜头，组织轨道与单镜头修改。每秒 254016000000 ticks；大整数用十进制字符串。保留非目标镜头与音轨参数。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `clip.rename` | Rename… |
| `clip.makeSubclip` | Make Subclip… |
| `clip.editSubclip` | Edit Subclip… |
| `clip.editOffline` | Edit Offline… |
| `clip.sourceSettings` | Source Settings… |
| `clip.audioChannels` | Audio Channels… |
| `clip.interpretFootage` | Interpret Footage… |
| `clip.modifyTimecode` | Timecode… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 135 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `clip` — 56

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `clip.rename` | Rename… | `describe clip.rename` |
| `clip.makeSubclip` | Make Subclip… | `describe clip.makeSubclip` |
| `clip.editSubclip` | Edit Subclip… | `describe clip.editSubclip` |
| `clip.editOffline` | Edit Offline… | `describe clip.editOffline` |
| `clip.sourceSettings` | Source Settings… | `describe clip.sourceSettings` |
| `clip.audioChannels` | Audio Channels… | `describe clip.audioChannels` |
| `clip.interpretFootage` | Interpret Footage… | `describe clip.interpretFootage` |
| `clip.modifyTimecode` | Timecode… | `describe clip.modifyTimecode` |
| `clip.frameHoldOptions` | Frame Hold Options… | `describe clip.frameHoldOptions` |
| `clip.frameHold` | Add Frame Hold | `describe clip.frameHold` |
| `clip.insertFrameHoldSegment` | Insert Frame Hold Segment | `describe clip.insertFrameHoldSegment` |
| `clip.fieldOptions` | Field Options… | `describe clip.fieldOptions` |
| `clip.timeInterpolation.frameSampling` | Frame Sampling | `describe clip.timeInterpolation.frameSampling` |
| `clip.timeInterpolation.frameBlending` | Frame Blending | `describe clip.timeInterpolation.frameBlending` |
| `clip.timeInterpolation.opticalFlow` | Optical Flow | `describe clip.timeInterpolation.opticalFlow` |
| `clip.scaleToFrameSize` | Scale to Frame Size | `describe clip.scaleToFrameSize` |
| `clip.fitToFrame` | Fit to frame | `describe clip.fitToFrame` |
| `clip.fillFrame` | Fill frame | `describe clip.fillFrame` |
| `clip.audioGain` | Audio Gain… | `describe clip.audioGain` |
| `clip.breakoutToMono` | Breakout to Mono | `describe clip.breakoutToMono` |
| `clip.extractAudio` | Extract Audio | `describe clip.extractAudio` |
| `clip.speedDuration` | Speed/Duration… | `describe clip.speedDuration` |
| `clip.sceneEditDetection` | Scene Edit Detection… | `describe clip.sceneEditDetection` |
| `clip.enable` | Enable | `describe clip.enable` |
| `clip.link` | Link | `describe clip.link` |
| `clip.group` | Group | `describe clip.group` |
| `clip.ungroup` | Ungroup | `describe clip.ungroup` |
| `clip.audioPeak` | Audio Clip Peak Amplitude | `describe clip.audioPeak` |
| `clip.nest` | Nest… | `describe clip.nest` |
| `clip.replaceFromSource` | From Source Monitor | `describe clip.replaceFromSource` |
| `clip.replaceFromSourceMatchFrame` | From Source Monitor, Match Frame | `describe clip.replaceFromSourceMatchFrame` |
| `clip.replaceFromBin` | From Bin | `describe clip.replaceFromBin` |
| `clip.restoreCaptionsFromSource` | Restore Captions from Source Clip | `describe clip.restoreCaptionsFromSource` |
| `clip.updateMetadata` | Update Metadata… | `describe clip.updateMetadata` |
| `clip.generateAudioWaveform` | Generate Audio Waveform | `describe clip.generateAudioWaveform` |
| `clip.automateToSequence` | Automate to Sequence… | `describe clip.automateToSequence` |
| `clip.synchronize` | Synchronize… | `describe clip.synchronize` |
| `clip.mergeClips` | Merge Clips… | `describe clip.mergeClips` |
| `clip.createMulticam` | Create Multi-Camera Source Sequence… | `describe clip.createMulticam` |
| `clip.multicamEnable` | Enable | `describe clip.multicamEnable` |
| `clip.multicamFlatten` | Flatten | `describe clip.multicamFlatten` |
| `clip.remix.enable` | Enable Remix | `describe clip.remix.enable` |
| `clip.remix.properties` | Remix Properties… | `describe clip.remix.properties` |
| `clip.remix.revert` | Revert Remix | `describe clip.remix.revert` |
| `clip.remix` | Remix | `describe clip.remix` |
| `clip.volumeUp` | Increase Clip Volume | `describe clip.volumeUp` |
| `clip.volumeDown` | Decrease Clip Volume | `describe clip.volumeDown` |
| `clip.volumeUpMany` | Increase Clip Volume Many | `describe clip.volumeUpMany` |
| `clip.volumeDownMany` | Decrease Clip Volume Many | `describe clip.volumeDownMany` |
| `clip.nudgeVolumeUp1` | Nudge Volume +1dB | `describe clip.nudgeVolumeUp1` |
| `clip.nudgeVolumeUp3` | Nudge Volume +3dB | `describe clip.nudgeVolumeUp3` |
| `clip.nudgeVolumeDown1` | Nudge Volume -1dB | `describe clip.nudgeVolumeDown1` |
| `clip.nudgeVolumeDown3` | Nudge Volume -3dB | `describe clip.nudgeVolumeDown3` |
| `clip.setPosterFrame` | Set Poster Frame | `describe clip.setPosterFrame` |
| `clip.clearPosterFrame` | Clear Poster Frame | `describe clip.clearPosterFrame` |
| `clip.setTimeInterpolation` | Set Time Interpolation | `describe clip.setTimeInterpolation` |

### `timeline` — 55

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `timeline.place` | Place Clip | `describe timeline.place` |
| `timeline.select` | Select Clips | `describe timeline.select` |
| `timeline.move` | Move Clips | `describe timeline.move` |
| `timeline.trim` | Trim Edit | `describe timeline.trim` |
| `timeline.roll` | Rolling Edit | `describe timeline.roll` |
| `timeline.slip` | Slip | `describe timeline.slip` |
| `timeline.slide` | Slide | `describe timeline.slide` |
| `timeline.rateStretch` | Rate Stretch | `describe timeline.rateStretch` |
| `timeline.razor` | Razor | `describe timeline.razor` |
| `timeline.setTrack` | Track Settings | `describe timeline.setTrack` |
| `timeline.setTargeting` | Track Targeting | `describe timeline.setTargeting` |
| `timeline.selectClipAtPlayhead` | Select Clip at Playhead | `describe timeline.selectClipAtPlayhead` |
| `timeline.selectNextClip` | Select Next Clip | `describe timeline.selectNextClip` |
| `timeline.selectPrevClip` | Select Previous Clip | `describe timeline.selectPrevClip` |
| `timeline.nudgeLeft` | Nudge Clip Selection Left One Frame | `describe timeline.nudgeLeft` |
| `timeline.nudgeRight` | Nudge Clip Selection Right One Frame | `describe timeline.nudgeRight` |
| `timeline.nudgeLeft5` | Nudge Clip Selection Left Five Frames | `describe timeline.nudgeLeft5` |
| `timeline.nudgeRight5` | Nudge Clip Selection Right Five Frames | `describe timeline.nudgeRight5` |
| `timeline.nudgeUp` | Nudge Clip Selection Up | `describe timeline.nudgeUp` |
| `timeline.nudgeDown` | Nudge Clip Selection Down | `describe timeline.nudgeDown` |
| `timeline.slipLeft` | Slip Clip Selection Left One Frame | `describe timeline.slipLeft` |
| `timeline.slipRight` | Slip Clip Selection Right One Frame | `describe timeline.slipRight` |
| `timeline.slipLeft5` | Slip Clip Selection Left Five Frames | `describe timeline.slipLeft5` |
| `timeline.slipRight5` | Slip Clip Selection Right Five Frames | `describe timeline.slipRight5` |
| `timeline.slideLeft` | Slide Clip Selection Left One Frame | `describe timeline.slideLeft` |
| `timeline.slideRight` | Slide Clip Selection Right One Frame | `describe timeline.slideRight` |
| `timeline.slideLeft5` | Slide Clip Selection Left Five Frames | `describe timeline.slideLeft5` |
| `timeline.slideRight5` | Slide Clip Selection Right Five Frames | `describe timeline.slideRight5` |
| `timeline.toggleAllVideoTargets` | Toggle All Video Targets | `describe timeline.toggleAllVideoTargets` |
| `timeline.toggleAllAudioTargets` | Toggle All Audio Targets | `describe timeline.toggleAllAudioTargets` |
| `timeline.toggleAllSourceVideo` | Toggle All Source Video | `describe timeline.toggleAllSourceVideo` |
| `timeline.toggleAllSourceAudio` | Toggle All Source Audio | `describe timeline.toggleAllSourceAudio` |
| `timeline.moveVideoTargetsUp` | Move All Video Targets Up | `describe timeline.moveVideoTargetsUp` |
| `timeline.moveVideoTargetsDown` | Move All Video Targets Down | `describe timeline.moveVideoTargetsDown` |
| `timeline.moveAudioTargetsUp` | Move All Audio Targets Up | `describe timeline.moveAudioTargetsUp` |
| `timeline.moveAudioTargetsDown` | Move All Audio Targets Down | `describe timeline.moveAudioTargetsDown` |
| `timeline.toggleMuteTargetedAudio` | Toggle Mute for All Targeted Audio Tracks | `describe timeline.toggleMuteTargetedAudio` |
| `timeline.toggleSoloTargetedAudio` | Toggle Solo for All Targeted Audio Tracks | `describe timeline.toggleSoloTargetedAudio` |
| `timeline.toggleOutputTargetedVideo` | Toggle Track Output for All Targeted Video Tracks | `describe timeline.toggleOutputTargetedVideo` |
| `timeline.toggleTargetV1` | Toggle Target Video 1 | `describe timeline.toggleTargetV1` |
| `timeline.toggleTargetV2` | Toggle Target Video 2 | `describe timeline.toggleTargetV2` |
| `timeline.toggleTargetV3` | Toggle Target Video 3 | `describe timeline.toggleTargetV3` |
| `timeline.toggleTargetV4` | Toggle Target Video 4 | `describe timeline.toggleTargetV4` |
| `timeline.toggleTargetV5` | Toggle Target Video 5 | `describe timeline.toggleTargetV5` |
| `timeline.toggleTargetV6` | Toggle Target Video 6 | `describe timeline.toggleTargetV6` |
| `timeline.toggleTargetV7` | Toggle Target Video 7 | `describe timeline.toggleTargetV7` |
| `timeline.toggleTargetV8` | Toggle Target Video 8 | `describe timeline.toggleTargetV8` |
| `timeline.toggleTargetA1` | Toggle Target Audio 1 | `describe timeline.toggleTargetA1` |
| `timeline.toggleTargetA2` | Toggle Target Audio 2 | `describe timeline.toggleTargetA2` |
| `timeline.toggleTargetA3` | Toggle Target Audio 3 | `describe timeline.toggleTargetA3` |
| `timeline.toggleTargetA4` | Toggle Target Audio 4 | `describe timeline.toggleTargetA4` |
| `timeline.toggleTargetA5` | Toggle Target Audio 5 | `describe timeline.toggleTargetA5` |
| `timeline.toggleTargetA6` | Toggle Target Audio 6 | `describe timeline.toggleTargetA6` |
| `timeline.toggleTargetA7` | Toggle Target Audio 7 | `describe timeline.toggleTargetA7` |
| `timeline.toggleTargetA8` | Toggle Target Audio 8 | `describe timeline.toggleTargetA8` |

### `trim` — 24

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `trim.edit` | Trim Edit | `describe trim.edit` |
| `trim.applyDefaultTransition` | Apply Default Transitions to Selection | `describe trim.applyDefaultTransition` |
| `trim.selectEditPoint` | Select Edit Point | `describe trim.selectEditPoint` |
| `trim.selectNearest` | Select Nearest Edit Point | `describe trim.selectNearest` |
| `trim.clear` | Clear Edit Point Selection | `describe trim.clear` |
| `trim.toggleType` | Toggle Trim Type | `describe trim.toggleType` |
| `trim.backward` | Trim Backward | `describe trim.backward` |
| `trim.forward` | Trim Forward | `describe trim.forward` |
| `trim.backwardMany` | Trim Backward Many | `describe trim.backwardMany` |
| `trim.forwardMany` | Trim Forward Many | `describe trim.forwardMany` |
| `trim.shuttle` | Dynamic Trim (Shuttle) | `describe trim.shuttle` |
| `trim.shuttleStop` | Dynamic Trim Stop | `describe trim.shuttleStop` |
| `trim.cancelDynamic` | Cancel Dynamic Trim | `describe trim.cancelDynamic` |
| `trim.playAround` | Play Around Edit | `describe trim.playAround` |
| `trim.tick` | Advance Trim Playback | `describe trim.tick` |
| `trim.monitor` | Trim Monitor State | `describe trim.monitor` |
| `trim.nudge` | Trim by Frames | `describe trim.nudge` |
| `trim.extendToPlayhead` | Extend Selected Edit to Playhead | `describe trim.extendToPlayhead` |
| `trim.ripplePrevious` | Ripple Trim Previous Edit to Playhead | `describe trim.ripplePrevious` |
| `trim.rippleNext` | Ripple Trim Next Edit to Playhead | `describe trim.rippleNext` |
| `trim.previous` | Trim Previous Edit to Playhead | `describe trim.previous` |
| `trim.next` | Trim Next Edit to Playhead | `describe trim.next` |
| `trim.extendPreviousEdit` | Extend Previous Edit To Playhead | `describe trim.extendPreviousEdit` |
| `trim.extendNextEdit` | Extend Next Edit To Playhead | `describe trim.extendNextEdit` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
