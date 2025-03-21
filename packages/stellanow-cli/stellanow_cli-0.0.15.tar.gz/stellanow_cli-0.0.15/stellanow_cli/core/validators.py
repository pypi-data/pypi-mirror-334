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

import typing as t
import uuid
from urllib.parse import urlparse

import click


def any_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> t.Any:
    return value


def url_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> t.Any:
    parsed = urlparse(value.strip())
    if not all([parsed.scheme, parsed.netloc]):
        click.BadParameter(f"Expected a valid URL, got '{value}' instead.")
    return value


def url_list_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> t.List[str]:
    if isinstance(value, list):
        return value
    urls = value.split(",")
    for url in urls:
        parsed = urlparse(url.strip())
        if not all([parsed.scheme, parsed.netloc]):
            click.BadParameter(f"Expected a valid URL, got '{url}' instead.")
    return value


def username_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> str:
    if not (6 <= len(value) < 200):
        click.BadParameter("Username must have at least 6 characters and less than 200 characters.")
    return value


def password_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> str:
    if not (10 <= len(value) < 255):
        click.BadParameter("Password must have at least 10 characters and less than 255 characters.")
    return value


def uuid_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: t.Any) -> str:
    try:
        uuid.UUID(value)
    except ValueError:
        raise click.BadParameter(f"{value} is not a valid UUID.")
    return value


def kafka_brokers_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: str) -> str:
    """
    Validates that each broker in a comma-separated list is a valid host address.
    """
    brokers = value.split(",")
    for broker in brokers:
        parsed = urlparse("dummy-scheme://" + broker)
        if not parsed.hostname or not parsed.port:
            raise click.BadParameter(f"Each Kafka broker must be in the format 'host:port'. Error parsing '{broker}'.")
    return value


def zip_file_validator(ctx: click.Context, param: t.Optional[click.Parameter], value: str):
    """
    Validates that the provided file is a ZIP file based on its extension.
    """
    if not value.lower().endswith(".zip"):
        raise click.UsageError("The input file must be a ZIP file.")
    return value
