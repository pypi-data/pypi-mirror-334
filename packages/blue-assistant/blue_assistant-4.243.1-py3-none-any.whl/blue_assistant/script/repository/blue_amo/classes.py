import copy

from blueness import module
from blue_objects import file, path

from blue_assistant import NAME
from blue_assistant.script.repository.generic.classes import GenericScript
from blue_assistant.script.repository.blue_amo.actions import dict_of_actions
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


class BlueAmoScript(GenericScript):
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
            self.vars["frame_count"] = 1

        holder_node_name = "generating_the_frames"
        logger.info(
            "{}: expanding {} X {}...".format(
                NAME,
                holder_node_name,
                self.vars["frame_count"],
            )
        )

        holder_node = self.nodes[holder_node_name]
        del self.nodes[holder_node_name]
        self.G.remove_node(holder_node_name)

        reduce_node = "stitching_the_frames"
        self.G.add_node(reduce_node)
        self.nodes[reduce_node] = {"action": "generic"}

        for index in range(self.vars["frame_count"]):
            node_name = f"generating_frame_{index+1:03d}"

            self.nodes[node_name] = copy.deepcopy(holder_node)

            self.G.add_node(node_name)
            self.G.add_edge(
                node_name,
                "slicing_into_frames",
            )
            self.G.add_edge(
                reduce_node,
                node_name,
            )

        assert self.save_graph()

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
