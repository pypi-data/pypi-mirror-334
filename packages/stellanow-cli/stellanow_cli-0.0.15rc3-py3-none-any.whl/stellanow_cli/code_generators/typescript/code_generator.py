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


class TypescriptLanguageConfig(LanguageConfig):
    @property
    def language(self) -> StellaLanguage:
        return StellaLanguage.TYPESCRIPT

    @property
    def type_mappings(self) -> Dict[FieldType, str]:
        return {
            FieldType.DECIMAL: "number",
            FieldType.INTEGER: "number",
            FieldType.BOOLEAN: "boolean",
            FieldType.STRING: "string",
            FieldType.DATE: "Date",
            FieldType.DATETIME: "Date",
            FieldType.MODEL: "any",
            FieldType.ANY: "any",
        }

    @property
    def reserved_words(self) -> set:
        return {
            "break",
            "case",
            "catch",
            "class",
            "const",
            "continue",
            "debugger",
            "default",
            "delete",
            "do",
            "else",
            "enum",
            "export",
            "extends",
            "false",
            "finally",
            "for",
            "function",
            "if",
            "import",
            "in",
            "instanceof",
            "new",
            "null",
            "return",
            "super",
            "switch",
            "this",
            "throw",
            "true",
            "try",
            "typeof",
            "var",
            "void",
            "while",
            "with",
            "as",
            "implements",
            "interface",
            "let",
            "package",
            "private",
            "protected",
            "public",
            "static",
            "yield",
            "any",
            "boolean",
            "number",
            "string",
            "symbol",
            "undefined",
        }

    @property
    def comment_def(self) -> CommentDefinition:
        return CommentDefinition(start="/**", middle=" * ", end="**/", single="//")

    @property
    def file_extension(self) -> str:
        return "ts"


class TypescriptCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__(TypescriptLanguageConfig())

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
        return inflection.dasherize(inflection.underscore(f"{inflection.camelize(event_name)}Message"))

    def get_file_name_for_model_name(self, model_name: str) -> str:
        return inflection.dasherize(inflection.underscore(f"{inflection.camelize(model_name)}Model"))
