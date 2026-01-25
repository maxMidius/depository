#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------

import uuid
from typing import Optional, Callable
from nicegui import ui
from rich import print


class ManimPlayer:
    """A NiceGUI component for displaying Manim animations via HTML5 video player.

    This component follows the same pattern as NiceCytoWrap, providing a consistent
    interface for embedding and controlling manim video playback in NiceGUI applications.
    """

    def __init__(
        self,
        width: str = "100%",
        height: str = "600px",
        controls: bool = True,
        autoplay: bool = False,
        loop: bool = False,
        on_play: Optional[Callable[[], None]] = None,
        on_pause: Optional[Callable[[], None]] = None,
        on_ended: Optional[Callable[[], None]] = None,
    ):
        """
        Initialize the ManimPlayer.

        Args:
            width: Width of the video player (default "100%")
            height: Height of the video player (default "600px")
            controls: Show video controls (default True)
            autoplay: Auto-play video when loaded (default False)
            loop: Loop video playback (default False)
            on_play: Callback when video starts playing
            on_pause: Callback when video is paused
            on_ended: Callback when video ends
        """
        self.width = width
        self.height = height
        self.controls = controls
        self.autoplay = autoplay
        self.loop = loop
        self.container_id = f"manim-{uuid.uuid4().hex[:8]}"
        self.video_id = f"{self.container_id}-video"

        # Callbacks
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_ended = on_ended

        # State
        self.current_video_url: Optional[str] = None
        self.is_mounted = False

        print(f"ManimPlayer created with ID: {self.container_id}")

    def mount_container(self) -> None:
        """Create the HTML5 video player container in the NiceGUI UI."""
        controls_attr = "controls" if self.controls else ""
        autoplay_attr = "autoplay" if self.autoplay else ""
        loop_attr = "loop" if self.loop else ""

        html = f'''
        <div id="{self.container_id}" style="width: {self.width}; height: {self.height}; display: flex; align-items: center; justify-content: center; background: #000;">
            <video id="{self.video_id}"
                   {controls_attr}
                   {autoplay_attr}
                   {loop_attr}
                   style="width: 100%; height: 100%; object-fit: contain;"
                   preload="metadata">
                <source src="" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        '''

        ui.html(html,sanitize=False)
        self.is_mounted = True

        # Setup event listeners if callbacks are provided
        if self.on_play or self.on_pause or self.on_ended:
            self._setup_event_listeners()

        print(f"ManimPlayer container mounted: {self.container_id}")

    def _setup_event_listeners(self) -> None:
        """Setup JavaScript event listeners for video events."""
        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (!video) {{
                console.warn("Video element not found: {self.video_id}");
                return;
            }}

            video.addEventListener("play", function() {{
                console.log("Manim video started playing");
                // Could trigger Python callback via FastAPI route if needed
            }});

            video.addEventListener("pause", function() {{
                console.log("Manim video paused");
            }});

            video.addEventListener("ended", function() {{
                console.log("Manim video ended");
            }});
        }})();
        '''

        ui.run_javascript(js_code)

    def load_video(self, video_url: str) -> None:
        """
        Load a video into the player.

        Args:
            video_url: URL to the video file (relative or absolute)
        """
        if not self.is_mounted:
            raise RuntimeError("Container must be mounted before loading video. Call mount_container() first.")

        js_code = f'''
        (function() {{
            console.log("Attempting to load video: {video_url}");

            var video = document.getElementById("{self.video_id}");
            if (!video) {{
                console.error("Video element not found: {self.video_id}");
                return;
            }}

            console.log("Video element found:", video);

            // Add error event listener
            video.addEventListener('error', function(e) {{
                console.error("Video error:", e);
                console.error("Video error code:", video.error ? video.error.code : "unknown");
                console.error("Video error message:", video.error ? video.error.message : "unknown");
            }}, false);

            // Add loadedmetadata event listener
            video.addEventListener('loadedmetadata', function() {{
                console.log("Video metadata loaded successfully");
                console.log("Video duration:", video.duration);
                console.log("Video dimensions:", video.videoWidth, "x", video.videoHeight);
            }}, false);

            var source = video.querySelector("source");
            if (source) {{
                console.log("Updating existing source");
                source.src = "{video_url}";
            }} else {{
                console.log("Creating new source element");
                source = document.createElement("source");
                source.src = "{video_url}";
                source.type = "video/mp4";
                video.appendChild(source);
            }}

            video.load();
            console.log("Video load() called for: {video_url}");
        }})();
        '''

        ui.run_javascript(js_code)
        self.current_video_url = video_url
        print(f"Loaded video: {video_url}")

    def play(self) -> None:
        """Start or resume video playback."""
        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (video) {{
                video.play().catch(function(err) {{
                    console.error("Error playing video:", err);
                }});
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def pause(self) -> None:
        """Pause video playback."""
        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (video) {{
                video.pause();
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def seek(self, time_seconds: float) -> None:
        """
        Seek to a specific time in the video.

        Args:
            time_seconds: Time in seconds to seek to
        """
        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (video) {{
                video.currentTime = {time_seconds};
                console.log("Seeked to {time_seconds} seconds");
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def set_playback_rate(self, rate: float) -> None:
        """
        Set video playback speed.

        Args:
            rate: Playback rate (0.5 = half speed, 1.0 = normal, 2.0 = double speed)
        """
        if rate <= 0:
            raise ValueError("Playback rate must be positive")

        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (video) {{
                video.playbackRate = {rate};
                console.log("Set playback rate to {rate}x");
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def set_volume(self, volume: float) -> None:
        """
        Set video volume.

        Args:
            volume: Volume level (0.0 = muted, 1.0 = maximum)
        """
        if not 0 <= volume <= 1:
            raise ValueError("Volume must be between 0 and 1")

        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (video) {{
                video.volume = {volume};
                console.log("Set volume to {volume}");
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode for the video player."""
        js_code = f'''
        (function() {{
            var video = document.getElementById("{self.video_id}");
            if (!video) return;

            if (!document.fullscreenElement) {{
                video.requestFullscreen().catch(function(err) {{
                    console.error("Error entering fullscreen:", err);
                }});
            }} else {{
                document.exitFullscreen();
            }}
        }})();
        '''
        ui.run_javascript(js_code)

    def reset_view(self) -> None:
        """Reset video to beginning and pause."""
        self.seek(0)
        self.pause()
