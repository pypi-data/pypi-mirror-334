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

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import inflection
from jinja2 import Environment, FileSystemLoader
from stellanow_api_internals.datatypes.workflow_mgmt import (
    StellaEventDetailed,
    StellaField,
    StellaFieldType,
    StellaModelDetailed,
)

from stellanow_cli.core.enums import FieldType, StellaLanguage


@dataclass
class CommentDefinition(ABC):
    start: str
    middle: str
    end: str
    single: str


@dataclass
class FieldDescriptor:
    original_name: str
    mapped_name: str
    type_str: str
    is_model: bool

    @classmethod
    def from_stella_field(cls, field, mapper, escape_reserved_words, model_details):
        field_type = mapper.map_field_type(field, model_details)
        is_model = field_type in mapper.model_types or field_type.endswith("Model")
        mapped_name = escape_reserved_words(field.name)
        return cls(field.name, mapped_name, field_type, is_model)


@dataclass
class EntityDescriptor:
    original_name: str
    mapped_name: str

    @classmethod
    def from_stella_entity(cls, entity, escape_reserved_words):
        return cls(entity.name, escape_reserved_words(entity.name))


@dataclass
class BaseClassSpec:
    id: str
    name: str
    json: str
    comment_def: CommentDefinition
    file_ext: str
    fields: List[FieldDescriptor]
    referenced_models: List[str]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))


@dataclass
class ModelClassSpec(BaseClassSpec):
    pass


@dataclass
class MessageClassSpec(BaseClassSpec):
    entities: List[EntityDescriptor] = field(default_factory=list)


class LanguageConfig(ABC):
    @property
    @abstractmethod
    def language(self) -> StellaLanguage:
        pass

    @property
    @abstractmethod
    def type_mappings(self) -> Dict[FieldType, str]:
        pass

    @property
    @abstractmethod
    def reserved_words(self) -> set:
        pass

    @property
    @abstractmethod
    def comment_def(self) -> CommentDefinition:
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    def map_field_type(self, field: StellaField, model_details: Dict[str, Any]) -> str:
        if isinstance(field.fieldType, dict):
            field_type = StellaFieldType(**field.fieldType)
        else:
            field_type = field.fieldType

        value_type = FieldType(field_type.value)

        if value_type == FieldType.MODEL and field_type.modelRef:
            model_name = inflection.camelize(model_details[field_type.modelRef].name, uppercase_first_letter=True)
            return f"{model_name}Model"
        return self.type_mappings.get(value_type, FieldType.ANY)

    @property
    def model_types(self) -> List[str]:
        return ["Any", "object"]  # Default; override if needed

    def escape_reserved_words(self, word: str) -> str:
        return f"{word}_" if word in self.reserved_words else word

    def __post_init__(self):
        missing_types = set(FieldType) - set(self.type_mappings.keys())
        if missing_types:
            raise ValueError(f"LanguageConfig for {self.language} missing mappings for: {missing_types}")


class CodeGenerator(ABC):
    def __init__(self, language_config: LanguageConfig):
        self.config = language_config

        self.env = self.__load_templates()

        self.env.filters["camel_case"] = lambda s: inflection.camelize(s, uppercase_first_letter=False)
        self.env.filters["pascal_case"] = lambda s: inflection.camelize(s, uppercase_first_letter=True)
        self.env.filters["kebab_case"] = lambda s: inflection.dasherize
        self.env.filters["snake_case"] = inflection.underscore
        self.env.filters["get_model_file_name"] = self.get_file_name_for_model_name

    def __load_templates(self) -> Environment:
        current_file_path = Path(__file__).parent

        language_templates_path = current_file_path / f"../{self.get_language()}/templates"
        shared_templates_path = current_file_path / "templates"  # Shared templates directory

        return Environment(
            loader=FileSystemLoader([language_templates_path, shared_templates_path]),
            extensions=["jinja2.ext.do"],
        )

    def _prepare_fields(self, fields, model_details: Dict[str, Any]) -> List[FieldDescriptor]:
        return [
            FieldDescriptor.from_stella_field(f, self.config, self.config.escape_reserved_words, model_details)
            for f in fields
        ]

    def _prepare_entities(self, entities) -> List[EntityDescriptor]:
        return [EntityDescriptor.from_stella_entity(e, self.config.escape_reserved_words) for e in entities]

    def _collect_referenced_models(self, fields: List[FieldDescriptor]) -> List[str]:
        return [f.type_str[:-5] for f in fields if f.is_model and f.type_str.endswith("Model")]

    def generate_model_class(self, model, model_details: Dict[str, Any], **kwargs) -> str:
        template = self.env.get_template("model.jinja2")
        spec = self.get_model_data(model, model_details, **kwargs)
        return template.render(spec=spec)

    def generate_message_class(self, event, model_details: Dict[str, Any], **kwargs) -> str:
        template = self.env.get_template("message.jinja2")
        spec = self.get_message_data(event, model_details, **kwargs)
        return template.render(spec=spec)  # Allow spec to unpack as kwargs for flexibility

    @abstractmethod
    def get_model_data(
        self,
        model: StellaModelDetailed,
        model_details: Dict[str, StellaModelDetailed],
        **kwargs,
    ) -> ModelClassSpec:
        """Return a language-specific spec object for model class generation."""

    @abstractmethod
    def get_message_data(
        self,
        event: StellaEventDetailed,
        model_details: Dict[str, StellaModelDetailed],
        **kwargs,
    ) -> MessageClassSpec:
        """Return a language-specific spec object or dict for message class generation."""

    @abstractmethod
    def get_file_name_for_event_name(self, event_name: str) -> str:
        pass

    @abstractmethod
    def get_file_name_for_model_name(self, model_name: str) -> str:
        pass

    def get_language(self) -> str:
        return self.config.language.value
