# FilmCraft main：只选择关联素材的一侧

main `09aaf9bf15d510eda1c413c0ccabb1d7e08b41c5`没有新增命令标识，`timeline.select`新增可选`linked`字段，见[实际目录差异](main-selection.json)。上游同提交`crates/engine/src/individual_selection_tests.rs`明确区分本次选择和全局关联选择设置。本指导结合目录与源码，新增关联音视频单侧场景已通过Windows原生main工程模型专项回归，不用原有纯视频样例替代。

## 单独编辑音频或视频

仅在用户确需单独一侧（如J/L-cut或只删某条音频）时使用：

1. 在当前内嵌会话读取时间线和实际clip ID，先识别其关联音频/视频对象及轨道、入出点、起始位置，另存工作副本。普通同步剪辑保持关联选择，不默认关闭。
2. 用当前MCP `command_run`执行以下方法映射，实际id须替换：

```text
id: timeline.select
params: {clips: [实际目标clipID], add: false, toggle: false, linked: false}
```

linked:false仅限制本次选择，不改变`sequence.linkedSelection`的全局开关。不要为了临时单选修改全局偏好。linked:true仍遵守全局开关关闭的状态，不能认为它强行重新关联。

3. inspect确认选择只有本次目标，再执行用户要求的编辑。确需仅删除这一侧时，确认当前选择仍只有目标后执行`edit.clear {}`，按当前精确选择删除。不要传`clips`或`clip`：main对显式目标仍按全局关联选择设置扩展伙伴，`linked:false`并不会改变后续显式删除的扩展规则。两次调用间若选择被用户或其他操作改变，先重新读取并选择，不能直接删除。
4. 比较关联伙伴及非目标轨道的起始位置、长度、源入出点和源文件保持，确认用户要求的同步/错开关系。需要撤回时用`edit.undo {}`并重新核对；保存新工程，重开听看相关片段。选择数量正确不等于声画交付正确。

本候选的旧安装器/参数守卫可能仍固定旧版本。新字段只发给实际声明该契约的main接口；不为调用成功绕过旧守卫或把另一个headless工程的选择当作当前画面。Windows原生main专项 [39011329666](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39011329666) 使用内置演示中的两对关联素材：复现显式删除扩展伙伴；分别仅删除视频或音频，确认非目标片段完整不变、单选不关闭全局关联、撤销恢复、保存重开均通过。仅验证工程模型；真实采访素材的解码试听、J/L-cut声画效果和宿主画面同步仍待验收。
