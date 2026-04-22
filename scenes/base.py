from manim import Scene, config

from shared.short_constants import FPS, FRAME_HEIGHT, FRAME_WIDTH, RES_HEIGHT, RES_WIDTH

config.pixel_width = RES_WIDTH
config.pixel_height = RES_HEIGHT
config.frame_rate = FPS

# Expanded Coordinate System (Crucial for Vertical)
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT


class ShortScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
