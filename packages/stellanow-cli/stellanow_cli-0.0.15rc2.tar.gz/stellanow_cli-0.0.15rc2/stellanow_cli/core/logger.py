"""
Copyright (C) 2022-2025 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import sys

from loguru import logger

logger.level("RAW", no=50)


def setup_logging(verbose: bool) -> None:
    logger.remove()

    info_format = " <level>{message}</level>"
    raw_format = " {message}"
    success_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    )
    default_fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    logger.add(
        sys.stdout,
        format=info_format,
        level="INFO",
        filter=lambda record: record["level"].name == "INFO",
        colorize=False,
    )

    logger.add(
        sys.stdout,
        format=raw_format,
        level="RAW",
        filter=lambda record: record["level"].name == "RAW",
        colorize=True,
    )

    logger.add(
        sys.stdout,
        format=success_format,
        level="INFO",
        filter=lambda record: record["level"].name == "SUCCESS",
        colorize=True,
    )

    level = "DEBUG" if verbose else "INFO"

    logger.add(
        sys.stdout,
        format=default_fmt,
        level=level,
        filter=lambda record: record["level"].name not in ["INFO", "SUCCESS", "RAW"],
        colorize=True,
    )
