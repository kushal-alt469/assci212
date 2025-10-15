import cv2
import os
import time
import numpy as np

# colorama will be imported at runtime only when color output is requested.
# Provide safe no-op fallbacks so the rest of the module can reference
# `Fore` and `Style` without requiring colorama to be installed.
COLORAMA_AVAILABLE = False
def colorama_init():
    return None
class _DummyColor:
    GREEN = ''
class _DummyStyle:
    RESET_ALL = ''
Fore = _DummyColor()
Style = _DummyStyle()

def convert_frame_to_ascii(frame, width=80):
    """
    Convert a frame to ASCII art using a character set based on brightness
    """

    ascii_chars = ".:-=+*#%@"
    
    height = int(frame.shape[0] * width / frame.shape[1] / 2) 
    if height == 0:
        height = 1
        
    resized_frame = cv2.resize(frame, (width, height))

    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    
    normalized = gray_frame / 255.0
    ascii_frame = ""
    
    for row in normalized:
        for pixel in row:
            index = int(pixel * (len(ascii_chars) - 1)) 
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    return ascii_frame

def play_video_in_terminal(video_path, width=80, fps=30):
    """
    Play Ser Harwin Strong a video in the terminal using ASCII characters
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    cap = cv2.VideoCapture(video_path)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / video_fps if video_fps > 0 else 1.0 / fps
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_art = convert_frame_to_ascii(frame, width)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)

            time.sleep(frame_delay)

    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")

    finally:
        cap.release()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play a video as ASCII art in the terminal")
    parser.add_argument('video', nargs='?', help='Path to video file')
    parser.add_argument('--width', '-w', type=int, default=None, help='Terminal width for ASCII art (default: 80)')
    parser.add_argument('--fps', type=int, default=0, help='Playback FPS override (default: use video FPS)')
    parser.add_argument('--color', choices=['green', 'none'], default='none', help='Print ASCII in color (green)')
    parser.add_argument('--max-frames', type=int, default=0, help='Stop after N frames (0 = unlimited)')
    args = parser.parse_args()

    video_path = args.video

    # If no video path provided on command line, fall back to interactive prompt
    if not video_path:
        try:
            video_path = input("Enter the path to the video file: ").strip()
        except EOFError:
            print("No video path provided. Exiting.")
            raise SystemExit(1)

    if not video_path:
        print("No video path provided. Exiting.")
        raise SystemExit(1)

    # Width fallback
    if args.width is not None:
        width = args.width
    else:
        try:
            width = int(input("Enter terminal width (default 80): ") or "80")
        except Exception:
            width = 80

    # FPS fallback
    fps = args.fps
    if fps < 0:
        fps = 0

    # Initialize colorama for Windows ANSI support if requested
    color = args.color
    if color != 'none':
        try:
            # import colorama at runtime using importlib to avoid static imports
            import importlib
            _col = importlib.import_module('colorama')
            _colorama_init = getattr(_col, 'init')
            _RealFore = getattr(_col, 'Fore')
            _RealStyle = getattr(_col, 'Style')
            _colorama_init()
            # assign module-level Fore/Style to the real ones
            Fore = _RealFore
            Style = _RealStyle
        except Exception:
            # if import/init fails, fall back to the no-op Fore/Style defined above
            pass

    # If max_frames provided, wrap the player to stop after N frames
    max_frames = args.max_frames

    if max_frames and max_frames > 0:
        # small wrapper to enforce frame limit
        def play_with_limit(path, width_, fps_):
            cap = cv2.VideoCapture(path)
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_delay = 1.0 / video_fps if video_fps > 0 else 1.0 / fps_
            frame_count = 0
            try:
                while frame_count < max_frames:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    ascii_art = convert_frame_to_ascii(frame, width_)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if color == 'green':
                        print(Fore.GREEN + ascii_art + Style.RESET_ALL)
                    else:
                        print(ascii_art)
                    frame_count += 1
                    time.sleep(frame_delay)
            except KeyboardInterrupt:
                print("\nVideo playback interrupted.")
            finally:
                cap.release()

        play_with_limit(video_path, width, fps)
    else:
        # no frame cap — use standard player but honor color
        if color == 'green':
            # monkey-patch print inside play_video_in_terminal by temporarily redefining builtins.print
            import builtins as _builtins
            orig_print = _builtins.print
            def _color_print(*args, **kwargs):
                orig_print(Fore.GREEN + "".join(map(str, args)) + Style.RESET_ALL, **kwargs)
            _builtins.print = _color_print
            try:
                play_video_in_terminal(video_path, width, fps)
            finally:
                _builtins.print = orig_print
        else:
            play_video_in_terminal(video_path, width, fps)