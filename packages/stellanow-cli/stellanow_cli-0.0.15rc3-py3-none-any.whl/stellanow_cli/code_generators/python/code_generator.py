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

import json
from typing import Dict

import inflection
from stellanow_api_internals.datatypes.workflow_mgmt import StellaEventDetailed, StellaModelDetailed

from stellanow_cli.code_generators.common.code_generator import (
    CodeGenerator,
    CommentDefinition,
    LanguageConfig,
    MessageClassSpec,
    ModelClassSpec,
)
from stellanow_cli.core.enums import FieldType, StellaLanguage
from stellanow_cli.exceptions.cli_exceptions import StellaNowCLINoEntityAssociatedWithEventException


class PythonLanguageConfig(LanguageConfig):
    @property
    def language(self) -> StellaLanguage:
        return StellaLanguage.PYTHON

    @property
    def type_mappings(self) -> Dict[FieldType, str]:
        return {
            FieldType.DECIMAL: "float",
            FieldType.INTEGER: "int",
            FieldType.BOOLEAN: "bool",
            FieldType.STRING: "str",
            FieldType.DATE: "date",
            FieldType.DATETIME: "datetime",
            FieldType.MODEL: "Any",
            FieldType.ANY: "Any",
        }

    @property
    def reserved_words(self) -> set:
        return {
            "False",
            "None",
            "True",
            "and",
            "as",
            "assert",
            "async",
            "await",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        }

    @property
    def comment_def(self) -> CommentDefinition:
        return CommentDefinition(start='"""', middle="", end='"""', single="#")

    @property
    def file_extension(self) -> str:
        return "py"


class PythonCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__(PythonLanguageConfig())

    def get_model_data(
        self,
        model: StellaModelDetailed,
        model_details: Dict[str, StellaModelDetailed],
        **kwargs,
    ) -> ModelClassSpec:
        fields = self._prepare_fields(model.fields.root, model_details)

        return ModelClassSpec(
            id=model.id,
            name=model.name,
            json=json.dumps(model.model_dump(), indent=4),
            fields=fields,
            referenced_models=self._collect_referenced_models(fields),
            comment_def=self.config.comment_def,
            file_ext=self.config.file_extension,
        )

    def get_message_data(
        self,
        event: StellaEventDetailed,
        model_details: Dict[str, StellaModelDetailed],
        **kwargs,
    ) -> MessageClassSpec:
        fields = self._prepare_fields(event.fields, model_details)
        entities = self._prepare_entities(event.entities)
        if not entities:
            raise StellaNowCLINoEntityAssociatedWithEventException()

        return MessageClassSpec(
            id=event.id,
            name=event.name,
            json=json.dumps(event.model_dump(), indent=4),
            fields=fields,
            entities=entities,
            referenced_models=self._collect_referenced_models(fields),
            comment_def=self.config.comment_def,
            file_ext=self.config.file_extension,
        )

    def get_file_name_for_event_name(self, event_name: str) -> str:
        return inflection.underscore(f"{event_name}Message")

    def get_file_name_for_model_name(self, model_name: str) -> str:
        return inflection.underscore(f"{model_name}Model")
