#!/usr/bin/env python3

import os
import sys
from time import perf_counter, sleep
import numpy as np
from PIL import Image


def process_frame(frame_in):

    array = np.asarray(Image.open(f"/tmp/pyscii-frames/{frame_in}"))

    frame_out = "\n".join(
        map("".join,
            [[f'\033[38;2;{p[0]};{p[1]};{p[2]}m\033[48;2;{q[0]};{q[1]};{q[2]}m▀'
              for p, q in zip(array[i], array[i+1])]
             for i in range(0, array.shape[0]-1, 2)]))

    return frame_out


if __name__ == "__main__":

    cols, rows = os.get_terminal_size()

    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: program <file_name>")
        sys.exit(0)

    os.system("rm -rf /tmp/pyscii-frames; mkdir /tmp/pyscii-frames")

    cmd = (f"ffprobe -v error -select_streams v:0 -show_entries "
           f"stream=r_frame_rate -of "
           f"default=noprint_wrappers=1:nokey=1 '{sys.argv[1]}'")

    framerate = os.popen(cmd).read().strip().split("/")
    framerate = int(framerate[0]) / int(framerate[1])

    os.system(f"ffmpeg -i '{sys.argv[1]}' -vf scale={cols}:{2*rows} "
              f"/tmp/pyscii-frames/%d.png > /dev/null 2>&1")

    frames = sorted(os.listdir("/tmp/pyscii-frames/"),
                    key=lambda x: int(x.split(".")[0]))

    for frame in frames:
        t0 = perf_counter()
        print(f"\n{process_frame(frame)}\033[0m", end="", flush=True)
        t1 = perf_counter()
        sleep(max(0, 1/framerate - (t1-t0)))

    os.system("rm -rf /tmp/pyscii-frames")
