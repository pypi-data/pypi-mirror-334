from typing import List, Dict, Set

from blueness import module
from blue_objects import file
from blue_objects import objects
from blue_objects.metadata import get_from_object, post_to_object

from blue_assistant import NAME
from blue_assistant.web.fetch import fetch_links_and_text
from blue_assistant.web.functions import url_to_filename
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


def crawl_list_of_urls(
    seed_urls: List[str],
    object_name: str,
    max_iterations: int = 10,
    use_cache: bool = False,
    verbose: bool = False,
) -> Dict[str, str]:
    logger.info(
        "{}.crawl_list_of_urls({}): {} -{}> {}".format(
            NAME,
            len(seed_urls),
            ", ".join(seed_urls),
            "use-cache-" if use_cache else "",
            object_name,
        )
    )

    crawl_cache: Dict[str, str] = (
        get_from_object(
            object_name,
            "crawl_cache",
            {},
        )
        if use_cache
        else {}
    )

    queue: Set[str] = set(seed_urls)

    iteration: int = 0
    while queue:
        url = queue.pop()
        logger.info(
            "{} {} ...".format(
                "✅" if url in crawl_cache else "🔗",
                url,
            )
        )
        if url in crawl_cache:
            continue

        url_summary = fetch_links_and_text(
            url=url,
            verbose=verbose,
        )
        content_type = url_summary.get("content_type", "unknown")

        if use_cache and "html" in content_type:
            file.save_yaml(
                filename=objects.path_of(
                    object_name=object_name,
                    filename="crawl_summary_cache/{}.yaml".format(url_to_filename(url)),
                ),
                data=url_summary,
            )

        crawl_cache[url] = content_type
        if "links" in url_summary:
            queue.update(url_summary["links"] - crawl_cache.keys())

        iteration += 1
        if max_iterations != -1 and iteration >= max_iterations:
            logger.warning(f"max iteration of {max_iterations} reached.")
            break

    if queue:
        logger.warning(f"queue: {len(queue)}")

    if use_cache:
        post_to_object(
            object_name,
            "crawl_cache",
            crawl_cache,
        )

    return crawl_cache
