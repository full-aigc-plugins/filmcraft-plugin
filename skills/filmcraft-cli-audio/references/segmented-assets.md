# 分段素材消费候选

此工作区候选尚未进入固定 Film 源 dev.10／插件 dev.11。公开工作流可通过 segmented-image-sequence 登记 Effect verified 生产检查点，逐段校验并归一成连续的 Film 收集素材，保留原检查点与段摘要。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" /absolute/plan.json --output /absolute/film --segmented-sequence-asset overlay=/absolute/segments/segments.json
```

SKILL_DIR 来自当前实际加载的 SKILL.md 目录。计划使用已有 asset.import／timeline.place，安装器按技能自身锁安装固定原生 CLI，不依赖兄弟技能。每段仍最多 512 MiB，原 v1 限制不变。缺段、重叠、错位、坏帧及未完成检查点拒绝。

收集后原输入和输出清单摘要不同，交付中 sourceSequenceSha256 保留输入摘要。移动修订消费收集包，文字返工使用新分段输入和新输出目录，保留源工程。完整长片头、固定发行及 Art 消费仍待验收。
