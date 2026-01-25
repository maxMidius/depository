#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Manim Player - Integration layer for displaying Manim animations in NiceGUI
"""

from .player import ManimPlayer
from .manim_manager import ManimRenderManager

__all__ = ['ManimPlayer', 'ManimRenderManager']
