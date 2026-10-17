# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 参考镜头匹配与风格分离

参考：[calesthio/generative-media-skills/color-grading-finishing](https://github.com/calesthio/generative-media-skills/blob/8c85352d5d75d4dcbe58480bd138e37b9742bab1/skills/production/post-production/color-grading-finishing/SKILL.md)。

先确认素材和序列的色彩设置，再选参考帧进行匹配；比较肤色、产品颜色和高光，匹配后再决定风格，而不是一开始叠加多个LUT。

原配方：`color-match`。输入与边界：示例参数必须按当前输入、选择和实际返回ID替换；$变量先解析，数组变量整字段替换，不能将本文件直接当原生CLI脚本执行。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `color.spaces` | `{}` |
| 2 | `sequence.colorSettings` | `{"workingSpace":"rec709","wideGamut":false,"autoToneMap":false}` |
| 3 | `lumetri.applyMatch` | `{"referenceFrame":0,"faceDetection":true}` |
| 4 | `sequence.inspect` | `{}` |

检查：相邻镜头的主体颜色和曝光衔接正常，参考帧明确。

能力边界：启用Rec.709设置不代表已完成未知Log输入转换或HDR交付认证。

原配方结果检查："相邻镜头反复切换比较肤色、中性物体、黑白点，不能只看一帧。"

原配方限制：参考帧需换成实际镜头；HDR素材不得盲设rec709和关闭tone map。

## 版本与执行

执行包装沿用本技能主文件。先检查序列、素材与片段ID。tick、秒和帧各按对应方法换算；示例clip=1不是通用目标。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
