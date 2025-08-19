from enum import Enum

class SizeButton(Enum):
    SMALL = "0.8em"
    MEDIUM = "1em"
    LARGE = "1.2em"

class SizeText(Enum):
    X_SMALL = "0.6em"
    SMALL = "0.8em"
    MEDIUM = "1em"
    LARGE = "1.2em"
    X_LARGE = "2em"

class SizeLogo(Enum):
    SMALL = "1.5em"
    MEDIUM = "2em"
    LARGE = "3.5em"

class SizeSpace(Enum):
    SMALL = "0.2em"
    MEDIUM = "1em"
    LARGE = "2em"
    X_LARGE = "4em"

class SizeGeneral(Enum):
    FULL = "100%"
    HALF = "50%"
    AUTO = "auto"

class SizeAvatar(Enum):
    SMALL = "2"
    DEFAULT = "3"
    LARGE = "6"
    X_LARGE = "8"

class SizeIcon(Enum):
    X_SMALL = 12
    SMALL = 16
    MEDIUM = 20
    LARGE = 24
    X_LARGE = 30

class BorderRadius(Enum):
    SMALL = "5px"
    DEFAULT = "25px"


