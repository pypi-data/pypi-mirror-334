from collections.abc import Sequence

import loguru

from . import Filter, filter_all, filter_once

DEFAULT_LEVEL: int | str = "DEBUG"


DEFAULT_FILTER: Filter = filter_all(
    {
        "": "INFO",
        "__main__": "TRACE",
        "liblaf": "DEBUG",
    },
    filter_once(),
)


DEFAULT_LEVELS: Sequence["loguru.LevelConfig"] = [
    {"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}
]
