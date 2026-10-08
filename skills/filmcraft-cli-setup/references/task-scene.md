# 安装诊断任务模板

## 输入

平台、Python 版本、固定锁、既有安装位置与错误回执。确认当前授权范围及要保留的非目标内容；从本技能所在目录读取资源。

## 首次任务

示例请求：核验锁定 CLI 的版本和安装摘要。

先检查平台和本技能自己的固定锁；使用本技能 bootstrap 与 cli 入口验证安装和版本。本任务不启动桌面或编辑工程。

```bash
: "${SKILL_DIR:?Set SKILL_DIR to the actually loaded skill directory}"
: "${RUNTIME_HOME:?Set RUNTIME_HOME to an independently authorized runtime directory}"
python3 -I -B "$SKILL_DIR/scripts/bootstrap.py" --runtime-home "$RUNTIME_HOME"
python3 -I -B "$SKILL_DIR/scripts/cli.py" --runtime-home "$RUNTIME_HOME" -- --version
```

核对回执中的固定版本、平台和二进制摘要。损坏既有安装会被拒绝，不覆盖原目录；保留诊断后，在另一个已获授权的新缓存目录安装同一固定版本，再核对摘要。桌面创作属于另一个任务，按需读取 [固定桌面安装](desktop-install.md)。

## 失败

摘要错误、不支持平台或下载失败时保留诊断；不浮动升级。记录实际错误与阶段，结果 unknown 时先检查原工程和回执，不自动重放。安装诊断按需读取 [首次使用诊断](first-use-failures.md)。

## 局部修订

修订请求：安装修复限于已确认损坏的固定版本；保留损坏缓存，在独立授权的新运行时目录安装并核对固定摘要，不编辑用户工程。原目标内复用已有授权，超出范围或授权约束变化才重新确认。

## 核验

版本、二进制摘要和安装位置；安装成功不代表创作通过。技术、创作和用户接受分别记录；缺少的维度标 NOT_RUN/manual_review，文件存在或目录检查不能替代验收。
