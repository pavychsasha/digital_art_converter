import os
from pathlib import Path
import constants


class ArgsValidator:
    @classmethod
    def validate_image(cls, image):
        if image is None:
            raise Exception("Could not open an image")

    @classmethod
    def validate_media_input(cls, path: str):
        absolute_path = os.path.abspath(path)
        if not os.path.exists(absolute_path):
            raise ValueError("Path does not exists")

        suffix = Path(absolute_path).suffix[1:]
        allowed_formats = constants.ALLOWED_IMAGE_FORMAT | constants.ALLOWED_VIDEO_FORMAT
        if suffix not in allowed_formats :
            supported_types_str = ", ".join(allowed_formats)
            raise ValueError(
                f"Incorrect media file type, supported types: {supported_types_str}",
            )

    @classmethod
    def validate_output_path(cls, path: str):
        if not path:
            return
        absolute_path = os.path.abspath(path)
        if os.path.exists(absolute_path):
            user_input = str(
                input(r"Output file exists, do you want to override? (y,n\other char)")
            )
            if user_input.lower() != "y":
                exit(0)

    @classmethod
    def validate_parameters(cls, args):
        cls.validate_media_input(args.path)

        cls.validate_output_path(args.output_path)
