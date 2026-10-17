# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 按实际台词交付字幕

参考：[affaan-m/ecc/video-editing](https://github.com/affaan-m/ecc/blob/76aaa77df6adc5b889e689007bf99b9a4f74af34/skills/video-editing/SKILL.md)；[sfkislev/flue/premiere](https://github.com/sfkislev/flue/blob/6c542fe2e490f47cd984abfc3b78e95021611fd2/skills/premiere/SKILL.md)。

以校对过的台词和源时间为输入，再建立字幕轨并填写起止。导出后回读SRT，抽查跨镜头、长句和人名；需要烧录时另外检查渲染能力。

原配方：`subtitle-delivery`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `captions.newTrack` | `{"format":"Subtitle","name":"中文校对字幕","language":"zh"}` |
| 2 | `captions.add` | `{"text":"经过校对的实际台词","seconds":1,"durationSeconds":3}` |
| 3 | `captions.list` | `{}` |
| 4 | `captions.export` | `{"path":"output/captions.srt","format":"srt"}` |

检查：字幕文字与声音一致，无不合理重叠和持续时间错误。

能力边界：导出SRT不代表已烧录，也不代表自动转录正确；不调用Premiere桥接器。

原配方结果检查："人名数字、断句、重叠、首尾和阅读时间逐项检查，实际回放核对。"

原配方限制：没有执行ASR时不能称为自动转录；例子台词需来自真实录音或用户文案。

## 版本与执行

执行包装沿用本技能主文件。先检查序列、素材与片段ID。tick、秒和帧各按对应方法换算；示例clip=1不是通用目标。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
