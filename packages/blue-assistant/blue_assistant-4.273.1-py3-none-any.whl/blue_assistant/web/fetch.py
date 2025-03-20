from typing import Dict, Any
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import urljoin
import re
import warnings

from blueness import module
from blue_options.logger import log_long_text, log_list

from blue_assistant import NAME
from blue_assistant.logger import logger

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

NAME = module.name(__file__, NAME)


def fetch_links_and_text(
    url: str,
    verbose: bool = False,
) -> Dict[str, Any]:
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        logger.warning(e)
        return {}

    if response.status_code != 200:
        logger.error(response)
        return {}

    content_type = response.headers.get("Content-Type", "")
    logger.info(f"content-type: {content_type}")

    links = set()
    text = ""

    if not any(
        thing in content_type
        for thing in [
            "pdf",
            "xml",
        ]
    ):
        soup = BeautifulSoup(response.text, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            a_url = urljoin(url, a_tag["href"])

            if a_url.startswith(url):
                logger.info(f"+= {a_url}")
                links.add(a_url)
                continue

            logger.info(f"ignored: {a_url}")

        text = soup.get_text(separator=" ", strip=True)

    # remove non-ASCII characters
    text = re.sub(r"[^\x20-\x7E]+", "", text)
    for thing in ["\r", "\n", "\t"]:
        text = text.replace(thing, " ")
    text = re.sub(r"\s+", " ", text).strip()

    if verbose:
        log_list(logger, list(links), "link(s)")
        log_long_text(logger, text)

    return {
        "url": url,
        "content_type": content_type,
        "links": links,
        "text": text,
    }
