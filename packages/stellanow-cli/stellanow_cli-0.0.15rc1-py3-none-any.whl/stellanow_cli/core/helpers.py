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

from pathlib import Path

from loguru import logger


class ProcessedFile:
    def __init__(self, filename: str):
        self.filename = filename

    def __iter__(self):
        return iter([self.filename])


class SkippedFile:
    def __init__(self, filename: str, reason: str):
        self.filename = filename
        self.reason = reason

    def __iter__(self):
        return iter([self.filename, self.reason])


def ensure_destination_exists(destination: str):
    """Ensure the destination directory exists, creating it if necessary."""
    path = Path(destination)
    if not path.is_dir():
        logger.info(f"Destination directory {destination} does not exist. Creating...")
        path.mkdir(parents=True, exist_ok=True)
