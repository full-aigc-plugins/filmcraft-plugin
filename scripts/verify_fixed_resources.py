#!/usr/bin/env python3
"""执行固定安装的完整恢复/原生回归，额外验证预算取消矩阵；不把源码测试当宿主验收。"""
import argparse
import hashlib
import json
from pathlib import Path

from verify_fixed_recovery import verify as recovery_verify

REQUIRED = {"budget-restart-unknown", "budget-disk-shortage", "budget-parent-child",
            "budget-reservation-owner-killed", "actual-budget-cancel-confirmed",
            "budget-cancel-unsupported", "budget-cancel-pid-reuse", "budget-cancel-reply-lost",
            "budget-parent-cancel-live-child", "budget-host-exited-child-alive",
            "actual-native-budget-and-cancellation"}
REQUIRED.update("budget-limit-" + name for name in ("timeMs", "diskBytes", "outputBytes", "slots", "revisions"))


def validate_resources(report):
    if report.get("result") != "PASS" or not report.get("allInstalledFilesUnchanged"):
        raise ValueError("fixed_install_not_qualified")
    rows = report.get("matrix", [])
    if not REQUIRED.issubset({row.get("scenario") for row in rows}):
        raise ValueError("resource_matrix_incomplete")
    resource = report.get("native", {}).get("resources", {})
    if (resource.get("schemaVersion") != 4 or resource.get("sharedScope") != resource.get("parentTaskId")
            or resource.get("parentTaskId") == resource.get("childTaskId")):
        raise ValueError("resource_scope_mismatch")
    reservations = resource.get("reservations", [])
    if (len(reservations) != 2 or {row.get("task_id") for row in reservations}
            != {resource["parentTaskId"], resource["childTaskId"]}
            or any(row.get("scope_id") != resource["sharedScope"] or row.get("state") != "settled" for row in reservations)):
        raise ValueError("resource_reservation_mismatch")
    child = next(row for row in reservations if row["task_id"] == resource["childTaskId"])
    if json.loads(child["allocation"])["revisions"] != 1:
        raise ValueError("resource_revision_charge_missing")
    output = resource.get("outputLimit", {})
    if (output.get("state") != "failed" or output.get("reason") != "budget_output_exceeded"
            or output.get("bytes", 0) <= 1 or output.get("dependencyAttempts") != 0
            or output.get("partialProjectPreserved") is not True):
        raise ValueError("resource_output_limit_unproven")
    cancellation = resource.get("cancellation", {})
    if (cancellation.get("state") != "cancelled" or cancellation.get("attempts") != 1
            or cancellation.get("stopped") is not True
            or cancellation.get("authorization") != "actual private host LocalAuthorizationStore"):
        raise ValueError("native_cancellation_unconfirmed")
    return resource


def verify(host, previous_host, authority, ref, output, python, node):
    recovery_verify(host, previous_host, authority, ref, output, python, node)
    output = output.absolute()
    original = (output / "report.json").read_bytes()
    report = json.loads(original)
    resource = validate_resources(report)
    (output / "recovery-report.json").write_bytes(original)
    report.update(schema="filmcraft-fixed-resource-acceptance/v1",
                  scope="FC-TX-003 tasks9.19-9.21; POSIX identity-bound Python runner, durable shared budgets and cancellation; not full V1",
                  recoveryReportSha256=hashlib.sha256(original).hexdigest(), resources=resource)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return {"result": "PASS", "tests": report["testCounts"], "resourceScenarios": len(REQUIRED),
            "reportSha256": hashlib.sha256((output / "report.json").read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["host", "previous-host", "authority", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ["ref", "python", "node"]:
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.host, args.previous_host, args.authority, args.ref, args.output, args.python, args.node)))
