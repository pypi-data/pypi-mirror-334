import os

from blue_objects import file, README

from blue_assistant import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "hue",
            "url": "./blue_assistant/script/repository/hue",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-assistant/20250314_143702.jpg?raw=true",
            "description": '"send a color command to the Hue LED lights in my apartment."',
        },
        {
            "name": "blue-amo",
            "url": "./blue_assistant/script/repository/blue_amo/README.md",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-amo-2025-02-03-nswnx6/stitching_the_frames-2.png?raw=true",
            "description": "A story developed and visualized, by AI.",
        },
        {
            "name": "orbital-data-explorer",
            "url": "./blue_assistant/script/repository/orbital_data_explorer",
            "marquee": "https://github.com/kamangir/assets/blob/main/blue-assistant/orbital-data-explorer.png?raw=true",
            "description": "Access to the [Orbital Data Explorer](https://ode.rsl.wustl.edu/), through AI. ⏸️",
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
        )
        for readme in [
            {
                "items": items,
                "cols": 2,
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
            {"path": "web/"},
        ]
    )
