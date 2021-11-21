# SCAV-P2
Repo to deliver the second lab of the SCAV subject

## Explanation

The p2_main.py file has a set of simple functions that will execute some ffmpeg commands. It can be run as:
```
python3 p2_main.py
```

The functions are the following:
- 1. Cut a provided video in N seconds. Right now it cuts from the start only.
- 2. Extracts the YUV histograms and shows them overlayed on the video.
- 3. Resize the video into 4 resolutions: 720p, 480p, 360p, 160p.
- 4. Change the audio tracks from a video. Change either to mono/stereo, or the codec used (aac, vorbis or mp3).
