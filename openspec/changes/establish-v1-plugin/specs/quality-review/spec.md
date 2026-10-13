# FilmCraft — quality-review

## Purpose

本能力定义 FilmCraft 在 quality-review 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前 FC-QA-001/002 八个合同场景已在固定 dev.59/source46/craft.5 的 macOS arm64 隔离 Codex/headless 副本验收：135/135 测试、49 条场景记录，证据见 `docs/evidence/filmcraft59-fixed-quality-revision-20261009/acceptance.json`。原生返工验证限于已支持的速度/时长等受限编译器，创作接受为 manual_review，用户接受及其他平台为 NOT_RUN；完整 V1 尚未完成。

## ADDED Requirements

### Requirement: FC-QA-002 受限局部修订

质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；候选或目标变化使相关旧验收失效；仅超出原授权范围或改变授权约束时要求新的授权。

#### Scenario: FC-QA-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成受限局部修订并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-QA-002-N 边界条件

- **WHEN** 连续修订无改善或达到预算
- **THEN** 停止自动修订，保留最佳可验证版本并报告未解决问题

#### Scenario: FC-QA-002-REVISION-SCOPE 修订范围与非目标保全

- **WHEN** 根据评审问题生成局部修订计划
- **THEN** 计划 SHALL 将问题绑定时间区间、对象或轨道、允许修改的字段及依赖，并核验预期源工程摘要；源工程已变化时拒绝使用过期计划
- **AND** 修订后核对非目标对象与依赖的差异，拒绝越界变更；新候选重新评审，旧候选得分不得直接沿用

#### Scenario: FC-QA-002-BOUNDED-LOOP 停滞停止与已有授权

- **WHEN** 修订达到轮数、失败次数、资源预算或 rubric 定义的无改善阈值
- **THEN** 系统 SHALL 停止自动修订，保存最佳已验证候选及未解决问题；没有已验证候选时如实报告，不把最后版本自动认定为最佳
- **AND** 原目标和授权约束内的局部修订继续复用授权；内容变化使相关质量证据失效，仅超出授权范围或改变授权约束才要求新的授权
