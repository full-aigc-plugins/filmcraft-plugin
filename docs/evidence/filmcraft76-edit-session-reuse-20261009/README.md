# 固定76编辑、音量与批量会话复用证据

固定插件76／技能源57新增44条编辑、导航、选择与撤销重做命令的双上下文有界验证，与既有42条不重叠；合计86条，另580条在此证据集中仅有发现记录。完整任务8.3仍未完成。

- `edits/`：逐命令矩阵、完整序列断言、保存重开／返工和非目标保全，88个真实空上下文拒绝。
- `targets/`：既有27条命令完整复验的报告与54项负向检查共享会话证明。
- `pcm/`：八条音量命令的20个原生WAV，使用独立FFmpeg／ffprobe验证全部双声道样本、dB倍率及恢复后样本相同。
- `session.json`：真实进程PID、启动次数、耗时及最终关闭结果。27项或44项负向检查各共享一个所属会话；bridge各共享一个签名桌面和一个MCP连接。

改造前每个负向用例独立启动一次。改造后四批142项只启动四个MCP会话，其中两批bridge合计两个桌面实例。每项仍经固定安装公开命令入口验证；仅明确的禁用拒绝允许继续，未知或异常结果停止，不重启重放。

QA脚本位于main，不在不可变76发布ZIP内。创建、重开、返工阶段仍使用独立会话；此次不声称提供通用交互会话API。未验证GUI手势、创作质量、全部参数和上下文适用性，也不关闭宿主／权限完整资格。

复验使用 `scripts/verify_installed_timeline_edits.py` 与 `scripts/verify_installed_target_commands.py` 的固定安装、运行时、版本SHA和新输出目录参数；PCM驱动另需时间线证据目录及FFmpeg／ffprobe。原始工程、逐步回执及媒体保留于私有验收目录，公共记录只含摘要和语义断言。报告绑定当前驱动摘要；历史逐项启动证据不被覆盖。

English: Fixed plugin76/source57 adds bounded observations for44 distinct commands, bringing the union to86;580 remain unobserved beyond discovery. Four owned empty-context batches run142 negative checks using four MCP processes and two signed bridge desktop processes. Actual PID stability and final cleanup are recorded. Eight volume commands additionally have20 native WAV outputs checked sample by sample with independent FFmpeg. This QA-only change is outside the frozen release ZIP. Positive create/reopen/revision phases still use separate sessions; exhaustive contexts, GUI gestures, creative acceptance and full host/permission qualification remain open.
