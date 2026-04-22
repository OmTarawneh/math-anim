from base import ShortScene
from manim import BLUE, Circle, Create


class Hello(ShortScene):
    def construct(self) -> None:
        circle = Circle()

        self.play(Create(circle))

        self.wait()
        self.play(circle.animate.set_color(BLUE))
        self.wait()
