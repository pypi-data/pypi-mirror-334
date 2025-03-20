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
from loguru import logger
from prettytable import PrettyTable

from stellanow_cli.core.validators import uuid_validator
from stellanow_cli.services.code_generator.code_generator import CodeGeneratorService, pass_code_generator_service


@click.command()
@click.option(
    "--project_id",
    required=True,
    prompt=True,
    callback=uuid_validator,
    help="UUID of the project associated with the organization saved in your configuration file.",
)
@pass_code_generator_service
def events(service: CodeGeneratorService, project_id: str, *args, **kwargs) -> None:
    """Fetches the latest event specifications from the API and output a list of the events into the terminal prompt."""
    workflow_client = service.create_workflow_client(project_id=project_id)
    _events = workflow_client.get_events(include_inactive=True)

    table = PrettyTable(["EventID", "Event Name", "Is Active", "Created At", "Updated At"])

    # Populate the table with data from your SkippedFile instances
    for event in _events:
        table.add_row([event.id, event.name, event.isActive, event.createdAt, event.updatedAt])

    logger.info(table)

    for event in _events:
        logger.info(f"ID: {event.id}, Name: {event.name}")


events_cmd = events
