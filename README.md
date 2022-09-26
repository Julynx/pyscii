# pyscii
A simple and extremely fast python script to turn video into ASCII the right way.

![Alt Text](https://i.imgur.com/G2uqxQo.png)

## Why pyscii?
### Easy to use
- Automatically fits the video to your terminal.
- Compatible with virtually all video formats.
- Detects and matches the framerate of the original video.

### Lightning speed
- FFMPEG downscales the input video to the size of your terminal before it is converted to ASCII.
- Video frames are stored as NumPy arrays.
- Function vectorizing allows for a high-performance transformation of these arrays into printable characters.

### Simple and lightweight
- Only uses basic python libraries like NumPy and PIL.
- Video conversion and frame extraction are efficiently handled by FFMPEG.
- All this under 120 lines of code.

## Dependencies
To install the required dependencies numpy and Pillow, run:
```
pip3 install numpy, Pillow
```
Then, make sure you have FFMPEG installed by running the command specific to your linux distribution. 
For Ubuntu:
```
sudo apt install ffmpeg
```

## Usage
From the downloaded folder:
```
python3 pyscii.py <video.mp4>
```
Or you can also ...
```
sudo mv pyscii.py /usr/bin/pyscii
sudo chmod +x /usr/bin/pyscii
```
... so you can call [pyscii](https://github.com/Julynx/pyscii) from anywhere like this:
```
pyscii <video.mp4>
```

## Versions
### pyscii.py

The recommended version is [pyscii.py](https://raw.githubusercontent.com/Julynx/pyscii/main/pyscii.py).
It transforms each frame into ASCII and starts printing them once they are all ready.
It ensures videos with a high framerate will play smoothly, even in low-end hardware, but it has an increased loading time.

### pyscii_dev.py

This alternative version, [pyscii_dev.py](https://raw.githubusercontent.com/Julynx/pyscii/main/pyscii_dev.py), processes each frame before printing and measures this computing time. It uses this information and the input video framerate to produce a constant output. It will significantly reduce loading times while increasing CPU usage while printing. It will only perform smoothly if you have a powerful enough device.
