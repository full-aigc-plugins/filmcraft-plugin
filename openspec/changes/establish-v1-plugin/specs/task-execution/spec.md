# FilmCraft — task-execution

## Purpose

本能力定义 FilmCraft 在 task-execution 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；同目标执行保护已有源码候选，完整任务合同尚未验收。

## ADDED Requirements

### Requirement: FC-TX-001 版本绑定与单写

执行 SHALL 绑定 planHash、inputHashes、projectRevision、runtimeIdentity 和有效授权范围；同一工程只有一个写入者，冲突不得覆盖用户修改。

#### Scenario: FC-TX-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成版本绑定与单写并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-TX-001-N 边界条件

- **WHEN** 用户在 GUI 中修改工程后提交旧计划
- **THEN** 返回 revision_conflict 并重新检查工程，不覆盖新修改

#### Scenario: FC-TX-001-OUTPUT 独立工作流同目标竞争

- **WHEN** 两个独立公开工作流请求同一个规范化输出路径
- **THEN** 安装完整性核验后、原生会话启动前 SHALL 对目标登记独占执行身份，记录计划、素材、源工程及运行时摘要；竞争者返回 output_execution_conflict，不启动第二个原生会话
- **AND** 不同输出路径互不阻塞，已有用户目录不被认领或修改

#### Scenario: FC-TX-001-INTERRUPT 执行所有者中断

- **WHEN** 独占执行登记后所有者异常退出或被终止，无法确认全部原生任务已停止
- **THEN** 持久化身份 SHALL 保留 running／reconciling，后续同目标返回 output_execution_reconciling；不得仅因操作系统文件锁已释放而重新执行
- **AND** 不自动删除登记或失败工程；完成停止证据和原产物检查后才能另行明确授权修订，此增量不宣称自动接管、完整幂等或预算实现


### Requirement: FC-TX-002 幂等与不明确结果恢复

任务 SHALL 在副作用前登记幂等键；超时且执行结果未知时进入 reconciling；核对原任务或产物前不得重新提交。

#### Scenario: FC-TX-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成幂等与不明确结果恢复并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-TX-002-N 边界条件

- **WHEN** 提交后断线且无法确定是否执行
- **THEN** 保存任务身份并核对已有结果，不增加重复写入或付费提交

### Requirement: FC-TX-003 取消与预算边界

任务 SHALL 区分 cancel_requested 与 cancelled；父子调用共享预算和截止时间；只允许一个层级负责同一副作用的重试。

#### Scenario: FC-TX-003-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成取消与预算边界并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-TX-003-N 边界条件

- **WHEN** 父任务取消但子渲染仍在运行
- **THEN** 保留占用并停止新依赖调度，确认停止后才标记 cancelled

### Requirement: FC-TX-004 公开工作流失败工程保留

公开工作流 SHALL 在已开始的暂存执行失败时保留原位置的原生工程、依赖素材及已完成回执；失败目录 SHALL 记录原异常、暂存路径、文件摘要及禁止自动重放。结果未知时 SHALL 标为 outcome_unknown，不作为成功交付。验证前置失败不创建恢复目录，已有用户输出不覆盖。成功交付仍执行既有重开和输出验收。

#### Scenario: FC-TX-004-P 保存后响应未知

- **WHEN** 原生保存完成后响应畸形或工具结构无效
- **THEN** 同一暂存位置的工程与依赖保留，摘要可核对并可用新会话打开
- **AND** 失败记录不提升为成功、不重放保存或继续下游编辑

#### Scenario: FC-TX-004-N 已有用户目录

- **WHEN** 目标输出已经存在或执行期间出现其他用户目录
- **THEN** 用户目录不被失败记录覆盖，原始异常继续返回，暂存恢复位置独立保留

#### Scenario: FC-TX-004-C 正常交付

- **WHEN** 全部原生操作、重开和输出检查成功
- **THEN** 交付保持既有格式与目录语义，不残留失败暂存
