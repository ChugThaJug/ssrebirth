# app/core/enums.py
from enum import Enum

class ChapterSource(str, Enum):
    AUTO = "auto"
    DESCRIPTION = "description"

class ProcessingMode(str, Enum):
    SIMPLE = "simple"
    DETAILED = "detailed"
    DETAILED_WITH_SCREENSHOTS = "detailed_with_screenshots"