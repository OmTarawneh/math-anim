"""ManimCE tutorial — basic to advanced, scene by scene.

How to use this file
--------------------
Each class below is an independent ManimCE Scene that teaches one
concept. Render any single scene with:

    uv run poe low  docs/tutorial.py <ClassName>     # fast, 15 fps
    uv run poe high docs/tutorial.py <ClassName>     # final, 60 fps
    uv run poe last-frame docs/tutorial.py <ClassName>  # PNG of last frame

Read the chapters in order — later scenes assume you have read the
docstrings of the earlier ones. Class names start with `C<chapter><letter>`
so alphabetical order in your editor matches teaching order.

Why the imports look the way they do
------------------------------------
1. `sys.path` is patched to add the project's `scenes/` directory.
   Manim only adds the *scene file's* directory to `sys.path`, but our
   shared base classes and color theme live in `scenes/`. This lets
   `from base import ...` resolve from a file in `docs/`.
2. `from manim import *` is the canonical ManimCE teaching idiom.
   In production code you would import only what you use, but for a
   reference tutorial the star import keeps every scene compact and
   makes copy-pasted snippets work without import edits. The project's
   ruff config already silences the related warnings (F401/F403/F405).

Project conventions used here
-----------------------------
- `NormalScene` (1920x1080), `ShortScene` (1080x1920), and
  `NormalThreeDScene` are defined in `scenes/base.py`. They pin
  resolution and apply the dark Claude background.
- Theme colors: `BG`, `FG`, `ACCENT`, `ACCENT_2`, `ACCENT_3`, `MUTED`
  from `scenes/theme.py`. Use these instead of raw hex codes so a
  future palette swap is a one-file change.
- Every `construct` is type-hinted `-> None` and is fully
  self-contained (no global state between scenes).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenes"))

import numpy as np
from manim import *
from manim import rate_functions as rf

from base import NormalScene, NormalThreeDScene, ShortScene
from theme import ACCENT, ACCENT_2, ACCENT_3, BG, FG, MUTED


# =============================================================================
# CHAPTER 01 — First Pixels
# -----------------------------------------------------------------------------
# Goal: get a single Mobject on screen, then animate creating it. Learn the
# minimum loop: build object -> self.play(...) -> self.wait().
# =============================================================================


class C01a_HelloCircle(NormalScene):
    """The smallest possible Manim scene.

    Concept: every animation lives inside `construct`. You build
    "Mobjects" (Manim objects), then call `self.play(Animation(mob))`
    to animate them, and `self.wait(seconds)` to hold the frame.

    Why this matters: this three-step loop — build, play, wait — is
    the entire mental model. Everything else is variations on it.

    Gotchas:
      - Calling `self.add(mob)` puts the Mobject on screen instantly
        with no animation. `self.play(Create(mob))` animates it in.
        Pick `add` for setup, `play` for storytelling.
      - Without a final `self.wait()`, the rendered video ends on the
        last animation frame with no pause — visually abrupt.
    """

    def construct(self) -> None:
        # `Circle` takes `radius`, `color`, and styling kwargs. Color
        # comes from our theme so the whole project stays cohesive.
        circle = Circle(radius=2.0, color=ACCENT)
        # `Create` traces the boundary; for filled shapes use
        # `DrawBorderThenFill` (see C04a).
        self.play(Create(circle))
        self.wait()


class C01b_ShapesGallery(NormalScene):
    """Tour of Manim's built-in geometric primitives.

    Concept: Manim ships with shape classes that all share the same
    styling API (`color`, `fill_opacity`, `stroke_width`, ...). Knowing
    which constructors exist saves you from rebuilding from `Polygon`.

    Why this matters: 80% of math diagrams are made of these shapes.
    Memorize the constructor signatures.

    Gotchas:
      - `Square(side_length=...)`, but `Rectangle(width=..., height=...)`.
      - `RegularPolygon(n)` for n-gons; `Star` is a regular polygram.
      - `Triangle()` has no required args (it's a regular 3-gon).
      - `Arrow` has start and end points; `Line` is the same but
        without arrowheads.
    """

    def construct(self) -> None:
        # Build a row of shapes. Group with `VGroup` so we can position
        # all of them at once via `arrange` (introduced fully in C02c).
        shapes = VGroup(
            Circle(radius=0.6, color=ACCENT),
            Square(side_length=1.2, color=ACCENT_2),
            Triangle(color=ACCENT_3),
            RegularPolygon(n=6, color=ACCENT),  # hexagon
            Star(n=5, outer_radius=0.7, color=ACCENT_2),
            Annulus(inner_radius=0.3, outer_radius=0.7, color=ACCENT_3),
        )
        # `arrange` lays children out along an axis with even spacing.
        shapes.arrange(RIGHT, buff=0.5)

        # Lines and arrows live in their own row beneath.
        line = Line(LEFT * 2, RIGHT * 2, color=FG)
        arrow = Arrow(LEFT * 2, RIGHT * 2, color=ACCENT, buff=0)
        dot = Dot(color=ACCENT_2, radius=0.1)
        lines = VGroup(line, arrow, dot).arrange(RIGHT, buff=0.5)
        lines.next_to(shapes, DOWN, buff=1.0)

        # Stagger creation so the eye sees each shape appear (LaggedStart
        # is detailed in C05b — for now, just trust it does this).
        self.play(LaggedStart(*[Create(s) for s in shapes], lag_ratio=0.15))
        self.play(LaggedStart(*[Create(s) for s in lines], lag_ratio=0.2))
        self.wait()


class C01c_StyleAndColor(NormalScene):
    """Styling Mobjects: stroke, fill, opacity, theme palette.

    Concept: every VMobject (vector mobject) has a stroke (outline)
    and a fill (interior). You set them via constructor kwargs or via
    `set_stroke` / `set_fill` after the fact. Opacity is independent
    of color.

    Why this matters: 90% of "this looks rough" comes from default
    stroke widths and full-opacity fills. Subtle fills + a bold accent
    on stroke is the single biggest readability win.

    Gotchas:
      - `Circle(color=ACCENT)` sets BOTH stroke and fill color, but
        leaves fill opacity at 0 (transparent). To get a filled shape
        you also need `fill_opacity=...` or `.set_fill(..., opacity=...)`.
      - `set_fill(color, opacity=...)` returns the mobject, so chains
        are fine: `Circle(...).set_fill(ACCENT, opacity=0.25)`.
      - Theme colors are hex strings; Manim's color constants
        (`RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`, `BLACK`, ...) are
        also fine but break theme cohesion.
    """

    def construct(self) -> None:
        # Stroke-only: outline is ACCENT, interior is empty.
        outline = Circle(radius=1.0, color=ACCENT, stroke_width=6)
        # Filled with translucent accent + thicker stroke. The 25%
        # opacity is the tutorial's default for "filled but readable".
        filled = Circle(radius=1.0, color=ACCENT).set_fill(ACCENT, opacity=0.25)
        # Two-tone: stroke and fill differ — useful for emphasizing
        # a boundary against a contrasting interior.
        twotone = (
            Circle(radius=1.0)
            .set_stroke(ACCENT_2, width=6)
            .set_fill(ACCENT_3, opacity=0.4)
        )

        VGroup(outline, filled, twotone).arrange(RIGHT, buff=1.0)

        labels = VGroup(
            Text("stroke only", color=MUTED, font_size=28),
            Text("translucent fill", color=MUTED, font_size=28),
            Text("stroke + fill", color=MUTED, font_size=28),
        )
        # `next_to` positions one mobject relative to another.
        for circ, label in zip([outline, filled, twotone], labels):
            label.next_to(circ, DOWN, buff=0.4)

        self.play(Create(outline), Create(filled), Create(twotone))
        self.play(*[FadeIn(lbl, shift=UP * 0.2) for lbl in labels])
        self.wait()


# =============================================================================
# CHAPTER 02 — Position, Layout, Grouping
# -----------------------------------------------------------------------------
# Goal: place objects exactly where you want them. Master absolute and
# relative positioning, and group objects so you can move whole layouts.
# =============================================================================


class C02a_PositioningAbsolute(NormalScene):
    """Absolute positioning with `move_to` and `shift`.

    Concept: every Mobject lives in a 3D coordinate space. `move_to(p)`
    teleports its center to point `p`. `shift(v)` translates by vector
    `v`. The constants `UP`, `DOWN`, `LEFT`, `RIGHT`, `IN`, `OUT`, and
    `ORIGIN` are unit vectors / origin in that space.

    Why this matters: relative layout (`next_to`, `arrange`) is usually
    nicer, but absolute coordinates are essential for plots, anchors,
    and reproducible diagrams.

    Gotchas:
      - `move_to` takes a *point*, `shift` takes a *vector*. Easy to
        confuse when both are written `2*UP+RIGHT`.
      - The frame center is `ORIGIN = [0, 0, 0]`. NormalScene's frame
        is 8 units tall by default, so `2 * UP` is one quarter of the
        way up the screen.
    """

    def construct(self) -> None:
        anchor = Dot(ORIGIN, color=MUTED)
        # `move_to` — absolute placement.
        a = Dot(color=ACCENT).move_to(2 * UP + 3 * LEFT)
        b = Dot(color=ACCENT_2).move_to(2 * DOWN + 3 * RIGHT)

        # `shift` — relative move from current position.
        c = Dot(color=ACCENT_3)  # starts at ORIGIN
        c.shift(2 * RIGHT + UP)

        labels = VGroup(
            Text("move_to(2*UP + 3*LEFT)", color=FG, font_size=22).next_to(a, UP, buff=0.2),
            Text("move_to(2*DOWN + 3*RIGHT)", color=FG, font_size=22).next_to(b, DOWN, buff=0.2),
            Text("shift(2*RIGHT + UP)", color=FG, font_size=22).next_to(c, UP, buff=0.2),
        )
        self.play(FadeIn(anchor), FadeIn(a), FadeIn(b), FadeIn(c))
        self.play(Write(labels))
        self.wait()


class C02b_PositioningRelative(NormalScene):
    """Relative positioning: `next_to`, `align_to`, `to_edge`, `to_corner`.

    Concept: position one Mobject relative to another (or to a frame
    edge). Manim figures out the bounding boxes for you.

    Why this matters: relative positioning survives changes. If you
    grow the title font, a `next_to(title, DOWN)` subtitle stays
    correctly placed; absolute coordinates would need editing.

    Gotchas:
      - `next_to(other, direction, buff=0.25)`: `buff` is the gap.
        Default 0.25 looks tight; bump to 0.4-0.6 for breathing room.
      - `to_edge(UP)` snaps to the top edge with a default buffer of
        ~0.5 units (`MED_LARGE_BUFF`). Pass `buff=` to override.
      - `align_to(other, direction)` aligns one edge of self to the
        same edge of `other` — handy for left-aligning a column of text.
    """

    def construct(self) -> None:
        title = Text("Title", color=FG, font_size=56).to_edge(UP)
        subtitle = (
            Text("subtitle, next_to title with buff=0.4", color=MUTED, font_size=28)
            .next_to(title, DOWN, buff=0.4)
        )
        corner = Square(side_length=0.8, color=ACCENT).to_corner(DR, buff=0.5)

        # A small column where each row left-aligns to the first row.
        row1 = Text("first row", color=FG, font_size=28)
        row2 = Text("second row", color=FG, font_size=28).next_to(row1, DOWN, buff=0.2)
        row3 = Text("third row is wider", color=FG, font_size=28).next_to(row2, DOWN, buff=0.2)
        # Without `align_to`, `next_to(..., DOWN)` centers each row.
        # `align_to(row1, LEFT)` snaps each row's LEFT edge to row1's.
        row2.align_to(row1, LEFT)
        row3.align_to(row1, LEFT)
        column = VGroup(row1, row2, row3).move_to(LEFT * 3)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
        self.play(FadeIn(corner))
        self.play(LaggedStart(Write(row1), Write(row2), Write(row3), lag_ratio=0.3))
        self.wait()


class C02c_VGroupAndArrange(NormalScene):
    """Group multiple Mobjects and lay them out as one.

    Concept: `VGroup(*mobjects)` bundles vector mobjects so `arrange`,
    `move_to`, `set_color`, and animations apply to the whole group.

    Why this matters: groups are how you build reusable layout units.
    A "title + subtitle + underline" trio becomes one object you can
    `to_edge(UP)` once, instead of positioning each piece manually.

    Gotchas:
      - `VGroup` is for VMobjects (vector); `Group` is for any Mobject
        including `ImageMobject`. Most of the time `VGroup` is right.
      - `arrange` mutates the group in place AND returns it.
      - `arrange_in_grid(rows, cols)` lays out into a grid; either
        `rows` or `cols` may be None to compute automatically.
    """

    def construct(self) -> None:
        # Six dots arranged in a row.
        dots_row = VGroup(*[Dot(color=ACCENT, radius=0.15) for _ in range(6)])
        dots_row.arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.5)

        # Same six dots in a 2x3 grid (separate instances; reusing the
        # row dots after arrange would re-layout them).
        grid_dots = VGroup(*[Dot(color=ACCENT_2, radius=0.15) for _ in range(6)])
        grid_dots.arrange_in_grid(rows=2, cols=3, buff=0.6)

        # Animate the group as a whole using `.animate` (covered fully
        # in C04b). Notice we move 6 dots with one animation call.
        self.play(LaggedStart(*[FadeIn(d) for d in dots_row], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(d) for d in grid_dots], lag_ratio=0.05))
        self.play(grid_dots.animate.shift(DOWN * 0.5).set_color(ACCENT_3))
        self.wait()


class C02d_ShortFormatLayout(ShortScene):
    """Composing for 1080x1920 portrait (vertical / Reels / Shorts).

    Concept: same Manim, different aspect ratio. ShortScene pins the
    frame to a tall canvas so `to_edge(UP)` and `to_edge(DOWN)` are
    far apart and centered text dominates.

    Why this matters: vertical formats live and die on big text and
    high-contrast layouts. The same NormalScene composition usually
    looks empty when rendered short.

    Gotchas:
      - The frame is taller than wide, so `RIGHT` and `LEFT` cover
        less screen than `UP`/`DOWN`. Avoid wide horizontal layouts.
      - `to_edge(UP, buff=1.0)` keeps text safely inside the visible
        area on phones (some apps clip the top/bottom).
    """

    def construct(self) -> None:
        title = Text("VERTICAL", color=FG, font_size=96, weight=BOLD).to_edge(UP, buff=1.5)
        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=8).next_to(title, DOWN, buff=0.4)
        # Stack a few hero numbers down the middle.
        rows = VGroup(
            Text("1080 px wide", color=MUTED, font_size=44),
            Text("1920 px tall", color=MUTED, font_size=44),
            Text("9 : 16 ratio", color=MUTED, font_size=44),
        ).arrange(DOWN, buff=0.6)
        rows.move_to(ORIGIN)
        bottom = Text("subscribe", color=ACCENT, font_size=56, weight=BOLD).to_edge(DOWN, buff=1.5)

        self.play(Write(title))
        self.play(GrowFromCenter(rule))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in rows], lag_ratio=0.3))
        self.play(FadeIn(bottom, shift=UP * 0.3))
        self.wait()


# =============================================================================
# CHAPTER 03 — Text, Math, Equations
# -----------------------------------------------------------------------------
# Goal: render words and formulas; animate equation manipulation. The
# TransformMatchingTex pattern in this chapter is THE workhorse for
# math explainers — internalize it.
# =============================================================================


class C03a_TextVsMathTexVsTex(NormalScene):
    """Three text classes: when each is the right tool.

    Concept:
      - `Text("...")` uses Pango (system fonts). Fast, supports
        emoji and non-Latin scripts. Use for prose, titles, UI labels.
      - `Tex(r"...")` runs LaTeX. Use for prose that mixes math
        inline and needs full LaTeX (e.g. `\\textit{}`).
      - `MathTex(r"...")` runs LaTeX in math mode (no \\$\\$). Use for
        formulas. Each positional arg becomes a separately-indexable
        submobject — critical for TransformMatchingTex (next scene).

    Why this matters: choosing the right one early avoids painful
    refactors. If you'll ever animate the equation's pieces, start
    with `MathTex` and pre-tokenize.

    Gotchas:
      - LaTeX requires a working TeX install. First render is slow
        (compile + cache); subsequent renders are fast.
      - Backslashes need escaping or raw strings: `r"\\frac{1}{2}"`.
    """

    def construct(self) -> None:
        plain = Text("Hello, world", color=FG, font_size=48)
        latex = Tex(r"Hello, $\int_0^1 x\,dx = \tfrac{1}{2}$", color=FG, font_size=48)
        math = MathTex(r"\int_0^1 x\,dx = \tfrac{1}{2}", color=FG, font_size=64)

        VGroup(plain, latex, math).arrange(DOWN, buff=0.8)

        labels = VGroup(
            Text("Text  (Pango)", color=MUTED, font_size=22),
            Text("Tex  (LaTeX, mixed)", color=MUTED, font_size=22),
            Text("MathTex  (LaTeX math mode)", color=MUTED, font_size=22),
        )
        for label, target in zip(labels, [plain, latex, math]):
            label.next_to(target, LEFT, buff=0.6)

        self.play(LaggedStart(Write(plain), Write(latex), Write(math), lag_ratio=0.4))
        self.play(FadeIn(labels))
        self.wait()


class C03b_TransformMatchingTex_AlgebraStep(NormalScene):
    """Animate one algebra step:  x + 2 = 5  ->  x = 5 - 2.

    Concept: `TransformMatchingTex` matches MathTex submobjects by
    rendered LaTeX string. Equal substrings glide to their new
    positions; unmatched parts fade.

    Why this matters: a plain `Transform(eq1, eq2)` between two
    MathTex objects produces a blurry crossfade — Manim has no idea
    which token is which. TransformMatchingTex turns the same call
    into a readable algebraic move. THE workhorse for math explainers.

    Gotchas:
      - Substring matching is greedy and string-based. If "2" appears
        twice with different meanings, Manim cannot tell them apart.
        Fix: split with explicit args so each token is its own submob:
            MathTex("x", "+", "2", "=", "5")
      - For non-math text, use `TransformMatchingShapes` (C03d).
    """

    def construct(self) -> None:
        # Token-split MathTex so matching is unambiguous; without the
        # split, "+" might match "-" by being a 1-character symbol.
        lhs = MathTex("x", "+", "2", "=", "5", color=FG, font_size=72)
        rhs = MathTex("x", "=", "5", "-", "2", color=FG, font_size=72)
        # Color the moved term so the eye tracks it across the step.
        lhs[2].set_color(ACCENT)  # "2"
        rhs[3].set_color(ACCENT)  # "-"
        rhs[4].set_color(ACCENT)  # "2"

        self.play(Write(lhs))
        self.wait(0.5)
        # run_time slightly longer than default so viewers can follow.
        self.play(TransformMatchingTex(lhs, rhs), run_time=1.5)
        self.wait()


class C03c_TransformMatchingTex_Multistep(NormalScene):
    """Chain three algebra steps and track a coefficient through all of them.

    Concept: build each successive equation as its own MathTex, then
    play TransformMatchingTex between adjacent pairs. Use color to
    keep the eye anchored on whichever term you want to follow.

    Why this matters: most "show your work" animations are this
    pattern: a sequence of equations where each step exposes the next
    move. The trick is keeping tokenizations consistent — same number
    of args, same string content for unchanged tokens.

    Gotchas:
      - If consecutive equations don't share *any* tokens, Manim falls
        back to crossfade. To force tracking, pre-split aggressively.
      - Re-coloring inside a TransformMatchingTex is tricky — set
        colors *before* the transform on both source and target.
    """

    def construct(self) -> None:
        eq1 = MathTex("3x", "+", "6", "=", "12", color=FG, font_size=72)
        eq2 = MathTex("3x", "=", "12", "-", "6", color=FG, font_size=72)
        eq3 = MathTex("3x", "=", "6", color=FG, font_size=72)
        eq4 = MathTex("x", "=", "2", color=FG, font_size=72)

        # Track the leading "3x" coefficient with ACCENT through every step.
        for eq in (eq1, eq2, eq3):
            eq[0].set_color(ACCENT)
        eq4[0].set_color(ACCENT)

        self.play(Write(eq1))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.4)
        self.wait(0.3)
        self.play(TransformMatchingTex(eq2, eq3), run_time=1.4)
        self.wait(0.3)
        self.play(TransformMatchingTex(eq3, eq4), run_time=1.4)
        self.wait()


class C03d_TransformMatchingShapes_Words(NormalScene):
    """Word-level transform for non-math text.

    Concept: `TransformMatchingShapes` matches glyphs by *shape*, not
    by string content. Useful when you have two `Text` blobs (Pango,
    not LaTeX) and want shared characters to glide between them.

    Why this matters: tokenized MathTex is great for formulas but
    overkill for prose. For two Text mobjects, this is the closest
    you get to "smart" word transitions.

    Gotchas:
      - Matching by shape can be surprising — different fonts or
        weights produce different glyph outlines and won't match.
      - For paragraph-level transitions, a plain crossfade
        (`ReplacementTransform`) is often cleaner than a shape match.
    """

    def construct(self) -> None:
        a = Text("morning", color=FG, font_size=72)
        b = Text("mourning", color=ACCENT, font_size=72)

        self.play(Write(a))
        self.wait(0.5)
        # Letters that exist in both ("m", "o", "r", "n", "i", "n", "g")
        # glide between positions; "u" is added.
        self.play(TransformMatchingShapes(a, b), run_time=1.5)
        self.wait()


# =============================================================================
# CHAPTER 04 — Animation Verbs
# -----------------------------------------------------------------------------
# Goal: know the standard creation, transformation, and destruction
# animations so you can pick the right verb for the moment.
# =============================================================================


class C04a_CreationAnimations(NormalScene):
    """The creation family: Create, Write, DrawBorderThenFill, FadeIn,
    GrowFromCenter, SpinInFromNothing.

    Concept: each verb is a different "how" for putting a Mobject on
    screen. Pick by tone — `Write` feels handwritten, `Create` feels
    geometric, `FadeIn` is neutral, `GrowFromCenter` and
    `SpinInFromNothing` are loud.

    Why this matters: mismatched verbs distract. A formula that
    `GrowFromCenter`s feels cartoonish; a circle that `Write`s feels
    bizarre because Write is for stroke-traced shapes (Text/Tex).

    Gotchas:
      - `Write` and `Create` both trace strokes, but `Write` is tuned
        for Text/Tex and may look choppy on filled shapes.
      - `DrawBorderThenFill` only makes sense for shapes with a fill.
    """

    def construct(self) -> None:
        # Six demo Mobjects, one per verb.
        c1 = Circle(radius=0.6, color=ACCENT)
        c2 = Text("Write", color=FG, font_size=36)
        c3 = Square(side_length=1.0, color=ACCENT_2).set_fill(ACCENT_2, opacity=0.3)
        c4 = Triangle(color=ACCENT_3)
        c5 = Star(n=5, outer_radius=0.6, color=ACCENT)
        c6 = RegularPolygon(n=6, color=ACCENT_2)

        row = VGroup(c1, c2, c3, c4, c5, c6).arrange(RIGHT, buff=0.7)

        labels = VGroup(
            Text("Create", color=MUTED, font_size=22),
            Text("Write", color=MUTED, font_size=22),
            Text("DrawBorderThenFill", color=MUTED, font_size=22),
            Text("FadeIn", color=MUTED, font_size=22),
            Text("GrowFromCenter", color=MUTED, font_size=22),
            Text("SpinInFromNothing", color=MUTED, font_size=22),
        )
        for lbl, mob in zip(labels, row):
            lbl.next_to(mob, DOWN, buff=0.4)

        # Play each verb on its labeled subject, slightly staggered.
        self.play(Create(c1), FadeIn(labels[0]))
        self.play(Write(c2), FadeIn(labels[1]))
        self.play(DrawBorderThenFill(c3), FadeIn(labels[2]))
        self.play(FadeIn(c4), FadeIn(labels[3]))
        self.play(GrowFromCenter(c5), FadeIn(labels[4]))
        self.play(SpinInFromNothing(c6), FadeIn(labels[5]))
        self.wait()


class C04b_TransformVariants(NormalScene):
    """Transform vs ReplacementTransform vs FadeTransform — what stays
    in the scene tree.

    Concept:
      - `Transform(a, b)`: morphs `a` to look like `b`. After the
        animation, `a` is the one in the scene; `b` is discarded.
      - `ReplacementTransform(a, b)`: morphs `a` into `b`. After the
        animation, `b` is in the scene; `a` is removed.
      - `FadeTransform(a, b)`: crossfade. Less precise than the above
        but no shape constraints — handy for text or images.

    Why this matters: future references ("now move that thing") must
    point at the right object. If you `Transform(a, b)` and then try
    to `self.play(b.animate.shift(UP))`, b isn't on screen — a is.
    `ReplacementTransform` removes the surprise.

    Gotchas:
      - The `.animate` syntax on a transformed mobject is fine; just
        be sure you're animating the one that actually exists.
      - For chains of transforms, ReplacementTransform is almost
        always what you want.
    """

    def construct(self) -> None:
        a = Square(side_length=1.5, color=ACCENT).shift(LEFT * 3)
        b = Circle(radius=0.8, color=ACCENT_2).shift(LEFT * 3)
        c = Triangle(color=ACCENT_3).scale(1.2).shift(RIGHT * 0.5)
        d = RegularPolygon(n=6, color=ACCENT).shift(RIGHT * 0.5)
        e = Text("morning", color=FG, font_size=48).shift(RIGHT * 4)
        f = Text("evening", color=ACCENT, font_size=48).shift(RIGHT * 4)

        labels = VGroup(
            Text("Transform", color=MUTED, font_size=22).next_to(a, DOWN, buff=2.0),
            Text("ReplacementTransform", color=MUTED, font_size=22).next_to(c, DOWN, buff=2.0),
            Text("FadeTransform", color=MUTED, font_size=22).next_to(e, DOWN, buff=2.0),
        )

        self.play(FadeIn(a), FadeIn(c), FadeIn(e), FadeIn(labels))
        self.wait(0.4)
        # `Transform` keeps `a` in scene; `b` exists only as a target.
        self.play(Transform(a, b))
        # `ReplacementTransform` swaps `c` out and `d` in.
        self.play(ReplacementTransform(c, d))
        # `FadeTransform` crossfades.
        self.play(FadeTransform(e, f))
        self.wait()


class C04c_DestructionAnimations(NormalScene):
    """Removing Mobjects: FadeOut, Uncreate, Unwrite.

    Concept: mirror image of the creation family. `Uncreate` reverses
    `Create`, `Unwrite` reverses `Write`, `FadeOut` is the neutral
    catch-all.

    Why this matters: smooth scene exits matter for pacing. Don't
    just leave clutter on screen between sections — fade or uncreate
    out, then bring the next section in.

    Gotchas:
      - `Unwrite` is tuned for Text/Tex; reversing a `Create` is what
        `Uncreate` is for.
      - To clear everything: `self.play(FadeOut(*self.mobjects))`.
        Useful between sections of a longer composition.
    """

    def construct(self) -> None:
        c = Circle(radius=1.0, color=ACCENT).shift(LEFT * 4)
        s = Square(side_length=1.5, color=ACCENT_2)
        t = Text("Unwrite me", color=FG, font_size=42).shift(RIGHT * 3.5)

        self.play(Create(c), Create(s), Write(t))
        self.wait(0.4)
        # Each Mobject leaves with the verb that suits its creation.
        self.play(Uncreate(c), FadeOut(s), Unwrite(t))
        self.wait()


# =============================================================================
# CHAPTER 05 — Timing, Rate, Composition
# -----------------------------------------------------------------------------
# Goal: control WHEN things happen and HOW they ease. Combine animations
# in parallel, in sequence, and with stagger.
# =============================================================================


class C05a_RunTimeAndRateFuncs(NormalScene):
    """`run_time` controls duration; `rate_func` controls easing.

    Concept: every Animation accepts `run_time` (seconds) and
    `rate_func` (a [0,1]->[0,1] function). The default is `smooth`
    (ease-in-out). Other built-ins: `linear`, `there_and_back`,
    `rush_into`, `rush_from`, `ease_in_quad`, `ease_out_quad`, ...

    Why this matters: easing is the difference between a video that
    feels alive and one that feels mechanical. Linear motion looks
    robotic to humans; smooth motion is the floor for "professional".

    Gotchas:
      - `there_and_back` returns to start, so chain it with care
        (the next animation begins from the original position).
      - You can write custom rate functions: any `f(t: float) -> float`
        that maps `[0,1] -> [0,1]` works.
    """

    def construct(self) -> None:
        # Four dots that all travel the same horizontal distance.
        start_x = -5
        end_x = 5
        dots = VGroup(*[Dot(color=ACCENT, radius=0.18) for _ in range(4)])
        for i, d in enumerate(dots):
            d.move_to([start_x, 1.5 - i * 1.0, 0])
        labels = VGroup(
            Text("linear", color=MUTED, font_size=24),
            Text("smooth (default)", color=MUTED, font_size=24),
            Text("there_and_back", color=MUTED, font_size=24),
            Text("rush_into", color=MUTED, font_size=24),
        )
        for lbl, d in zip(labels, dots):
            lbl.next_to(d, LEFT, buff=0.4)

        self.play(FadeIn(dots), FadeIn(labels))
        # Animate all four with different rate_func, same run_time.
        self.play(
            dots[0].animate.move_to([end_x, 1.5, 0]),
            dots[1].animate.move_to([end_x, 0.5, 0]),
            dots[2].animate.move_to([end_x, -0.5, 0]),
            dots[3].animate.move_to([end_x, -1.5, 0]),
            run_time=2.5,
            rate_func=rf.linear,  # only applies if not overridden per-anim
        )
        # The above applies `linear` to all four. To get a real side-by-side
        # comparison, animate each as its own play with its own rate_func.
        # We do that here by resetting and replaying.
        for d, y in zip(dots, [1.5, 0.5, -0.5, -1.5]):
            d.move_to([start_x, y, 0])
        self.play(
            AnimationGroup(
                dots[0].animate(rate_func=rf.linear).move_to([end_x, 1.5, 0]),
                dots[1].animate(rate_func=rf.smooth).move_to([end_x, 0.5, 0]),
                dots[2].animate(rate_func=rf.there_and_back).move_to([end_x, -0.5, 0]),
                dots[3].animate(rate_func=rf.rush_into).move_to([end_x, -1.5, 0]),
                lag_ratio=0,
            ),
            run_time=2.5,
        )
        self.wait()


class C05b_AnimationGroup_LaggedStart(NormalScene):
    """Parallel vs staggered playback. `AnimationGroup`, `LaggedStart`,
    `Succession`.

    Concept:
      - `AnimationGroup(*anims)` plays all at once (default `lag_ratio=0`).
      - `LaggedStart(*anims, lag_ratio=0.3)` staggers starts: each
        animation begins after `lag_ratio * previous.run_time`.
      - `Succession(*anims)` plays strictly one after another.

    Why this matters: a row of items appearing simultaneously is busy;
    the same row with `lag_ratio=0.15` reads as "one then the next"
    and the eye tracks naturally.

    Gotchas:
      - `lag_ratio=1.0` is identical to `Succession`.
      - `lag_ratio=0.0` is identical to `AnimationGroup`.
      - Inside `self.play(LaggedStart(...), run_time=N)`, N is the
        TOTAL duration including the stagger.
    """

    def construct(self) -> None:
        # Eight bars of increasing height — a natural staggered intro.
        heights = [0.5, 0.9, 1.4, 1.8, 2.2, 1.6, 1.0, 0.6]
        bars = VGroup(
            *[
                Rectangle(width=0.6, height=h, color=ACCENT, fill_opacity=0.6)
                for h in heights
            ]
        )
        bars.arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to(DOWN * 0.5)

        # Build a fresh copy for each pattern so we can show all three.
        title = Text("LaggedStart, lag_ratio=0.15", color=FG, font_size=32).to_edge(UP)
        self.play(FadeIn(title))
        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
            run_time=2.0,
        )
        self.wait(0.5)
        self.play(FadeOut(bars), Unwrite(title))

        bars2 = bars.copy()
        title2 = Text("AnimationGroup (parallel)", color=FG, font_size=32).to_edge(UP)
        self.play(FadeIn(title2))
        self.play(
            AnimationGroup(*[GrowFromEdge(b, DOWN) for b in bars2], lag_ratio=0),
            run_time=1.0,
        )
        self.wait()


class C05c_ShortFormatBeatTiming(ShortScene):
    """Pacing a 15-second vertical clip so it feels snappy.

    Concept: short-form video lives on rhythm. Hook in <2s, body in
    8-10s, payoff in 3-4s. Each beat should be a `self.play` followed
    by an intentional `wait` long enough to read but short enough to
    keep momentum.

    Why this matters: most beginner ManimCE shorts feel slow because
    every animation defaults to 1s and every `wait()` is 1s. Add up
    a few of those and you're past 30s with nothing said.

    Gotchas:
      - `wait(0.4)` is usually enough between beats. Save full `wait()`
        for the hold at the very end.
      - Run-time of `Write` scales with text length; for short hooks,
        force it: `Write(text, run_time=0.6)`.
    """

    def construct(self) -> None:
        # Beat 1 — hook (0-2s)
        hook = Text("did you know?", color=ACCENT, font_size=72, weight=BOLD)
        hook.to_edge(UP, buff=2.0)
        self.play(Write(hook, run_time=0.7))
        self.wait(0.4)

        # Beat 2 — claim (2-6s)
        claim = MathTex(
            r"e^{i\pi} + 1 = 0",
            color=FG,
            font_size=88,
        )
        self.play(FadeIn(claim, shift=UP * 0.3, run_time=0.6))
        self.wait(0.6)

        # Beat 3 — emphasis (6-10s)
        box = SurroundingRectangle(claim, color=ACCENT, buff=0.3)
        self.play(Create(box, run_time=0.6))
        self.play(Indicate(claim, color=ACCENT_2, scale_factor=1.15, run_time=0.8))
        self.wait(0.4)

        # Beat 4 — payoff (10-15s)
        tag = Text("Euler's identity", color=MUTED, font_size=44).to_edge(DOWN, buff=2.0)
        self.play(FadeIn(tag, shift=UP * 0.2, run_time=0.6))
        self.wait(1.5)


# =============================================================================
# CHAPTER 06 — Updaters and ValueTrackers
# -----------------------------------------------------------------------------
# Goal: make Mobjects react every frame to changing state. This unlocks
# tangent lines that follow a slider, counters that tick, and any kind
# of "live" geometry.
# =============================================================================


class C06a_AddUpdaterBasics(NormalScene):
    """`mob.add_updater(lambda m, dt: ...)` runs every frame.

    Concept: an updater is a function called once per rendered frame.
    Signature is `(mob, dt) -> None`; you mutate `mob` in place. `dt`
    is seconds since the last frame.

    Why this matters: animations describe a transition; updaters
    describe ongoing behavior. Anything that should "always" happen
    (orbit, oscillate, follow) is an updater.

    Gotchas:
      - Forgetting to remove updaters with `remove_updater` (or
        `clear_updaters()`) leaves them running through later
        animations — usually you want them off after the segment.
      - Updaters run BEFORE animations on the same frame, which can
        cause subtle ordering bugs.
    """

    def construct(self) -> None:
        sun = Dot(color=ACCENT, radius=0.2)
        planet = Dot(color=ACCENT_2, radius=0.12).move_to(RIGHT * 2)
        # Updater closure captures `planet` and `sun`. We use an angle
        # variable on the planet itself so it persists across frames.
        planet.angle = 0.0

        def orbit(m: Mobject, dt: float) -> None:
            m.angle += dt * 1.5  # radians per second
            m.move_to(sun.get_center() + 2 * np.array([np.cos(m.angle), np.sin(m.angle), 0]))

        planet.add_updater(orbit)
        self.add(sun, planet)
        # `wait` advances time, so updaters fire even without `play`.
        self.wait(4)
        # Always clean up updaters when the segment ends.
        planet.clear_updaters()


class C06b_ValueTrackerNumber(NormalScene):
    """`ValueTracker` + `DecimalNumber` for animated counters.

    Concept: `ValueTracker(x)` is a Mobject whose only state is a
    scalar. You animate it with `tracker.animate.set_value(y)`. Other
    Mobjects with updaters read `tracker.get_value()` to stay in sync.

    Why this matters: separating "what changes" (the tracker) from
    "what shows" (the readouts and geometry) makes it trivial to wire
    up multiple dependent visuals — counter, bar, dot position — to
    the same scalar.

    Gotchas:
      - Without an updater, the DecimalNumber doesn't know to refresh.
        `add_updater(lambda m: m.set_value(tracker.get_value()))`.
      - For integer counters, use `num_decimal_places=0`.
    """

    def construct(self) -> None:
        tracker = ValueTracker(0)
        readout = DecimalNumber(0, num_decimal_places=0, color=ACCENT, font_size=120)
        readout.add_updater(lambda m: m.set_value(tracker.get_value()))

        label = Text("subscribers", color=MUTED, font_size=36)
        VGroup(readout, label).arrange(DOWN, buff=0.4)

        self.add(readout, label)
        # Tween the scalar; the updater pulls each frame's value out.
        self.play(tracker.animate.set_value(10000), run_time=4, rate_func=rf.smooth)
        self.wait()
        readout.clear_updaters()


class C06c_AlwaysRedraw(NormalScene):
    """`always_redraw(lambda: ...)` for derived geometry.

    Concept: `always_redraw(fn)` returns a Mobject that is REBUILT
    from `fn()` every frame. Use it when an object's *shape* (not
    just position) depends on tracker state.

    Why this matters: `add_updater` mutates an existing Mobject;
    `always_redraw` replaces it entirely. Replacement is simpler when
    the geometry is a pure function of state — e.g. a chord on a
    circle, where endpoints depend on an angle tracker.

    Gotchas:
      - The lambda must build a fresh Mobject each call; reusing the
        same Mobject reference across calls breaks the redraw.
      - `always_redraw` Mobjects can't be transformed cleanly (their
        identity changes each frame). Use plain `add_updater` if you
        need `Transform` to work mid-animation.
    """

    def construct(self) -> None:
        circle = Circle(radius=2.5, color=MUTED).set_stroke(width=2)
        angle = ValueTracker(0)

        # Dot is rebuilt each frame at the tracker-defined angle.
        dot = always_redraw(
            lambda: Dot(
                circle.point_from_proportion((angle.get_value() / TAU) % 1.0),
                color=ACCENT,
                radius=0.12,
            )
        )
        # Radial line from center to the dot — also rebuilt each frame.
        radius_line = always_redraw(
            lambda: Line(circle.get_center(), dot.get_center(), color=ACCENT_2)
        )

        self.play(Create(circle))
        self.add(radius_line, dot)
        self.play(angle.animate.set_value(TAU), run_time=4, rate_func=rf.smooth)
        self.wait()


# =============================================================================
# CHAPTER 07 — Coordinate Systems and Plotting
# -----------------------------------------------------------------------------
# Goal: place mathematics in a coordinate system. Plot functions, mark
# areas, draw tangents, and convert between math coordinates and screen
# coordinates with c2p / p2c.
# =============================================================================


class C07a_AxesAndPlot(NormalScene):
    """`Axes` + `plot` + axis labels.

    Concept: `Axes(x_range, y_range)` builds a coordinate system.
    `axes.plot(fn)` returns a graph (a ParametricFunction in disguise)
    of `fn` over the axes' x_range. Axis labels via `get_x_axis_label`
    and `get_y_axis_label`.

    Why this matters: plots are the bread and butter of math
    explainers. Get the axes right once and reuse the pattern.

    Gotchas:
      - `x_range` is `[start, end, step]`. The step controls the tick
        spacing, not the plotting resolution.
      - Functions must be defined over the full x_range or you'll get
        a numerical error. Use `x_range=[a, b]` on `plot` to limit it.
    """

    def construct(self) -> None:
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=10,
            y_length=5.5,
            axis_config={"color": MUTED, "include_tip": True},
        )
        graph = axes.plot(lambda x: 0.5 * x**2 - 1, color=ACCENT)
        graph_label = axes.get_graph_label(graph, MathTex("y = \\tfrac{1}{2}x^2 - 1"))
        graph_label.set_color(FG)

        x_label = axes.get_x_axis_label(MathTex("x").set_color(FG))
        y_label = axes.get_y_axis_label(MathTex("y").set_color(FG))

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(graph_label))
        self.wait()


class C07b_NumberPlaneAndDots(NormalScene):
    """`NumberPlane` and `c2p` / `p2c` to bridge math <-> screen coords.

    Concept: `NumberPlane` is `Axes` with grid lines. `c2p(x, y)` =
    coords-to-point: takes math coordinates and returns the screen
    point. `p2c(point)` is the inverse.

    Why this matters: any time you place a Mobject *at* a math
    coordinate, you go through `c2p`. Forgetting this is the most
    common "why is my dot in the wrong place" bug.

    Gotchas:
      - `c2p` returns a 3D point even for 2D scenes (z=0). Pass it
        straight to `move_to` — no slicing needed.
      - `NumberPlane` gridlines can dominate the frame; lower the
        `background_line_style` opacity if needed.
    """

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_color": MUTED, "stroke_opacity": 0.3},
            axis_config={"color": MUTED},
        )
        # Place dots at specific math coordinates via c2p.
        coords = [(-3, 2), (1, -1), (3, 3), (-2, -2)]
        dots = VGroup(*[Dot(plane.c2p(x, y), color=ACCENT) for x, y in coords])
        labels = VGroup(
            *[
                MathTex(f"({x},{y})", color=FG, font_size=28).next_to(d, UR, buff=0.1)
                for (x, y), d in zip(coords, dots)
            ]
        )

        self.play(Create(plane))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))
        self.play(LaggedStart(*[Write(lbl) for lbl in labels], lag_ratio=0.2))
        self.wait()


class C07c_ParametricAndPolar(NormalScene):
    """`ParametricFunction` for parametric and polar curves.

    Concept: `ParametricFunction(fn, t_range)` plots `fn(t)` for `t`
    in t_range. `fn` returns a 3D point. For polar, parametrize as
    `(r(t)*cos(t), r(t)*sin(t), 0)`.

    Why this matters: many curves (Lissajous, cardioid, rose) are
    naturally parametric, not y=f(x). Trying to plot them with `plot`
    fails because they aren't single-valued.

    Gotchas:
      - The function's output must be a numpy array of shape (3,).
        Forgetting the trailing 0 gives "shape (2,)" errors.
      - `t_range = [start, end, step]` — `step` is the plotting
        resolution. Smaller step = smoother curve = slower render.
    """

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_color": MUTED, "stroke_opacity": 0.2},
            axis_config={"color": MUTED},
        )

        # A rose curve: r = cos(2*theta) -> (cos(2t)*cos(t), cos(2t)*sin(t)).
        def rose(t: float) -> np.ndarray:
            r = np.cos(2 * t)
            return plane.c2p(r * np.cos(t), r * np.sin(t))

        curve = ParametricFunction(rose, t_range=[0, TAU, 0.01], color=ACCENT)

        label = MathTex("r = \\cos(2\\theta)", color=FG, font_size=44).to_edge(UP)

        self.play(Create(plane))
        self.play(Create(curve, run_time=3, rate_func=rf.linear))
        self.play(Write(label))
        self.wait()


class C07d_AreaUnderCurve_Riemann(NormalScene):
    """`get_area` + `get_riemann_rectangles` driven by a ValueTracker.

    Concept: `axes.get_area(graph, x_range)` shades under a graph.
    `axes.get_riemann_rectangles(graph, x_range, dx)` returns
    rectangles. Wrap the rectangles in `always_redraw` to shrink dx
    interactively.

    Why this matters: this is the canonical "calculus is the limit"
    visual. Watching dx -> 0 is more convincing than any prose.

    Gotchas:
      - `dx` must divide the interval evenly (or you get a partial
        last rectangle). Choose interval and dx values that fit.
      - Rectangles can be VERY many at small dx; render time scales.
    """

    def construct(self) -> None:
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"color": MUTED},
        )
        graph = axes.plot(lambda x: 0.5 * x**2 + 0.5, color=ACCENT, x_range=[0, 3])
        label = MathTex("f(x) = \\tfrac{1}{2}x^2 + \\tfrac{1}{2}", color=FG, font_size=36)
        label.to_edge(UP)

        dx = ValueTracker(0.5)
        # always_redraw rebuilds rectangles each frame from current dx.
        rects = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph,
                x_range=[0, 3],
                dx=dx.get_value(),
                color=ACCENT_2,
                fill_opacity=0.5,
                stroke_width=1,
            )
        )

        self.play(Create(axes), Write(label))
        self.play(Create(graph))
        self.add(rects)
        self.play(dx.animate.set_value(0.05), run_time=4, rate_func=rf.smooth)
        self.wait()


class C07e_TangentLineWithSlope(NormalScene):
    """Live tangent line + slope readout via ValueTracker + always_redraw.

    Concept: a ValueTracker holds `x`. The tangent line, dot on the
    curve, and slope readout are all `always_redraw`/`add_updater`
    derivatives of that single tracker. Slide x; everything follows.

    Why this matters: this is the "secret" of every smooth derivative
    animation you've ever admired. One scalar + a few derived
    visuals = a tight, debuggable scene.

    Gotchas:
      - For a tangent line, you need the derivative. Either compute
        analytically (here) or numerically with a small h.
      - The tangent line's length is a styling choice — pick something
        that looks reasonable across the whole x sweep.
    """

    def construct(self) -> None:
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4.5,
            axis_config={"color": MUTED},
        )
        graph = axes.plot(np.sin, color=ACCENT)
        x_t = ValueTracker(-2.0)

        def f(x: float) -> float:
            return float(np.sin(x))

        def fp(x: float) -> float:  # f-prime, the derivative of sin.
            return float(np.cos(x))

        dot = always_redraw(
            lambda: Dot(axes.c2p(x_t.get_value(), f(x_t.get_value())), color=ACCENT_2)
        )

        def make_tangent() -> Line:
            x = x_t.get_value()
            slope = fp(x)
            half = 1.2
            x0, x1 = x - half, x + half
            y0, y1 = f(x) - slope * half, f(x) + slope * half
            return Line(axes.c2p(x0, y0), axes.c2p(x1, y1), color=ACCENT_3, stroke_width=4)

        tangent = always_redraw(make_tangent)

        slope_text = always_redraw(
            lambda: MathTex(
                f"f'(x) = {fp(x_t.get_value()):+.2f}",
                color=FG,
                font_size=42,
            ).to_edge(UP)
        )

        self.play(Create(axes), Create(graph))
        self.add(tangent, dot, slope_text)
        self.play(x_t.animate.set_value(2.0), run_time=4, rate_func=rf.smooth)
        self.wait()


# =============================================================================
# CHAPTER 08 — Annotation, Indicators, Braces
# -----------------------------------------------------------------------------
# Goal: draw the viewer's eye to specific parts of the frame. Braces,
# indicators, and arrows are how you say "look here".
# =============================================================================


class C08a_BraceWithLabel(NormalScene):
    """`Brace` underneath an expression, with a label.

    Concept: `Brace(mob, direction)` draws a curly brace along the
    given side of `mob`'s bounding box. `brace.get_text("...")` and
    `brace.get_tex(r"...")` return a positioned label.

    Why this matters: braces are the standard mathematical convention
    for grouping and naming. Use them when the semantics of "this
    chunk together is X" matter.

    Gotchas:
      - Brace direction is a unit vector (e.g. `DOWN` for under).
      - For long expressions, you may need to brace just a sub-part.
        Slice the MathTex: `Brace(eq[2:5], DOWN)`.
    """

    def construct(self) -> None:
        eq = MathTex("a^2", "+", "2ab", "+", "b^2", color=FG, font_size=72)
        # Brace under the cross term only.
        cross = eq[2]
        cross.set_color(ACCENT)
        brace = Brace(cross, DOWN, color=ACCENT)
        label = brace.get_text("cross term")
        label.set_color(MUTED)

        self.play(Write(eq))
        self.play(GrowFromCenter(brace), FadeIn(label, shift=DOWN * 0.2))
        self.wait()


class C08b_Indicators(NormalScene):
    """Indicate, Circumscribe, Flash, Wiggle, FocusOn.

    Concept: short, punchy animations that don't permanently change
    the Mobject — they just call attention to it. Use sparingly.

    Why this matters: a viewer's eye lands where motion is. If
    everything moves equally, nothing stands out. Indicators give you
    a "look here" beat without rebuilding state.

    Gotchas:
      - These animations are loud. One per beat is plenty; two or
        three back-to-back overload the viewer.
      - `Flash` defaults look small; bump `flash_radius` for impact.
    """

    def construct(self) -> None:
        # A 3x3 grid; we'll indicate one cell at a time.
        cells = VGroup(
            *[Square(side_length=1.0, color=MUTED, stroke_width=2) for _ in range(9)]
        ).arrange_in_grid(rows=3, cols=3, buff=0.1)
        nums = VGroup(
            *[MathTex(str(i + 1), color=FG, font_size=42) for i in range(9)]
        )
        for n, c in zip(nums, cells):
            n.move_to(c)

        self.play(Create(cells), Write(nums))
        self.wait(0.3)
        # Cycle through different indicators on different cells.
        self.play(Indicate(VGroup(cells[0], nums[0]), color=ACCENT))
        self.play(Circumscribe(VGroup(cells[4], nums[4]), color=ACCENT_2))
        self.play(Flash(cells[8].get_center(), color=ACCENT_3, flash_radius=0.7))
        self.play(Wiggle(VGroup(cells[2], nums[2]), scale_value=1.15))
        self.play(FocusOn(cells[6].get_center(), opacity=0.4))
        self.wait()


class C08c_ArrowsAndCallouts(NormalScene):
    """`Arrow`, `CurvedArrow`, and labeled callouts.

    Concept: arrows point at things. `Arrow(start, end)` is straight;
    `CurvedArrow(start, end, angle=...)` arcs. Combine with a `Text`
    or `MathTex` `next_to` the arrow midpoint for a callout.

    Why this matters: callouts are how diagrams stop being decorative
    and start being explanatory.

    Gotchas:
      - `Arrow(buff=0.1)` is a buffer between arrow tip and target —
        keep it small or the arrow looks detached.
      - For arrows tracking a moving Mobject, use `always_redraw` so
        the arrow updates each frame.
    """

    def construct(self) -> None:
        circle = Circle(radius=1.2, color=ACCENT).shift(LEFT * 3)
        square = Square(side_length=2.0, color=ACCENT_2).shift(RIGHT * 3)

        arrow1 = Arrow(circle.get_right(), square.get_left(), color=FG, buff=0.1)
        arrow2 = CurvedArrow(
            square.get_top() + UP * 0.1,
            circle.get_top() + UP * 0.1,
            color=ACCENT_3,
            angle=-PI / 3,
        )

        callout = Text("morphs into", color=MUTED, font_size=24)
        callout.next_to(arrow1, DOWN, buff=0.15)

        self.play(Create(circle), Create(square))
        self.play(GrowArrow(arrow1), Write(callout))
        self.play(Create(arrow2))
        self.wait()


# =============================================================================
# CHAPTER 09 — Camera and Assets
# -----------------------------------------------------------------------------
# Goal: move the camera around your scene; bring in external assets.
# =============================================================================


class C09a_MovingCamera_ZoomPan(MovingCameraScene):
    """Pan and zoom with `MovingCameraScene`.

    Concept: `MovingCameraScene` exposes `self.camera.frame` — a
    Mobject representing the camera's view. Animate it with
    `self.camera.frame.animate.scale(0.5).move_to(target)` to
    zoom and pan.

    Why this matters: zooming into detail (e.g. a single Riemann
    rectangle) lets one scene cover macro and micro views without
    rebuilding geometry.

    Gotchas:
      - This scene inherits from `MovingCameraScene`, NOT our
        project's `NormalScene`. We're stepping outside the project's
        bases here because `NormalScene` doesn't include camera
        controls. The cost: we manually set `background_color` since
        we lose `_apply_normal()` and `BG`.
      - `self.camera.frame.animate.scale(0.5)` zooms IN (smaller frame
        = bigger visible content). `scale(2.0)` zooms out.
    """

    def construct(self) -> None:
        # Manual setup since we're not on NormalScene.
        self.camera.background_color = BG

        # A field of dots; we'll zoom into one.
        dots = VGroup(
            *[Dot(np.array([x, y, 0]), color=ACCENT, radius=0.06)
              for x in np.arange(-6, 6.5, 0.5)
              for y in np.arange(-3, 3.5, 0.5)]
        )
        target = Dot(np.array([1.5, 1.0, 0]), color=ACCENT_2, radius=0.15)
        target_label = MathTex("(1.5, 1.0)", color=FG, font_size=24).next_to(target, UR, buff=0.1)

        self.play(FadeIn(dots), FadeIn(target))
        self.wait(0.4)
        # Zoom in by shrinking the frame and centering on the target.
        self.play(
            self.camera.frame.animate.scale(0.35).move_to(target),
            run_time=2,
        )
        self.play(Write(target_label))
        self.wait(0.5)
        # Zoom back out.
        self.play(
            self.camera.frame.animate.scale(1 / 0.35).move_to(ORIGIN),
            run_time=1.5,
        )
        self.wait()


class C09b_SVGAndImage(NormalScene):
    """`SVGMobject` and `ImageMobject` — when assets exist.

    Concept: vector assets become `SVGMobject` (transformable like
    any VMobject); raster images become `ImageMobject` (limited
    transforms — cannot be `Create`d like a path).

    Why this matters: not everything is a mathematical object. Logos,
    diagrams from outside Manim, photos — these are how you bring
    your animation into a real-world context.

    Gotchas:
      - This scene needs `assets/sample.svg` to exist. If it doesn't,
        we render a placeholder so the file at least runs.
      - `SVGMobject` supports `Create`, `Write`, color changes;
        `ImageMobject` mostly supports `FadeIn`, scale, position.
      - SVGs with embedded raster or filters import poorly. Keep them
        path-only when possible.
    """

    def construct(self) -> None:
        asset = Path(__file__).resolve().parent.parent / "assets" / "sample.svg"
        if not asset.exists():
            # Skip-with-message guard so the scene runs even without the asset.
            msg = Text(
                "Place an SVG at assets/sample.svg to see this lesson",
                color=MUTED,
                font_size=32,
            )
            self.play(Write(msg))
            self.wait()
            return

        svg = SVGMobject(str(asset)).set_color(ACCENT).scale(2.0)
        self.play(Create(svg, run_time=2))
        self.play(svg.animate.set_color(ACCENT_2).scale(0.8))
        self.wait()


# =============================================================================
# CHAPTER 10 — 3D
# -----------------------------------------------------------------------------
# Goal: render in three dimensions. Use NormalThreeDScene for camera
# orientation and ambient rotation, and Surface for parametric surfaces.
# =============================================================================


class C10a_ThreeDAxes_Basics(NormalThreeDScene):
    """`ThreeDAxes` and `set_camera_orientation`.

    Concept: 3D scenes use a camera with two angles: `phi` (vertical
    tilt, 0 = top-down, 90deg = side-on) and `theta` (rotation around
    z-axis). `set_camera_orientation(phi=..., theta=...)` snaps the
    camera; `move_camera` animates it.

    Why this matters: 3D requires a camera mindset. Pick angles that
    show the geometry's structure, not the angles you'd pick "if it
    were 2D".

    Gotchas:
      - Angles are in radians. Use `* DEGREES` for readability:
        `phi=70 * DEGREES`.
      - 3D scenes ignore most VMobject styling tricks (e.g. you cannot
        easily use `set_fill` for a 2D shape inside a 3D scene).
    """

    def construct(self) -> None:
        # Tilt down 70deg, swing 30deg around z. Standard "iso-ish" view.
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        # Place a cube at the origin so the axes have a 3D reference.
        cube = Cube(side_length=1.0, fill_color=ACCENT, fill_opacity=0.6, stroke_color=FG)

        self.play(Create(axes))
        self.play(FadeIn(cube))
        self.wait()


class C10b_Surface_Function(NormalThreeDScene):
    """`Surface` of z = f(x, y) with checkerboard coloring.

    Concept: `Surface(uv_func, u_range, v_range)` builds a parametric
    surface. Pass a function returning a 3D point; here we use
    `axes.c2p` so the surface lives in axes coordinates.

    Why this matters: every "function of two variables" picture in
    multivariable calculus is a Surface. Checker coloring helps the
    eye read curvature.

    Gotchas:
      - `resolution` is a (u_count, v_count) pair. Higher = smoother
        but slower. 20-30 each is usually enough for a tutorial.
      - `set_fill_by_checkerboard` takes two colors and applies them
        in alternating UV cells. Apply BEFORE adding to the scene.
    """

    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[0, 4, 1],
            x_length=5, y_length=5, z_length=3,
        )

        def saddle(u: float, v: float) -> np.ndarray:
            return axes.c2p(u, v, u**2 - v**2)

        surface = Surface(
            saddle,
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(24, 24),
        )
        surface.set_fill_by_checkerboard(ACCENT, ACCENT_2, opacity=0.7)
        surface.set_stroke(color=FG, width=0.5)

        self.play(Create(axes))
        self.play(Create(surface, run_time=2))
        self.wait()


class C10c_AmbientRotationAndMove(NormalThreeDScene):
    """`begin_ambient_camera_rotation` and `move_camera` for cinematics.

    Concept: ambient rotation spins the camera continuously (no
    `play` needed — happens during `wait`). `move_camera` animates
    a snap to new angles, like a camera cut.

    Why this matters: a slowly rotating 3D scene feels alive even
    when no animation is happening. Combine with a `move_camera` at
    the end to land on a hero angle.

    Gotchas:
      - Always pair `begin_ambient_camera_rotation` with
        `stop_ambient_camera_rotation` or the camera keeps spinning
        through subsequent renders within the same scene.
      - `move_camera` overrides ambient rotation while it runs.
    """

    def construct(self) -> None:
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=4,
        )
        sphere = Surface(
            lambda u, v: 1.4 * np.array([np.sin(u) * np.cos(v), np.sin(u) * np.sin(v), np.cos(u)]),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU],
            resolution=(24, 24),
        )
        sphere.set_fill_by_checkerboard(ACCENT, ACCENT_3, opacity=0.7)
        sphere.set_stroke(color=FG, width=0.4)

        self.play(Create(axes), Create(sphere))
        self.begin_ambient_camera_rotation(rate=0.4)  # radians/sec around z
        self.wait(3)
        self.stop_ambient_camera_rotation()
        # Hero shot: snap to a top-down then back.
        self.move_camera(phi=20 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()


# =============================================================================
# CHAPTER 11 — Showcase
# -----------------------------------------------------------------------------
# Goal: combine everything you've learned into one tight piece. Read
# the inline cross-references (e.g. "see C06b") to find the chapter
# that introduced each technique.
# =============================================================================


class C11_Showcase_DerivativeStory(NormalScene):
    """The derivative of sin(x), as a 30-second story.

    Title -> axes -> curve -> sliding tangent (C06c, C07e) -> live
    slope readout (C06b) -> TransformMatchingTex from numeric slope to
    symbolic derivative (C03b) -> Brace + Indicate finale (C08a, C08b).

    Concept: every technique here was introduced earlier in this
    file. The composition itself is the lesson — pacing, beat
    structure, and the discipline of letting one tracker drive the
    geometry while a separate `play` chain drives the prose.
    """

    def construct(self) -> None:
        # ---- Beat 1: title (see C02b for to_edge / next_to layout) ----
        title = Text("the derivative of sin(x)", color=FG, font_size=44).to_edge(UP, buff=0.5)
        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=4).next_to(title, DOWN, buff=0.2)
        rule.stretch_to_fit_width(title.width)
        self.play(Write(title), GrowFromCenter(rule))
        self.wait(0.4)

        # ---- Beat 2: axes + curve (see C07a) ----
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": MUTED},
        ).shift(DOWN * 0.5)
        graph = axes.plot(np.sin, color=ACCENT)
        graph_label = axes.get_graph_label(graph, MathTex("\\sin(x)", color=FG))
        self.play(Create(axes), run_time=1.0)
        self.play(Create(graph), Write(graph_label))
        self.wait(0.3)

        # ---- Beat 3: sliding tangent + live slope (see C06b, C07e) ----
        x_t = ValueTracker(-2.5)

        dot = always_redraw(
            lambda: Dot(axes.c2p(x_t.get_value(), float(np.sin(x_t.get_value()))), color=ACCENT_2)
        )

        def make_tangent() -> Line:
            x = x_t.get_value()
            slope = float(np.cos(x))
            half = 1.0
            return Line(
                axes.c2p(x - half, np.sin(x) - slope * half),
                axes.c2p(x + half, np.sin(x) + slope * half),
                color=ACCENT_3,
                stroke_width=5,
            )

        tangent = always_redraw(make_tangent)
        slope_readout = always_redraw(
            lambda: MathTex(
                f"\\text{{slope}} = {float(np.cos(x_t.get_value())):+.2f}",
                color=FG,
                font_size=36,
            ).to_corner(UR, buff=0.6)
        )

        self.add(tangent, dot, slope_readout)
        self.play(x_t.animate.set_value(2.5), run_time=4, rate_func=rf.smooth)
        self.wait(0.3)

        # ---- Beat 4: TransformMatchingTex slope -> symbolic (see C03b) ----
        # Replace the live readout with a static MathTex so we can
        # transform it into the symbolic derivative.
        slope_readout.clear_updaters()
        symbolic = MathTex(
            r"\frac{d}{dx}\sin(x) = \cos(x)",
            color=FG,
            font_size=44,
        ).to_corner(UR, buff=0.6)
        self.play(FadeTransform(slope_readout, symbolic), run_time=1.4)
        self.wait(0.4)

        # ---- Beat 5: brace + indicate finale (see C08a, C08b) ----
        cosine_graph = axes.plot(np.cos, color=ACCENT_2)
        cosine_label = axes.get_graph_label(cosine_graph, MathTex("\\cos(x)", color=ACCENT_2))
        self.play(Create(cosine_graph), Write(cosine_label))
        self.play(Indicate(symbolic, color=ACCENT, scale_factor=1.1))
        self.wait(1.5)
