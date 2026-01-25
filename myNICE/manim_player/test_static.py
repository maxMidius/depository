#!/usr/bin/env python3
"""Test static file serving"""

from pathlib import Path
from nicegui import ui, app

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / 'static'

print(f"ROOT: {ROOT}")
print(f"STATIC_DIR: {STATIC_DIR}")
print(f"STATIC_DIR exists: {STATIC_DIR.exists()}")

# Check for video files
renders_dir = STATIC_DIR / 'renders'
if renders_dir.exists():
    videos = list(renders_dir.glob("*.mp4"))
    print(f"\nFound {len(videos)} videos:")
    for v in videos:
        print(f"  - {v.name}")
        print(f"    Size: {v.stat().st_size / 1024:.1f} KB")
        print(f"    Should be accessible at: /static/renders/{v.name}")

# Mount static files
app.add_static_files('/static', str(STATIC_DIR))
print(f"\nStatic files mounted: /static -> {STATIC_DIR}")

@ui.page('/')
def index():
    ui.label("Static File Test").classes('text-2xl font-bold mb-4')

    # Test different URL formats
    if renders_dir.exists():
        for video in renders_dir.glob("*.mp4"):
            with ui.card().classes('mb-4 p-4'):
                ui.label(f"Video: {video.name}").classes('font-bold mb-2')

                # Test 1: With leading slash
                url1 = f"/static/renders/{video.name}"
                ui.label(f"Test 1 - With leading slash: {url1}").classes('text-sm')
                ui.html(f'''
                    <video controls width="400" style="margin: 10px 0">
                        <source src="{url1}" type="video/mp4">
                    </video>
                ''', sanitize=False)

                # Test 2: Without leading slash
                url2 = f"static/renders/{video.name}"
                ui.label(f"Test 2 - Without leading slash: {url2}").classes('text-sm mt-4')
                ui.html(f'''
                    <video controls width="400" style="margin: 10px 0">
                        <source src="{url2}" type="video/mp4">
                    </video>
                ''', sanitize=False)

                # Test 3: Using NiceGUI's ui.video
                url3 = f"/static/renders/{video.name}"
                ui.label(f"Test 3 - Using ui.video: {url3}").classes('text-sm mt-4')
                ui.video(url3, controls=True).style('width: 400px; margin: 10px 0')

    ui.markdown("""
    ### Instructions:
    1. Open browser console (F12)
    2. Look at Network tab
    3. See which video requests succeed (200) vs fail (404)
    4. Check if any of the three test methods work
    """)

if __name__ in {"__main__", "__mp_main__"}:
    print("\n" + "="*60)
    print("Starting static file test server...")
    print("Open: http://localhost:8080")
    print("="*60 + "\n")
    ui.run(port=8080, reload=False)
