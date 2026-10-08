# dev.53 发行范围

插件 dev.53 锁定已发布技能源 dev.45／2933f2dfe35dbf49fedc1fb54bc792b600a7dedd。13 个技能、666 条命令以及默认 craft.4 运行时身份不变。

该发行包含完成的素材准备任务 9.31：7 场景、18 输入均记录来源、许可、摘要和预期。固定 dev.52 的真实派生 VFR 探针虽保存、导出和完整解码通过，但音频相关性 0.49865 低于 0.98；失败证据继续保留，不能作为媒体验收通过。

独立源仓新增 PCM 采样定位修复候选和隔离构建入口，保留真实间隔与既有维护补丁；3 项 PCM 专项与 43 项 codec 库回归通过。该候选未进入默认安装锁，构建和原生验收须单独核验。详见[固定技能源候选记录](https://github.com/full-aigc-skills/filmcraft-skills/blob/v0.1.0-dev.45/docs/FilmCraft-PCM-Candidate.zh_CN.md)。

OpenSpec 9.32/9.33、50 项完整 V1 任务、其他平台／宿主、全命令及创作／用户接受仍开放。只发布开发预览，不归档规格或加入可安装市场。

发行前补充候选验证：私有 craft.5 构建完成，同一真实派生 VFR 工程导出原生 PCM WAV，独立解码相关性0.999995、偏移0采样，通过0.98阈值。该结果只针对候选及这一PCM输出，不替代固定安装、成片AAC、完整媒体矩阵或其他平台。见[探针](evidence/pcm-candidate-20261009/native-wav-probe.json)与[构建回执](evidence/pcm-candidate-20261009/build-receipt.json)。
