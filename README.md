# pyscii
A simple and extremely fast python script to turn video into ASCII the right way.

## Why pyscii?
### Easy to use
- Automatically fits the video to your terminal.
- Compatible with virtually all video formats.
- Detects and matches the framerate of the original video.

### Extremely fast
- FFMPEG downscales the input video to the size of your terminal before it is converted to ASCII.
- Video frames are stored as NumPy arrays.
- Function vectorizing allows for a high-performance transformation of these arrays into printable characters.

### Simple and lightweight
- Only uses basic python libraries like NumPy and PIL.
- Video conversion and frame extraction are handled by FFMPEG.
- All this under 130 lines of code.

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
... so you can call pyscii from anywhere like this:
```
pyscii <video.mp4>
```
