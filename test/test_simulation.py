import subprocess
import sys
import time

def test_runs_in_simulation_mode():
    # Run for ~2 seconds and ensure it starts successfully
    proc = subprocess.Popen(
        [sys.executable, "src/app.py"],
        env={**dict(os.environ), "SIMULATE": "1"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(2.0)
    proc.terminate()
    out, _ = proc.communicate(timeout=5)
    assert "[SIMULATION]" in out

