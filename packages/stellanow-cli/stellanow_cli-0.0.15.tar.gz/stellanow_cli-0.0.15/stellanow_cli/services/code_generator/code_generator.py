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

from dataclasses import dataclass
from typing import Optional

from stellanow_api_internals.clients.workflow_manager_client import WorkflowManagerClient

from stellanow_cli.core.decorators import make_stella_context_pass_decorator
from stellanow_cli.services.service import StellaNowService, StellaNowServiceConfig

CODE_GENERATOR_SERVICE_NAME = "code-generator-service"
OIDC_CLIENT_ID = "tools-cli"


@dataclass
class CodeGeneratorServiceConfig(StellaNowServiceConfig):
    base_url: str
    username: str
    password: str
    organization_id: str


class CodeGeneratorService(StellaNowService):
    def __init__(self, config: CodeGeneratorServiceConfig) -> None:  # noqa
        self._config = config

    @classmethod
    def service_name(cls) -> str:
        return CODE_GENERATOR_SERVICE_NAME

    def create_workflow_client(self, project_id: Optional[str]) -> WorkflowManagerClient:
        return WorkflowManagerClient(
            base_url=self._config.base_url,
            username=self._config.username,
            password=self._config.password,
            organization_id=self._config.organization_id,
            project_id=project_id,
        )


pass_code_generator_service = make_stella_context_pass_decorator(CodeGeneratorService)
