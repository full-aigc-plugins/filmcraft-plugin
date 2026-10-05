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
