import os
from pathlib import Path

import loguru
from environs import env
from rich.console import Console

from liblaf import grapes

from . import DEFAULT_FILTER, DEFAULT_LEVEL, Filter


def console_handler(
    console: Console | None = None,
    level: int | str = DEFAULT_LEVEL,
    filter_: Filter | None = None,
) -> "loguru.HandlerConfig":
    if console is None:
        console = grapes.logging_console()
    if filter_ is None:
        filter_ = DEFAULT_FILTER

    def sink(message: "loguru.Message") -> None:
        console.print(message, end="", no_wrap=True, crop=False, overflow="ignore")

    return {
        "sink": sink,
        "level": level,
        "format": "[green]{time:YYYY-MM-DD HH:mm:ss.SSS}[/green] | [logging.level.{level}]{level: <8}[/logging.level.{level}] | [cyan]{name}[/cyan]:[cyan]{function}[/cyan]:[cyan]{line}[/cyan] - {message}",
        "filter": filter_,
    }


def file_handler(
    fpath: str | os.PathLike[str] | None = None,
    level: int | str = DEFAULT_LEVEL,
    filter_: Filter | None = None,
) -> "loguru.HandlerConfig":
    if fpath is None:
        fpath = env.path("LOGGING_FILE", default=Path("run.log"))
    if filter_ is None:
        filter_ = DEFAULT_FILTER
    return {"sink": fpath, "level": level, "filter": filter_, "mode": "w"}


def jsonl_handler(
    fpath: str | os.PathLike[str] | None = None,
    level: int | str = DEFAULT_LEVEL,
    filter_: Filter | None = None,
) -> "loguru.HandlerConfig":
    if fpath is None:
        fpath = env.path("LOGGING_JSONL", default=Path("run.log.jsonl"))
    if filter_ is None:
        filter_ = DEFAULT_FILTER
    return {
        "sink": fpath,
        "level": level,
        "filter": filter_,
        "serialize": True,
        "mode": "w",
    }
