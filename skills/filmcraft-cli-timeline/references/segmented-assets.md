# 分段透明动画素材：导入、收集与移动返工

公开工作流支持通过 segmented-image-sequence 登记 Effect 已完成的分段生产检查点，逐段校验并归一成连续的 Film 收集素材，保留原检查点与段摘要。CLI 身份从本技能 runtime.lock.json 和实际安装回执读取；不要使用历史候选版本判断当前是否支持。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" /absolute/plan.json --output /absolute/film --segmented-sequence-asset overlay=/absolute/segments/segments.json
```

SKILL_DIR 来自当前实际加载的 SKILL.md 目录。计划使用已有 asset.import／timeline.place，安装器按技能自身锁安装固定原生 CLI，不依赖兄弟技能。每段仍最多 512 MiB，原 v1 限制不变。缺段、重叠、错位、坏帧及未完成检查点拒绝。

收集后原输入和输出清单摘要不同，交付中 sourceSequenceSha256 保留输入摘要。移动修订消费收集包，文字返工使用新分段输入和新输出目录，保留源工程。固定发行及 Art 联调状态见包内 README 和对应版本验收；历史候选通过不能代替当前输入的检查。

## 时间线与完整素材

计划 document 显式指定与输入一致的有理 frameRate，例如 {"num":24,"den":1}。通过 asset.import 绑定 overlay，再用 timeline.place 放到V2；背景放V1。每秒254016000000 ticks，五秒为1270080000000 ticks。1920×1080、24fps、五秒序列必须保留120帧，不能沿用默认帧率使持续时间缩短。

--segmented-sequence-asset 接收 segments.json；--sequence-asset 接收普通 sequence.json，两者不可互换。交付 assets 中 sourceSequenceSha256 绑定输入检查点，sequenceMetadata 保存归一后的收集合同。收集工程必须包含全部帧，不只保存第一帧。

移动工程后以 --source 指向收集完整的交付目录，核对 expectedProjectSha256；原素材目录断开后仍通过原生重关联打开。替换片头先导入新的分段素材，再用 clip.replaceFromBin 修改首次 timeline.place 保存的剪辑绑定；不猜测clip ID、不重建无关背景或配音。新输出目录保留原工程，独立解码检查成片帧数、帧率、持续时间及透明合成动画。

缺段、重叠、错位、坏帧、摘要冲突或未完成检查点均拒绝，不发布不完整成片。交接给 **artcraft-cli-execute** 技能。安装：`npx skills add full-aigc-skills/artcraft-skills --skill artcraft-cli-execute`。
