NAME = "blue_assistant"

ICON = "🧠"

DESCRIPTION = f"{ICON} An AI Assistant."

VERSION = "4.380.1"

REPO_NAME = "blue-assistant"

MARQUEE = (
    "https://github.com/kamangir/assets/raw/main/blue-assistant/marquee.png?raw=true"
)

ALIAS = "@assistant"


def fullname() -> str:
    return f"{NAME}-{VERSION}"
