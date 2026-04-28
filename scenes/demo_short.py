from base import ShortScene
from manim import UP, Circle, DrawBorderThenFill, Text, Write
from theme import ACCENT, FG


class ShortDemo(ShortScene):
    def construct(self) -> None:
        circle = Circle(radius=2.0, color=ACCENT).set_fill(ACCENT, opacity=0.25)
        title = Text("short", color=FG, font_size=72).to_edge(UP)
        self.play(DrawBorderThenFill(circle))
        self.play(Write(title))
        self.wait()
