"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import json
import os
import tempfile
import typing as t
import uuid
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from time import sleep

import click
import paho.mqtt.client as mqtt
from loguru import logger

from stellanow_cli.core.validators import url_validator, uuid_validator, zip_file_validator


@dataclass
class EntityTypeIds:
    entityTypeDefinitionId: str
    entityId: str


@dataclass
class Metadata:
    eventTypeDefinitionId: str
    entityTypeIds: t.List[EntityTypeIds]
    messageId: str = field(default_factory=lambda: str(uuid.uuid4()))
    messageOriginDateUTC: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


@dataclass
class Value:
    metadata: Metadata
    payload: str


@dataclass
class Key:
    organizationId: str
    projectId: str


@dataclass
class MsgWrapper:
    key: Key
    value: Value


def create_message(org_id, project_id, event_type, entity_type, entity_id, payload) -> MsgWrapper:
    entity_type_ids = EntityTypeIds(entityTypeDefinitionId=entity_type, entityId=entity_id)
    metadata = Metadata(eventTypeDefinitionId=event_type, entityTypeIds=[entity_type_ids])
    value = Value(metadata=metadata, payload=payload)
    key = Key(organizationId=org_id, projectId=project_id)

    return MsgWrapper(key=key, value=value)


def on_connect(client, userdata, flags, reason_code, properties):  # noqa
    if reason_code == 0:
        logger.info("Connected to MQTT Broker!")
    else:
        logger.error(f"Failed to connect, return code {reason_code}\n")


def on_publish(client, userdata, mid, reason_code, properties):  # noqa
    logger.info(f"Message published: {mid}")


@click.command()
@click.option(
    "--mqtt_username",
    required=True,
    prompt=True,
    help="Username to authenticate with MQTT broker.",
)
@click.option(
    "--mqtt_password",
    required=True,
    prompt=True,
    hide_input=True,
    help="Password to authenticate with MQTT broker.",
)
@click.option(
    "--mqtt_broker",
    required=True,
    prompt=True,
    callback=url_validator,
    help="MQTT broker to connect to.",
)
@click.option(
    "--mqtt_port",
    default=8083,
    help="Port for MQTT broker connection, default is 8883 for SSL.",
)
@click.option(
    "--input_file",
    required=True,
    prompt=True,
    type=click.Path(exists=True),
    callback=zip_file_validator,
    help="File containing game state data to send.",
)
@click.option(
    "--org_id",
    required=True,
    prompt=True,
    callback=uuid_validator,
    help="Stella Now Organization I D.",
)
@click.option(
    "--project_id",
    required=True,
    prompt=True,
    callback=uuid_validator,
    help="Stella Now Project ID.",
)
@click.option(
    "--event_type",
    required=True,
    prompt=True,
    help="Event type definition ID for the game state data.",
)
@click.option(
    "--entity_type",
    required=True,
    prompt=True,
    help="Entity type definition ID for the game state data.",
)
@click.option("--entity_id", required=True, prompt=True, help="Entity ID for the game state data.")
@click.option(
    "--infinite",
    default=False,
    is_flag=True,
    help="If set, the game state data will be sent continuously until the process is interrupted.",
)
def simulate_game_match(
    mqtt_username: str,
    mqtt_password: str,
    mqtt_broker: str,
    mqtt_port: int,
    input_file: str,
    org_id: str,
    project_id: str,
    event_type: str,
    entity_type: str,
    entity_id: str,
    infinite: bool,
    *args,
    **kwargs,
) -> None:
    """Simulate a full match of a game by sending game state data to a MQTT broker."""
    ...

    topic = f"in/{org_id}"

    # Initialize the MQTT Client
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        transport="websockets",
        protocol=mqtt.MQTTv5,
        client_id="tools-cli",
    )
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Configure SSL/TLS
    client.tls_set()  # Default parameters for SSL. Adjust as necessary for your broker's configuration.

    # Connect to the MQTT Broker
    client.connect(mqtt_broker, mqtt_port, 60)

    # Start the network loop in a separate thread
    client.loop_start()

    try:
        while True:
            # Unpack the ZIP file and process each JSON file
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(input_file, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)  # Extract files to the temporary directory
                    for root, dirs, files in os.walk(temp_dir):
                        sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))
                        for filename in sorted_files:
                            if filename.endswith(".json"):
                                file_path = os.path.join(root, filename)
                                with open(file_path, "r") as f:
                                    data = json.load(f)
                                    message = json.dumps(
                                        asdict(
                                            create_message(
                                                org_id,
                                                project_id,
                                                event_type,
                                                entity_type,
                                                entity_id,
                                                json.dumps(data),
                                            )
                                        )
                                    )
                                    # Uncomment the next line to publish
                                    client.publish(topic, payload=message, qos=1)
                                    logger.info(f"Published {filename}")

                                    sleep(0.1)
            if not infinite:
                break  # Exit the outer loop if infinite processing is not required
    finally:
        client.loop_stop()  # Stop the network loop
        client.disconnect()  # Disconnect from the MQTT broker

    client.loop_stop()
    client.disconnect()


simulate_game_match_cmd = simulate_game_match
