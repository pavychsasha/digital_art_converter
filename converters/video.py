import os
import sys
import shutil
import subprocess
import threading

import time
import cv2

import tempfile

from moviepy import VideoFileClip

from converters import image
from pathlib import Path


import options



class VideoConverter:
    def __init__(
        self,
        path: str,
        colored: bool = False,
        threshold: int | None = None,
        ascii_font_aspect: float = 2.0,
        output_type: options.OutputType = options.OutputType.CONSOLE,
        output_path: str | None = None,
    ):
        self.path = path
        self.colored = colored
        self.ascii_font_aspect = ascii_font_aspect
        self.output_type = output_type
        self.output_path = output_path
        self.threshold = threshold

        self.fps = None
        self.cap = None
        self.audio_segment = None
        self.frames_number = 0
        self._temp_dir = None

    @property
    def temp_dir(self):
        if not self._temp_dir:
            self._temp_dir = tempfile.mkdtemp()
        return self._temp_dir

    def _clear_terminal(self):
        if os.name == 'nt':  # 'nt' refers to Windows
            os.system('cls')
        else:  # 'posix' refers to Unix-like systems (Linux, macOS)
            os.system('clear')

    def extract_audio(self):
        video_clip = VideoFileClip(self.path)
        audio_clip = video_clip.audio
        if audio_clip:
            audio_clip.write_audiofile(f"{self.temp_dir}/audio.mp3")
            audio_clip.close()
        video_clip.close()
        print("Extracted audio")

    def convert_video_to_ascii(self):
        self.cap = cv2.VideoCapture(self.path)

        if not self.cap.isOpened():
            print("Error, could not open the file")
            return

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        i = 0
        self.extract_audio()
        while True:

            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.colored:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            image_converter = image.ImageConverter(
                image=frame,
                colored=self.colored,
                threshold=self.threshold,
                ascii_font_aspect=self.ascii_font_aspect,
                output_type=self.output_type,
                output_path=self.output_path
            )
            if self.threshold is None:
                self.threshold = image_converter.threshold

            image_converter.export_ascii_to_file(
                outptput_path=f"{self.temp_dir}/frame_{i}"
            )
            i += 1

        self.frames_number = i

    def play_audio(self):
        if os.path.exists(os.path.join(self.temp_dir, "audio.mp3")):
            subprocess.call(["afplay", f"{self.temp_dir}/audio.mp3"])

    def print_video_as_ascii(self):
        if not self.cap:
            self.convert_video_to_ascii()

        frame_duration = 1.0 / self.fps if self.fps else None
        frames = [
          Path(f"{self.temp_dir}/frame_{i}").read_text()
          for i in range(self.frames_number)
        ]

        hide_cursor = "\033[?25l"
        show_cursor = "\033[?25h"
        clear_screen = "\033[H\033[J"

        sys.stdout.write(hide_cursor)
        sys.stdout.flush()

        start_time = time.perf_counter()
        audio_thread = threading.Thread(target=self.play_audio, daemon=True)
        audio_thread.start()

        try:
            for idx, frame in enumerate(frames):
                sys.stdout.write(clear_screen)
                sys.stdout.write(frame)
                sys.stdout.flush()

                if frame_duration:
                    next_deadline = start_time + (idx + 1) * frame_duration
                    sleep_for = next_deadline - time.perf_counter()
                if sleep_for > 0:
                    time.sleep(sleep_for)
        finally:
            audio_thread.join()
            shutil.rmtree(self.temp_dir)
            sys.stdout.write(show_cursor)
            sys.stdout.flush()
