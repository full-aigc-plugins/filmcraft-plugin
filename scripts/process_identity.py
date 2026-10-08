"""只读获取内核进程出生身份，供 POSIX 本任务取消门禁使用。"""
import ctypes
import json
import os
from pathlib import Path
import sys


def identity(pid):
    if sys.platform.startswith("linux"):
        proc = Path("/proc") / str(pid)
        value = (proc / "stat").read_text().rsplit(")", 1)[1].split()
        return {"pid": pid, "ppid": int(value[1]), "pgid": int(value[2]),
                "uid": proc.stat().st_uid, "started": value[19],
                "boot": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
                "executable": os.readlink(proc / "exe")}
    if sys.platform == "darwin":
        class BsdInfo(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint32) for name in (
                "flags", "status", "xstatus", "pid", "ppid", "uid", "gid",
                "ruid", "rgid", "svuid", "svgid", "rfu")]
            _fields_ += [("comm", ctypes.c_char * 16), ("name", ctypes.c_char * 32)]
            _fields_ += [(name, ctypes.c_uint32) for name in (
                "nfiles", "pgid", "pjobc", "e_tdev", "e_tpgid", "nice")]
            _fields_ += [("start_sec", ctypes.c_uint64), ("start_usec", ctypes.c_uint64)]
        lib = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
        info = BsdInfo()
        lib.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
        result = lib.proc_pidinfo(pid, 3, 0, ctypes.byref(info), ctypes.sizeof(info))
        if result != ctypes.sizeof(info) or info.pid != pid:
            raise OSError("process identity unavailable")
        buffer = ctypes.create_string_buffer(4096)
        lib.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
        if lib.proc_pidpath(pid, buffer, len(buffer)) <= 0:
            raise OSError("process path unavailable")
        # boottime 保证重启后的相同 PID/starttime 也不能匹配。
        import subprocess
        boot = subprocess.run(["/usr/sbin/sysctl", "-n", "kern.boottime"], check=True,
                              capture_output=True, text=True, timeout=2).stdout.strip()
        return {"pid": pid, "ppid": info.ppid, "pgid": info.pgid, "uid": info.uid,
                "started": f"{info.start_sec}.{info.start_usec:06d}", "boot": boot,
                "executable": buffer.value.decode("utf-8")}
    raise OSError("unsupported process identity platform")


if __name__ == "__main__":
    try:
        print(json.dumps(identity(int(sys.argv[1]))))
    except (OSError, ValueError, IndexError):
        print(json.dumps({"status": "unknown"}))
        sys.exit(1)
