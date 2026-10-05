# 字幕编辑操作指南

## 目标与前置

导入、创建、修改字幕文本、时间、样式并交付 SRT。字幕必须在序列范围内；SRT 不保留完整字体、位置与样式，原生字幕工程继续交付。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

`describe <id>` 核对参数，再用 `exec <id> <JSON>` 或 `run <JSONL>`；写命令必须同批次保存或配合 `--save-as`。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `captions.newTrack` | Add New Caption Track… |
| `captions.deleteTrack` | Delete Caption Track |
| `captions.setTrack` | Caption Track Settings |
| `captions.setStyle` | Caption Track Style |
| `captions.add` | Add Caption at Playhead |
| `captions.split` | Split Caption |
| `captions.merge` | Merge Captions |
| `captions.setText` | Edit Caption Text |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。


## 中文字幕与已有配音

本技能自带 `examples/chinese-short-film.json`，创建 640×360、24 fps、3 秒原生工程。`shot` 和 `voice` 为已有素材，须至少覆盖约定区间；此例不调用声音生成或上传服务。中文字体示例使用当前 macOS CLI 发现的 `Heiti SC`。先查询 `fonts.list {"system":true}`；该字体不存在时停止并明确选择用户认可的可用中文字体，不静默替换。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" "$SKILL_DIR/examples/chinese-short-film.json" \
  --asset "shot=$SHOT_PATH" --asset "voice=$VOICE_PATH" --output chinese-v1
```

`SHOT_PATH` 与 `VOICE_PATH` 必须为实际已有素材的绝对路径。检查原生字幕的 Unicode 文本、zh-CN 语言、起止 ticks 与样式；SRT 文本正确不能代替画面检查，需要核对烧录字幕可读且没有方框缺字。输出须包含可重开的 `.fcproj`、素材引用、帧预览、SRT 和带音轨的成片。

仅调整文字时，通过 `captions.setText`、原字幕返回 ID 与 `expectedProjectSha256` 另存新工程，保持原音轨与字幕时间。测试夹具可使用显式已安装的系统声音生成参考语音；此操作只属于测试准备，不是本技能自动声音生成能力。

### 当前发布版中文烧录缺陷（2026-10-06）

官方 CLI 0.2.0 的字幕烧录忽略轨道 `font`，即使 `fonts.list` 返回中文字体也可能输出缺字方框。中文模板目前是验收输入，不能据此宣称中文成片通过。原生工程和 SRT 可以保留 Unicode，但必须检查实际烧录画面；遇到方框应报告渲染失败，不能把非空 PNG 当作可用字幕。dev.5 将使用独立维护版 0.2.0-craft.1，其固定公开地址首次安装与中文成片验收已通过；必须使用本技能自己的运行时锁，禁止替换已发布的官方 0.2.0 文件。
