# 固定76标记与序列设置验收

新增27条标记及2条序列设置命令，headless／所属签名桌面bridge各复用一个实例。与既有86条不重叠，合计115条有界观察；551条在此证据集中仍只有发现，不关闭完整任务8.3或七项V1门禁。

覆盖program目标的普通及拆分入出点、片段／选择范围、范围／章节／FlashCue标记、编辑／清除、导航，以及序列宽高／名称／采样率／混音布局和工作色彩设置。每阶段逐项验证变更、undo、redo与恢复。四个创建／真实重开返工阶段共484次持久序列字段比较；playhead精确断言导航目标，selection等临时字段不计入持久保全。

固定craft.5的 `sequence.inspect` 省略标记comment。首轮验收错误期待查询含comment，原始失败回执和工程摘要保留；最终方案另外保存80个非空标记状态，从原生fcproj逐字段验证评论、名称、颜色、类型、ID、时间与时长。四项oracle测试确认缺少保存证据、评论丢失、非目标一tick变化均被拒绝。

所有29条命令拒绝未知参数，合计58项；空上下文实际禁用的命令另经公开入口拒绝。标记和设置保存后重开，局部返工恢复基线；整个序列与工程逐字段比较。最终next_id仅因一个持久标记分配而精确增加1，这是显式预期，不是删除或归一化字段；其他工程字段仅归一化已知saveAs工程名，原输入和中间输入摘要不变。

`matrix.json` 保留666条各维度状态，`observations.json` 记录语义断言、回执和工程摘要，`session.json` 记录固定PID、启动次数和最终关闭。原始工程和逐步回执在私有目录。QA驱动在main，未修改冻结技能／插件ZIP；不证明source目标、全部参数／适用状态、GUI手势、实际渲染或创作质量。

English:29 disjoint marker/settings commands pass bounded program-target checks in both contexts, reusing one owned session per mode. Four create/reopen-revision phases compare persistent sequence fields484 times. Frozen inspect omits marker comments, so80 actual saved marker-state projects independently verify all metadata; the original verifier assumption failure is retained. Final explicit revision matches the entire baseline project except the expected one-step ID allocator advancement; source inputs remain byte-identical. The union is115 commands, with551 unobserved beyond discovery. Full task8.3 and seven V1 gates remain open; this QA supplement does not alter the frozen ZIP or qualify exhaustive contexts/GUI/creative quality.
