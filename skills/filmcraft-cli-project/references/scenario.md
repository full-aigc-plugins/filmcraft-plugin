# 工程与序列操作指南

## 目标与前置

创建、打开、保存 fcproj 和组织序列、素材箱。保存原工程前核对摘要；另存新工程，不覆盖用户并行修改。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `file.newProject` | Project… |
| `file.openDemoProject` | Demo Project |
| `file.newSequence` | Sequence… |
| `file.newSequenceFromClip` | Sequence From Clip |
| `file.newBin` | Bin |
| `file.newBinFromSelection` | Bin From Selection |
| `file.newSearchBin` | Search Bin |
| `file.newOfflineFile` | Offline File… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 119 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `file` — 44

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.newProject` | Project… | `describe file.newProject` |
| `file.openDemoProject` | Demo Project | `describe file.openDemoProject` |
| `file.newSequence` | Sequence… | `describe file.newSequence` |
| `file.newSequenceFromClip` | Sequence From Clip | `describe file.newSequenceFromClip` |
| `file.newBin` | Bin | `describe file.newBin` |
| `file.newBinFromSelection` | Bin From Selection | `describe file.newBinFromSelection` |
| `file.newSearchBin` | Search Bin | `describe file.newSearchBin` |
| `file.newOfflineFile` | Offline File… | `describe file.newOfflineFile` |
| `file.newAdjustmentLayer` | Adjustment Layer… | `describe file.newAdjustmentLayer` |
| `file.newBarsAndTone` | Bars and Tone… | `describe file.newBarsAndTone` |
| `file.newBlackVideo` | Black Video… | `describe file.newBlackVideo` |
| `file.newColorMatte` | Color Matte… | `describe file.newColorMatte` |
| `file.newCountingLeader` | Universal Counting Leader… | `describe file.newCountingLeader` |
| `file.newTransparentVideo` | Transparent Video… | `describe file.newTransparentVideo` |
| `file.importDemoFootage` | Demo Footage | `describe file.importDemoFootage` |
| `file.importAaf` | Import AAF… | `describe file.importAaf` |
| `file.open` | Open Project… | `describe file.open` |
| `file.close` | Close | `describe file.close` |
| `file.closeProject` | Close Project | `describe file.closeProject` |
| `file.closeAllProjects` | Close All Projects | `describe file.closeAllProjects` |
| `file.closeAllOtherProjects` | Close All Other Projects | `describe file.closeAllOtherProjects` |
| `file.save` | Save | `describe file.save` |
| `file.saveAs` | Save As… | `describe file.saveAs` |
| `file.saveCopy` | Save a Copy… | `describe file.saveCopy` |
| `file.saveAsTemplate` | Save as Template… | `describe file.saveAsTemplate` |
| `file.saveAll` | Save All | `describe file.saveAll` |
| `file.revert` | Revert | `describe file.revert` |
| `file.recover` | Recover Unsaved Changes… | `describe file.recover` |
| `file.discardRecovery` | Discard Unsaved Changes | `describe file.discardRecovery` |
| `file.recoveryList` | List Recoverable Sessions | `describe file.recoveryList` |
| `file.autoSaveNow` | Auto Save Now | `describe file.autoSaveNow` |
| `file.autoSaveStatus` | Auto Save Status | `describe file.autoSaveStatus` |
| `file.listAutoSaves` | Browse Auto-Saves | `describe file.listAutoSaves` |
| `file.replaceFonts` | Replace Fonts in Projects… | `describe file.replaceFonts` |
| `file.importFromMediaBrowser` | Import from Media Browser | `describe file.importFromMediaBrowser` |
| `file.import` | Import… | `describe file.import` |
| `file.importImageSequence` | Import Image Sequence… | `describe file.importImageSequence` |
| `file.mediaPropertiesFile` | File… | `describe file.mediaPropertiesFile` |
| `file.mediaProperties` | Selection… | `describe file.mediaProperties` |
| `file.projectSettings.general` | General… | `describe file.projectSettings.general` |
| `file.projectSettings.scratchDisks` | Scratch Disks… | `describe file.projectSettings.scratchDisks` |
| `file.projectManager` | Project Manager… | `describe file.projectManager` |
| `file.templates` | List Project Templates | `describe file.templates` |
| `file.newProjectFromTemplate` | New Project from Template | `describe file.newProjectFromTemplate` |

### `project` — 35

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `project.select` | Select Project Items | `describe project.select` |
| `project.delete` | Clear | `describe project.delete` |
| `project.moveToBin` | Move to Bin | `describe project.moveToBin` |
| `project.setMarks` | Set Source In/Out | `describe project.setMarks` |
| `project.inspect` | Inspect Project | `describe project.inspect` |
| `project.ingestSettings` | Ingest Settings… | `describe project.ingestSettings` |
| `project.view.get` | Project Panel View | `describe project.view.get` |
| `project.view.set` | Set Project Panel View | `describe project.view.set` |
| `project.columns.list` | List Project Columns | `describe project.columns.list` |
| `project.columns.set` | Metadata Display | `describe project.columns.set` |
| `project.columns.resize` | Resize Column | `describe project.columns.resize` |
| `project.sort` | Sort Project Items | `describe project.sort` |
| `project.items` | List Project Panel Rows | `describe project.items` |
| `project.viewPreset.list` | List View Presets | `describe project.viewPreset.list` |
| `project.viewPreset.save` | Save Current View Preset | `describe project.viewPreset.save` |
| `project.viewPreset.saveAs` | Save As New View Preset | `describe project.viewPreset.saveAs` |
| `project.viewPreset.restore` | Restore View Preset | `describe project.viewPreset.restore` |
| `project.viewPreset.rename` | Rename View Preset | `describe project.viewPreset.rename` |
| `project.viewPreset.delete` | Delete View Preset | `describe project.viewPreset.delete` |
| `project.freeform.layout` | Freeform Layout | `describe project.freeform.layout` |
| `project.freeform.move` | Move Clip Cards | `describe project.freeform.move` |
| `project.freeform.resize` | Clip Size | `describe project.freeform.resize` |
| `project.freeform.alignToGrid` | Align to Grid | `describe project.freeform.alignToGrid` |
| `project.freeform.reset` | Reset to Grid | `describe project.freeform.reset` |
| `project.freeform.stack` | Stack Clips | `describe project.freeform.stack` |
| `project.freeform.unstack` | Unstack Clips | `describe project.freeform.unstack` |
| `project.freeform.saveArrangement` | Save Arrangement | `describe project.freeform.saveArrangement` |
| `project.freeform.restoreArrangement` | Restore Arrangement | `describe project.freeform.restoreArrangement` |
| `project.freeform.deleteArrangement` | Delete Arrangement | `describe project.freeform.deleteArrangement` |
| `project.freeform.arrangements` | List Arrangements | `describe project.freeform.arrangements` |
| `project.freeform.options` | Freeform View Options… | `describe project.freeform.options` |
| `project.renameBin` | Rename Bin | `describe project.renameBin` |
| `project.searchBinItems` | Search Bin Contents | `describe project.searchBinItems` |
| `project.editSearchBin` | Edit Search Bin | `describe project.editSearchBin` |
| `project.deleteSearchBin` | Delete Search Bin | `describe project.deleteSearchBin` |

### `sequence` — 40

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `sequence.open` | Open in Timeline | `describe sequence.open` |
| `sequence.close` | Close Sequence | `describe sequence.close` |
| `sequence.settings` | Sequence Settings… | `describe sequence.settings` |
| `sequence.renderEffectsInToOut` | Render Effects In to Out | `describe sequence.renderEffectsInToOut` |
| `sequence.renderInToOut` | Render In to Out | `describe sequence.renderInToOut` |
| `sequence.renderSelection` | Render Selection | `describe sequence.renderSelection` |
| `sequence.renderAudio` | Render Audio | `describe sequence.renderAudio` |
| `sequence.deleteRenderFiles` | Delete Render Files | `describe sequence.deleteRenderFiles` |
| `sequence.deleteRenderFilesInToOut` | Delete Render Files In to Out | `describe sequence.deleteRenderFilesInToOut` |
| `sequence.matchFrame` | Match Frame | `describe sequence.matchFrame` |
| `sequence.reverseMatchFrame` | Reverse Match Frame | `describe sequence.reverseMatchFrame` |
| `sequence.addEdit` | Add Edit | `describe sequence.addEdit` |
| `sequence.addEditAllTracks` | Add Edit to All Tracks | `describe sequence.addEditAllTracks` |
| `sequence.applyVideoTransition` | Apply Video Transition | `describe sequence.applyVideoTransition` |
| `sequence.applyAudioTransition` | Apply Audio Transition | `describe sequence.applyAudioTransition` |
| `sequence.lift` | Lift | `describe sequence.lift` |
| `sequence.extract` | Extract | `describe sequence.extract` |
| `sequence.closeGap` | Close Gap | `describe sequence.closeGap` |
| `sequence.goToNextGap` | Next in Sequence | `describe sequence.goToNextGap` |
| `sequence.goToPrevGap` | Previous in Sequence | `describe sequence.goToPrevGap` |
| `sequence.goToNextGapInTrack` | Next in Track | `describe sequence.goToNextGapInTrack` |
| `sequence.goToPrevGapInTrack` | Previous in Track | `describe sequence.goToPrevGapInTrack` |
| `sequence.snap` | Snap in Timeline | `describe sequence.snap` |
| `sequence.linkedSelection` | Linked Selection | `describe sequence.linkedSelection` |
| `sequence.selectionFollowsPlayhead` | Selection Follows Playhead | `describe sequence.selectionFollowsPlayhead` |
| `sequence.showThroughEdits` | Show Through Edits | `describe sequence.showThroughEdits` |
| `sequence.normalizeMixTrack` | Normalize Mix Track… | `describe sequence.normalizeMixTrack` |
| `sequence.makeSubsequence` | Make Subsequence | `describe sequence.makeSubsequence` |
| `sequence.transcribe` | Transcribe Sequence… | `describe sequence.transcribe` |
| `sequence.simplify` | Simplify Sequence… | `describe sequence.simplify` |
| `sequence.addTracks` | Add Tracks… | `describe sequence.addTracks` |
| `sequence.deleteTracks` | Delete Tracks… | `describe sequence.deleteTracks` |
| `sequence.colorSettings` | Color Management… | `describe sequence.colorSettings` |
| `sequence.setTransition` | Edit Transition Settings | `describe sequence.setTransition` |
| `sequence.joinThroughEdits` | Join Through Edits | `describe sequence.joinThroughEdits` |
| `sequence.throughEdits` | List Through Edits | `describe sequence.throughEdits` |
| `sequence.deleteTrack` | Delete Track | `describe sequence.deleteTrack` |
| `sequence.renderBar` | Render Bar | `describe sequence.renderBar` |
| `sequence.inspect` | Inspect Sequence | `describe sequence.inspect` |
| `sequence.revealNested` | Reveal Nested Sequence | `describe sequence.revealNested` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
