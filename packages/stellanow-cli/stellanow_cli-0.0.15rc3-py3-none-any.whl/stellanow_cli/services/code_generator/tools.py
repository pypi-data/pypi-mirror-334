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

import os
from typing import Any, Callable, Dict, List, Set, Tuple

from loguru import logger
from stellanow_api_internals.clients.workflow_manager_client import WorkflowManagerClient
from stellanow_api_internals.datatypes.workflow_mgmt import (
    StellaEvent,
    StellaEventDetailed,
    StellaFieldType,
    StellaModelDetailed,
    StellaModelFieldType,
)

from stellanow_cli.code_generators.common.code_generator import CodeGenerator, LanguageConfig
from stellanow_cli.core.enums import StellaDataStructure
from stellanow_cli.core.helpers import ProcessedFile, SkippedFile, ensure_destination_exists
from stellanow_cli.exceptions.cli_exceptions import StellaNowCLIException


def collect_model_references(workflow_client: WorkflowManagerClient, events: List[StellaEvent]) -> Set[str]:
    model_refs = set()
    for event in events:
        detailed_event = workflow_client.get_event_details(event.id)
        for field in detailed_event.fields:
            if isinstance(field.fieldType, dict):
                field_type = StellaFieldType(**field.fieldType)
            else:
                field_type = field.fieldType

            if field_type.value == StellaDataStructure.MODEL:
                model_refs.add(field_type.modelRef)
    return model_refs


def collect_all_model_references(workflow_client: WorkflowManagerClient, model_ids: Set[str]) -> Set[str]:
    all_model_refs = set(model_ids)
    checked_model_refs = set()

    while model_ids:
        current_id = model_ids.pop()
        if current_id in checked_model_refs:
            continue

        model_details = workflow_client.get_model_details(current_id)
        for field in model_details.fields.root:
            if isinstance(field.fieldType, Dict):
                field_type = StellaModelFieldType(**field.fieldType)
            else:
                field_type = field.fieldType
            if field_type.value == StellaDataStructure.MODEL and field_type.modelRef:
                if field_type.modelRef not in all_model_refs:
                    model_ids.add(field_type.modelRef)
                    all_model_refs.add(field_type.modelRef)

        checked_model_refs.add(current_id)

    return all_model_refs


def fetch_model_details(workflow_client: WorkflowManagerClient, model_refs: set) -> Dict[str, StellaModelDetailed]:
    models_details: Dict[str, StellaModelDetailed] = {}
    for model_id in model_refs:
        models_details[model_id] = workflow_client.get_model_details(model_id)
    return models_details


def _generate_files(
    items: List[Any],
    generate_method: Callable[[Any, Dict[str, StellaModelDetailed], Any], str],
    get_file_name_method: Callable[[str], str],
    lang_conf: LanguageConfig,
    models_details: Dict[str, StellaModelDetailed],
    destination: str,
    force: bool,
    is_model: bool = False,
    **kwargs,
) -> Tuple[List[ProcessedFile], List[SkippedFile]]:
    processed_files = []
    skipped_files = []

    for item in items:
        logger.info(f"Generating class for item: {item.name}")

        if is_model:
            file_path = os.path.join(
                destination, "Models", f"{get_file_name_method(item.name)}.{lang_conf.file_extension}"
            )
        else:
            file_path = os.path.join(destination, f"{get_file_name_method(item.name)}.{lang_conf.file_extension}")

        if not force and os.path.exists(file_path):
            logger.info("Skipped ...")
            skipped_files.append(SkippedFile(item.name, "File Already Exist"))
            continue

        try:
            code = generate_method(item, models_details, **kwargs)
            ensure_destination_exists(os.path.dirname(file_path))
            with open(file_path, "w") as file:
                file.write(code)
            processed_files.append(ProcessedFile(item.name))
        except StellaNowCLIException as e:
            logger.info("Skipped ...")
            skipped_files.append(SkippedFile(item.name, e.message))

    return processed_files, skipped_files


def generate_model_files(
    generator: CodeGenerator,
    models_details: Dict[str, StellaModelDetailed],
    destination: str,
    force: bool,
    **kwargs,
) -> Tuple[List[ProcessedFile], List[SkippedFile]]:
    return _generate_files(
        items=list(models_details.values()),
        generate_method=generator.generate_model_class,
        get_file_name_method=generator.get_file_name_for_model_name,
        lang_conf=generator.config,
        models_details=models_details,
        destination=destination,
        force=force,
        is_model=True,
        **kwargs,
    )


def generate_event_files(
    generator: CodeGenerator,
    events: List[StellaEvent],
    event_names: List[str],
    workflow_client: WorkflowManagerClient,
    models_details: Dict[str, StellaModelDetailed],
    destination: str,
    force: bool,
    **kwargs,
) -> Tuple[Set[str], List[ProcessedFile], List[SkippedFile]]:
    events_not_found = set(event_names) if event_names else set()
    events_to_generate: List[StellaEventDetailed] = []

    for event in events:
        if event_names and event.name not in event_names:
            continue
        event_detailed = workflow_client.get_event_details(event.id)
        events_not_found.discard(event.name)
        events_to_generate.append(event_detailed)

    processed_files, skipped_files = _generate_files(
        items=events_to_generate,
        generate_method=generator.generate_message_class,
        get_file_name_method=generator.get_file_name_for_event_name,
        lang_conf=generator.config,
        models_details=models_details,
        destination=destination,
        force=force,
        **kwargs,
    )

    return events_not_found, processed_files, skipped_files
