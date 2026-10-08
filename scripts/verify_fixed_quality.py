#!/usr/bin/env python3
"""复用固定安装完整回归，并要求独立原生及真实时序/音频校准证据。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from verify_fixed_resources import verify as resource_verify

REQUIRED = {"actual-native-independent-quality", *["quality-media-" + name for name in (
    "aligned", "shifted", "stereo-clipped", "broken", "missing-audio", "bad-subtitle", "missing-tools")]}


def validate_quality(report):
    if report.get("result") != "PASS" or not report.get("allInstalledFilesUnchanged"):
        raise ValueError("fixed_install_not_qualified")
    rows = {row["scenario"]: row for row in report.get("matrix", [])}
    if not REQUIRED.issubset(rows):
        raise ValueError("quality_matrix_incomplete")
    native = rows["actual-native-independent-quality"]
    result = native["result"]
    if (result["engineeringAcceptance"] != "PASS" or result["technicalAcceptance"] != "PASS"
            or result["creativeAcceptance"] != "manual_review" or result["userAcceptance"] != "NOT_RUN"
            or not native.get("originalProjectPreserved")
            or native["receipt"]["context"]["source"] != "external-process"
            or native["receipt"]["context"]["pid"] <= 0):
        raise ValueError("native_quality_unconfirmed")
    expectations = {"aligned": (None, "PASS"), "shifted": ("avSync", "FAIL"),
                    "stereo-clipped": ("audioClipping", "FAIL"), "broken": ("decode", "FAIL"),
                    "missing-audio": ("audioClipping", "FAIL"), "bad-subtitle": ("subtitleTiming", "FAIL"),
                    "missing-tools": (None, "NOT_RUN")}
    for name, (dimension, status) in expectations.items():
        row = rows["quality-media-" + name]
        value = row["result"]
        actual = value["dimensions"][dimension]["status"] if dimension else value["technicalAcceptance"]
        if (actual != status or value["userAcceptance"] != "NOT_RUN"
                or value["creativeAcceptance"] != "manual_review"
                or (status == "FAIL" and value["decision"] != "blocked")
                or not row.get("files") or not row.get("reviewer", {}).get("implementationSha256")):
            raise ValueError("quality_measurement_unconfirmed")
    return [rows[name] for name in sorted(REQUIRED)]


def verify(host, previous_host, authority, ref, output, python, node, ffmpeg, ffprobe):
    old = os.environ.get("FILMCRAFT_QUALITY_TOOLS")
    os.environ["FILMCRAFT_QUALITY_TOOLS"] = json.dumps({"ffmpeg": str(ffmpeg.resolve(strict=True)), "ffprobe": str(ffprobe.resolve(strict=True))})
    try:
        resource_verify(host, previous_host, authority, ref, output, python, node)
    finally:
        if old is None: os.environ.pop("FILMCRAFT_QUALITY_TOOLS", None)
        else: os.environ["FILMCRAFT_QUALITY_TOOLS"] = old
    output = output.absolute()
    original = (output / "report.json").read_bytes()
    report = json.loads(original)
    quality = validate_quality(report)
    (output / "resource-report.json").write_bytes(original)
    report.update(schema="filmcraft-fixed-quality-acceptance/v1", quality=quality,
                  resourceReportSha256=hashlib.sha256(original).hexdigest(),
                  scope="FC-QA-001 tasks9.22-9.24; independent evidence, generated temporal/audio calibration; creative and user acceptance remain open")
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return {"result": "PASS", "tests": report["testCounts"], "qualityScenarios": len(REQUIRED),
            "reportSha256": hashlib.sha256((output / "report.json").read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["host", "previous-host", "authority", "output", "ffmpeg", "ffprobe"]:
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ["ref", "python", "node"]:
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(**vars(args))))
