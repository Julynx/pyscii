#!/usr/bin/env python3

import os
import sys
import numpy as np
import time
from PIL import Image, ImageOps


def pixel_to_ascii(brightness) -> str:
    palette = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`\". "[::-1]
    return palette[int((brightness/255) * (len(palette) - 1))]


if __name__ == "__main__":

    rows, cols = os.get_terminal_size()
    vecToAscii = np.vectorize(pixel_to_ascii)

    # Check input arguments
    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: program <file_name>")
        exit(0)
    video_name = sys.argv[1]

    # Delete the previous video frames
    os.system("rm -rf /tmp/pyscii-frames; mkdir /tmp/pyscii-frames")

    # Detect the video framerate
    cmd = (f"ffprobe -v error -select_streams v:0 -show_entries "
           f"stream=r_frame_rate -of "
           f"default=noprint_wrappers=1:nokey=1 '{video_name}'")

    framerate = os.popen(cmd).read().strip().split("/")
    framerate = int(framerate[0]) / int(framerate[1])

    # Extract frames from video
    cmd = (f"ffmpeg -i '{video_name}' -vf scale={rows}:{cols} "
           f"/tmp/pyscii-frames/%d.png")

    os.system(cmd + " > /dev/null 2>&1")
    frames = sorted(os.listdir("/tmp/pyscii-frames/"),
                    key=lambda x: int(x.split(".")[0]))

    # Main loop
    for frame in frames:

        t0 = time.time()

        # Load frame with pillow, grayscale it and make it a numpy array
        image = Image.open(f"/tmp/pyscii-frames/{frame}")
        array = np.asarray(ImageOps.grayscale(image))

        # Convert the numpy array to a string
        frame = "\n".join(["".join(row) for row in vecToAscii(array)])

        t1 = time.time()

        print("\n" + frame, end="")
        time.sleep(max(((1 / framerate) - (t1 - t0)), 0))

    # Cleanup and exit
    os.system("rm -rf /tmp/pyscii-frames")
    exit(0)
