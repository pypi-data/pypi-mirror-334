from typing import List

from blueness import module
from openai_commands.text_generation import api

from blue_assistant import NAME
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.env import (
    BLUE_ASSISTANT_TEXT_DEFAULT_MODEL,
    BLUE_ASSISTANT_TEXT_MAX_TOKENS,
)
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


# https://platform.openai.com/docs/guides/text-generation
def generate_text(
    script: BaseScript,
    node_name: str,
) -> bool:
    logger.info(f"{NAME}: {script} @ {node_name} ...")

    messages: List = []
    list_of_context_nodes = script.get_context(node_name)
    logger.info("node context: {}".format(" <- ".join(list_of_context_nodes)))
    for context_node in reversed(list_of_context_nodes):
        messages += [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": script.apply_vars(script.nodes[context_node]["prompt"]),
                    }
                ],
            }
        ]

        if script.nodes[context_node].get("completed", False):
            messages += [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": script.nodes[context_node].get("output", ""),
                        }
                    ],
                }
            ]

    success, output, _ = api.generate_text(
        messages=messages,
        model=BLUE_ASSISTANT_TEXT_DEFAULT_MODEL,
        max_tokens=BLUE_ASSISTANT_TEXT_MAX_TOKENS,
        verbose=script.verbose,
    )
    if not success:
        return success

    logger.info(f"🗣️ output: {output}")
    script.nodes[node_name]["output"] = output

    return True
