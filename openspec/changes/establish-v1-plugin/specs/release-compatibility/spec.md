# FilmCraft — release-compatibility

## Purpose

本能力定义 FilmCraft 在 release-compatibility 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；已有实现与限定范围证据不等于完整需求验收。

## ADDED Requirements

### Requirement: FC-RL-001 宿主与发布证据

发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。

#### Scenario: FC-RL-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成宿主与发布证据并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-RL-001-N 边界条件

- **WHEN** 只有 OpenSpec 校验与文档检查通过
- **THEN** 状态保持 documentation-baseline，所有实现任务仍未完成

#### Scenario: FC-RL-001-CURRENT-FACTS 当前身份与历史证据分离

- **WHEN** 生成当前技能数量、版本、能力状态与发行说明
- **THEN** 当前事实 SHALL 从 manifest、技能锁、有效运行时锁及场景清单的明确映射生成并检查一致性；明确历史根运行时锁与当前技能源运行时锁、桌面身份的不同用途
- **AND** 历史报告保留原版本及结果，不改写为当前验收；中英文当前事实一致，NOT_RUN 和失败不得因版本升级被转为通过

#### Scenario: FC-RL-001-LAYERED-CI 源码与固定发行分层验证

- **WHEN** 独立技能源或插件提交进入验证和发行流程
- **THEN** 源仓 SHALL 验证离线单元、场景、链接、资源同步、命令契约与入口一致性；插件 SHALL 验证固定源完整性、元数据和协议映射；固定安装副本 SHALL 独立完成冷启动、原生交付及适用宿主和模式验收
- **AND** 不以 package.json 是否存在等条件静默跳过必需检查；缺环境时显式记录 NOT_RUN；TRACE 结构分数、fixture、源码测试、CI、真实媒体、宿主和目标平台结果分别报告

#### Scenario: FC-RL-001-OPTIMIZATION-TRACE 优化场景与验收记录可追溯

- **WHEN** 报告 Dreamina 对照优化的完成情况或据此判断固定组合可发布
- **THEN** 每组优化 SHALL 映射到本变更既有需求、具体场景和任务；验收记录包含执行层级、源码及候选内容身份、固定技能源与插件身份、运行时、平台/模式、输入摘要、预期/实际结果和日志引用
- **AND** 每个必需场景分别记录 PASS、FAIL 或 NOT_RUN，不以整体测试数量掩盖缺失场景；非适用维度说明原因，文档校验及参考仓结果不得提升为 FilmCraft 行为通过

### Requirement: FC-RL-002 权限与秘密边界

运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。

#### Scenario: FC-RL-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成权限与秘密边界并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-RL-002-N 边界条件

- **WHEN** 素材元数据包含额外命令或路径越界请求
- **THEN** 作为数据处理并拒绝越权执行，日志不泄露秘密

## Implementation evidence (non-normative)

`docs/evidence/codex-current-release.json` binds current fixed releases to two actual Codex CLI/app-server versions, five enabled namespaced skills, installed public workflow outcomes and explicit exclusions. The corresponding bilingual Host-Verification-Architecture documents specify the repeatable check. RL-001 tasks remain unchecked until their full P0 prerequisites and scenarios pass.
