import subprocess
import tempfile
import os
import sys
import threading
from typing import Dict, Any
import resource

def _limit_resources():
    try:
        resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
        resource.setrlimit(resource.RLIMIT_CPU, (60, 120))
        resource.setrlimit(resource.RLIMIT_NOFILE, (32, 64))
    except Exception:
        pass

def run_script(script_text: str, timeout: int = 120) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "generated_task.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script_text)
        cmd = [sys.executable, path]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=td, text=True, preexec_fn=_limit_resources)
        timer = threading.Timer(timeout, proc.kill)
        timed_out = False
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            rc = proc.returncode
        finally:
            timer.cancel()
            if proc.returncode is None:
                proc.kill()
                timed_out = True
                rc = -9
        return {"exit_code": rc, "stdout": stdout, "stderr": stderr, "timed_out": timed_out}
