import shutil

import cv2
import numpy as np

import constants


def get_image(path):
    # TODO: make image colorful with optional output
    return cv2.imread(path, 0)


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


def convert_image_to_ascii(
    image: np.ndarray.ndarray,
) -> np.ndarray.ndarray:
    # vectorized mapping for speed + consistency

    threshold = np.percentile(image, 92)

    image = np.where(image > threshold, 255, image)

    idx = (image.astype(np.float32) / 255.0) * (len(constants.GRAYSCALE) - 1)
    idx = idx.astype(np.int32)
    lut = np.frombuffer(constants.GRAYSCALE.encode(), dtype=np.uint8)

    for row in idx:
        line = bytes(lut[row]).decode("ascii")
        print(line)


def image_to_ascii(image_path: str) -> None:
    image = get_image(image_path)

    resized_image = resize_image(image)
    convert_image_to_ascii(resized_image)
