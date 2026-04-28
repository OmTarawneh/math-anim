from base import NormalScene
from manim import UP, Axes, Create, Text, Write
from theme import ACCENT, FG, MUTED


class NormalDemo(NormalScene):
    def construct(self) -> None:
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": MUTED},
        )
        graph = ax.plot(lambda x: 0.5 * x**2 - 1, color=ACCENT)
        title = Text("normal", color=FG, font_size=48).to_edge(UP)
        self.play(Create(ax))
        self.play(Create(graph))
        self.play(Write(title))
        self.wait()
