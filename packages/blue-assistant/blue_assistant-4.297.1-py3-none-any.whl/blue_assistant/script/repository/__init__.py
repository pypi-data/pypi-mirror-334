from typing import List, Type

from blue_assistant.script.repository.generic.classes import GenericScript
from blue_assistant.script.repository.blue_amo.classes import BlueAmoScript
from blue_assistant.script.repository.hue.classes import HueScript
from blue_assistant.script.repository.orbital_data_explorer.classes import (
    OrbitalDataExplorerScript,
)

list_of_script_classes: List[Type[GenericScript]] = [
    GenericScript,
    BlueAmoScript,
    HueScript,
    OrbitalDataExplorerScript,
]

list_of_script_names: List[str] = [
    script_class.name for script_class in list_of_script_classes
]
