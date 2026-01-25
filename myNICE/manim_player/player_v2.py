#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Alternative ManimPlayer using NiceGUI's built-in video element
"""

import uuid
from typing import Optional, Callable
from nicegui import ui
from rich import print


class ManimPlayerV2:
    """A NiceGUI component for displaying Manim animations using built-in ui.video."""

    def __init__(
        self,
        width: str = "100%",
        height: str = "600px",
        controls: bool = True,
        autoplay: bool = False,
        loop: bool = False,
    ):
        """
        Initialize the ManimPlayer.

        Args:
            width: Width of the video player (default "100%")
            height: Height of the video player (default "600px")
            controls: Show video controls (default True)
            autoplay: Auto-play video when loaded (default False)
            loop: Loop video playback (default False)
        """
        self.width = width
        self.height = height
        self.controls = controls
        self.autoplay = autoplay
        self.loop = loop
        self.container_id = f"manim-v2-{uuid.uuid4().hex[:8]}"

        # State
        self.current_video_url: Optional[str] = None
        self.is_mounted = False
        self.video_element = None

        print(f"ManimPlayerV2 created with ID: {self.container_id}")

    def mount_container(self) -> None:
        """Create the video player container using NiceGUI's built-in video element."""

        # Use NiceGUI's built-in video element
        self.video_element = ui.video(
            src="",  # Will be set later
            controls=self.controls,
            autoplay=self.autoplay,
            loop=self.loop
        ).style(f"width: {self.width}; height: {self.height}; background: #000;")

        self.is_mounted = True
        print(f"ManimPlayerV2 container mounted: {self.container_id}")

    def load_video(self, video_url: str) -> None:
        """
        Load a video into the player.

        Args:
            video_url: URL to the video file (relative or absolute)
        """
        if not self.is_mounted or self.video_element is None:
            raise RuntimeError("Container must be mounted before loading video. Call mount_container() first.")

        print(f"Loading video: {video_url}")

        # Update the source using NiceGUI's API
        self.video_element.set_source(video_url)
        self.current_video_url = video_url

        print(f"Video source set to: {video_url}")

    def play(self) -> None:
        """Start or resume video playback."""
        if self.video_element:
            js_code = '''
            const videos = document.getElementsByTagName("video");
            if (videos.length > 0) {
                const video = videos[videos.length - 1];  // Get last video element
                video.play();
                console.log("Playing video");
            }
            '''
            ui.run_javascript(js_code)

    def pause(self) -> None:
        """Pause video playback."""
        if self.video_element:
            js_code = '''
            const videos = document.getElementsByTagName("video");
            if (videos.length > 0) {
                const video = videos[videos.length - 1];
                video.pause();
                console.log("Paused video");
            }
            '''
            ui.run_javascript(js_code)

    def reset_view(self) -> None:
        """Reset video to beginning."""
        if self.video_element:
            js_code = '''
            const videos = document.getElementsByTagName("video");
            if (videos.length > 0) {
                const video = videos[videos.length - 1];
                video.currentTime = 0;
                video.pause();
                console.log("Reset video");
            }
            '''
            ui.run_javascript(js_code)
