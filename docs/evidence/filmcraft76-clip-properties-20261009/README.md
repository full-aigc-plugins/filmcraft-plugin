# 固定76片段属性验收

新增15条命令：重命名、速度／倒放、启用、帧保持选项／添加帧保持、场选项、三种时间插值及通用插值设置、音频增益、缩放标志、分组／取消分组与关联。与既有115条不重叠，合计130条有界观察，536条在此证据集中仅发现。

两个模式各使用一个所属实例。每阶段75个原生保存工程，共300次完整工程比较；逐项验证变更、undo、redo和恢复，且组合属性实际保存重开后显式修订回基线。仅归一化已知saveAs工程名，目标字段之外的效果、轨道、片段、素材、设置和ID分配器均保持精确比较。分组分配／恢复、关联双端变化、默认字段省略、精确速度时长、帧保持和源输入摘要分别断言。

首轮75个独立检查点通过，但组合倒放后holdOn=in的预期错误。倒放入点应保持最后消费源帧，按 `(source_in+source_duration-1)` 向下对齐帧边界；固定原生结果与该时间语义一致。原回执和工程摘要保留，最终驱动修正断言后完整复验，不是产品修复。

30项未知参数在输出／启动前拒绝，28项实际空上下文禁用命令经公开入口拒绝。六个原生WAV以独立FFmpeg／ffprobe解码，逐文件比较全部24000个双声道样本：-3dB倍率、量化容差、RMS误差及恢复样本完全一致。该测量不启动FilmCraft。

`matrix.json` 为逐命令维度矩阵，`observations.json` 为语义／回执／工程摘要，`session.json` 为固定PID／启动次数／最终清理，`pcm.json` 为独立输出测量。完整原始工程及WAV在私有目录。五项oracle测试拒绝保持滤镜丢失、非目标一tick变化、增益／插值错误及意外ID推进；插件Python104项通过。

这只证明有界属性、持久化与指定音频输出，未证明光流或场处理的视频算法、全部参数／资源／适用上下文、GUI手势或创作质量。QA驱动在main，冻结技能与ZIP未改变。完整任务8.3和七项V1门禁保持开放。

English:15 disjoint clip-property commands pass bounded headless and owned signed-desktop checks, one session per mode.300 complete native project checkpoints assert target changes, undo/redo, allocator/link/group/default semantics and non-target preservation. Combined properties persist through actual reopen and explicit revision restores the entire baseline project. Six native WAV outputs independently prove -3dB gain over all stereo samples and exact restored PCM. The first combined reverse-frame-hold oracle mistake is retained and corrected using last-consumed-source-frame semantics. The union is130 commands,536 unobserved beyond discovery; optical-flow/field-processing video algorithms, exhaustive contexts, GUI/creative and seven full V1 gates remain open.
