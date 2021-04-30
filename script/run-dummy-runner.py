import os
import re
import select
import signal
import subprocess
import sys
import time

# Constants
MAX_TIMEOUT_SEC = 20
EXPECTED_MESSAGE = "Listening for Jobs"
DUMMY_RUNNER_COMMAND = ["./run.sh"]

def run_and_watch() -> int:
    """
    Run dummy runner and watch it's connected to Github server.
    If it's not connected until the timeout, it returns non-zero.
    """

    with subprocess.Popen(DUMMY_RUNNER_COMMAND, stdout=subprocess.PIPE, bufsize=0, preexec_fn=os.setsid) as p:
        start = time.time()
        poller = select.poll()
        poller.register(p.stdout, select.POLLIN)

        try:
            while True:
                if poller.poll(1):
                    line = p.stdout.readline().decode("UTF-8")
                    m = re.search(EXPECTED_MESSAGE, line)
                    if m:
                        print("Runner connected to GitHub.")
                        return 0

                time.sleep(1)
                if (time.time() - start) > MAX_TIMEOUT_SEC:
                    print(f"Runner failed to start. (Timeout={MAX_TIMEOUT_SEC})")
                    return 1
        finally:
            # NOTE: Need to stop runner (Withou this, the main process hangs)
            print(f"Stopping runner")
            # NOTE: Need to kill children via pgid/sid.
            pgrp = os.getpgid(p.pid)
            os.killpg(pgrp, signal.SIGTERM)
            p.terminate()
            p.wait(1)


if __name__ == "__main__":
    ret = run_and_watch()
    sys.exit(ret)