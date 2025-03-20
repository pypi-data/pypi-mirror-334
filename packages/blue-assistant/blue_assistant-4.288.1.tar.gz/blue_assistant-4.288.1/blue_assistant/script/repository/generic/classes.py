from typing import Dict, List
import os
from tqdm import tqdm


from blueness import module
from blue_objects import file, path
from blue_objects.metadata import post_to_object

from blue_assistant import NAME
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.script.actions import dict_of_actions
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


class GenericScript(BaseScript):
    name = path.name(file.path(__file__))

    def perform_action(
        self,
        node_name: str,
        use_cache: bool,
    ) -> bool:
        action_name = self.nodes[node_name].get("action", "unknown")
        logger.info(f"---- node: {node_name} ---- ")

        if action_name not in dict_of_actions:
            logger.error(f"{action_name}: action not found.")
            return False

        return dict_of_actions[action_name](
            script=self,
            node_name=node_name,
            use_cache=use_cache,
        )

    def run(
        self,
        use_cache: bool = True,
    ) -> bool:
        if not super().run(use_cache=use_cache):
            return False

        success: bool = True
        while (
            not all(self.nodes[node].get("completed", False) for node in self.nodes)
            and success
        ):
            for node_name in tqdm(self.nodes):
                if self.nodes[node_name].get("completed", False):
                    continue

                if not self.nodes[node_name].get("runnable", True):
                    logger.info(f"Not runnable, skipped: {node_name}.")
                    self.nodes[node_name]["completed"] = True
                    continue

                pending_dependencies = [
                    node_name_
                    for node_name_ in self.G.successors(node_name)
                    if not self.nodes[node_name_].get("completed", False)
                ]
                if pending_dependencies:
                    logger.info(
                        'node "{}": {} pending dependenci(es): {}'.format(
                            node_name,
                            len(pending_dependencies),
                            ", ".join(pending_dependencies),
                        )
                    )
                    continue

                if not self.perform_action(
                    node_name=node_name,
                    use_cache=use_cache,
                ):
                    success = False
                    break

                self.nodes[node_name]["completed"] = True

        if not post_to_object(
            self.object_name,
            "output",
            self.metadata,
        ):
            return False

        return success
