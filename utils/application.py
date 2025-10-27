from pathlib import Path

import converters.video
import converters.image
import options
import constants


class Application:
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

    @property
    def is_image(self):
        if Path(self.path).suffix[1:] in constants.ALLOWED_IMAGE_FORMAT:
            return True
        return False

    def run(self):
        if self.is_image:
                    
            image = converters.image.ImageConverter(
                image_path=self.path,
                colored=self.colored,
                output_path=self.output_path,
                threshold=self.threshold,
                output_type=self.output_type,
            )
            image.print_ascii_image()
        else:
            video = converters.video.VideoConverter(
                path=self.path,
                colored=self.colored,
                output_path=self.output_path,
                threshold=self.threshold,
                output_type=self.output_type,
            )
            video.print_video_as_ascii()

