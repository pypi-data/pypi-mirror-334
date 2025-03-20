import os

from blue_options.help.functions import get_help
from blue_objects import file, README

from blue_assistant import NAME, VERSION, ICON, REPO_NAME
from blue_assistant.help.functions import help_functions


items = README.Items(
    [
        {
            "name": "orbital-data-explorer",
            "url": "./blue_assistant/script/repository/orbital_data_explorer",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-assistant/PDS/uahirise-ESP_086795_1970.png?raw=true",
            "description": "Poking around [Orbital Data Explorer](https://ode.rsl.wustl.edu/) with an [AI DAG](./blue_assistant/script/repository/orbital_data_explorer/metadata.yaml). ⏸️",
        },
        {
            "name": "@hue",
            "url": "./blue_assistant/script/repository/hue",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-assistant/20250314_143702-2.png?raw=true",
            "description": '"[Hey AI](./blue_assistant/script/repository/hue/metadata.yaml), help me write code to send color commands to the [Hue LED lights](https://www.philips-hue.com/en-ca) in my apartment."',
        },
        {
            "name": "blue-amo",
            "url": "./blue_assistant/script/repository/blue_amo/README.md",
            "marquee": "https://github.com/kamangir/assets/blob/main/test_blue_assistant_script_run-2025-03-15-06pbpf/generating_frame_007.png?raw=true",
            "description": "Story development and visualization, with an [AI DAG](./blue_assistant/script/repository/blue_amo/metadata.yaml).",
        },
        {
            "name": "🌀 blue script",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true",
            "description": "A minimal AI DAG interface.",
            "url": "./blue_assistant/script/",
        },
        {},
        {
            "name": "`@web`",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true",
            "description": "A minimal web interface for an AI agent.",
            "url": "./blue_assistant/web/",
        },
    ]
)


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            cols=readme.get("cols", 3),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
            help_function=lambda tokens: get_help(
                tokens,
                help_functions,
                mono=True,
            ),
        )
        for readme in [
            {
                "items": items,
                "cols": 3,
                "path": "..",
            },
            {"path": "script/repository/blue_amo"},
            #
            {"path": "script/repository/orbital_data_explorer/docs/round-1.md"},
            {"path": "script/repository/orbital_data_explorer/docs"},
            #
            {"path": "script/repository/hue/docs/round-1.md"},
            {"path": "script/repository/hue/docs"},
            #
            {"path": "script/"},
            {"path": "web/"},
        ]
    )
