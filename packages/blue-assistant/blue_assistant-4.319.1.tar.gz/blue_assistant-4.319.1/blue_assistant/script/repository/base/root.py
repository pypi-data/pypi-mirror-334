import os
from typing import Dict, List
from functools import reduce
import networkx as nx
from tqdm import tqdm

from blue_options.options import Options
from blue_objects import file, path, objects
from blue_objects.metadata import post_to_object
from blueflow.workflow import dot_file

from blue_assistant.logger import logger


class RootScript:
    name = path.name(file.path(__file__))

    def __init__(
        self,
        object_name: str,
        test_mode: bool = False,
        verbose: bool = False,
    ):
        self.nodes_changed = False

        self.object_name = object_name

        self.test_mode = test_mode

        self.verbose = verbose

        self.dict_of_actions = {}

        metadata_filename = os.path.join(
            file.path(__file__),
            f"../{self.name}",
            "metadata.yaml",
        )
        self.metadata: Dict
        success, self.metadata = file.load_yaml(metadata_filename)
        assert success, f"cannot load {self.name}/metadata.yaml"

        self.metadata.setdefault("script", {})
        assert isinstance(
            self.script,
            dict,
        ), "script: expected dict, received {}.".format(
            self.script.__class__.__name__,
        )

        self.script.setdefault("nodes", {})
        assert isinstance(
            self.nodes,
            dict,
        ), "nodes: expected dict, received {}.".format(
            self.nodes.__class__.__name__,
        )

        self.script.setdefault("vars", {})
        assert isinstance(
            self.vars,
            dict,
        ), "vars: expected dict, received {}.".format(
            self.vars.__class__.__name__,
        )

        if self.test_mode:
            logger.info("🧪  test mode is on.")

            if "test_mode" in self.script:
                updates = self.script["test_mode"]
                logger.info(f"🧪  vars.update({updates})")
                self.vars.update(updates)

            for node_name, node in self.nodes.items():
                if "test_mode" in node:
                    updates = node["test_mode"]
                    logger.info(f"🧪  {node_name}.update({updates})")
                    node.update(updates)

        logger.info(
            "loaded {} node(s): {}".format(
                len(self.nodes),
                ", ".join(self.nodes.keys()),
            )
        )

        logger.info(
            "loaded {} var(s): {}".format(
                len(self.vars),
                ", ".join(self.vars.keys()),
            )
        )
        if verbose:
            for var_name, var_value in self.vars.items():
                logger.info("{}: {}".format(var_name, var_value))

        assert self.generate_graph(), "cannot generate graph."

    def __str__(self) -> str:
        return "{}[{} var(s), {} node(s) -> {}]".format(
            self.__class__.__name__,
            len(self.vars),
            len(self.nodes),
            self.object_name,
        )

    def apply_vars(self, text: str) -> str:
        for var_name, var_value in self.vars.items():
            text = text.replace(f":::{var_name}", str(var_value))

        for node_name, node in self.nodes.items():
            node_output = node.get("output", "")
            if isinstance(node_output, str):
                text = text.replace(f":::{node_name}", node_output)

        return text

    def generate_graph(
        self,
        verbose: bool = False,
    ) -> bool:
        self.G: nx.DiGraph = nx.DiGraph()

        list_of_nodes = list(self.nodes.keys())
        for node in self.nodes.values():
            list_of_nodes += node.get("depends-on", "").split(",")

        list_of_nodes = list({node_name for node_name in list_of_nodes if node_name})
        if verbose:
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

    def perform_action(
        self,
        node_name: str,
    ) -> bool:
        action_name = self.nodes[node_name].get("action", "unknown")
        logger.info(f"---- node: {node_name} ---- ")

        if action_name in self.dict_of_actions:
            return self.dict_of_actions[action_name](
                script=self,
                node_name=node_name,
            )

        logger.error(f"{action_name}: action not found.")
        return False

    def run(
        self,
        runnable: str = "",
    ) -> bool:
        logger.info(f"{self.name}.run -> {self.object_name}")

        if runnable:
            logger.info(f"applying runnables: {runnable}")
            runnable_options = Options(runnable)
            for node_name, node_is_runnable in runnable_options.items():
                logger.info(f"{node_name}.runnable={node_is_runnable}")
                self.nodes[node_name]["runnable"] = node_is_runnable

        success: bool = True
        while (
            not all(self.nodes[node].get("completed", False) for node in self.nodes)
            and success
        ):
            self.nodes_changed = False

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

                if not self.perform_action(node_name=node_name):
                    success = False
                    break

                self.nodes[node_name]["completed"] = True

                cache_filename = self.nodes[node_name].get("cache", "")
                if cache_filename:
                    if not file.save_text(
                        objects.path_of(
                            object_name=self.object_name,
                            filename=cache_filename,
                        ),
                        [self.nodes[node_name].get("output", "")],
                    ):
                        success = False
                        break

                if self.nodes_changed:
                    logger.info("🪄  nodes changed.")
                    break

        if not post_to_object(
            self.object_name,
            "output",
            self.metadata,
        ):
            success = False

        return success

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
        return self.metadata["script"]

    @property
    def nodes(self) -> Dict[str, Dict]:
        return self.metadata["script"]["nodes"]

    @property
    def vars(self) -> Dict:
        return self.metadata["script"]["vars"]
