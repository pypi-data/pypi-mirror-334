import select
import subprocess
import time

import ipywidgets
from IPython.display import display


# TODO: This work only on Linux
def ICmdRunWithLogTrail(run_cmd, logfile):
    process = subprocess.Popen(f"{run_cmd}", shell=True)
    running = True

    out = ipywidgets.Output(
        layout={"border": "1px solid black", "width": "100%", "height": "360px"}
    )
    display(out)

    out.clear_output()

    tail = subprocess.Popen(
        ["tail", "-f", logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    tail_poll = select.poll()
    tail_poll.register(tail.stdout)

    chunks = 0
    while running:
        res = process.poll()
        running = res is None

        content = ""
        while tail_poll.poll(1):
            data = tail.stdout.readline()
            if data is not None:
                content += data.decode()
                chunks += 1

        if content != "":
            out.append_stdout(content)

        # 100 line buffer
        if chunks > 100:
            chunks = 0
            out.clear_output(wait=True)

        time.sleep(0.5)

    content = ""
    while tail_poll.poll(1):
        data = tail.stdout.readline()
        if data is not None:
            content += data.decode()
            chunks += 1

    if content != "":
        out.append_stdout(content)

    # Kill the tail process
    tail.kill()
    process.communicate()
    return process.returncode
