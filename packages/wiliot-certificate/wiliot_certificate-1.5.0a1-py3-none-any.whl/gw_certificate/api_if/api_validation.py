import json
from jsonschema import Draft202012Validator
import pkg_resources
from enum import Enum

from gw_certificate.ag.ut_defines import GW_CONF, GW_API_VERSION
from gw_certificate.common.debug import debug_print

class MESSAGE_TYPES(Enum):
    STATUS = "status"
    DATA = "data"
    LOGS = "logs"

LATEST_API = "205"
api_version = LATEST_API

def validate_message(message_type: MESSAGE_TYPES, message: dict) -> tuple[bool, str]:
    """
    Validate MQTT message
    :type message_type: MESSAGE_TYPES
    :param message_type: MQTT message type
    :type message: dict
    :param message: MQTT Message
    :return: tuple (bool, str)
    """
    global api_version

    # NOTE When Connection test is not ran (using the -tests flag), default api_version is the latest
    if message_type == MESSAGE_TYPES.STATUS:
        api_version = message[GW_CONF][GW_API_VERSION]
        debug_print(f'API version set as {api_version} according to the status message.')
    json_path = pkg_resources.resource_filename(__name__, f"{api_version}/{message_type.value}.json")
    with open(json_path) as f:
        relevant_schema = json.load(f)
    validator = Draft202012Validator(relevant_schema)
    valid = validator.is_valid(message)
    errors = [e for e in validator.iter_errors(message)]
    return (valid, errors)