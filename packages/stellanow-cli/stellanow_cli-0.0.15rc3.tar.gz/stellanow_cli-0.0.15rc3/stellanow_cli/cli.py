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

from importlib.metadata import version

import click
from loguru import logger

from stellanow_cli.commands.code_generator.code_generator_service_group import code_generator_service
from stellanow_cli.commands.configure.configure_group import configure
from stellanow_cli.commands.data_dna_stream_tester.data_dna_stream_tester_group import data_dna_stream_tester
from stellanow_cli.core.context import DEFAULT, StellaNowContext, pass_stella_context

__version__ = version("stellanow-cli")


@click.group()
@click.version_option(version=__version__, message="%(version)s")
@click.option(
    "--profile",
    "-p",
    default=DEFAULT,
    help="The profile name for storing a particular set of configurations. If no profile is "
    "specified, the configurations will be stored under the 'DEFAULT' profile.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enables verbose mode, which outputs more detailed logging messages.",
)
@pass_stella_context
def cli(stella_ctx: StellaNowContext, profile: str, verbose: bool) -> None:
    """Command-line interface for the StellaNow SDK code generation and comparison tool."""
    stella_ctx.profile = profile
    stella_ctx.verbose = verbose

    logger.info(f"Command executed in context of profile: {stella_ctx.profile} ")


cli.add_command(configure)
cli.add_command(code_generator_service)
cli.add_command(data_dna_stream_tester)
