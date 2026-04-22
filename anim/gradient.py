from manim import BLUE, Circle, Create, Scene


class Hello(Scene):
    def construct(self) -> None:
        circle = Circle()

        self.play(Create(circle))

        self.wait()
        self.play(circle.animate.set_color(BLUE))
        self.wait()
