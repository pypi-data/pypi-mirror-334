from typing import Dict
from blueness import module
from tqdm import tqdm

from openai_commands.text_generation import api

from blue_assistant import NAME
from blue_assistant.web.functions import crawl_list_of_urls
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


def researching_the_questions(
    script: BaseScript,
    node_name: str,
) -> bool:
    logger.info(f"{NAME}: ...")

    visited_urls = crawl_list_of_urls(
        seed_urls=script.vars["seed_urls"],
        object_name=script.object_name,
        max_iterations=script.nodes[node_name]["max_iterations"],
    )

    success, output, _ = api.generate_text(
        prompt=script.nodes[node_name]["prompt"].replace(
            ":::input", " ".join([content for content in visited_urls.values()])
        ),
        verbose=script.verbose,
    )
    if not success:
        return success

    logger.info(output)

    script.nodes[node_name]["visited_urls"] = visited_urls
    script.nodes[node_name]["output"] = output

    return True
