#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Manim Player Demo Application

This demo showcases:
1. Gallery of available manim scenes
2. Render on-demand capability
3. Video playback with controls
4. Hybrid view combining Cytoscape + Manim (optional)
"""

from pathlib import Path
from nicegui import ui, app
from rich import print

# Add parent directories to path
import sys
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "explainer"))

from player import ManimPlayer
from manim_manager import ManimRenderManager

# ---------------------------------------------------------------------
# Static files setup
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / 'static'
print(f"ROOT directory: {ROOT}")
print(f"STATIC directory: {STATIC_DIR}")
print(f"STATIC directory exists: {STATIC_DIR.exists()}")

# Mount static files
app.add_static_files('/static', str(STATIC_DIR))
print(f"Static files mounted at /static -> {STATIC_DIR}")

# ---------------------------------------------------------------------
# Initialize Manim Manager
# ---------------------------------------------------------------------
manager = ManimRenderManager(
    scenes_dir=ROOT / 'scenes',
    output_dir=ROOT / 'static' / 'renders'
)

# Global state
player: ManimPlayer = None
current_scene = None
render_status = None


# ---------------------------------------------------------------------
# UI Functions
# ---------------------------------------------------------------------

def create_scene_card(scene_info):
    """Create a card for a scene in the gallery."""
    with ui.card().classes('w-80'):
        ui.label(scene_info.name).style(
            "font-weight: bold; font-size: 1.1em; margin-bottom: 5px"
        )
        ui.label(f"Category: {scene_info.category}").style(
            "color: #888; font-size: 0.9em"
        )
        ui.label(scene_info.description).style(
            "margin-top: 10px; margin-bottom: 15px"
        )

        # Check if video is cached
        cached = manager.get_cached_video(scene_info.name)
        if cached:
            metadata = manager.get_video_metadata(scene_info.name)
            size_mb = metadata.get('file_size_mb', 0) if metadata else 0
            ui.label(f"✓ Cached ({size_mb} MB)").style("color: green; font-size: 0.85em")

        with ui.row().style("gap: 10px; margin-top: 10px"):
            ui.button(
                "Play",
                on_click=lambda s=scene_info: load_and_play_scene(s),
                color="primary"
            ).classes('flex-1')

            ui.button(
                "Render",
                on_click=lambda s=scene_info: render_scene_interactive(s),
                color="secondary"
            ).classes('flex-1')


def load_and_play_scene(scene_info):
    """Load scene into player and start playback."""
    global current_scene, player

    print(f"Loading scene: {scene_info.name}")

    # Check if player exists
    if player is None:
        ui.notify(
            "Please visit the 'Player' tab first to initialize the video player.",
            type="warning"
        )
        return

    # Check if cached
    cached_video = manager.get_cached_video(scene_info.name)

    if cached_video:
        video_url = f"/static/renders/{scene_info.name}.mp4"
        print(f"Loading video URL: {video_url}")
        player.load_video(video_url)
        current_scene = scene_info.name
        ui.notify(f"Playing: {scene_info.name}", type="positive")
    else:
        ui.notify(
            f"Scene '{scene_info.name}' not rendered yet. Click 'Render' first.",
            type="warning"
        )


def render_scene_interactive(scene_info):
    """Render scene with progress feedback."""
    global render_status

    print(f"Rendering scene: {scene_info.name}")

    # Show progress dialog
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Rendering: {scene_info.name}").style("font-weight: bold; font-size: 1.2em")
        ui.label("This may take a few moments...").style("margin-bottom: 15px")

        progress_log = ui.log().style("height: 200px; width: 500px; background: #1e1e1e; color: #fff")

        def on_progress(line):
            """Progress callback for rendering."""
            progress_log.push(line)

        dialog.open()

        # Render in background (simplified - in production, use async)
        try:
            ui.notify("Starting render...", type="info")

            # Note: This is synchronous and will block the UI
            # In production, use asyncio or background tasks
            video_path = manager.render_scene(
                scene_name=scene_info.name,
                quality="medium",
                on_progress=on_progress,
                force_rerender=False
            )

            progress_log.push(f"\n✓ Render complete: {video_path}")
            ui.notify(f"Rendered: {scene_info.name}", type="positive")

            # Auto-load into player (if player exists)
            if player is not None:
                video_url = f"/static/renders/{scene_info.name}.mp4"
                player.load_video(video_url)
                progress_log.push(f"Loaded into player: {video_url}")
            else:
                progress_log.push("Note: Visit 'Player' tab to watch the video")

        except Exception as e:
            progress_log.push(f"\n✗ Error: {e}")
            ui.notify(f"Render failed: {e}", type="negative")

        # Close button
        ui.button("Close", on_click=dialog.close).classes('mt-4')


def clear_cache():
    """Clear all cached videos."""
    manager.clear_cache()
    ui.notify("Cache cleared successfully", type="positive")


# ---------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------

@ui.page('/')
def main_page():
    """Main application page."""
    global player

    ui.label("Manim Animation Gallery").style(
        "font-size: 2em; font-weight: bold; margin-bottom: 20px"
    )

    # Tabs for different sections
    with ui.tabs().classes('w-full') as tabs:
        gallery_tab = ui.tab("Gallery", icon="view_module")
        player_tab = ui.tab("Player", icon="play_circle")
        about_tab = ui.tab("About", icon="info")

    with ui.tab_panels(tabs, value=gallery_tab).classes('w-full'):
        # Gallery Tab
        with ui.tab_panel(gallery_tab):
            ui.label("Available Animations").style("font-size: 1.5em; font-weight: bold; margin-bottom: 15px")

            # Discover scenes
            scenes = manager.discover_scenes()

            if not scenes:
                ui.label("No scenes found. Check that scene files exist in the scenes/ directory.").style(
                    "color: orange; margin: 20px"
                )
            else:
                ui.label(f"Found {len(scenes)} scenes").style("margin-bottom: 15px")

                # Group by category
                categories = {}
                for scene in scenes:
                    if scene.category not in categories:
                        categories[scene.category] = []
                    categories[scene.category].append(scene)

                # Display by category
                for category, category_scenes in categories.items():
                    ui.label(category.replace('_', ' ').title()).style(
                        "font-size: 1.3em; font-weight: bold; margin-top: 20px; margin-bottom: 10px"
                    )

                    with ui.row().style("gap: 20px; flex-wrap: wrap"):
                        for scene in category_scenes:
                            create_scene_card(scene)

            # Utility buttons
            with ui.row().style("margin-top: 30px; gap: 10px"):
                ui.button("Clear Cache", on_click=clear_cache, color="red")
                ui.button(
                    "Refresh Scenes",
                    on_click=lambda: ui.navigate.reload(),
                    color="secondary"
                )

        # Player Tab
        with ui.tab_panel(player_tab):
            ui.label("Manim Video Player").style("font-size: 1.5em; font-weight: bold; margin-bottom: 15px")

            # Create player
            global player
            player = ManimPlayer(width="100%", height="600px")
            player.mount_container()

            # Player controls
            with ui.row().style("margin-top: 20px; gap: 10px"):
                ui.button("Play", on_click=lambda: player.play(), icon="play_arrow", color="primary")
                ui.button("Pause", on_click=lambda: player.pause(), icon="pause", color="secondary")
                ui.button("Reset", on_click=lambda: player.reset_view(), icon="replay", color="secondary")

            # Playback speed
            ui.label("Playback Speed:").style("margin-top: 20px")
            with ui.row().style("gap: 10px"):
                ui.button("0.5x", on_click=lambda: player.set_playback_rate(0.5), color="secondary")
                ui.button("1x", on_click=lambda: player.set_playback_rate(1.0), color="primary")
                ui.button("1.5x", on_click=lambda: player.set_playback_rate(1.5), color="secondary")
                ui.button("2x", on_click=lambda: player.set_playback_rate(2.0), color="secondary")

            # Info
            ui.label("Select a scene from the Gallery tab to play it here.").style(
                "margin-top: 20px; color: #888"
            )

        # About Tab
        with ui.tab_panel(about_tab):
            ui.label("About Manim Player").style("font-size: 1.5em; font-weight: bold; margin-bottom: 15px")

            ui.markdown("""
            ## Manim Animation Player

            This application demonstrates the integration of **Manim** (Mathematical Animation Engine)
            with **NiceGUI** for creating and sharing technical explainer animations.

            ### Features

            - **Gallery View**: Browse available animation scenes by category
            - **On-Demand Rendering**: Render scenes at different quality levels
            - **Video Caching**: Rendered videos are cached for fast playback
            - **Playback Controls**: Play, pause, speed control, fullscreen
            - **Web Sharing**: Deploy to share animations on the web

            ### Scene Categories

            1. **Algorithms**: Sorting, searching, graph algorithms (Bubble Sort, Binary Search, Dijkstra)
            2. **Networks**: Network flows, packet routing, TCP handshake
            3. **Code Execution**: Function call stack, variable scope, array memory
            4. **System Flows**: Microservices, data pipelines, request-response

            ### How to Use

            1. **Gallery Tab**: Browse scenes and click "Render" to create the animation
            2. **Player Tab**: Watch the rendered animation with playback controls
            3. Rendered videos are cached in `static/renders/` for fast replay

            ### Quality Settings

            - **Low** (480p15): Fast rendering, smaller files
            - **Medium** (720p30): Balanced quality and size (default)
            - **High** (1080p60): High quality, larger files
            - **4K** (2160p60): Maximum quality, very large files

            ### Technical Stack

            - **Manim Community**: Animation rendering engine
            - **NiceGUI**: Web UI framework (Python + FastAPI)
            - **HTML5 Video**: Browser-native video playback
            - **FFmpeg**: Video encoding (required by manim)

            ### Next Steps

            - Create custom scenes in `scenes/` directory
            - Combine with Cytoscape interactive diagrams (HybridExplainer)
            - Add voiceover support
            - Deploy to web server for sharing

            ---

            Built with Manim Player v1.0
            """)


# ---------------------------------------------------------------------
# Run application
# ---------------------------------------------------------------------

if __name__ in {"__main__", "__mp_main__"}:
    print("Starting Manim Player Demo Application...")
    print(f"Scenes directory: {manager.scenes_dir}")
    print(f"Output directory: {manager.output_dir}")

    ui.run(
        title="Manim Animation Player",
        favicon="🎬",
        dark=None,
        reload=False
    )
