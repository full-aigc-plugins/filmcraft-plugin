# FilmCraft 固定快照身份验收

[English](FilmCraft-Fixed-Identity.md)。正式合同为 FC-RL-001-CURRENT-FACTS，对应 [任务 9.6](../openspec/changes/establish-v1-plugin/tasks.md)。完整发行、宿主和创作验收继续按各自规范推进。

## 来源与实现

目标组合为插件 dev.43、技能源 dev.40 / `2eb9e0f169b3cfea1bf810aa0293c51bdbed4177`、CLI craft.4。技能源从实际固定 CLI 重新采集命令目录，修复旧参考二进制摘要；666 行参数及各单技能已有子集保持不变。旧 dev.42 及历史报告仍保留其原 MISMATCH，不改写历史证据。

`scripts/verify_fixed_install.py` 是单 FilmCraft 的安装编排入口：从本地固定标签读取 manifest、技能锁和执行文件摘要，核对公开标签解引用提交，再创建全新 CODEX_HOME、注册仅供本次验证的本地清单并安装公开标签。不修改用户日常插件或配置，不进入正式市场。附注标签比较提交身份，不拿标签对象摘要误作提交。

宿主读取和技能核验复用 ArtCraft 固定协议所有者提交 `09d4ac5b8ff82f8fe819189e4be487b45ab2472b` 内的 verify_codex_host.py 函数；记录该文件摘要，不从所有者可变工作树执行，也不修改其代码。验证真实 app-server 的技能发现、全部技能内容及插件执行文件；名称正确但内容变化仍拒绝。

```bash
python3 -I -B scripts/verify_fixed_install.py --codex "$CODEX_CLI" --authority "$ARTCRAFT_REPOSITORY" --ref v0.1.0-dev.43 --output "$NEW_OUTPUT_DIRECTORY"
python3 -B scripts/current_facts.py --check
```

已有输出拒绝复用。私有安装目录清单只保留在隔离验证目录中；公开报告不包含这些路径。安装后的原始文件保持不变，篡改测试只使用安装副本的独立复制件。

## 验收与状态

[固定身份报告](evidence/filmcraft43-fixed-identity-20261008.json) 分别记录：当前身份一致性、生成结果可重复、单字段篡改拒绝、历史证据不升级，以及实际安装后的公开 CLI/工作流结果。只有上述任务所需证据完成才勾选 9.6。基础验证器已经从公开 dev.42 标签完成 13 技能发现、零加载错误及 18 个执行文件核对，此记录不代替新 dev.43 验收。

源码测试、固定安装、实际宿主发现和模型路由分别报告。发现技能不证明自动路由准确，目录一致不证明逐命令成功，身份 MATCH 不把完整组合的 NOT_PROVEN 改为通过。完整模式/平台、升级回退、预算取消、质量与用户接受及完整 V1 仍开放。
