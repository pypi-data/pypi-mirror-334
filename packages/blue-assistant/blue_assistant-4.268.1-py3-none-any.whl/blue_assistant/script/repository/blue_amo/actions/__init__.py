from typing import Dict, Callable

from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.script.repository.blue_amo.actions import (
    slicing_into_frames,
    stitching_the_frames,
)


dict_of_actions: Dict[str, Callable[[BaseScript, str], bool]] = {
    "slicing_into_frames": slicing_into_frames.slicing_into_frames,
    "stitching_the_frames": stitching_the_frames.stitching_the_frames,
}
