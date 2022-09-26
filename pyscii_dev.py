#!/usr/bin/env python3

"""
@file     pyscii.py
@date     25/09/2022
@version  0.9.8_dev
@license  GNU General Public License v2.0
@url      github.com/Julynx/pyscii
@author   Julio Cabria
-------------------------------------------------------------------------------
This version does real time processing of each frame before printing it
instead of preprocessing all the frames and then printing them like the
regular version.

It has a shorter startup time, but it has a bigger load on the CPU while
printing the frames so your device has to have enough power to process the
frames in real time.
"""

import os
import sys
import numpy as np
import time
from PIL import Image, ImageOps


def pixel_to_ascii(brightness) -> str:
    palette = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`\". "[::-1]
    normalized_grayscl = brightness/255
    return palette[int(normalized_grayscl * (len(palette) - 1))]


def main() -> int:

    rt = "\033[1A\033[2K"  # reset line
    rows, cols = os.get_terminal_size()

    # Check input arguments
    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: program <file_name>")
        return 0
    video_name = sys.argv[1]

    # Delete the previous video frames
    os.system("rm -rf /tmp/pyscii-frames")
    os.mkdir("/tmp/pyscii-frames")

    # Detect the video framerate
    cmd = (f"ffprobe -v error -select_streams v:0 -show_entries "
           f"stream=r_frame_rate -of "
           f"default=noprint_wrappers=1:nokey=1 '{video_name}'")
    framerate = os.popen(cmd).read().strip().split("/")
    framerate = int(framerate[0]) / int(framerate[1])

    ##
    # Extract frames from video
    ##
    cmd = (f"ffmpeg -i '{video_name}' -vf scale={rows}:{cols} "
           f"/tmp/pyscii-frames/%d.png")
    print("Processing video...")
    t0 = time.time()
    os.system(cmd + " > /dev/null 2>&1")
    frames = sorted(os.listdir("/tmp/pyscii-frames/"),
                    key=lambda x: int(x.split(".")[0]))
    t1 = time.time()
    print(f"{rt}Processing took {round((t1-t0)*1000, 2)} ms")

    ##
    # Load frames with pillow, grayscale them and make them a numpy array
    # then convert them to ascii and print them
    ##
    vecToAscii = np.vectorize(pixel_to_ascii)
    for frame in frames:

        t0 = time.time()
        image = Image.open(f"/tmp/pyscii-frames/{frame}")
        image = ImageOps.grayscale(image)
        ascii_array = vecToAscii(np.asarray(image))
        frame = "\n".join(["".join(row) for row in ascii_array])
        t1 = time.time()

        print("\n" + frame, end="")
        interval = max(((1/framerate)-(t1 - t0)), 0)
        print("Interval: ", interval)
        time.sleep(interval)

    return 0


if __name__ == "__main__":
    main()
