import numpy as np
from base import ShortScene
from manim import *

import shared.short_constants as sc


class Hook(ShortScene):
    def construct(self) -> None:
        # Using a Sans-Serif font is highly recommended for mobile
        question = Text(
            "How do you find\nthe maximum\nunder a constraint?",
            font=sc.FONT_PRIMARY,
            font_size=sc.FONT_SIZE_XL,
            line_spacing=sc.SPACING_NORMAL,
            weight=BOLD,
        ).move_to(UP * 3)  # Moved slightly higher in the safe zone

        sub = Text(
            "Lagrange Multipliers",
            font=sc.FONT_PRIMARY,
            font_size=sc.FONT_SIZE_L,
            color=YELLOW,
            weight=SEMIBOLD,
        ).next_to(question, DOWN, buff=1.0)

        self.play(FadeIn(question, shift=UP * 0.3), run_time=sc.TIME_NORMAL)
        self.wait(1.5)

        self.play(FadeIn(sub, shift=UP * 0.2), run_time=sc.TIME_NORMAL)
        self.wait(1.5)

        self.play(FadeOut(question, sub), run_time=0.5)


class GradientIntro(ShortScene):
    def construct(self) -> None:
        TITLE_Y = UP * 5.5

        title = Text("The Gradient", font_size=sc.FONT_SIZE_L, color=YELLOW).move_to(
            TITLE_Y
        )

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=6, y_length=4
        ).move_to(UP * 1.5)

        point = plane.c2p(1, 0.5)
        dot = Dot(point, color=WHITE, radius=0.12)

        grad_vec = Arrow(
            start=point,
            end=point
            + plane.c2p(1, 0.5)
            - plane.c2p(0, 0),  # direction (1, 0.5) scaled
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )

        label = Text("steepest ascent", font_size=sc.FONT_SIZE_M, color=RED).next_to(
            grad_vec, RIGHT, buff=0.2
        )

        nabla = MathTex(r"\nabla f", font_size=72, color=RED).move_to(DOWN * 3.5)

        # Build up
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.play(Create(plane), run_time=1.2)
        self.play(FadeIn(dot), run_time=0.4)
        self.wait(0.3)
        self.play(GrowArrow(grad_vec), run_time=0.8)
        self.play(FadeIn(label), run_time=0.5)
        self.wait(0.8)

        # Drop in the symbol
        self.play(Write(nabla), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(title, plane, dot, grad_vec, label, nabla), run_time=0.6)


class ConstraintSetup(ShortScene):
    def construct(self):
        title = Text("The Problem", font_size=sc.FONT_SIZE_L, color=YELLOW).move_to(
            UP * 5.5
        )

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=5.5,
        ).move_to(UP * 1.0)

        # Constraint: unit circle
        constraint = Circle(radius=plane.get_x_unit_size(), color=BLUE, stroke_width=5)
        constraint.move_to(plane.c2p(0, 0))

        g_label = MathTex(r"g(x,y)=0", font_size=sc.FONT_SIZE_M, color=BLUE)
        g_label.next_to(constraint, UP * 0.5 + RIGHT * 2.5, buff=0.1)

        # Level curves of f(x,y) = x + y → lines x + y = c
        level_curves = VGroup()
        for c_val in [-1.2, -0.5, 0.5, 1.2]:
            # x + y = c  →  y = c - x, parametrize as a Line
            lc = Line(
                plane.c2p(-2, c_val + 2),
                plane.c2p(2, c_val - 2),
                color=YELLOW,
                stroke_width=3,
            ).set_opacity(0.7)
            level_curves.add(lc)

        f_label = MathTex(r"f = c", font_size=sc.FONT_SIZE_L, color=YELLOW).move_to(
            plane.c2p(1.5, -1.2)
        )

        insight = Text(
            "find the highest level curve\nthat still touches g = 0",
            font_size=sc.FONT_SIZE_L,
            line_spacing=1.3,
            color=WHITE,
        ).move_to(DOWN * 4.2)

        # Build up
        self.play(FadeIn(title), run_time=0.5)
        self.play(Create(plane), run_time=0.8)
        self.play(Create(constraint), run_time=0.8)
        self.play(FadeIn(g_label), run_time=0.4)
        self.wait(0.4)
        self.play(
            LaggedStart(*[Create(lc) for lc in level_curves], lag_ratio=0.2),
            run_time=1.0,
        )
        self.play(FadeIn(f_label), run_time=0.4)
        self.wait(0.5)
        self.play(FadeIn(insight, shift=UP * 0.2), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(*self.mobjects), run_time=0.5)
