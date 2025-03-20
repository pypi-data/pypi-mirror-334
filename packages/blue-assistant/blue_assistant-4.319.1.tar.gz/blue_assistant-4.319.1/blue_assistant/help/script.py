from typing import List

from blue_options.terminal import show_usage, xtra

from blue_assistant.script.repository import list_of_script_names


def help_list(
    tokens: List[str],
    mono: bool,
) -> str:
    args = [
        "[--delim +]",
        "[--log 0]",
    ]

    return show_usage(
        [
            "@assistant",
            "script",
            "list",
        ]
        + args,
        "list scripts.",
        mono=mono,
    )


def help_run(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("~download,dryrun,~upload", mono=mono)

    script_options = "script=<script>"

    args = [
        "[--test_mode 1]",
        "[--verbose 1]",
        "[--runnable <~node_1,~node_2>]",
    ]

    return show_usage(
        [
            "@assistant",
            "script",
            "run",
            f"[{options}]",
            f"[{script_options}]",
            "[-|<object-name>]",
        ]
        + args,
        "run <object-name>.",
        {
            "script: {}".format(" | ".join(list_of_script_names)): [],
        },
        mono=mono,
    )


help_functions = {
    "list": help_list,
    "run": help_run,
}
