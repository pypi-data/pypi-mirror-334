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

import click

from stellanow_cli.core.context import StellaNowContext, pass_stella_context
from stellanow_cli.core.decorators import prompt
from stellanow_cli.core.validators import password_validator, url_validator, uuid_validator
from stellanow_cli.services.code_generator.code_generator import CodeGeneratorService, CodeGeneratorServiceConfig


@click.command()
@prompt("--base_url", callback=url_validator)
@prompt("--username")
@prompt("--password", callback=password_validator, hide_input=True)
@prompt("--organization_id", callback=uuid_validator)
@pass_stella_context
def code_generator_service(
    stella_ctx: StellaNowContext,
    base_url: str,
    username: str,
    password: str,
    organization_id: str,
) -> None:
    """Sets up the necessary credentials and configurations for a specific profile or for the DEFAULT profile if none
    is specified."""
    code_generator_config = CodeGeneratorServiceConfig(
        base_url=base_url,
        username=username,
        password=password,
        organization_id=organization_id,
    )
    stella_ctx.save_service_config(CodeGeneratorService.service_name(), code_generator_config.to_profile_data())


configure_code_generators_cmd = code_generator_service
