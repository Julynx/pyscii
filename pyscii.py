#!/usr/bin/env python3

"""
@file     pyscii.py
@date     24/09/2022
@version  0.9.3
@license  GNU General Public License v2.0
@url      github.com/Julynx/pyscii
@author   Julio Cabria
"""

import os
import sys
import numpy as np
import time
from PIL import Image, ImageOps


def pixel_to_ascii(brightness) -> str:
    palette = ("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvun"
               "xrjft/\|()1{}[]?-_+~i!lI;:,\"^`\". "[::-1])
    normalized_grayscl = brightness/255
    return palette[int(normalized_grayscl * (len(palette) - 1))]


def main() -> int:

    rt = "\033[1A\033[2K"  # reset line
    rows, cols = os.get_terminal_size()

    # Check input arguments
    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: program <file_name>")
        return 0
    else:
        video_name = sys.argv[1]

    # Delete the previous video frames if the folder exists
    if os.path.exists("/tmp/pyscii-frames"):
        os.system("rm -rf /tmp/pyscii-frames")
    os.mkdir("/tmp/pyscii-frames")

    # Detect the video framerate
    cmd = (f"ffprobe -v error -select_streams v:0 -show_entries "
           f"stream=r_frame_rate -of "
           f"default=noprint_wrappers=1:nokey=1 {video_name}")
    framerate = os.popen(cmd).read().strip().split("/")
    framerate = int(framerate[0]) / int(framerate[1])

    ##
    # Extract frames from video
    ##
    cmd = (f"ffmpeg -i {video_name} -vf scale={rows}:{cols} "
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
    ##
    t0 = time.time()
    i_arrays = []
    for i, frame in enumerate(frames):
        print("Loading frame {}/{}".format(i+1, len(frames)))
        print(f"{rt}", end="")

        image = Image.open(f"/tmp/pyscii-frames/{frame}")
        image = ImageOps.grayscale(image)
        i_array = np.asarray(image)

        i_arrays.append(i_array)
    t1 = time.time()
    print(f"Loading took {round((t1-t0)*1000, 2)} ms")

    ##
    # Transform each element of each numpy array into a character
    ##
    t0 = time.time()
    ii_arrays = []
    vecToAscii = np.vectorize(pixel_to_ascii)
    for i, i_array in enumerate(i_arrays):
        print("Transforming frame {}/{}".format(i+1, len(frames)))
        print(f"{rt}", end="")
        ii_array = vecToAscii(i_array)
        ii_arrays.append(ii_array)
    t1 = time.time()
    print(f"Transforming took {round((t1-t0)*1000, 2)} ms")

    ##
    # Transform each numpy array into a string
    ##
    t0 = time.time()
    frame_buffer = []
    for i, ii_array in enumerate(ii_arrays):
        print("Generating frame {}/{}".format(i+1, len(frames)))
        print(f"{rt}", end="")
        frame = "\n".join(["".join(row) for row in ii_array])
        frame_buffer.append(frame)
    t1 = time.time()
    print(f"Generating took {round((t1-t0)*1000, 2)} ms")

    ##
    # Print each string as a frame
    ##
    for frame in frame_buffer:
        print("\n" + frame, end="")
        time.sleep(1/framerate)

    return 0


if __name__ == "__main__":
    main()
