from manim import Scene, config

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60


class ShortScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
