#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------

import os
import subprocess
import importlib.util
import inspect
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from icecream import ic
from rich import print


@dataclass
class SceneInfo:
    """Information about a manim scene"""
    name: str
    description: str
    category: str
    file_path: Path
    class_ref: Any = None


class ManimRenderManager:
    """Manages manim scene rendering and caching"""

    QUALITY_PRESETS = {
        "low": ("l", "480p15"),
        "medium": ("m", "720p30"),
        "high": ("h", "1080p60"),
        "4k": ("k", "2160p60"),
    }

    def __init__(self, scenes_dir: Path, output_dir: Path):
        """
        Initialize the ManimRenderManager.

        Args:
            scenes_dir: Directory containing manim scene definitions
            output_dir: Directory where rendered videos will be stored
        """
        self.scenes_dir = Path(scenes_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.render_cache: Dict[str, Path] = {}
        print(f"ManimRenderManager initialized:")
        print(f"  Scenes directory: {self.scenes_dir}")
        print(f"  Output directory: {self.output_dir}")

    def discover_scenes(self) -> List[SceneInfo]:
        """
        Discover all manim Scene classes in the scenes directory.

        Returns:
            List of SceneInfo objects for all discovered scenes
        """
        scenes = []

        if not self.scenes_dir.exists():
            print(f"Scenes directory does not exist: {self.scenes_dir}")
            return scenes

        # Find all Python files in scenes directory
        for py_file in self.scenes_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                # Load module from file
                spec = importlib.util.spec_from_file_location(
                    f"manim_scenes.{py_file.stem}", py_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find all Scene subclasses
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Check if it's a Scene subclass (not Scene itself)
                        if hasattr(obj, '__bases__'):
                            base_names = [base.__name__ for base in obj.__bases__]
                            if 'Scene' in base_names or 'ThreeDScene' in base_names:
                                description = (obj.__doc__ or "No description").strip().split('\n')[0]
                                category = py_file.stem

                                scenes.append(SceneInfo(
                                    name=name,
                                    description=description,
                                    category=category,
                                    file_path=py_file,
                                    class_ref=obj
                                ))

            except Exception as e:
                print(f"Error loading {py_file}: {e}")

        print(f"Discovered {len(scenes)} scenes")
        for scene in scenes:
            print(f"  - {scene.name} ({scene.category}): {scene.description}")

        return scenes

    def get_cached_video(self, scene_name: str) -> Optional[Path]:
        """
        Get cached video path if it exists.

        Args:
            scene_name: Name of the scene

        Returns:
            Path to cached video file, or None if not found
        """
        # Check memory cache first
        if scene_name in self.render_cache:
            video_path = self.render_cache[scene_name]
            if video_path.exists():
                return video_path

        # Check filesystem
        video_path = self.output_dir / f"{scene_name}.mp4"
        if video_path.exists():
            self.render_cache[scene_name] = video_path
            return video_path

        return None

    def render_scene(
        self,
        scene_name: str,
        scene_file: Optional[Path] = None,
        quality: str = "medium",
        on_progress: Optional[Callable[[str], None]] = None,
        force_rerender: bool = False
    ) -> Path:
        """
        Render a manim scene via subprocess.

        Args:
            scene_name: Name of the Scene class to render
            scene_file: Path to the Python file containing the scene (optional, will auto-discover)
            quality: Quality preset ("low", "medium", "high", "4k")
            on_progress: Callback function for progress updates (receives stdout lines)
            force_rerender: Force re-rendering even if cached video exists

        Returns:
            Path to rendered video file

        Raises:
            ValueError: If scene file not found or quality preset invalid
            RuntimeError: If rendering fails
        """
        # Check cache first
        if not force_rerender:
            cached = self.get_cached_video(scene_name)
            if cached:
                print(f"Using cached video for {scene_name}: {cached}")
                return cached

        # Validate quality preset
        if quality not in self.QUALITY_PRESETS:
            raise ValueError(f"Invalid quality: {quality}. Must be one of {list(self.QUALITY_PRESETS.keys())}")

        quality_flag, quality_name = self.QUALITY_PRESETS[quality]

        # Auto-discover scene file if not provided
        if scene_file is None:
            scenes = self.discover_scenes()
            matching_scenes = [s for s in scenes if s.name == scene_name]
            if not matching_scenes:
                raise ValueError(f"Scene '{scene_name}' not found in {self.scenes_dir}")
            scene_file = matching_scenes[0].file_path

        if not scene_file.exists():
            raise ValueError(f"Scene file not found: {scene_file}")

        # Prepare output filename
        output_file = self.output_dir / f"{scene_name}.mp4"

        # Build manim command
        cmd = [
            "manim",
            "render",
            f"-q{quality_flag}",  # -ql, -qm, -qh, -qk
            str(scene_file),
            scene_name,
            "--output_file", str(output_file),
            "--disable_caching",  # Ensure fresh render
        ]

        print(f"Rendering {scene_name} at {quality_name} quality...")
        print(f"Command: {' '.join(cmd)}")

        try:
            # Run manim render command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Stream output
            if process.stdout:
                for line in process.stdout:
                    line = line.rstrip()
                    if on_progress:
                        on_progress(line)
                    else:
                        print(f"  {line}")

            # Wait for completion
            return_code = process.wait()

            if return_code != 0:
                raise RuntimeError(f"Manim rendering failed with return code {return_code}")

            # Verify output file exists
            if not output_file.exists():
                raise RuntimeError(f"Rendering completed but output file not found: {output_file}")

            # Update cache
            self.render_cache[scene_name] = output_file

            print(f"Successfully rendered {scene_name} to {output_file}")
            return output_file

        except Exception as e:
            print(f"Error rendering scene {scene_name}: {e}")
            raise

    def clear_cache(self, scene_name: Optional[str] = None) -> None:
        """
        Clear video cache.

        Args:
            scene_name: If provided, clear only this scene's cache.
                       If None, clear all cached videos.
        """
        if scene_name:
            # Clear specific scene
            video_path = self.output_dir / f"{scene_name}.mp4"
            if video_path.exists():
                video_path.unlink()
                print(f"Deleted cached video: {video_path}")

            if scene_name in self.render_cache:
                del self.render_cache[scene_name]
        else:
            # Clear all videos
            for video_file in self.output_dir.glob("*.mp4"):
                video_file.unlink()
                print(f"Deleted cached video: {video_file}")

            self.render_cache.clear()

        print("Cache cleared successfully")

    def get_video_metadata(self, scene_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a rendered video.

        Args:
            scene_name: Name of the scene

        Returns:
            Dictionary with metadata (file size, duration, etc.) or None if not found
        """
        video_path = self.get_cached_video(scene_name)
        if not video_path:
            return None

        stat = video_path.stat()
        metadata = {
            "file_path": str(video_path),
            "file_size": stat.st_size,
            "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified_time": stat.st_mtime,
        }

        # Try to get video duration using ffprobe if available
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                metadata["duration_seconds"] = round(duration, 2)
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        return metadata
