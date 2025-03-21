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

from stellanow_cli.commands.code_generator.events import events_cmd
from stellanow_cli.commands.code_generator.generate import generate_cmd
from stellanow_cli.commands.code_generator.models import models_cmd
from stellanow_cli.core.context import StellaNowContext, pass_stella_context
from stellanow_cli.core.decorators import option_with_config_lookup
from stellanow_cli.core.validators import password_validator, url_validator, uuid_validator
from stellanow_cli.services.code_generator.code_generator import CodeGeneratorService, CodeGeneratorServiceConfig


@click.group(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@option_with_config_lookup(
    "--base_url",
    service_class=CodeGeneratorService,
    callback=url_validator,
    help="Base Service url",
)
@option_with_config_lookup("--username", service_class=CodeGeneratorService, help="Base Service Api key")
@option_with_config_lookup(
    "--password",
    service_class=CodeGeneratorService,
    callback=password_validator,
    hide_input=True,
    help="Base Service Api Secret",
)
@option_with_config_lookup(
    "--organization_id",
    service_class=CodeGeneratorService,
    callback=uuid_validator,
    hide_input=True,
    help="Name of Organization",
)
@pass_stella_context
@click.pass_context
def code_generator_service(
    ctx: click.Context,
    stella_ctx: StellaNowContext,
    base_url: str,
    username: str,
    password: str,
    organization_id: str,
    *args,
    **kwargs,
) -> None:
    ctx.obj = CodeGeneratorService(
        CodeGeneratorServiceConfig(
            base_url=base_url,
            username=username,
            password=password,
            organization_id=organization_id,
        )
    )

    stella_ctx.add_service(service=ctx.obj)


code_generator_service.add_command(events_cmd)
code_generator_service.add_command(generate_cmd)
code_generator_service.add_command(models_cmd)
