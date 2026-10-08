# FilmCraft — artifact-delivery

## Purpose

本能力定义 FilmCraft 在 artifact-delivery 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；回执映射已有源码候选，完整交付合同尚未验收。

## ADDED Requirements

### Requirement: FC-AR-001 产物血缘与包完整性

产物 SHALL 登记逻辑 ID、不可变版本、内容摘要、来源任务、原生工程和依赖；交付前重新校验文件，移动后可按清单重关联。

#### Scenario: FC-AR-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成产物血缘与包完整性并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-AR-001-N 边界条件

- **WHEN** 输出文件被替换但文件名未变
- **THEN** 哈希校验失败并使原验收失效

#### Scenario: FC-AR-001-RECEIPT-LINEAGE 回执关联与公共协议映射

- **WHEN** 一次执行产生命令回执、交付清单、失败阶段记录、输出执行记录或质量评审回执
- **THEN** FilmCraft SHALL 通过显式映射关联 taskId、计划摘要、输入摘要、技能源修订、运行时身份、操作尝试及产物摘要，使每个结论可以回到实际执行及候选产物
- **AND** craft-task/v1 与 craft-artifact/v1 继续由 ArtCraft 持有；FilmCraft 仅定义领域字段与映射，保留既有公开格式，必要的不兼容变更采用显式版本迁移

#### Scenario: FC-AR-001-RECEIPT-MISMATCH 缺失或冲突的回执

- **WHEN** 回执缺失、输入或候选摘要变化，或不同记录的执行身份相互冲突
- **THEN** 系统 SHALL 保留原始记录并报告 unknown、stale 或 conflict，不拼接成完整成功证据
- **AND** 原生工程承担编辑数据事实源、执行账本承担操作状态事实源、质量证据承担评审结论事实源；各回执是关联记录，不新建相互竞争的任务状态权威

#### Scenario: FC-AR-001-LEGACY-MAPPING 旧格式回执与操作尝试关联

- **WHEN** 消费既有 command receipt、filmcraft-delivery/v1、craft-failed-stage/v1 或 filmcraft-output-execution/v1
- **THEN** 领域适配 SHALL 保留原始字节和摘要，以明确算法区分公共规范化计划、Python 命令计划和工作流计划摘要，关联当前账本中的 taskId、attemptId、输入版本、技能源身份和运行时
- **AND** 缺失的旧字段保持 unknown，不补造历史身份；相同种类的冲突回执不得覆盖原记录，跨尝试数据不得拼接；文件内容变化后当前证据标记 stale
- **AND** 领域映射仅使用固定 ArtCraft 公共协议字段，不创建另一套公共 schema；成功命令或关联完整不自动提升技术、创作或用户接受状态

### Requirement: FC-AR-002 原生工程与交换损失

交付 SHALL 同时保留约定的原生工程与导出；工程需重新打开检查，交换中的扁平化、栅格化、字体和效果损失必须显式记录。

#### Scenario: FC-AR-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成原生工程与交换损失并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-AR-002-N 边界条件

- **WHEN** 交换格式不能保留所用效果
- **THEN** 保留原工程，报告损失并阻止未接受的有损替代交付

#### Scenario: 绑定原生工程的交换损失报告

- **WHEN** 生成当前版本原生工程和约定导出
- **THEN** 交付 exchange-loss.json 并由 manifest 文件摘要绑定，记录原生工程、重开检查及每个导出摘要；格式损失、实际结构观察与未验证保真分别使用 lost、observed、unknown
- **AND** 原生工程必须保留，导出仅作 derivative；未知字体和效果保真不得标记已验证，缺失、损坏、身份错配或有损 nativeSubstitute 拒绝技术交付
