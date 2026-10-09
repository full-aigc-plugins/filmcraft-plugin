# 固定 dev.76 读取根与默认临时目录补证

`report.json` 绑定不可变插件提交、源 dev.57、发布 ZIP 和实际安装副本。`read-boundaries.json` 保留 494 项逐例结果，其中 390 项实际 macOS 公开入口拒绝，104 项是先导入标准依赖再覆盖 `sys.platform` 的 Linux／Windows 分支模拟，不能作为目标系统执行验收。

复验读取根：

```sh
python3 -I -B scripts/verify_installed_read_boundaries.py --installed-plugin <fixed-installed-plugin> --output <fresh-private-output>
```

输出目录必须尚不存在；脚本使用自有畸形／软链接夹具，验证拒绝发生在安装和输出创建前，且原输入摘要不变、根外路径不回显。两轮夹具失败的驱动与日志摘要保留于报告，不归类为产品失败。

默认临时目录下 13 项目标测试，以及真实原生只读账本探测／拒绝激活、精确授权激活、扩根／撤销授权拒绝均通过。原生驱动继承的 candidate／NOT_RUN 标签原样保留，本层报告绑定实际固定 dev.76 安装目标。旧 SQLite I/O 失败仍由前一证据报告保存，根因未知；本次未修改产品代码，不推断磁盘空间与失败存在因果关系。

本补证生产脚本属于 main，未写入不可变 dev.76 ZIP；完整权限、秘密引用消费者、全命令上下文及宿主资格仍未通过，七项完整 V1 任务保持开放。
