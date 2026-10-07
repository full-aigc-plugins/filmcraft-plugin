# 调色与 LUT操作指南

## 目标与前置

调整镜头色彩、使用许可明确的 LUT 与颜色预设。核对工作空间和 LUT 来源；渲染前后采样帧比较，不能把参数写入当颜色正确。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `color.spaces` | List Colour Spaces |
| `lumetri.presets` | List Lumetri Presets |
| `lumetri.applyPreset` | Apply Lumetri Preset |
| `lumetri.presetThumbnails` | Lumetri Preset Thumbnails |
| `lut.import` | Import LUT… |
| `lut.list` | List LUTs |
| `lut.remove` | Remove LUT |
| `lut.export` | Export LUT |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 13 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `color` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `color.spaces` | List Colour Spaces | `describe color.spaces` |

### `lumetri` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `lumetri.presets` | List Lumetri Presets | `describe lumetri.presets` |
| `lumetri.applyPreset` | Apply Lumetri Preset | `describe lumetri.applyPreset` |
| `lumetri.presetThumbnails` | Lumetri Preset Thumbnails | `describe lumetri.presetThumbnails` |
| `lumetri.setInputLut` | Set Input LUT | `describe lumetri.setInputLut` |
| `lumetri.setLook` | Set Creative Look | `describe lumetri.setLook` |
| `lumetri.applyMatch` | Apply Match | `describe lumetri.applyMatch` |
| `lumetri.setSection` | Toggle Lumetri Section | `describe lumetri.setSection` |

### `lut` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `lut.import` | Import LUT… | `describe lut.import` |
| `lut.list` | List LUTs | `describe lut.list` |
| `lut.remove` | Remove LUT | `describe lut.remove` |
| `lut.export` | Export LUT | `describe lut.export` |

### `scopes` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `scopes.read` | Read Lumetri Scopes | `describe scopes.read` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
