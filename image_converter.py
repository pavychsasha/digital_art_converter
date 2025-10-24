import shutil

import cv2
import numpy as np

import constants


def get_image(path, colored=False):
    type = 1 if colored else 0
    return cv2.imread(path, type)


def resize_image(
    image: np.ndarray,
    aspect: float = 2.0,
) -> np.ndarray:
    """
    Fit to terminal width and compensate for character cell aspect ratio.
    aspect = char_height / char_width (≈2.0 for most fonts)
    """
    h, w = image.shape[:2]
    # leave 1 col to avoid wrap
    terminal_size = shutil.get_terminal_size()
    cols = terminal_size.columns
    lines = terminal_size.lines

    new_w = cols
    new_h = max(1, int(round(h / w * new_w / aspect)))

    if new_h > lines:
        scale = lines / new_h
        new_w = max(1, int(round(new_w * scale)))
        new_h = max(1, int(round(new_h * scale)))

    scale_w = new_w / w
    interp = cv2.INTER_AREA if scale_w < 1 else cv2.INTER_CUBIC

    return cv2.resize(image, (new_w, new_h), interpolation=interp)


def _convert_grey_img_to_ascii(image):
    threshold = np.percentile(image, 92)
    image = np.where(image > threshold, 255, image)

    idx = (image.astype(np.float32) / 255.0) * (len(constants.GRAYSCALE) - 1)
    idx = idx.astype(np.int32)
    lut = np.frombuffer(constants.GRAYSCALE.encode(), dtype=np.uint8)

    res = []
    for row in idx:
        line = bytes(lut[row]).decode("ascii")
        res.append(line)
    return res


def _convert_colored_img_to_ascii(image):
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = np.percentile(grey_img, constants.IMAGE_THRESHOLD_PERCENTILE)
    image = np.where(image > threshold, 255, image)

    converted_grey_img = _convert_grey_img_to_ascii(grey_img)
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


def convert_image_to_ascii(
    image: np.ndarray.ndarray,
    colored: bool = False,
) -> np.ndarray.ndarray:
    if colored:
        return _convert_colored_img_to_ascii(image)
    return _convert_grey_img_to_ascii(image)


def print_ascii_image(ascii_image, colored=False):
    for line in ascii_image:
        print(line)


def image_to_ascii(image_path: str, colored: bool = False) -> None:
    image = get_image(image_path, colored)

    resized_image = resize_image(image)
    res = convert_image_to_ascii(resized_image, colored)
    print_ascii_image(
        res,
    )
