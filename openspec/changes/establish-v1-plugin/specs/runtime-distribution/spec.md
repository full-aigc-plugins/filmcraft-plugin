# FilmCraft — runtime-distribution

## Purpose

本能力定义 FilmCraft 在 runtime-distribution 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前实现与验收状态以 tasks 和逐场景证据为准。

## ADDED Requirements

### Requirement: FC-RT-001 运行时来源与完整性

运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。

#### Scenario: FC-RT-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行时来源与完整性并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-RT-001-N 边界条件

- **WHEN** 下载内容与锁定摘要不符
- **THEN** 拒绝安装且现有运行时仍可使用

#### Scenario: 并行首次安装与复用
- **WHEN** 两个进程同时安装或复用同一锁定 CLI
- **THEN** 安装互斥等待最多 120 秒，取得锁后核验并复用已原子发布的版本；不存在重复下载或部分安装被运行
- **AND** 超时返回 runtime_install_busy，保留已有安装，不自动重放任何编辑或渲染

#### Scenario: FC-RT-001-RECEIPT 已有安装回执绑定

- **WHEN** 首次安装后再次使用锁定 CLI，安装回执缺失、损坏或其版本、平台、来源及制品摘要与当前锁不符
- **THEN** 系统 SHALL 拒绝复用并报告安装回执错误，不下载、不运行或覆盖现有 CLI；现有文件保持可检查
- **AND** 有效回执 SHALL 与固定版本、平台、制品摘要和来源匹配；说明性证据字段不作为安装身份

### Requirement: FC-RT-002 运行能力与隔离升级

适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。

#### Scenario: FC-RT-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行能力与隔离升级并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: FC-RT-002-N 边界条件

- **WHEN** 新运行时缺少计划要求的能力
- **THEN** 执行前报 capability_missing，禁止静默替换工具


#### Scenario: [FC-RT-002-DOWNLOAD-RECOVERY] 原生制品下载的临时中断

- **WHEN** 首用下载锁定原生CLI制品发生SSL EOF、超时、连接中断、短读或408／429／5xx
- **THEN** 安装器 SHALL 丢弃半包并最多执行三次只读下载，之后仍执行原摘要／安全解压／版本检查，不重试原生编辑
- **AND** 证书、权限、磁盘、大小限制、摘要及非临时HTTP拒绝错误 SHALL 不被重试或放宽；固定发行及安装首用另行验收

#### Scenario: FC-RT-002-CAPABILITY-SNAPSHOT 运行能力快照

- **WHEN** 执行器为某计划完成运行时探测
- **THEN** 快照 SHALL 绑定实际 CLI 版本及二进制摘要、命令目录和可获得的参数契约摘要、headless 或 bridge 模式、平台，以及使用 bridge 时的桌面二进制身份
- **AND** 记录计划所需编解码器、模型和字体的实际探测结果；未探测或无法确认的项保持 unknown，不以命令 ID 存在或 enabled 标志证明可执行

#### Scenario: FC-RT-002-CONTRACT-DRIFT 参数契约与执行上下文漂移

- **WHEN** 版本、命令参数类型或必填约束、原生模式、平台或必要资源与受验组合不同
- **THEN** 系统 SHALL 阻止依赖已知不兼容能力的副作用并报告差异；无法判定的前置条件 SHALL 保持 blocked 或 unknown，等待补齐证据
- **AND** 不将 JSON 风格字符串臆造为完整 JSON Schema；静态目录、正负执行、保存重开、非目标保全、平台及模式的验证状态分别记录，旧组合证据不得自动覆盖新组合

#### Scenario: FC-RT-002-PLAN-REQUIRES 计划前置能力声明

- **WHEN** 命令计划或领域工作流声明可选的顶层 requires 对象
- **THEN** 系统 SHALL 在安装或输出写入前验证声明结构；允许声明 mode、platform、runtimeVersion、runtimeSha256、desktopSha256、parametersSha256 及 resources，资源项仅声明 kind 为 codec、model 或 font 的 name，不接受调用者提供的可用状态
- **AND** 未声明 requires 的既有有效计划保持兼容，但仍执行必要的实时命令契约和资源检查；领域工作流仅支持 headless；bridge SHALL 核验桌面版本和二进制摘要，无法确认桌面身份时阻止依赖编辑
- **AND** 实际快照与声明不一致时报告差异并阻止受影响副作用；声明本身不证明任何能力已通过验收

#### Scenario: FC-RT-002-RESOURCE-PROBE 资源发现与实际使用分离

- **WHEN** 计划声明必要资源，或某操作在引用解析后确定所需编解码器、字体或转录模型
- **THEN** 系统 SHALL 在同一原生执行上下文中，通过已核对契约的只读 export.formats、fonts.list 或 transcript.models 查询探测，并在依赖副作用前检查结果；查询不存在、失败或结果结构无法确认时保持 unknown
- **AND** 模型出现在目录中不等于已安装；发现字体或编码器不等于显示、推理或导出验收通过；显式模型安装成功后的后续操作 SHALL 使用更新后的探测结果，不复用安装前的缺失结论
- **AND** 探测不自动安装模型、修改字体或替换编码器；缺失或 unknown 阻止受影响操作，失败阶段保留快照和探测证据，不泄露无关本地路径；命令目录之后发生契约漂移时，后续依赖调用仍须拒绝

### Requirement: FC-DS-001 Owned standalone desktop workflow
Each domain skill SHALL offer `desktop.py run PLAN --output NEW_DIRECTORY` that validates the plan before installation, verifies fixed desktop and CLI identities, starts only its own isolated desktop, confirms the loopback listener belongs to that process, executes the existing full-command bridge gateway, and closes only its owned desktop/MCP processes on success or failure. Photo authentication SHALL use a private token file and the same authorized output root in both desktop and CLI. Unknown editing outcomes SHALL not be replayed.

#### Scenario: First use without a running desktop
- **WHEN** a standalone skill runs a valid plan against empty runtime caches
- **THEN** fixed desktop and CLI are installed, an owned bridge is started and the workflow receipt plus desktop lifecycle receipt are preserved

#### Scenario: Invalid plan or startup failure
- **WHEN** the plan is invalid
- **THEN** no installation or desktop launch occurs
- **WHEN** owned desktop startup or MCP initialization fails
- **THEN** only owned processes are closed, logs and failure receipts are retained, and edits are not retried

#### Scenario: Interrupted command is not replayed
- **WHEN** a standalone desktop workflow is interrupted with an editing request started
- **THEN** completed steps remain preserved, the started request becomes unknown, and failure plus owned-process lifecycle receipts are written before exit code 130

#### Scenario: Ambiguous JSON plan
- **WHEN** a plan contains duplicate object keys or nonfinite numeric values
- **THEN** the runner rejects it before installing or starting a desktop

#### Scenario: Workflow metadata cannot be overwritten
- **WHEN** a command plan names desktop-session.json, desktop.log, .desktop-data or artcraft-domain-command.json as a root deliverable through $output
- **THEN** validation rejects the plan before installation or editing, preserving workflow receipts and owned desktop configuration

#### Scenario: Bounded TLS download recovery
- **WHEN** a pinned desktop download fails with curl TLS handshake exit35
- **THEN** the installer retries at most three total attempts with clean private downloads and bounded connection/request timeouts before any desktop starts
- **AND** other failure classes are propagated without an extra outer retry; archive identity and signature checks remain mandatory
