"""ManimCE exercises — practice scenes you implement yourself.

How to use this file
--------------------
Each class below is a stub. Read its docstring (Goal / Concepts to use
/ Hints), then replace the `raise NotImplementedError` with your
implementation. Render to check:

    uv run poe low docs/exercises.py <ExerciseName>

How to check yourself
---------------------
Solutions are NOT in this repo by design — looking at a worked solution
before grappling with the problem skips the hard part of learning.
Strategy:

    1. Implement the exercise.
    2. Render the matching tutorial scene (E03 -> C03b, etc.) and
       compare visually.
    3. If you're stuck on syntax, search for the class/function name
       in `docs/tutorial.py`.

Difficulty curves with the tutorial chapters. The last three (E18-E20)
are open-ended creative challenges with no "right" answer.

Imports follow the same pattern as docs/tutorial.py — see the header
docstring there for why the sys.path dance and star import.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenes"))

import numpy as np
from base import NormalScene, NormalThreeDScene, ShortScene
from manim import *
from manim import rate_functions as rf
from theme import ACCENT, ACCENT_2, ACCENT_3, BG, FG, MUTED

# =============================================================================
# Exercises 01-04 — Foundations: shapes, layout, equations
# =============================================================================


class E01_DrawAndStyle(NormalScene):
    """Goal: draw a centered square with a copper stroke (ACCENT) and a
    25%-opacity ACCENT fill, then a labeled dot positioned just above
    the square. Animate them in: the square with DrawBorderThenFill,
    the dot with FadeIn, the label with Write.

    Concepts to use:
      - Square, Dot, Text
      - set_fill / fill_opacity
      - next_to for positioning
      - DrawBorderThenFill, FadeIn, Write

    Hints:
      - `Square(side_length=2.0).set_fill(ACCENT, opacity=0.25)`.
      - The dot's label can be `Text("vertex", color=MUTED, font_size=24)`
        positioned with `.next_to(dot, UP, buff=0.15)`.
      - End with `self.wait()` to hold the final frame.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E02_LayoutThreeShapes(NormalScene):
    """Goal: three different shapes arranged in a horizontal row using
    VGroup.arrange, evenly spaced, vertically centered on the frame.
    Pick any three primitives (Circle, Square, Triangle, Star, ...).

    Concepts to use:
      - VGroup
      - arrange(RIGHT, buff=...)
      - LaggedStart for the staggered intro

    Hints:
      - `VGroup(circle, square, triangle).arrange(RIGHT, buff=0.8)`.
      - For the intro: `LaggedStart(*[Create(s) for s in group], lag_ratio=0.2)`.
      - All three can use the same theme color, or you can vary
        ACCENT / ACCENT_2 / ACCENT_3 for variety.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E03_AlgebraStepOnYourOwn(NormalScene):
    """Goal: animate one algebra step  2x - 4 = 10  ->  2x = 14
    so that the "2x" stays in place and "-4" visibly moves to the
    right side flipping sign.

    Concepts to use:
      - MathTex with explicit token splitting (each token = own arg)
      - TransformMatchingTex
      - Color highlighting on the moved term

    Hints:
      - Tokenize as `MathTex("2x", "-", "4", "=", "10")` and
        `MathTex("2x", "=", "14")`. The "+4" merges into "14"; if you
        want to show it explicitly first, use intermediate
        `MathTex("2x", "=", "10", "+", "4")` and then a second step.
      - Color the moved term with ACCENT BEFORE the transform.
      - `run_time=1.5` reads better than the default for math.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E04_QuadraticFactoring(NormalScene):
    """Goal: animate factoring  x^2 - 5x + 6  ->  (x - 2)(x - 3).

    Concepts to use:
      - Multi-stage TransformMatchingTex (several intermediate forms)
      - Color tracking through stages
      - run_time tuned per step

    Hints:
      - You may need three or four stages: original ->
        x^2 - 2x - 3x + 6 -> x(x-2) - 3(x-2) -> (x-2)(x-3).
      - Tokenize aggressively. Same tokens (e.g. "x", "-", "2") in
        consecutive equations let TransformMatchingTex track them.
      - Color the "-2" and "-3" in ACCENT and ACCENT_2 so you can
        see how each survives through to the final factored form.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 05-07 — Layout, animation verbs, timing
# =============================================================================


class E05_TitleCard_Short(ShortScene):
    """Goal: a 15-second VERTICAL title card. Title at top fades in,
    subtitle slides up from below the title, an accent underline grows
    from center, then everything holds for the rest of the time.

    Concepts to use:
      - ShortScene base class (1080x1920)
      - to_edge(UP, buff=...) for safe-area placement
      - GrowFromCenter / GrowFromEdge
      - FadeIn(shift=...) for slide-in
      - Tight run_time and wait values

    Hints:
      - Title font_size around 88; subtitle around 44.
      - `Line(...).stretch_to_fit_width(title.width)` gives an
        underline that exactly matches the title width.
      - Final `self.wait(8)` or similar lets it sit on the title.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E06_RateFuncCompare(NormalScene):
    """Goal: three dots traveling the same horizontal distance with
    `linear`, `smooth`, and `there_and_back`, side by side, each
    labeled with its rate_func name.

    Concepts to use:
      - .animate with rate_func= per animation
      - AnimationGroup or playing them in one self.play call
      - Text labels next_to each dot's start position

    Hints:
      - All three animations should use the same `run_time` so the
        comparison is fair.
      - Place the labels at the LEFT of each dot's start.
      - `there_and_back` returns to start, so visually the dot ends
        where it started — this is the lesson.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E07_LaggedStartChain(NormalScene):
    """Goal: five circles arranged in a row appear one after another
    with `LaggedStart(..., lag_ratio=0.3)`.

    Concepts to use:
      - VGroup, arrange
      - LaggedStart with lag_ratio
      - FadeIn or GrowFromCenter on each circle

    Hints:
      - `lag_ratio=0.3` means each circle starts 30% of the previous
        animation's run_time after the previous one began.
      - Wrap with `self.play(LaggedStart(*[FadeIn(c) for c in circles],
        lag_ratio=0.3), run_time=2.0)` to control the total.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 08-09 — Updaters and ValueTrackers
# =============================================================================


class E08_Counter(NormalScene):
    """Goal: a centered, large number counts from 0 to 100 over 4
    seconds with ease-out, driven by a ValueTracker and a DecimalNumber.

    Concepts to use:
      - ValueTracker
      - DecimalNumber with num_decimal_places=0
      - add_updater to read tracker -> set DecimalNumber value
      - rate_func=rf.ease_out_quad or similar

    Hints:
      - `tracker = ValueTracker(0)`, then animate
        `tracker.animate.set_value(100)`.
      - Updater: `lambda m: m.set_value(tracker.get_value())`.
      - Don't forget `clear_updaters()` after the play.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E09_FollowingDot(NormalScene):
    """Goal: a static circle drawn in MUTED, with a dot on its
    circumference whose position is driven by a ValueTracker (angle in
    radians). A radial line from the center to the dot is drawn with
    `always_redraw` so it follows automatically.

    Concepts to use:
      - ValueTracker as an angle
      - always_redraw for the dot AND the radial line
      - circle.point_from_proportion(t) for parametrizing 0..TAU

    Hints:
      - The dot's position: `circle.point_from_proportion(
        (angle.get_value() / TAU) % 1.0)`.
      - Animate the angle from 0 to TAU; rate_func=rf.smooth gives a
        natural ease.
      - Three Mobjects total: circle (static), dot (always_redraw),
        line (always_redraw).
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 10-12 — Plotting and calculus visuals
# =============================================================================


class E10_PlotSineAndCosine(NormalScene):
    """Goal: an Axes from -2π to 2π. Plot sin(x) in ACCENT and cos(x)
    in ACCENT_2. Add a small legend (top-right corner) with two
    MathTex labels showing which color is which.

    Concepts to use:
      - Axes with custom x_range / y_range
      - axes.plot with multiple graphs
      - MathTex
      - VGroup + arrange for the legend

    Hints:
      - `x_range=[-2*PI, 2*PI, PI/2]`, `y_range=[-1.5, 1.5, 0.5]`.
      - Legend entry = small colored Line + MathTex label, grouped:
        `VGroup(line, label).arrange(RIGHT, buff=0.2)`.
      - Stack the two legend rows vertically with `arrange(DOWN, ...)`.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E11_RiemannRectanglesShrink(NormalScene):
    """Goal: Riemann rectangles for f(x) = x^2 on [0, 2]. Animate `dx`
    from 0.5 down to 0.05 via a ValueTracker. The graph itself stays
    on screen during the shrink.

    Concepts to use:
      - Axes + plot
      - axes.get_riemann_rectangles
      - always_redraw rebuilding rectangles each frame
      - ValueTracker

    Hints:
      - Build the always_redraw with a closure on dx.get_value():
        `axes.get_riemann_rectangles(graph, x_range=[0,2],
        dx=dx.get_value(), color=ACCENT_2, fill_opacity=0.5)`.
      - Animate `dx.animate.set_value(0.05)` over 4 seconds.
      - Smaller dx means many more rectangles — render takes longer.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E12_TangentLineSlider(NormalScene):
    """Goal: tangent line on f(x) = sin(x), driven by a ValueTracker
    over the x-axis. Show the slope value as a MathTex always_redraw
    in the top-right corner.

    Concepts to use:
      - axes.plot, axes.c2p
      - ValueTracker for x position
      - always_redraw for tangent line, dot, slope readout
      - Numerical or analytic derivative (cos(x))

    Hints:
      - The tangent line at x has slope cos(x). Pick a half-length
        (say 1.0) and build endpoints at (x±half, sin(x)±slope*half).
      - Animate x from -2.5 to 2.5 over ~4 seconds.
      - MathTex string with f-string formatting:
        `f"f'(x) = {float(np.cos(x_t.get_value())):+.2f}"`.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 13-14 — Annotation and emphasis
# =============================================================================


class E13_BraceTheTerm(NormalScene):
    """Goal: write the expression  a^3 + 3a^2 b + 3ab^2 + b^3  and
    place a Brace under the middle two terms (3a^2 b + 3ab^2) labeled
    "the cross terms".

    Concepts to use:
      - MathTex with token splitting so the middle terms are
        addressable as a slice
      - Brace with direction=DOWN
      - brace.get_text(...)

    Hints:
      - Tokenize so `MathTex("a^3", "+", "3a^2 b", "+", "3ab^2", "+", "b^3")`.
      - `Brace(eq[2:5], DOWN)` covers the middle three submobjects
        (the two terms plus the "+" between them).
      - Color the cross terms in ACCENT before placing the brace so
        the eye sees the grouping.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E14_IndicateThePivot(NormalScene):
    """Goal: render a 3x3 matrix of MathTex numbers (your choice).
    Highlight the (2,2) entry with `Circumscribe` first, then
    `Indicate`. Hold for a beat. Treat (1,1) as the top-left.

    Concepts to use:
      - MathTex matrix or VGroup of cells
      - Circumscribe, Indicate
      - Sequential play calls (no LaggedStart needed)

    Hints:
      - Easiest: build a `VGroup` of nine `MathTex` cells with
        `arrange_in_grid(rows=3, cols=3, buff=0.6)`.
      - The "(2,2) entry" with 0-indexing is `cells[4]` (middle of
        the 3x3 grid).
      - Both indicators accept `color=ACCENT`.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 15-17 — Camera and 3D
# =============================================================================


class E15_ZoomToDetail(MovingCameraScene):
    """Goal: a field of small dots. Start with the camera wide, then
    zoom in (shrink the camera frame) on a specific dot for a beat,
    then zoom back out.

    Concepts to use:
      - MovingCameraScene (NOT NormalScene — see C09a comments)
      - self.camera.frame.animate.scale(...).move_to(...)
      - self.camera.background_color = BG (manual since no NormalScene)

    Hints:
      - Generate dots in a grid: `[Dot([x, y, 0]) for x in
        np.arange(-6, 6.5, 0.5) for y in np.arange(-3, 3.5, 0.5)]`.
      - Pick a target dot and animate
        `self.camera.frame.animate.scale(0.3).move_to(target)`.
      - To zoom out, `scale(1/0.3)` and `move_to(ORIGIN)`.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E16_RotatingCubeAndAxes(NormalThreeDScene):
    """Goal: ThreeDAxes plus a Cube at the origin. Use ambient camera
    rotation for ~4 seconds, then stop. End with `wait()`.

    Concepts to use:
      - NormalThreeDScene
      - set_camera_orientation
      - ThreeDAxes, Cube
      - begin_ambient_camera_rotation / stop_ambient_camera_rotation

    Hints:
      - Initial orientation: `phi=70 * DEGREES, theta=30 * DEGREES`.
      - `Cube(side_length=1.0, fill_color=ACCENT, fill_opacity=0.6)`.
      - Always pair `begin_ambient_camera_rotation` with `stop_...`
        before the final wait.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E17_ParaboloidSurface(NormalThreeDScene):
    """Goal: render the surface z = x^2 + y^2 (a paraboloid) over
    [-1.5, 1.5] in both x and y. Start with the camera nearly
    top-down, then `move_camera` to an oblique view to reveal the
    bowl shape.

    Concepts to use:
      - Surface with axes.c2p inside the lambda
      - set_fill_by_checkerboard
      - move_camera

    Hints:
      - Top-down: `phi=10 * DEGREES, theta=-90 * DEGREES`.
      - Oblique: `phi=65 * DEGREES, theta=-45 * DEGREES`.
      - `move_camera(phi=..., theta=..., run_time=2)` animates the
        transition.
      - resolution=(24, 24) is plenty.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


# =============================================================================
# Exercises 18-20 — Open-ended creative challenges
# -----------------------------------------------------------------------------
# No template, no fixed expectation. Whatever you build, prioritize
# clarity and pacing over feature count.
# =============================================================================


class E18_Open_PythagorasProof(NormalScene):
    """Goal (open-ended): animate ANY visual proof of the Pythagorean
    theorem (a^2 + b^2 = c^2). There are dozens of proofs; pick one
    you like and animate the rearrangement.

    Suggestions:
      - The "two squares" proof: start with a (a+b) x (a+b) square
        with four right triangles inside; rearrange to expose the
        a^2 + b^2 region, then to expose the c^2 region.
      - Bhaskara's proof: rearrange triangles inside the square.
      - Garfield's trapezoid proof.

    Concepts likely to use:
      - VGroup, Rectangle, Polygon, Triangle
      - Transform / ReplacementTransform for rearrangements
      - MathTex for the formula reveal
      - Brace for labeling sides

    Hints:
      - Build the pieces as a VGroup so you can transform them
        positionally without losing identity.
      - End with the equation a^2 + b^2 = c^2 written out and
        Indicated.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E19_Open_TaylorApproximation(NormalScene):
    """Goal (open-ended): animate sin(x) being approximated by Taylor
    polynomial terms accumulating one at a time. Start with the
    constant approximation (degree 1: T(x) = x), then add the cubic
    term, then quintic, etc. Show how each new term pulls the
    approximation closer to sin(x).

    Concepts likely to use:
      - Axes + multiple plots
      - ReplacementTransform between successive Taylor polys
      - MathTex for the running formula in a corner
      - LaggedStart for the term reveals

    Hints:
      - Define a function `taylor_sin(x, n_terms)` that sums the
        first n_terms of the Taylor series.
      - Plot each successive approximation in ACCENT_2; keep the
        original sin(x) in ACCENT for reference.
      - `MathTex(r"x", r"-", r"\\tfrac{x^3}{6}", r"+", r"\\tfrac{x^5}{120}",
        ...)` — use TransformMatchingTex (see C03c).
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")


class E20_Open_ShortReel_TheoremTease(ShortScene):
    """Goal (open-ended): a 15-30 second VERTICAL reel that teases any
    mathematical theorem of your choice. Examples: pigeonhole, Euler's
    identity, the Basel problem, the four-color theorem.

    Structure suggestion:
      - 0-2s: hook ("did you know?")
      - 2-8s: the setup or the visualization
      - 8-12s: the punchline / formula reveal
      - 12-15s: tag or callback that holds for a beat

    Concepts likely to use:
      - ShortScene (1080x1920)
      - Tight run_times (~0.6s) and short waits (~0.4s)
      - SurroundingRectangle for emphasis
      - Indicate for the punchline beat

    Hints:
      - Read C05c again for short-form pacing notes.
      - Resist the temptation to cram. One idea, told tight, beats
        three ideas told slowly.
      - Hold the final frame for ~1.5s so phone scrubbers can read it.
    """

    def construct(self) -> None:
        raise NotImplementedError("Implement me — see docstring.")
