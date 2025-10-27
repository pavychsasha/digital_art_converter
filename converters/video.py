import os
import time
import cv2

from converters import image
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


    def _clear_terminal(self):
        if os.name == 'nt':  # 'nt' refers to Windows
            os.system('cls')
        else:  # 'posix' refers to Unix-like systems (Linux, macOS)
            os.system('clear')

    def convert_video_to_ascii(self):
        self.cap = cv2.VideoCapture(self.path)

        if not self.cap.isOpened():
            print("Error, could not open the file")
            return


        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        i = 1
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.colored:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # TODO: should I instantiate all of the frames,
            # or I can just pre-process all of the frames, and then play that?
            image_converter = image.ImageConverter(
                image=frame,
                colored=self.colored,
                threshold=self.threshold,
                ascii_font_aspect=self.ascii_font_aspect,
                output_type=self.output_type,
                output_path=self.output_path
            )

            # TODO: make it more generic and buffer-like, so  this folder will be auto created
            # and auto deleted, or even let user decide about the output
            image_converter.export_ascii_to_file(outptput_path=f"result/frame_{i}")
            i += 1



    def print_video_as_ascii(self):
        if not self.cap:
            self.convert_video_to_ascii()
        delay = 1.0 / self.fps

        i = 1
        while os.path.exists(f"result/frame_{i}"):
            with open(f"result/frame_{i}") as file:
                print('\033[J', end='')
                print(file.read(), end='')
                print('\033[?25l', end='')
            time.sleep(delay)
            i += 1

        self._clear_terminal()
