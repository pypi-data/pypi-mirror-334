from typing import Dict
from blueness import module
from tqdm import tqdm

from blue_options.logger import log_list
from openai_commands.text_generation import api

from blue_assistant import NAME
from blue_assistant.web.functions import crawl_list_of_urls
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


def web_crawl(
    script: BaseScript,
    node_name: str,
) -> bool:
    logger.info(f"{NAME}: {script} @ {node_name} ...")

    seed_url_var_name = script.nodes[node_name].get("seed_urls", "")
    if not isinstance(seed_url_var_name, str):
        logger.error(f"{node_name}: seed_urls must be a string.")
        return False
    # to allow both :::<var-name> and <var-name> - for convenience :)
    if seed_url_var_name.startswith(":::"):
        seed_url_var_name = seed_url_var_name[3:].strip()
    if not seed_url_var_name:
        logger.error(f"{node_name}: seed_urls not found.")
        return False
    if seed_url_var_name not in script.vars:
        logger.error(f"{node_name}: {seed_url_var_name}: seed_urls not found in vars.")
        return False

    seed_urls = script.vars[seed_url_var_name]
    log_list(logger, seed_urls, "seed url(s)")

    visited_urls = crawl_list_of_urls(
        seed_urls=seed_urls,
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
