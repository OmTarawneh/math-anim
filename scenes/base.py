from manim import Scene, ThreeDScene, config
from theme import BG


def _apply_short() -> None:
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_height = 14.222
    config.frame_width = 14.222 * (1080 / 1920)


def _apply_normal() -> None:
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_height = 8.0
    config.frame_width = 8.0 * (16 / 9)


class ShortScene(Scene):
    def __init__(self, **kwargs):
        _apply_short()
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.camera.background_color = BG


class NormalScene(Scene):
    def __init__(self, **kwargs):
        _apply_normal()
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.camera.background_color = BG


class NormalThreeDScene(ThreeDScene):
    def __init__(self, **kwargs):
        _apply_normal()
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.camera.background_color = BG
