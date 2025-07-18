import cv2
import sys, time, os, argparse

ASCII_CHARACTERS = ".,-~:;=!*#$@"[::-1]

def frame_to_ascii(frame, width: int) -> str:
    height = int((frame.shape[0] / frame.shape[1]) * width * 0.55)
    resized = cv2.resize(frame, (width, height))

    ascii_frame = ""
    for row in resized:
        for pixel in row:
            ascii_frame += ASCII_CHARACTERS[int(pixel) * len(ASCII_CHARACTERS) // 256]
        ascii_frame += "\n"
    return ascii_frame

def get_ascii_frames(video_file_path: str, width: int) -> list[str]:
    capture = cv2.VideoCapture(video_file_path)
    frames = []

    try:
        while True:
            isRead, frame = capture.read()
            if not isRead:
                break

            grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Make sure its in the correct grayscale
            ascii_frame = frame_to_ascii(grayscale_frame, width=80)
            frames.append(ascii_frame)

    finally:
        capture.release()

    return frames

def draw_frames_in_terminal(video_file_path: str, width: int, fps: int):
    os.system('cls' if os.name == 'nt' else 'clear')

    for frame in get_ascii_frames(video_file_path, width):
        sys.stdout.write('\x1b[H' + frame)  # draw frame
        sys.stdout.flush()
        time.sleep(1 / fps)  # 24 FPS

def main():
    parser = argparse.ArgumentParser(description="Convert video to ascii")
    parser.add_argument("video_file_path", type=str)
    parser.add_argument("width", type=int)
    parser.add_argument("fps", type=int)

    args = parser.parse_args()

    draw_frames_in_terminal(args.video_file_path, 100, 24)

if __name__ == "__main__":
    main()