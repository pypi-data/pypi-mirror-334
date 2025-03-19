from blue_objects import file, path

from blue_assistant.script.repository.generic.classes import GenericScript
from blue_assistant.script.repository.orbital_data_explorer.actions import (
    dict_of_actions,
)


class OrbitalDataExplorerScript(GenericScript):
    name = path.name(file.path(__file__))

    def __init__(
        self,
        object_name: str,
        test_mode: bool = False,
        verbose: bool = False,
    ):
        super().__init__(
            object_name=object_name,
            test_mode=test_mode,
            verbose=verbose,
        )

        if self.test_mode:
            self.nodes["researching_the_questions"]["max_iterations"] = 3

    def perform_action(
        self,
        node_name: str,
    ) -> bool:
        if not super().perform_action(node_name=node_name):
            return False

        if node_name in dict_of_actions:
            return dict_of_actions[node_name](
                script=self,
                node_name=node_name,
            )

        return True
