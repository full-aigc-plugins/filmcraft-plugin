#!/usr/bin/env python3
"""在新的评审进程测量冻结作品；不读取生成器聊天/自评，不评价审美或用户接受。"""
import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def finding(status, reason, evidence=None, **metrics):
    value = {"status": status, "reason": reason, "evidence": evidence or []}
    if metrics:
        value["metrics"] = metrics
    return value


def run(argv, limit=64 * 1024 * 1024):
    # 输出写到受限私有文件而非无界管道；到达上限/超时不能当完整测量。
    def bounded():
        import resource
        resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))
    try:
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                    timeout=20, check=False, preexec_fn=bounded if sys.platform != "win32" else None)
            out.seek(0); err.seek(0)
            data, diagnostics = out.read(limit + 1), err.read(min(limit, 16384))
            if len(data) >= limit or result.returncode < 0:
                return None, b"", "measurement_limit_or_signal"
            return result.returncode, data, diagnostics.decode("utf-8", "replace")
    except (OSError, subprocess.TimeoutExpired):
        return None, b"", "measurement_unavailable_or_timeout"


def caption_times(path, duration):
    def milliseconds(value):
        hours, minutes, seconds, fraction = map(int, re.split(r"[:,]", value))
        return ((hours * 60 + minutes) * 60 + seconds) * 1000 + fraction
    matches = re.findall(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})", path.read_text())
    if not matches:
        return finding("NOT_RUN", "No readable subtitle cue timestamps; manual subtitle review required")
    cues = [(milliseconds(start), milliseconds(end)) for start, end in matches]
    valid = all(0 <= start < end <= duration * 1000 + 100 for start, end in cues)
    valid = valid and all(cues[i][0] >= cues[i - 1][0] for i in range(1, len(cues)))
    return finding("PASS" if valid else "FAIL", "Subtitle sidecar timing bounds; burned-in readability is not measured",
                   ["captions.srt", "full-video-pts"], cueCount=len(cues), cuesMs=cues)


def onset_events(values, threshold, rate, minimum_gap):
    result, active, last = [], False, -1e9
    for index, value in enumerate(values):
        present = value > threshold
        time = index / rate
        if present and not active and time - last >= minimum_gap:
            result.append(time); last = time
        active = present
    return result


def measure(request, artifacts, tools):
    dimensions = {name: finding("manual_review", "Independent temporal/creative review is required")
                  for name in ("subtitleReadability", "continuity", "rhythm")}
    dimensions.update({name: finding("NOT_RUN", "Required independent media evidence is unavailable")
                       for name in ("decode", "videoTiming", "audioClipping", "avSync", "subtitleTiming")})
    capabilities = []
    engineering = finding("NOT_RUN", "Independent native reopen tool unavailable")
    native = tools.get("native")
    if native:
        code, data, _ = run([native, "--project", str(artifacts / "project.fcproj"), "inspect"])
        if code == 0:
            try:
                value = json.loads(data)
                if not isinstance(value.get("sequence"), dict) or not isinstance(value["sequence"].get("settings"), dict):
                    raise ValueError("native inspect shape")
                engineering = finding("PASS", "Independent pinned native project reopen succeeded", ["native-inspect"],
                                      inspectionSha256=hashlib.sha256(data).hexdigest())
                capabilities.append("native-reopen")
            except (ValueError, KeyError, TypeError):
                engineering = finding("FAIL", "Native inspect did not return a valid reopened sequence", ["native-inspect"])
        elif code is not None:
            engineering = finding("FAIL", "Independent native project reopen failed", ["native-inspect"])
    ffmpeg, ffprobe = tools.get("ffmpeg"), tools.get("ffprobe")
    movie = artifacts / "film.mp4"
    if not ffmpeg or not ffprobe or not movie.is_file():
        return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}
    base = [ffmpeg, "-v", "error", "-nostdin", "-protocol_whitelist", "file,pipe"]
    code, _, _ = run(base + ["-xerror", "-i", str(movie), "-map", "0:v:0", "-map", "0:a?", "-f", "null", "-"])
    if code is None:
        dimensions["decode"] = finding("NOT_RUN", "Full decode was unavailable or exceeded measurement bounds")
        return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}
    if code != 0:
        dimensions["decode"] = finding("FAIL", "Full video/audio decode failed", ["ffmpeg-full-decode"])
        return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}
    probe_base = [ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe"]
    code, raw, _ = run(probe_base + ["-show_streams", "-show_format", "-of", "json", str(movie)], 8 * 1024 * 1024)
    if code != 0:
        return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}
    try:
        probe = json.loads(raw)
        videos = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        audio = [stream for stream in probe["streams"] if stream["codec_type"] == "audio"]
        duration = float(probe["format"]["duration"])
        if not videos or not math.isfinite(duration) or duration <= 0:
            raise ValueError("video metadata")
    except (ValueError, KeyError, TypeError):
        return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}
    dimensions["decode"] = finding("PASS", "Full video/audio stream decode completed", ["ffmpeg-full-decode"], durationSeconds=duration)
    code, raw, _ = run(probe_base + ["-select_streams", "v:0", "-show_frames", "-show_entries",
                                   "frame=best_effort_timestamp_time", "-of", "json", str(movie)], 16 * 1024 * 1024)
    pts = []
    if code == 0:
        try:
            pts = [float(frame["best_effort_timestamp_time"]) for frame in json.loads(raw)["frames"]]
            if not all(math.isfinite(value) for value in pts):
                raise ValueError("nonfinite pts")
        except (ValueError, KeyError, TypeError):
            pts = []
    if len(pts) > 1:
        capabilities.append("full-video")
        steps = [second - first for first, second in zip(pts, pts[1:])]
        valid = all(step > 0 for step in steps)
        expected = request["criteria"]["goal"].get("expectedDurationMs")
        if expected is not None:
            valid = valid and abs(duration * 1000 - expected) <= max(steps) * 1000 + 1
        dimensions["videoTiming"] = finding("PASS" if valid else "FAIL", "Decoded presentation timestamps and requested duration",
                                            ["full-video-pts"], frames=len(pts), firstPts=pts[0], lastPts=pts[-1], durationSeconds=duration)
    else:
        capabilities.append("static-frame")
        dimensions["videoTiming"] = finding("NOT_RUN", "Complete multi-frame timestamps were not obtained")
    if (artifacts / "captions.srt").is_file():
        dimensions["subtitleTiming"] = caption_times(artifacts / "captions.srt", duration)
        capabilities.append("caption-timeline")
    pcm = array.array("f")
    channels = 1
    thresholds = request["criteria"]["rubric"]["thresholds"]
    measurements = []
    complete_audio = bool(audio)
    for index, stream in enumerate(audio):
        stream_channels = stream.get("channels")
        if not isinstance(stream_channels, int) or not 1 <= stream_channels <= 64:
            complete_audio = False
            continue
        code, raw, _ = run(base + ["-i", str(movie), "-map", f"0:a:{index}", "-ar", "48000", "-f", "f32le", "-"])
        if code != 0 or not raw or len(raw) % (4 * stream_channels):
            complete_audio = False
            continue
        decoded = array.array("f")
        decoded.frombytes(raw)
        if sys.byteorder != "little":
            decoded.byteswap()
        if not all(math.isfinite(value) for value in decoded):
            complete_audio = False
            continue
        # 逐声道测量，避免相反相位在 mono 下混后抵消削波；也检查每条音轨。
        fractions = [sum(abs(value) >= thresholds["clippingAmplitude"] for value in decoded[channel::stream_channels])
                     / (len(decoded) // stream_channels) for channel in range(stream_channels)]
        measurements.append({"stream": index, "channels": stream_channels, "peak": max(abs(value) for value in decoded),
                             "clippedFractions": fractions, "samplesPerChannel": len(decoded) // stream_channels})
        if index == 0:
            pcm, channels = decoded, stream_channels
    clipped = any(max(row["clippedFractions"]) > thresholds["clippingFraction"] for row in measurements)
    if clipped or complete_audio:
        if complete_audio:
            capabilities.append("decoded-audio")
        dimensions["audioClipping"] = finding("FAIL" if clipped else "PASS",
                                              "Per-channel PCM clipping across every audio stream", ["decoded-audio-pcm"],
                                              streams=measurements, sampleRate=48000)
    elif not audio and request["criteria"]["goal"]["audioRequired"]:
        dimensions["audioClipping"] = finding("FAIL", "Required audio stream is absent", ["full-media-stream-inventory"])
    markers = request["criteria"]["goal"].get("syncMarkers")
    if markers and pts and pcm:
        code, gray, _ = run(base + ["-i", str(movie), "-map", "0:v:0", "-vf", "scale=16:16,format=gray", "-fps_mode", "passthrough", "-f", "rawvideo", "-"])
        if code == 0 and len(gray) == len(pts) * 256:
            brightness = [sum(gray[start:start + 256]) / (256 * 255) for start in range(0, len(gray), 256)]
            visual = [pts[index] for index, value in enumerate(brightness) if value > 0.8 and (index == 0 or brightness[index - 1] <= 0.8)]
            # 10ms窗口的最大幅度检出脉冲包络，避免把每个正弦过零当新事件。
            envelope = [max(abs(value) for value in pcm[start:start + 480 * channels]) for start in range(0, len(pcm), 480 * channels)]
            audible = onset_events(envelope, 0.1, 100, 0.1)
            audio_start = float(audio[0].get("start_time", 0))
            audible = [value + audio_start for value in audible]
            capabilities.append("content-sync")
            count = markers["expectedEvents"]
            errors = [abs(a - v) * 1000 for a, v in zip(audible, visual)]
            valid = len(audible) == len(visual) == count and max(errors, default=1e9) <= thresholds["syncToleranceMs"]
            dimensions["avSync"] = finding("PASS" if valid else "FAIL", "Explicit flash/pulse calibration markers; not general lip-sync or music judgment",
                                           ["full-video-flash-onsets", "decoded-audio-pulse-onsets"], visualSeconds=visual, audioSeconds=audible,
                                           errorsMs=errors, expectedEvents=count)
    return {"engineering": engineering, "dimensions": dimensions, "evidenceCapabilities": capabilities}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("request", "artifacts", "tools"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    request_bytes = args.request.read_bytes()
    request = json.loads(request_bytes)
    result = measure(request, args.artifacts, json.loads(args.tools.read_text()))
    print(json.dumps({"schema": "filmcraft-review-assessment/v1", "requestSha256": hashlib.sha256(request_bytes.removesuffix(b"\n")).hexdigest(),
                      "assessment": result}, ensure_ascii=False, allow_nan=False))
