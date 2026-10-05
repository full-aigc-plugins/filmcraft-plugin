# 原生剪辑计划 / Native editing plans

`workflow.py` 是可独立安装的剪辑入口。它自动安装锁定的官方 CLI，在持续 MCP 会话中导入、编排、添加字幕，调用原生 Project Manager 收集素材，再重新打开 `.fcproj`、渲染预览并导出 H.264。运行入口只依赖 Python 3.11+ 和自动安装的 CLI；当前支持 macOS arm64。

The helper bootstraps the pinned official CLI, imports and arranges media in a persistent MCP session, adds captions, collects dependencies using the native Project Manager, reopens the native project, renders previews and exports H.264. The helper requires Python 3.11+ and the automatically installed CLI; runtime support currently covers macOS arm64.

## 从已有素材制作短片 / Create from existing media

示例为 320×180、12 fps、两秒短片；输入镜头与配音均须至少两秒。实际任务应调整尺寸、帧率、素材入出点、字幕和预览时刻。

The example produces a two-second 320×180 film at 12 fps. Input footage and voice audio must be at least two seconds long. Adjust the plan to the actual request.

```bash
python3 /mnt/skills/user/filmcraft-cli-audio/scripts/workflow.py \
  /mnt/skills/user/filmcraft-cli-audio/examples/short-film.json \
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
