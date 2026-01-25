#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Manim Player Demo Application - Version 2 (using NiceGUI's built-in video)
"""

from pathlib import Path
from nicegui import ui, app
from rich import print
import sys

sys.path.insert(0, str(Path(__file__).parent))
from manim_manager import ManimRenderManager

# ---------------------------------------------------------------------
# Static files setup
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / 'static'
app.add_static_files('/static', str(STATIC_DIR))

print(f"Static files: /static -> {STATIC_DIR}")

# ---------------------------------------------------------------------
# Initialize Manim Manager
# ---------------------------------------------------------------------
manager = ManimRenderManager(
    scenes_dir=ROOT / 'scenes',
    output_dir=ROOT / 'static' / 'renders'
)

# Global state
video_player = None
current_scene = None


def create_scene_card(scene_info):
    """Create a card for a scene in the gallery."""
    with ui.card().classes('w-80'):
        ui.label(scene_info.name).style("font-weight: bold; font-size: 1.1em")
        ui.label(f"Category: {scene_info.category}").style("color: #888; font-size: 0.9em")
        ui.label(scene_info.description).style("margin-top: 10px; margin-bottom: 15px")

        # Check if cached
        cached = manager.get_cached_video(scene_info.name)
        if cached:
            metadata = manager.get_video_metadata(scene_info.name)
            size_mb = metadata.get('file_size_mb', 0) if metadata else 0
            ui.label(f"✓ Cached ({size_mb} MB)").style("color: green; font-size: 0.85em")

        with ui.row().style("gap: 10px; margin-top: 10px"):
            ui.button(
                "Play",
                on_click=lambda s=scene_info: load_video(s),
                color="primary"
            ).classes('flex-1')

            ui.button(
                "Render",
                on_click=lambda s=scene_info: render_scene(s),
                color="secondary"
            ).classes('flex-1')


def load_video(scene_info):
    """Load video into player."""
    global current_scene, video_player

    if video_player is None:
        ui.notify("Please visit Player tab first", type="warning")
        return

    cached = manager.get_cached_video(scene_info.name)
    if not cached:
        ui.notify(f"Please render '{scene_info.name}' first", type="warning")
        return

    video_url = f"/static/renders/{scene_info.name}.mp4"
    print(f"Loading: {video_url}")

    # Update video source
    video_player.set_source(video_url)
    current_scene = scene_info.name

    ui.notify(f"Playing: {scene_info.name}", type="positive")


def render_scene(scene_info):
    """Render a scene."""
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Rendering: {scene_info.name}").classes('text-lg font-bold')
        progress = ui.log().style("height: 300px; width: 600px; background: #1e1e1e; color: #fff")

        def on_progress(line):
            progress.push(line)

        dialog.open()

        try:
            video_path = manager.render_scene(
                scene_name=scene_info.name,
                quality="medium",
                on_progress=on_progress
            )

            progress.push(f"\n✓ Complete: {video_path}")
            ui.notify(f"Rendered: {scene_info.name}", type="positive")

            # Auto-load if player exists
            if video_player:
                video_url = f"/static/renders/{scene_info.name}.mp4"
                video_player.set_source(video_url)
                progress.push(f"Loaded into player")

        except Exception as e:
            progress.push(f"\n✗ Error: {e}")
            ui.notify(f"Render failed: {e}", type="negative")

        ui.button("Close", on_click=dialog.close).classes('mt-4')


@ui.page('/')
def main():
    global video_player

    ui.label("Manim Animation Player").classes('text-3xl font-bold mb-4')

    with ui.tabs().classes('w-full') as tabs:
        gallery_tab = ui.tab("Gallery", icon="view_module")
        player_tab = ui.tab("Player", icon="play_circle")

    with ui.tab_panels(tabs, value=gallery_tab).classes('w-full'):
        # Gallery
        with ui.tab_panel(gallery_tab):
            ui.label("Available Animations").classes('text-2xl font-bold mb-4')

            scenes = manager.discover_scenes()

            if not scenes:
                ui.label("No scenes found").classes('text-orange-500')
            else:
                ui.label(f"Found {len(scenes)} scenes").classes('mb-4')

                # Group by category
                categories = {}
                for scene in scenes:
                    if scene.category not in categories:
                        categories[scene.category] = []
                    categories[scene.category].append(scene)

                for category, cat_scenes in categories.items():
                    ui.label(category.replace('_', ' ').title()).classes('text-xl font-bold mt-4 mb-2')
                    with ui.row().style("gap: 20px; flex-wrap: wrap"):
                        for scene in cat_scenes:
                            create_scene_card(scene)

        # Player
        with ui.tab_panel(player_tab):
            ui.label("Video Player").classes('text-2xl font-bold mb-4')

            # Use NiceGUI's built-in video element
            video_player = ui.video(
                src="",
                controls=True,
                autoplay=False
            ).style("width: 100%; max-width: 1200px; height: 600px; background: #000;")

            # Controls
            with ui.row().classes('gap-2 mt-4'):
                ui.button("Play", icon="play_arrow", on_click=lambda: ui.run_javascript(
                    'document.querySelector("video").play()'
                ))
                ui.button("Pause", icon="pause", on_click=lambda: ui.run_javascript(
                    'document.querySelector("video").pause()'
                ))
                ui.button("Reset", icon="replay", on_click=lambda: ui.run_javascript(
                    'document.querySelector("video").currentTime = 0; document.querySelector("video").pause()'
                ))

            ui.label("Select a scene from Gallery to play").classes('text-gray-500 mt-4')


if __name__ in {"__main__", "__mp_main__"}:
    print("Starting Manim Player v2...")
    ui.run(title="Manim Player", port=8080, reload=False)
