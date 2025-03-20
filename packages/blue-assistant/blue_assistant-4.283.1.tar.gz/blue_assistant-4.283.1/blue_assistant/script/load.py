from typing import Tuple, Type

from blue_assistant.script.repository import list_of_script_classes
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.logger import logger


def load_script(
    script_name: str,
    object_name: str,
    test_mode: bool = False,
    verbose: bool = False,
) -> Tuple[bool, BaseScript]:
    found: bool = False
    script_class: Type[BaseScript] = BaseScript
    for script_class_option in list_of_script_classes:
        if script_class_option.name == script_name:
            found = True
            script_class = script_class_option
            break

    if not found:
        logger.error(f"{script_name}: script not found.")

    return found, script_class(
        object_name=object_name,
        test_mode=test_mode,
        verbose=verbose,
    )
