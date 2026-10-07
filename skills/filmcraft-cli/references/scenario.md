# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 135 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `command` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `command.list` | List Commands | `describe command.list` |

### `edit` — 37

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `edit.undo` | Undo | `describe edit.undo` |
| `edit.redo` | Redo | `describe edit.redo` |
| `edit.cut` | Cut | `describe edit.cut` |
| `edit.copy` | Copy | `describe edit.copy` |
| `edit.paste` | Paste | `describe edit.paste` |
| `edit.pasteInsert` | Paste Insert | `describe edit.pasteInsert` |
| `edit.pasteAttributes` | Paste Attributes… | `describe edit.pasteAttributes` |
| `edit.removeAttributes` | Remove Attributes… | `describe edit.removeAttributes` |
| `edit.clear` | Clear | `describe edit.clear` |
| `edit.rippleDelete` | Ripple Delete | `describe edit.rippleDelete` |
| `edit.selectAll` | Select All | `describe edit.selectAll` |
| `edit.selectAllMatching` | Select All Matching | `describe edit.selectAllMatching` |
| `edit.deselectAll` | Deselect All | `describe edit.deselectAll` |
| `edit.find` | Find… | `describe edit.find` |
| `edit.findNext` | Find Next | `describe edit.findNext` |
| `edit.duplicate` | Duplicate | `describe edit.duplicate` |
| `edit.selectLabelGroup` | Select Label Group | `describe edit.selectLabelGroup` |
| `edit.label.violet` | Violet | `describe edit.label.violet` |
| `edit.label.iris` | Iris | `describe edit.label.iris` |
| `edit.label.caribbean` | Caribbean | `describe edit.label.caribbean` |
| `edit.label.lavender` | Lavender | `describe edit.label.lavender` |
| `edit.label.cerulean` | Cerulean | `describe edit.label.cerulean` |
| `edit.label.forest` | Forest | `describe edit.label.forest` |
| `edit.label.rose` | Rose | `describe edit.label.rose` |
| `edit.label.mango` | Mango | `describe edit.label.mango` |
| `edit.label.purple` | Purple | `describe edit.label.purple` |
| `edit.label.blue` | Blue | `describe edit.label.blue` |
| `edit.label.teal` | Teal | `describe edit.label.teal` |
| `edit.label.magenta` | Magenta | `describe edit.label.magenta` |
| `edit.label.tan` | Tan | `describe edit.label.tan` |
| `edit.label.green` | Green | `describe edit.label.green` |
| `edit.label.brown` | Brown | `describe edit.label.brown` |
| `edit.label.yellow` | Yellow | `describe edit.label.yellow` |
| `edit.removeUnused` | Remove Unused | `describe edit.removeUnused` |
| `edit.consolidateDuplicates` | Consolidate Duplicates | `describe edit.consolidateDuplicates` |
| `edit.editOriginal` | Edit Original | `describe edit.editOriginal` |
| `edit.label` | Label | `describe edit.label` |

### `events` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `events.list` | List Events | `describe events.list` |
| `events.clear` | Clear All Events | `describe events.clear` |

### `fonts` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `fonts.list` | List Fonts | `describe fonts.list` |

### `help` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `help.systemReport` | System Compatibility Report | `describe help.systemReport` |

### `history` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `history.list` | List History | `describe history.list` |

### `markers` — 31

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `markers.markIn` | Mark In | `describe markers.markIn` |
| `markers.markOut` | Mark Out | `describe markers.markOut` |
| `markers.markClip` | Mark Clip | `describe markers.markClip` |
| `markers.markSelection` | Mark Selection | `describe markers.markSelection` |
| `markers.markSplitVideoIn` | Video In | `describe markers.markSplitVideoIn` |
| `markers.markSplitVideoOut` | Video Out | `describe markers.markSplitVideoOut` |
| `markers.markSplitAudioIn` | Audio In | `describe markers.markSplitAudioIn` |
| `markers.markSplitAudioOut` | Audio Out | `describe markers.markSplitAudioOut` |
| `markers.goToIn` | Go to In | `describe markers.goToIn` |
| `markers.goToOut` | Go to Out | `describe markers.goToOut` |
| `markers.goToSplitVideoIn` | Video In | `describe markers.goToSplitVideoIn` |
| `markers.goToSplitVideoOut` | Video Out | `describe markers.goToSplitVideoOut` |
| `markers.goToSplitAudioIn` | Audio In | `describe markers.goToSplitAudioIn` |
| `markers.goToSplitAudioOut` | Audio Out | `describe markers.goToSplitAudioOut` |
| `markers.clearIn` | Clear In | `describe markers.clearIn` |
| `markers.clearOut` | Clear Out | `describe markers.clearOut` |
| `markers.clearInOut` | Clear In and Out | `describe markers.clearInOut` |
| `markers.add` | Add Marker | `describe markers.add` |
| `markers.addRange` | Add Range Marker | `describe markers.addRange` |
| `markers.addRangeInOut` | Add Range Marker to In and Out | `describe markers.addRangeInOut` |
| `markers.goNext` | Go to Next Marker | `describe markers.goNext` |
| `markers.goPrev` | Go to Previous Marker | `describe markers.goPrev` |
| `markers.clearCurrent` | Clear Selected Marker | `describe markers.clearCurrent` |
| `markers.clearAll` | Clear Markers | `describe markers.clearAll` |
| `markers.showAllMarkerColors` | Show All Marker Colors | `describe markers.showAllMarkerColors` |
| `markers.filterColors` | Marker Colour Filter | `describe markers.filterColors` |
| `markers.edit` | Edit Marker… | `describe markers.edit` |
| `markers.addChapter` | Add Chapter Marker… | `describe markers.addChapter` |
| `markers.addFlashCue` | Add Flash Cue Marker… | `describe markers.addFlashCue` |
| `markers.rippleSequenceMarkers` | Ripple Sequence Markers | `describe markers.rippleSequenceMarkers` |
| `markers.copyPasteIncludesSequenceMarkers` | Copy Paste Includes Sequence Markers | `describe markers.copyPasteIncludesSequenceMarkers` |

### `mediaCache` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `mediaCache.info` | Media Cache Info | `describe mediaCache.info` |
| `mediaCache.clean` | Delete Media Cache Files | `describe mediaCache.clean` |

### `metadata` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `metadata.get` | Get Metadata | `describe metadata.get` |
| `metadata.set` | Edit Metadata | `describe metadata.set` |

### `perf` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `perf.stats` | Performance Statistics | `describe perf.stats` |

### `playhead` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `playhead.set` | Set Playhead | `describe playhead.set` |
| `playhead.step` | Step Frames | `describe playhead.step` |
| `playhead.stepForward` | Step Forward One Frame | `describe playhead.stepForward` |
| `playhead.stepBack` | Step Back One Frame | `describe playhead.stepBack` |
| `playhead.stepForward5` | Step Forward Five Frames | `describe playhead.stepForward5` |
| `playhead.stepBack5` | Step Back Five Frames | `describe playhead.stepBack5` |
| `playhead.nextEdit` | Go to Next Edit Point | `describe playhead.nextEdit` |
| `playhead.prevEdit` | Go to Previous Edit Point | `describe playhead.prevEdit` |
| `playhead.start` | Go to Sequence Start | `describe playhead.start` |
| `playhead.end` | Go to Sequence End | `describe playhead.end` |
| `playhead.nextEditAnyTrack` | Go to Next Edit Point on Any Track | `describe playhead.nextEditAnyTrack` |
| `playhead.prevEditAnyTrack` | Go to Previous Edit Point on Any Track | `describe playhead.prevEditAnyTrack` |
| `playhead.selectedClipStart` | Go to Selected Clip Start | `describe playhead.selectedClipStart` |
| `playhead.selectedClipEnd` | Go to Selected Clip End | `describe playhead.selectedClipEnd` |

### `prefs` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `prefs.get` | Get Preferences | `describe prefs.get` |
| `prefs.set` | Set Preferences | `describe prefs.set` |
| `prefs.reset` | Reset Preferences | `describe prefs.reset` |
| `prefs.schema` | Settings Schema | `describe prefs.schema` |

### `presets` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `presets.list` | List Effect Presets | `describe presets.list` |
| `presets.save` | Save Preset | `describe presets.save` |
| `presets.apply` | Apply Preset | `describe presets.apply` |
| `presets.delete` | Delete Preset | `describe presets.delete` |
| `presets.rename` | Rename Preset | `describe presets.rename` |
| `presets.export` | Export Presets | `describe presets.export` |
| `presets.import` | Import Presets | `describe presets.import` |

### `shortcuts` — 16

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shortcuts.list` | List Keyboard Shortcuts | `describe shortcuts.list` |
| `shortcuts.get` | Get Shortcuts of a Command | `describe shortcuts.get` |
| `shortcuts.set` | Assign Shortcut | `describe shortcuts.set` |
| `shortcuts.clear` | Clear Shortcut | `describe shortcuts.clear` |
| `shortcuts.undo` | Undo Shortcut Change | `describe shortcuts.undo` |
| `shortcuts.redo` | Redo Shortcut Change | `describe shortcuts.redo` |
| `shortcuts.conflicts` | Shortcut Conflicts | `describe shortcuts.conflicts` |
| `shortcuts.forKey` | Shortcuts on a Key | `describe shortcuts.forKey` |
| `shortcuts.resolve` | Resolve Shortcut | `describe shortcuts.resolve` |
| `shortcuts.presets` | Keyboard Shortcut Presets | `describe shortcuts.presets` |
| `shortcuts.loadPreset` | Load Shortcut Preset | `describe shortcuts.loadPreset` |
| `shortcuts.savePreset` | Save Shortcut Preset As | `describe shortcuts.savePreset` |
| `shortcuts.deletePreset` | Delete Shortcut Preset | `describe shortcuts.deletePreset` |
| `shortcuts.export` | Export Keyboard Shortcuts | `describe shortcuts.export` |
| `shortcuts.import` | Import Keyboard Shortcuts | `describe shortcuts.import` |
| `shortcuts.audit` | Shortcut Audit | `describe shortcuts.audit` |

### `state` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `state.inspect` | Inspect Editor State | `describe state.inspect` |

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
