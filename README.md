# Digital Art Converter

## Project Overview

Digital Art Converter renders visual media as text-based art directly in your terminal. Static images are resized to your console, quantized against a luminance threshold, and mapped to ASCII characters (with optional ANSI color). Videos are decoded frame-by-frame with OpenCV,
converted using the same ASCII pipeline, and streamed back at the source FPS while MoviePy extracts and plays the original audio in a background thread. Basic CLI validation ensures the media path exists, the format is supported, and accidental overwrites are confirmed.

[![Watch the video](https://img.youtube.com/vi/cYDkAKYTWk0/maxresdefault.jpg)](https://youtu.be/cYDkAKYTWk0)

## Installation Instructions

1. Install Python ≥ 3.13
 The project relies on modern typing syntax (| unions) and other features present in Python 3.13 and later.
2. Install uv (https://docs.astral.sh/uv/)

 curl -Ls https://astral.sh/uv/install.sh | sh
3. Clone the repository and sync dependencies

 git clone https://github.com/<your-org>/digital_art_converter.git
 cd digital_art_converter
 uv sync
4. Ensure required system tools are available
  - FFmpeg (MoviePy needs it for audio extraction)
  - A command-line audio player available on your OS (afplay, paplay, start, etc.)
5. Verify the installation

 uv run python main.py -h

> Media assets
> To respect copyright, the repository does not ship with sample photos or videos. Download or supply your own media locally before running the converter.

## Usage

Execute everything via uv run from the project root:

- Basic image conversion

uv run python main.py -p /path/to/image.png
- Colored ASCII with a manual threshold

uv run python main.py -p /path/to/photo.jpg --colored True --threshold 210
- Video playback in ASCII

uv run python main.py -p /path/to/video.mp4

The converter clears the terminal, streams ASCII frames at the detected FPS, and launches audio playback through the platform-specific player.

Key CLI options (utils/argparser.py):

- -p / --path (required) – media file to convert (image or video).
- -c / --colored – pass True to enable ANSI-colored ASCII output.
- --threshold – integer 0–255; defaults to the 95th percentile of pixel intensities.
- --output-path – reserved for future file export support (currently unused).
- --type – accepts static or webcam (webcam mode not yet implemented).
- --output_type – accepts console, file, or all; only console output is wired up today.

Video conversions write intermediate ASCII frames to a temporary directory (via tempfile.mkdtemp()) and clean it up when the process exits or VideoConverter.cleanup() runs.

## TODO List

1. Improve CLI ergonomics – replace boolean arguments with store_true flags and normalise enum handling so users aren’t required to type literal True/False.
2. Support file/combined output modes – honour --output-path and OutputType.FILE/ALL so conversions can be saved without copying from stdout.
3. Stabilise video playback housekeeping – decouple temp-dir cleanup from sys.exit, guard the sleep calculations when FPS is missing, and make playback stop cleanly without terminating the interpreter.
4. Revisit cross-platform audio playback – implement a reliable, portable audio backend once the crashes seen under the current Python runtime are addressed.
5. Implement webcam capture – the CLI already exposes MediaType.WEBCAM; add an OpenCV capture loop for live ASCII previews.
6. Add built-in media download support – offer an optional helper to download remote videos/images to a local cache, making it easier to prepare source media while keeping the repository free of copyrighted assets.
7. Document runtime prerequisites – expand the README with FFmpeg installation tips, audio-backend requirements, and guidance for sourcing media (since none are bundled).
