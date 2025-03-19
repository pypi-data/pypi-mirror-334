from typing import Dict, List
import os
import networkx as nx
from functools import reduce

from blueness import module
from blue_objects import file, objects
from blue_objects.metadata import post_to_object
from blueflow.workflow import dot_file

from blue_assistant import NAME
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


class BaseScript:
    name = "base"

    def __init__(
        self,
        object_name: str,
        test_mode: bool = False,
        verbose: bool = False,
    ):
        self.object_name = object_name

        self.test_mode = test_mode
        if self.test_mode:
            logger.info("💰 test mode is on.")

        self.verbose = verbose

        metadata_filename = os.path.join(
            file.path(__file__),
            f"../{self.name}",
            "metadata.yaml",
        )
        self.metadata: Dict
        success, self.metadata = file.load_yaml(metadata_filename)
        assert success, f"cannot load {self.name}/metadata.yaml"

        logger.info("loaded {} node(s)".format(len(self.nodes)))

        logger.info("loaded {} variable(s)".format(len(self.vars)))
        if verbose:
            for var_name, var_value in self.vars.items():
                logger.info("{}: {}".format(var_name, var_value))

        assert self.generate_graph(), "cannot generate graph"

    def apply_vars(self, text: str) -> str:
        for var_name, var_value in self.vars.items():
            text = text.replace(f":::{var_name}", str(var_value))

        return text

    def generate_graph(self) -> bool:
        self.G: nx.DiGraph = nx.DiGraph()

        list_of_nodes = list(self.nodes.keys())
        for node in self.nodes.values():
            list_of_nodes += node.get("depends-on", "").split(",")

        list_of_nodes = list({node_name for node_name in list_of_nodes if node_name})
        logger.info(
            "{} node(s): {}".format(
                len(list_of_nodes),
                ", ".join(list_of_nodes),
            )
        )

        for node_name in list_of_nodes:
            self.G.add_node(node_name)

        for node_name, node in self.nodes.items():
            for dependency in node.get("depends-on", "").split(","):
                if dependency:
                    self.G.add_edge(node_name, dependency)

        return self.save_graph()

    def get_context(
        self,
        node_name: str,
    ) -> List[str]:
        return reduce(
            lambda x, y: x + y,
            [self.get_context(successor) for successor in self.G.successors(node_name)],
            [node_name],
        )

    def run(self) -> bool:
        logger.info(
            "{}.run: {}:{} -> {}".format(
                NAME,
                self.__class__.__name__,
                self.name,
                self.object_name,
            )
        )

        return post_to_object(
            self.object_name,
            "script",
            self.script,
        )

    def save_graph(self) -> bool:
        return dot_file.save_to_file(
            objects.path_of(
                filename="workflow.dot",
                object_name=self.object_name,
            ),
            self.G,
            caption=" | ".join(
                [
                    self.name,
                    self.object_name,
                ]
            ),
            add_legend=False,
        )

    # Aliases
    @property
    def script(self) -> Dict:
        return self.metadata.get("script", {})

    @property
    def nodes(self) -> Dict[str, Dict]:
        return self.metadata.get("script", {}).get("nodes", {})

    @property
    def vars(self) -> Dict:
        return self.metadata.get("script", {}).get("vars", {})
