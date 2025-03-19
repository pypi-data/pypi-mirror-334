from typing import Dict, Callable

from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.script.repository.orbital_data_explorer.actions import (
    researching_the_questions,
)


dict_of_actions: Dict[str, Callable[[BaseScript, str], bool]] = {
    "researching_the_questions": researching_the_questions.researching_the_questions,
}
