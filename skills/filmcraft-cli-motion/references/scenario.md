# 图文与镜头动画操作指南

## 目标与前置

创建文字图形、效果参数与镜头关键帧。只编辑指定对象与属性；复杂独立合成可按名称交给 effectcraft-cli-animation，不更换 fcproj 交付要求。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `effects.apply` | Apply Effect |
| `effects.remove` | Remove Effect |
| `effects.setParam` | Set Effect Parameter |
| `effects.toggleAnimation` | Toggle Animation |
| `effects.toggleEnabled` | Toggle Effect |
| `effects.reset` | Reset Effect |
| `effects.addKeyframe` | Add/Remove Keyframe |
| `effects.deleteKeyframe` | Delete Keyframe |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 105 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `effects` — 13

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `effects.apply` | Apply Effect | `describe effects.apply` |
| `effects.remove` | Remove Effect | `describe effects.remove` |
| `effects.setParam` | Set Effect Parameter | `describe effects.setParam` |
| `effects.toggleAnimation` | Toggle Animation | `describe effects.toggleAnimation` |
| `effects.toggleEnabled` | Toggle Effect | `describe effects.toggleEnabled` |
| `effects.reset` | Reset Effect | `describe effects.reset` |
| `effects.addKeyframe` | Add/Remove Keyframe | `describe effects.addKeyframe` |
| `effects.deleteKeyframe` | Delete Keyframe | `describe effects.deleteKeyframe` |
| `effects.moveKeyframe` | Move Keyframe | `describe effects.moveKeyframe` |
| `effects.setInterpolation` | Keyframe Interpolation | `describe effects.setInterpolation` |
| `effects.setKeyframe` | Edit Keyframe | `describe effects.setKeyframe` |
| `effects.list` | List Effects | `describe effects.list` |
| `effects.setDefaultTransition` | Set Selected as Default Transition | `describe effects.setDefaultTransition` |

### `graphics` — 81

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `graphics.newText` | Text | `describe graphics.newText` |
| `graphics.newShape` | Shape | `describe graphics.newShape` |
| `graphics.setText` | Edit Text | `describe graphics.setText` |
| `graphics.set` | Set Graphic Properties | `describe graphics.set` |
| `graphics.selectLayer` | Select Graphic Layer | `describe graphics.selectLayer` |
| `graphics.deleteLayer` | Delete Graphic Layer | `describe graphics.deleteLayer` |
| `graphics.arrangeLayer` | Arrange Graphic Layer | `describe graphics.arrangeLayer` |
| `graphics.align` | Align Layers | `describe graphics.align` |
| `graphics.distribute` | Distribute Layers | `describe graphics.distribute` |
| `graphics.list` | List Graphic Layers | `describe graphics.list` |
| `graphics.newVerticalText` | Vertical Text | `describe graphics.newVerticalText` |
| `graphics.newRectangle` | Rectangle | `describe graphics.newRectangle` |
| `graphics.newEllipse` | Ellipse | `describe graphics.newEllipse` |
| `graphics.newPolygon` | Polygon | `describe graphics.newPolygon` |
| `graphics.newFromFile` | From file… | `describe graphics.newFromFile` |
| `graphics.alignFrame.left` | Left | `describe graphics.alignFrame.left` |
| `graphics.alignFrame.hcenter` | Center Horizontally | `describe graphics.alignFrame.hcenter` |
| `graphics.alignFrame.right` | Right | `describe graphics.alignFrame.right` |
| `graphics.alignFrame.top` | Top | `describe graphics.alignFrame.top` |
| `graphics.alignFrame.vcenter` | Center Vertically | `describe graphics.alignFrame.vcenter` |
| `graphics.alignFrame.bottom` | Bottom | `describe graphics.alignFrame.bottom` |
| `graphics.alignGroup.left` | Left | `describe graphics.alignGroup.left` |
| `graphics.alignGroup.hcenter` | Center Horizontally | `describe graphics.alignGroup.hcenter` |
| `graphics.alignGroup.right` | Right | `describe graphics.alignGroup.right` |
| `graphics.alignGroup.top` | Top | `describe graphics.alignGroup.top` |
| `graphics.alignGroup.vcenter` | Center Vertically | `describe graphics.alignGroup.vcenter` |
| `graphics.alignGroup.bottom` | Bottom | `describe graphics.alignGroup.bottom` |
| `graphics.alignSelection.left` | Left | `describe graphics.alignSelection.left` |
| `graphics.alignSelection.hcenter` | Center Horizontally | `describe graphics.alignSelection.hcenter` |
| `graphics.alignSelection.right` | Right | `describe graphics.alignSelection.right` |
| `graphics.alignSelection.top` | Top | `describe graphics.alignSelection.top` |
| `graphics.alignSelection.vcenter` | Center Vertically | `describe graphics.alignSelection.vcenter` |
| `graphics.alignSelection.bottom` | Bottom | `describe graphics.alignSelection.bottom` |
| `graphics.distributeVertically` | Distribute Vertically | `describe graphics.distributeVertically` |
| `graphics.distributeSpaceVertically` | Distribute Space Vertically | `describe graphics.distributeSpaceVertically` |
| `graphics.distributeHorizontally` | Distribute Horizontally | `describe graphics.distributeHorizontally` |
| `graphics.distributeSpaceHorizontally` | Distribute Space Horizontally | `describe graphics.distributeSpaceHorizontally` |
| `graphics.bringToFront` | Bring to Front | `describe graphics.bringToFront` |
| `graphics.bringForward` | Bring Forward | `describe graphics.bringForward` |
| `graphics.sendBackward` | Send Backward | `describe graphics.sendBackward` |
| `graphics.sendToBack` | Send to Back | `describe graphics.sendToBack` |
| `graphics.selectNextGraphic` | Select Next Graphic | `describe graphics.selectNextGraphic` |
| `graphics.selectPreviousGraphic` | Select Previous Graphic | `describe graphics.selectPreviousGraphic` |
| `graphics.selectNextLayer` | Select Next Layer | `describe graphics.selectNextLayer` |
| `graphics.selectPreviousLayer` | Select Previous Layer | `describe graphics.selectPreviousLayer` |
| `graphics.resetAllParameters` | Reset All Parameters | `describe graphics.resetAllParameters` |
| `graphics.resetDuration` | Reset Duration | `describe graphics.resetDuration` |
| `graphics.template.list` | List Graphics Templates | `describe graphics.template.list` |
| `graphics.template.apply` | Apply Graphics Template | `describe graphics.template.apply` |
| `graphics.template.export` | Export As Motion Graphics Template… | `describe graphics.template.export` |
| `graphics.template.install` | Install Motion Graphics Template… | `describe graphics.template.install` |
| `graphics.template.remove` | Remove Graphics Template | `describe graphics.template.remove` |
| `graphics.template.set` | Set Template Property | `describe graphics.template.set` |
| `graphics.template.controls` | List Template Properties | `describe graphics.template.controls` |
| `graphics.template.thumbnail` | Graphics Template Thumbnail | `describe graphics.template.thumbnail` |
| `graphics.setRoll` | Roll/Crawl Options | `describe graphics.setRoll` |
| `graphics.setResponsiveTime` | Responsive Design - Time | `describe graphics.setResponsiveTime` |
| `graphics.pin` | Responsive Design - Position | `describe graphics.pin` |
| `graphics.setCharStyle` | Character Style | `describe graphics.setCharStyle` |
| `graphics.upgradeCaption` | Upgrade Caption to Graphic | `describe graphics.upgradeCaption` |
| `graphics.upgradeToSourceGraphic` | Upgrade to Source Graphic | `describe graphics.upgradeToSourceGraphic` |
| `graphics.fonts.used` | List Fonts Used | `describe graphics.fonts.used` |
| `graphics.fontSizeUp` | Increase Font Size by One Unit | `describe graphics.fontSizeUp` |
| `graphics.fontSizeDown` | Decrease Font Size by One Unit | `describe graphics.fontSizeDown` |
| `graphics.fontSizeUp5` | Increase Font Size by Five Units | `describe graphics.fontSizeUp5` |
| `graphics.fontSizeDown5` | Decrease Font Size by Five Units | `describe graphics.fontSizeDown5` |
| `graphics.leadingUp` | Increase Leading by One Unit | `describe graphics.leadingUp` |
| `graphics.leadingDown` | Decrease Leading by One Unit | `describe graphics.leadingDown` |
| `graphics.leadingUp5` | Increase Leading by Five Units | `describe graphics.leadingUp5` |
| `graphics.leadingDown5` | Decrease Leading by Five Units | `describe graphics.leadingDown5` |
| `graphics.alignTextLeft` | Left align text | `describe graphics.alignTextLeft` |
| `graphics.alignTextCenter` | Center align text | `describe graphics.alignTextCenter` |
| `graphics.alignTextRight` | Right align text | `describe graphics.alignTextRight` |
| `graphics.nudgeLeft` | Nudge Selected Object to left by one | `describe graphics.nudgeLeft` |
| `graphics.nudgeRight` | Nudge Selected Object to right by one | `describe graphics.nudgeRight` |
| `graphics.nudgeUp` | Nudge Selected Object up by one | `describe graphics.nudgeUp` |
| `graphics.nudgeDown` | Nudge Selected Object down by one | `describe graphics.nudgeDown` |
| `graphics.nudgeLeft5` | Nudge Selected Object to left by five | `describe graphics.nudgeLeft5` |
| `graphics.nudgeRight5` | Nudge Selected Object to right by five | `describe graphics.nudgeRight5` |
| `graphics.nudgeUp5` | Nudge Selected Object up by five | `describe graphics.nudgeUp5` |
| `graphics.nudgeDown5` | Nudge Selected Object down by five | `describe graphics.nudgeDown5` |

### `masks` — 11

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `masks.add` | Create Mask | `describe masks.add` |
| `masks.remove` | Delete Mask | `describe masks.remove` |
| `masks.set` | Change Mask | `describe masks.set` |
| `masks.moveVertex` | Move Mask Vertex | `describe masks.moveVertex` |
| `masks.translate` | Move Mask | `describe masks.translate` |
| `masks.addVertex` | Add Mask Vertex | `describe masks.addVertex` |
| `masks.removeVertex` | Delete Mask Vertex | `describe masks.removeVertex` |
| `masks.track` | Track Selected Mask | `describe masks.track` |
| `masks.toggleVertexSmooth` | Convert Mask Vertex | `describe masks.toggleVertexSmooth` |
| `masks.select` | Select Mask | `describe masks.select` |
| `masks.list` | List Masks | `describe masks.list` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
