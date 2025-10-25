import enum


class MediaType(enum.Enum):
    STATIC = "static"
    WEBCAM = "webcam"


class OutputType(enum.Enum):
    CONSOLE = "console"
    FILE = "file"
    ALL = "all"
