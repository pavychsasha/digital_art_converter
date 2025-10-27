import shutil

import cv2
import numpy as np

import constants
import options

import utils.validators


class ImageConverter:
    def __init__(
        self,
        image_path: str | None = None,
        image: np.ndarray | None = None,
        colored: bool = False,
        threshold: int | None = None,
        ascii_font_aspect: float = 2.0,
        output_type: options.OutputType = options.OutputType.CONSOLE,
        output_path: str | None = None,
    ):
        self.image_path = image_path
        self.colored = colored
        self.ascii_font_aspect = ascii_font_aspect

        self.output_type = output_type
        self.output_path = output_path

        self._threshold = threshold
        self._image = image
        self._grey_image = None
        self._ascii_image = None
        self._padding = 0

        self.resize_image()

    @property
    def image(self):
        if self._image is None:
            img_type = 1 if self.colored else 0
            try:
                self._image = cv2.imread(self.image_path, img_type)
                utils.validators.ArgsValidator.validate_image(self._image)
            except Exception as exc:
                raise Exception(f"Error during image retrieval: {exc}")
        return self._image

    @property
    def grey_img(self):
        if self._grey_image is None:
            if self.colored:
                self._grey_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            else:
                self._grey_image = self.image

        return self._grey_image

    @property
    def threshold(self):
        if not self._threshold:
            self._threshold = np.percentile(
                self.grey_img, constants.IMAGE_THRESHOLD_PERCENTILE
            )
        return self._threshold

    @property
    def ascii_image(self):
        if not self._ascii_image:
            self._ascii_image = self._get_ascii_image()
        return self._ascii_image

    def _convert_colored_img_to_ascii(self):
        image = np.where(self.image > self.threshold, 255, self.image)

        converted_grey_img = self._convert_grey_img_to_ascii()
        res = []
        for row_idx, row in enumerate(converted_grey_img):
            line = ""
            for col_idx, pixel in enumerate(row):
                b, g, r = image[row_idx, col_idx]

                color_code = f"\033[38;2;{r};{g};{b}m"
                line += f"{color_code}{pixel}"
            line += "\033[0m"
            res.append(line)
        return res

    def _convert_grey_img_to_ascii(self):
        image = np.where(self.grey_img > self.threshold, 255, self.grey_img)

        idx = (image.astype(np.float32) / 255.0) * (len(constants.GRAYSCALE) - 1)
        idx = idx.astype(np.int32)
        lut = np.frombuffer(constants.GRAYSCALE.encode(), dtype=np.uint8)

        res = []
        for row in idx:
            line = bytes(lut[row]).decode("ascii")
            res.append(line)
        return res

    def _get_ascii_image(
        self,
    ) -> np.ndarray.ndarray:
        if self.colored:
            return self._convert_colored_img_to_ascii()
        return self._convert_grey_img_to_ascii()

    def get_target_size(self):
        """
        Fit to terminal width and compensate for character cell aspect ratio.
        aspect = char_height / char_width (≈2.0 for most fonts)
        """

        h, w = new_h, new_w = self.image.shape[:2]

        if self.output_type == options.OutputType.CONSOLE:
            terminal_size = shutil.get_terminal_size()
            cols = terminal_size.columns
            # leave 1 col to avoid wrap
            lines = terminal_size.lines - 1

            new_w = cols
            new_h = max(1, int(round(h / w * new_w / self.ascii_font_aspect)))

            if new_h > lines:
                scale = lines / new_h
                new_w = max(1, int(round(new_w * scale)))
                new_h = max(1, int(round(new_h * scale)))

            if new_w < cols:
                self._padding = (cols - new_w) // 2

        return new_w, new_h

    def resize_image(self):
        new_w, new_h = self.get_target_size()

        self._image = cv2.resize(self.image, (new_w, new_h))
        self._grey_image = None

    def print_ascii_image_from_file(file_path):
        with open(file_path, "r") as file:
            print(file.read())

    def print_ascii_image(self):
        for line in self.ascii_image:
            print(line)

    def export_ascii_to_file(self, outptput_path: str):

        with open(outptput_path, "w+") as file:
            for line in self.ascii_image:
                file.write(" "*self._padding + line + "\n")
