from enum import Enum

class FontFamily(Enum):
    DEFAULT = "Inter, sans-serif"
    SPACE_MONO = "Space Mono, monospace"
    MAJOR_MONO_DISPLAY = "Major Mono Display, monospace"
    PLASTER = "Plaster, system-ui"
    INCOSOLATA = "Inconsolata, monospace"
    
class FontWeight(Enum):
    LIGHT = "300"
    NORMAL = "400"
    MEDIUM = "500"
    BOLD = "700"
