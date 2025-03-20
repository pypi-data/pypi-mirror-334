from typing import List, Dict, Set, Tuple
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


def url_to_filename(
    url: str,
    max_length: int = 255,
) -> str:
    # Remove the URL scheme (http://, https://)
    filename = re.sub(r"^https?://", "", url)

    # Replace unwanted characters with an underscore
    filename = re.sub(r"[^\w\s-]", "_", filename)

    # Replace slashes with a hyphen to preserve some structure
    filename = re.sub(r"\/", "-", filename)

    # Replace spaces with underscores
    filename = filename.replace(" ", "_")

    # Ensure the filename length is not too long
    if len(filename) > max_length:
        filename = filename[:max_length]

    return filename
