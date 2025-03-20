import enum
from datetime import datetime

from typing import Optional, Any

from .element import Element
from .submodule import Container


class Camera(Container):
    type = "uiCamera"

    def __init__(
        self,
        name,
        display_name: str = None,
        uri: str = None,
        output_type: str = None,
        mp4_output_length: int = None,
        wake_delay: int = 5,
        children: Optional[list[Element]] = None,
        **kwargs,
    ):
        super().__init__(name, display_name, children=children, **kwargs, is_available=None, help_str=None)
        # fixme: do we need to specify is_available and help_str to be None?

        self.uri = uri
        self.output_type = output_type
        self.mp4_output_length = mp4_output_length
        self.wake_delay = wake_delay

class CameraHistory(Camera):
    type = "uiCameraFeed"


doover_ui_camera = Camera
doover_ui_camera_history = CameraHistory