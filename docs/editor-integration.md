# 编辑器接入

实现与构建见 [编辑器指南](../ui/README.md)。新增 [场景技能](scene-skills.md) 为本地候选，未替换已有锁定快照。

本轮规格由目录仓 `full-aigc-plugins/openspec/changes/add-craft-editor-scenes` 持有；本仓已有 OpenSpec 变更保留，不自动归档。

## 最新编辑器与内置回退

宿主与插件之间使用 **stdio MCP**；本地 HTTP 仅承载编辑器页面与页面桥接，不作为远程 MCP 服务。stdio 避免本地工具调用引入 HTTP MCP 服务，但整体编辑速度仍取决于引擎、素材和页面，不宣称未经测量的性能倍数。

首次调用 `open_editor` / `open_browser_editor` 时检查官方最新版本，下载并校验完整 WASM/JS 包。本插件使用 GitHub 最新稳定 Web Release，并通过页面 API 连接当前编辑器。不会下载 CLI 或升级宿主插件。

元数据请求超时 5 秒、归档下载超时 45 秒；HTTP 失败、缺少 SHA-256、摘要不符、异常 ZIP、工具输入契约变化或缓存损坏时使用内置版本。校验通过的下载缓存在 `~/.cache/full-aigc/editors`，可以用 `CRAFT_EDITOR_CACHE_DIR` 指定其他绝对目录。活动会话固定版本，重开页面不重新切换；缓存损坏会回退，不自动删除已有缓存。

`editor_status` 和打开工具结果中的 `runtime` 返回 `source`（download/cache/bundled）、`version`、下载摘要或 `reason`。`version` 对九款 Craft 面板表示面板包版本，不等同于引擎版本。结构与工具 schema 校验不能保证未来上游版本的全部运行行为；升级后的实际编辑需按场景检查。

需要完全离线时，在现有 stdio MCP 配置的 env 中加 `"CRAFT_EDITOR_UPDATE": "off"`，直接使用内置包。更新不修改包内 `ui/dist/editor` 和原来的锁文件；内置版本始终保留。内置资源缺失仍是安装包错误，不能依赖网络掩盖。

## 插件安装与界面

优先通过插件市场安装完整发布包，不需要手工填写每个 MCP 的绝对路径。开发仓必须先构建编辑器资源；仅克隆源码不等于已安装运行包。

| 入口 | 配置 | 路径基准 |
| --- | --- | --- |
| 标准 Agent Plugins | `plugin.json`、`mcp.json` | `${PLUGIN_ROOT}` 由支持该规范的宿主展开 |
| Codex | `.codex-plugin/plugin.json`、`.codex-plugin/mcp.json` | 相对 `cwd` 由宿主定位到插件根目录 |
| Claude Code | `.claude-plugin/plugin.json`、根 `.mcp.json` | `${CLAUDE_PLUGIN_ROOT}` 由宿主展开 |

连接后调用 `open_editor` 或 `open_browser_editor`，显式传入本次任务目录 `workspace`。这是用户文件的位置，不是插件安装位置，不写死在安装清单中。

支持 MCP Apps 的宿主可呈现工具关联的 UI 资源；支持内置浏览器的桌面宿主可打开 `open_browser_editor` 返回的地址。Claude Code 终端本身不提供浏览器面板。支持插件或 stdio MCP 并不自动意味着支持内嵌 UI；缺少 UI 能力时只能在浏览器打开同一会话，不能宣称宿主内嵌已通过。

stdio 负责 Agent 与插件通信，本地 HTTP 负责页面和同会话编辑桥接。Agent 指令作用于当前页面的编辑器状态；等待 `editor_status` 就绪后再执行编辑。保存源工程后重开检查，关闭 MCP 进程前先保存。

本轮优先验证标准插件入口、Codex 和 Claude Code 清单。仅支持 MCP 的工具不属于当前安装交付范围。
