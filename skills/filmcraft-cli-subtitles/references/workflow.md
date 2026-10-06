# 原生剪辑计划 / Native editing plans

`workflow.py` 是可独立安装的剪辑入口。它自动安装锁定的 CLI，在持续 MCP 会话中导入、编排、添加字幕，调用原生 Project Manager 收集素材，再重新打开 `.fcproj`、渲染预览并导出 H.264。运行入口只依赖 Python 3.11+ 和自动安装的 CLI；当前支持 macOS arm64。

The helper bootstraps the pinned CLI, imports and arranges media in a persistent MCP session, adds captions, collects dependencies using the native Project Manager, reopens the native project, renders previews and exports H.264. The helper requires Python 3.11+ and the automatically installed CLI; runtime support currently covers macOS arm64.

## 从已有素材制作短片 / Create from existing media

示例为 320×180、12 fps、两秒短片；输入镜头与配音均须至少两秒。实际任务应调整尺寸、帧率、素材入出点、字幕和预览时刻。

The example produces a two-second 320×180 film at 12 fps. Input footage and voice audio must be at least two seconds long. Adjust the plan to the actual request.

以下 `SKILL_DIR` 沿用本技能 `SKILL.md` 的实际加载目录，脚本和示例均来自同一技能。

```bash
python3 "$SKILL_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/short-film.json" \
  --asset shot=/absolute/path/shot.mp4 \
  --asset voice=/absolute/path/voice.wav \
  --output /absolute/path/film-v1
```

替换技能根为当前已加载技能的真实绝对位置。`--asset name=path` 计算输入摘要；也可在 JSON 的 `assets` 中提供 `path` 和 `sha256`。助手复制素材到隔离工作目录，复制前后均检查摘要。它使用已有声音，不生成声音或上传素材。

Replace the skill root with its actual loaded location. `--asset` computes input digests; alternatively provide `assets` entries with `path` and `sha256`. Assets are checked before and after copying. This workflow uses existing audio and does not generate voices or upload media.

## 精确时间 / Exact timing

每秒 `254016000000` ticks。`time`、`sourceIn`、`duration` 和 `frames` 以十进制字符串传递；不使用浮点数表示长时间线。`document.frameRate` 为 `{"num":12,"den":1}`，建立序列后核对原生时间基准；无法精确保留时停止。

One second equals `254016000000` ticks. Time, source-in, duration and frame samples use decimal strings. The frame rate is rational and is checked against the native sequence after creation.

`asset.import` 的 `as` 返回 `{item: ID}`；`timeline.place` 返回 `{clips: [ID]}`。`{"$ref":"shot.item"}` 与 `{"$ref":"shotClip.clips"}` 引用实际返回值。字幕通过 `caption.add` 的 `startTicks`、`durationTicks` 指定时间，样式使用受支持的 `captions.setStyle`。源素材越界、字幕越界、缺少字体均停止交付。

Import and placement aliases reference native item and clip IDs. Caption timing uses `startTicks` and `durationTicks`; supported native caption commands control styling. Out-of-range clips or captions and missing fonts stop delivery.

## 局部修改与素材移动 / Revisions and relocation

静态音轨增益可使用 `mixer.setStrip`，参数严格为 `{"strip":"A1","volumeDb":-6.0}`；支持 A1、A2 等明确音轨和有限分贝数值。此入口不支持总线、路由、录音或自动化字段。另存修订后解码成片音频核对实际幅度，不能只检查命令返回成功。

For static track gain, use `mixer.setStrip` with exactly `{"strip":"A1","volumeDb":-6.0}`. Explicit audio tracks and finite decibel values are supported. Bus, routing, recording and automation fields are rejected. Decode the exported movie to verify the actual amplitude after saving a revision.

使用 `--source /absolute/path/film-v1`，把该包 `manifest.json` 中 `files["project.fcproj"]` 写入新计划的 `expectedProjectSha256`。省略 `document`，输出到新的目录。示例替换镜头：

```json
{
  "expectedProjectSha256": "COPY_PRIOR_PROJECT_DIGEST",
  "operations": [
    {"command":"asset.import","params":{"asset":"replacement"},"as":"replacement"},
    {"command":"clip.replaceFromBin","params":{"clips":{"$ref":"shotClip.clips"},"item":{"$ref":"replacement.item"}}}
  ],
  "frames":["127008000000","381024000000"],
  "export":{"audioRequired":true}
}
```

通过 `--asset replacement=/absolute/path/new-shot.mp4` 提供新素材。修改前重新核对原工程摘要；不覆盖原工程。收集后的工程使用原生绝对路径。移动交付包后，通过同一 `--source` 入口验证包内素材摘要并执行原生 `media.relink`，即可恢复引用；直接在其他位置打开旧文件的 GUI 自动重关联未验收。

Pass the replacement asset with `--asset`. The previous project stays unchanged. Collected projects contain native absolute media paths. After moving a delivery folder, this workflow verifies packaged media hashes and performs native relinking. Automatic GUI relinking has not been verified.

## 成功与失败 / Success and failure

成功包包含 `.fcproj`、引用素材、字幕 SRT、PNG 预览、MP4、原生检查结果、操作记录、导出流检查和摘要清单。正式输出由 FilmCraft 原生引擎完成，随后用同一个 CLI 检查流信息并解码视频。测试另用 ffprobe、ffmpeg 和 Pillow 核对视频帧数、音频同步及字幕像素；这些工具不是助手运行依赖。

A successful delivery contains the editable project, referenced assets, SRT, PNG previews, MP4, inspection snapshots, operation records and a hashed manifest. Native export is checked and video-decoded by the same CLI. Tests additionally use ffprobe, ffmpeg and Pillow for stream, synchronization and pixel checks.

输出目录必须不存在。原生素材收集使用最终目录保存稳定引用；收集或导出失败时，目录保留 `failure.json` 和诊断材料，没有成功清单。不能把失败目录当作成片交付，也不能盲目覆盖；修正后使用新目录重试。摘要冲突、缺素材及时间越界等预检错误不会创建输出目录。

The output directory must not exist. Native collection targets the final directory to preserve stable references. Collection or export failure retains diagnostic files and `failure.json` without a success manifest. Use a new output directory after correcting the failure. Preflight conflicts and invalid media or timing do not create a delivery directory.

当前未覆盖完整 Harness 的任务账本、恢复状态机、宿主安装、更多导出格式和真实创意质量验收。技术测试通过不能代替这些验收。

The full Harness ledger, recovery state machine, plugin-host installation, additional export formats and creative review remain separate acceptance work.

有可见字幕轨时默认传入 `burnCaptions=true`，避免预览有字幕而成片遗漏。`export.burnCaptions=false` 显式选择仅工程/侧车字幕；两个导出布尔标志都拒绝字符串和数字。

## 必需音轨门禁 / Required source audio

默认 audioRequired 为 true。成功交付同时要求原生时间线中的音频片段引用具有音频流的已登记素材，以及导出音频流存在。导出器自动生成的静音 AAC 流不能代替源音轨。失败返回 export_audio_missing，保留原生工程、电影、预览、audio-check.json、export-probe.json 和 failure.json，不写成功 manifest，也不覆盖失败目录重试。

有意无声的视频必须明确设置 audioRequired 为 false。用户提供的静音 WAV 具有真实源音轨，可以正常通过；本门禁不以波形幅度为零拒绝素材。audio-check.json 随成功 manifest 摘要保存，也在失败目录保留用于诊断。

By default audioRequired is true. A native timeline audio clip must reference registered media containing an audio stream, and the exported movie must contain an audio stream. Automatically generated silent AAC is insufficient. Failure returns export_audio_missing, retains the native project/movie/preview plus audio-check.json, export-probe.json and failure.json, and publishes no success manifest. Use a fresh output for retries. Explicitly set audioRequired false for video-only delivery; an intentional silent WAV remains valid source audio.

## 动画序列合同候选 / Animated sequence contract candidate

序列登记使用 `assets.<alias> = {"kind":"image-sequence","path":"/absolute/path/sequence.json","sha256":"<清单摘要>"}`，或 `--sequence-asset <alias>=/absolute/path/sequence.json`。不能只登记首帧。清单采用 `craft-image-sequence/v1`；校验全部帧、真实 RGBA 像素、帧率与时间基。工作流按原生序列导入，读取原生属性核对时长与通道，收集全部帧和清单，并在移目录后以包内首帧重关联，保留原生类型和帧率。交付 `manifest.json.files` 包含嵌套帧依赖；`assets.<alias>.path` 指向包内 `sequence.json`。

当前是工作流候选，依赖带帧率、整段收集与序列重关联修复的维护版 CLI。公开固定安装锁尚未升级，旧 CLI 不支持时必须拒绝而不能静默降为图片。公开发行、冷安装和 Art 混合联调仍待验收。

Register a sequence with `kind: image-sequence`, the absolute `sequence.json` path and its SHA-256, or `--sequence-asset alias=/absolute/path/sequence.json`. Registering only the first frame is insufficient. The workflow verifies the complete RGBA frame set and rational timebase, imports a native sequence, checks actual native media properties, collects every frame and the manifest, and relinks from packaged frames after relocation. Nested frame hashes are included in delivery `files`; the asset path points to the packaged manifest.

This candidate needs the maintained CLI with explicit rate, complete collection and sequence relinking fixes. The public installer lock is unchanged. An unsupported native CLI must fail instead of treating the sequence as a still. Fixed release, cold installation and Art mixed acceptance remain open.
