#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Simple test script to verify manim player works
"""

from pathlib import Path
from nicegui import ui, app
import sys

sys.path.insert(0, str(Path(__file__).parent))
from player import ManimPlayer

# Setup static files
ROOT = Path(__file__).resolve().parent
app.add_static_files('/static', str(ROOT / 'static'))

print(f"Static files served from: {ROOT / 'static'}")
print(f"Checking for videos in: {ROOT / 'static/renders'}")

# List available videos
renders_dir = ROOT / 'static/renders'
if renders_dir.exists():
    videos = list(renders_dir.glob("*.mp4"))
    print(f"Found {len(videos)} video(s):")
    for video in videos:
        print(f"  - {video.name} ({video.stat().st_size / 1024:.1f} KB)")
else:
    print("No renders directory found!")

@ui.page('/')
def test_page():
    """Simple test page"""
    ui.label("Manim Player Test").style("font-size: 2em; font-weight: bold; margin-bottom: 20px")

    # Create player
    player = ManimPlayer(width="800px", height="600px")
    player.mount_container()

    # Load video buttons
    ui.label("Load a video:").style("margin-top: 20px; font-weight: bold")

    with ui.row().style("gap: 10px; margin-top: 10px"):
        if renders_dir.exists():
            for video in renders_dir.glob("*.mp4"):
                video_url = f"/static/renders/{video.name}"
                ui.button(
                    video.stem,
                    on_click=lambda url=video_url, name=video.stem: (
                        player.load_video(url),
                        ui.notify(f"Loading: {name}", type="info")
                    )
                )

    # Player controls
    ui.label("Controls:").style("margin-top: 20px; font-weight: bold")
    with ui.row().style("gap: 10px; margin-top: 10px"):
        ui.button("Play", on_click=lambda: player.play(), icon="play_arrow")
        ui.button("Pause", on_click=lambda: player.pause(), icon="pause")
        ui.button("Reset", on_click=lambda: player.reset_view(), icon="replay")

    # Instructions
    ui.markdown("""
    ### Debug Instructions:

    1. Open browser developer console (F12)
    2. Click a button to load a video
    3. Check console for any errors or messages
    4. Look for:
       - "Attempting to load video: /static/renders/..."
       - "Video element found"
       - "Video metadata loaded successfully"
    5. If you see errors, check:
       - Network tab to see if video file is being requested
       - If 404 error, the static path is wrong
       - If CORS error, check server configuration
    """)

if __name__ in {"__main__", "__mp_main__"}:
    print("\nStarting test server...")
    print("Open http://localhost:8080 in your browser")
    print("Then check the browser console (F12) for debug messages\n")

    ui.run(
        title="Manim Player Test",
        port=8080,
        reload=False
    )
