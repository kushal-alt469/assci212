# ASCII Art Video Player

Simple script that converts video frames to ASCII art and plays them in the terminal.

Requirements
- Python 3.8+ (3.13 tested)
- See `requirements.txt` (opencv-python, numpy)

Install

1. Create a virtual environment (recommended):

```pwsh
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Run

Interactive mode (prompts for path/width/fps):

```pwsh
python index.py
```

Non-interactive (pass video path as argument):

```pwsh
python index.py "path\to\video.mp4"
```

Color and testing options

- Print ASCII in green:

```pwsh
python index.py .\vid.mp4 --color green
```

- Stop after N frames (useful for testing):

```pwsh
python index.py .\vid.mp4 --max-frames 10
```

Notes
- On Windows the terminal will be cleared with `cls` between frames.
- If performance is slow, reduce `width` when prompted.
