# FilmCraft — release-compatibility

## Purpose

本能力定义 FilmCraft 在 release-compatibility 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；已有实现与限定范围证据不等于完整需求验收。

## ADDED Requirements

### Requirement: FC-RL-002 权限与秘密边界

运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。

#### Scenario: FC-RL-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成权限与秘密边界并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-RL-002-N 边界条件

- **WHEN** 素材元数据包含额外命令或路径越界请求
- **THEN** 作为数据处理并拒绝越权执行，日志不泄露秘密

#### Scenario: FC-RL-002-PLAN-FIELDS 计划扩展字段不得进入交付

- **WHEN** 不可信工作流 JSON 在顶层或操作对象加入未定义字段，包括元数据中的指令或凭据值
- **THEN** 公开入口 SHALL 在素材读取、运行时安装、原生执行及输出创建前拒绝，返回固定错误代码，不回显字段名或值
- **AND** 顶层仅接受既有 document、assets、operations、frames、export、expectedProjectSha256、requires；操作对象仅接受 command、params、as；既有完整命令计划入口提示保持兼容
- **AND** 原生参数、用户创作文本、宿主秘密引用和读取／写入根授权分别验证，不把该字段边界修复当作完整权限与秘密验收。


#### Scenario: FC-RL-002-DOMAIN-PARAMETERS 领域包装操作拒绝未定义参数

- **WHEN** 不可信领域工作流在既有包装操作的 params 或 timeline.move.moves 对象中加入未定义字段
- **THEN** 公开入口 SHALL 在素材读取、运行时安装及输出创建前拒绝，返回固定 invalid_workflow_parameters，不回显未知字段名称或值
- **AND** 原有静态增益、运动与 LUT 专项参数错误保持兼容；既有参数、结果引用和字幕中的创作文本仍按数据处理，不通过关键词过滤删除用户文本
- **AND** native.command 的完整注册表参数、可信素材／输出根与宿主秘密引用仍须独立验收，不能由包装操作字段校验替代。

#### Scenario: FC-RL-002-TRUSTED-ROOTS 可信授权根与原生进程隔离

- **WHEN** 宿主提交领域工作流并提供独立可信的读取／写入根目录策略
- **THEN** 读取素材、源交付和计划前 SHALL 验证其授权根，根目录身份进入执行授权主体；改变或扩大根目录需要新的精确宿主授权，计划或素材元数据不得授予目录权限
- **AND** 原生子进程 SHALL 受到同一目录边界限制，不能借完整注册表命令读取根外素材或写入根外工程；平台不支持可靠隔离时明确拒绝，不降级为无隔离成功
- **AND** 安装器和运行时／模型缓存的维护授权与原生编辑写入授权分离；原生编辑不得修改已锁定运行时或技能目录。

#### Scenario: FC-RL-002-CHILD-ENV 执行进程不得继承宿主秘密

- **WHEN** 宿主环境包含未提供给本地编辑任务的凭据、代理秘密或额外解释器注入变量
- **THEN** 原生编辑及其辅助进程 SHALL 仅接收明确允许的运行环境，不继承宿主全部环境、秘密值或解释器注入项
- **AND** 本地原生剪辑不要求云端密钥；有凭据需求的新能力须单独定义宿主秘密引用消费合同，不能通过计划中的字面密钥或额外环境字段绕过。

#### Scenario: FC-RL-002-MAINTENANCE-ROOTS 维护探测权限独立绑定

- **WHEN** 宿主请求运行时安装／升级能力探测或使用探测回执切换运行时
- **THEN** 维护入口 SHALL 要求独立可信的读取／写入根，在计划读取与授权查询之前拒绝缺失策略或越界计划／缓存路径；规范化根摘要进入探测及切换授权主体
- **AND** 固定安装器仅在对应精确维护授权通过后运行；原生能力探测继续使用目录沙箱，保护技能、固定运行时及显式模型缓存，维护授权不得扩大原生编辑写入范围
- **AND** 根策略扩张、撤销或探测期间身份变化需重新授权；只读主题计算不得安装、创建许可或修改账本。
- **AND** 候选描述、计划、探测回执和账本的读取 SHALL 在打开或解析前检查可信读取根；激活／回滚 SHALL 在读取探测回执及查询授权前检查账本写入根。只读主题与探测允许读取已授权但不可写的账本，不得因此获得切换权限。

#### Scenario: FC-RL-002-READONLY-MODELS 显式模型缓存不被覆盖

- **WHEN** 宿主通过独立运行环境指定现有本地模型目录并将其纳入可信读取根
- **THEN** 完整命令入口和所属桌面及其MCP客户端 SHALL 消费同一显式模型目录，不用空的输出配置目录覆盖它，也不把读取授权扩大为模型下载／维护写入授权
- **AND** 越界或畸形模型引用在安装、素材摘要读取及输出创建前拒绝；原生编辑沙箱保护该显式模型目录，临时截图与其他输出仍落在独立授权写入目录
- **AND** 无显式模型目录时保留本次私有数据目录；真实缓存推理、模型摘要保全和缺失模型拒绝分别验收，禁止以目录存在代替推理成功。

#### Scenario: FC-RL-002-RAW-LAUNCHER 原生转发入口同等隔离

- **WHEN** 宿主使用独立技能的 cli.py 公开入口读取工程、执行原生命令或启动原生会话
- **THEN** 入口 SHALL 在安装及工程读取前要求独立可信读写根，原生执行使用同一目录沙箱并保护技能、固定运行时、源工程和显式模型缓存；子进程仅接收允许的运行环境
- **AND** 仅精确 --version、help、commands、commands --json 四种无工程发现形式可保留无编辑根兼容；追加 --project、数据路径或其他参数不享有豁免
- **AND** 模型维护 SHALL 使用独立 --model-maintenance 标志，仅接受 exec transcript.downloadModel、唯一合法 model 字段和显式 --data-dir；数据目录须已存在且具有独立写入授权，不得位于技能、运行时或解释器目录
- **AND** 模型维护原生进程仅可写该数据目录，使用独立限定网络出站权限；普通编辑不获得该权限，维护入口不得组合工程或编辑参数。既有损坏安装诊断、原错误及未知结果不重放语义保持兼容。

#### Scenario: FC-RL-002-REGISTRY-PARAMETERS 完整命令参数不接受未定义字段

- **WHEN** 不可信完整命令计划、领域 native.command 或 cli.py exec 的注册表命令 params 含有未在固定原生参数合同定义的顶层字段
- **THEN** 公开入口 SHALL 在素材读取、运行时安装、原生执行及输出创建前拒绝，返回固定 invalid_native_parameters，不回显字段名称或值，也不写入计划／执行回执
- **AND** 校验覆盖全部666个固定注册表命令，准确处理原生别名、联合参数及已有匹配选项；合法字幕、路径和创作文本按数据保留，不通过秘密关键词过滤替代合同校验
- **AND** 解析后的参数容器及结果引用继续满足既有验证，不能用本项顶层字段校验替代嵌套类型、目录沙箱、宿主秘密引用或全命令上下文验收。

## Implementation evidence (non-normative)

`docs/evidence/codex-current-release.json` binds current fixed releases to two actual Codex CLI/app-server versions, five enabled namespaced skills, installed public workflow outcomes and explicit exclusions. The corresponding bilingual Host-Verification-Architecture documents specify the repeatable check.
