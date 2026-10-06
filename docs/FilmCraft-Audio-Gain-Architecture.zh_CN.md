# FilmCraft 静态音轨增益架构与验收

当前为候选技能源能力；固定插件 dev.7 尚未包含此入口。规格事实源为插件 OpenSpec 的 FC-DM-003-GAIN。

工程工作流原先拒绝 mixer.setStrip，尽管独立音频技能已提供该原生命令。现在允许 strip 为 A1、A2 等明确音轨，且仅包含有限数值 volumeDb。总线、录音、路由、自动化等字段继续拒绝；录音或声音生成不由本入口承担。

```mermaid
flowchart LR
    A[明确音轨和分贝增益] --> B[参数校验]
    B --> C[固定原生 CLI mixer.setStrip]
    C --> D[另存 fcproj 与原生成片]
    D --> E[解码音频并核对幅度]
```

创建与修订均使用技能自己的 scripts/workflow.py。修订示例操作：

```json
{"command":"mixer.setStrip","params":{"strip":"A1","volumeDb":-6.0}}
```

候选首次使用测试仅复制一个音频技能到隔离项目 .agents/skills，并从空运行目录公开安装固定 CLI。真实 1 项通过（5.010 秒）：-6 dB 的解码 RMS 比例为 0.5011754631，理论值 0.5011872336；原交付文件、镜头与音频片段、字幕、技能资源摘要保留。目标回归先因 unsupported_command 失败，最小实现后 8 项通过。证据：[候选记录](evidence/audio-gain-candidate.json)。

尚未证明多音轨相互混音、自动化、GUI、模型派发或创作质量。固定技能源发布、插件 vendor 更新及固定安装副本复验尚待执行；不得把候选测试写为当前插件已交付。
