from typing import Dict, Callable, Tuple

from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.script.actions.generic import generic_action
from blue_assistant.script.actions.generate_image import generate_image
from blue_assistant.script.actions.generate_text import generate_text
from blue_assistant.logger import logger


dict_of_actions: Dict[str, Callable[[BaseScript, str], bool]] = {
    "generic": generic_action,
    "generate_image": generate_image,
    "generate_text": generate_text,
}
