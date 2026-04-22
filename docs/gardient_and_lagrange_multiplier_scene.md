# Gradient & Lagrange Multipliers — YouTube Shorts Scene Guide

---

## Best Practices for ManimCE Vertical Shorts

Before writing a single line of code, internalize these principles. They will save you hours of rework.

### Canvas & Layout
- **Frame is ~8 units wide, ~14 units tall** in 1080×1920. Everything is taller than it is wide. Think in columns, not rows.
- **Safe zone is ±5 vertical, ±3.5 horizontal.** YouTube Shorts crops on some devices. Never put critical content outside this box.
- **Use `VGroup(...).arrange(DOWN, buff=0.5)`** as your primary layout tool. Horizontal `arrange(RIGHT)` will push things off-screen fast.
- **Never center everything at ORIGIN for every scene.** Divide the canvas into thirds: top (`UP * 4`), middle (`ORIGIN`), bottom (`DOWN * 4`). Assign roles to each zone and keep them consistent across scenes.

### Typography
- **Minimum font size is 48** for body text. Anything smaller is unreadable on mobile.
- **Titles: 72–96.** Section headers: 60–72. Body/labels: 48–56.
- **Use `Text` for plain labels, `MathTex` for equations.** Never mix them in the same `VGroup` without `.scale()` alignment checks.
- **Keep equations short.** If a `MathTex` string renders wider than 6 units, break it into two lines or scale it down with `.scale(0.85)`.
- **Avoid full sentences.** You have ~3.5 seconds per scene beat. One concept, one line.

### Timing
- **60 seconds total, ~8–10 distinct beats.** Each beat = one `self.play()` + one `self.wait()`.
- **`self.wait(0.5)`** between transitions. **`self.wait(1.0)`** to let a key idea breathe. **`self.wait(1.5)`** only for the climax reveal.
- **Use `run_time=` explicitly** on every `self.play()`. Don't rely on defaults — 1.0s for reveals, 0.6s for fast transitions, 1.5s for complex transforms.
- **Total runtime budget:** animations ~30s + waits ~30s = 60s. Track it as you write.

### Colors
- **Dark background always.** ManimCE default `BLACK` or `#1a1a2e` (deep navy) works well.
- **Use at most 3 accent colors.** Suggested palette for math content:
  - Constraint curve: `BLUE` (`#58C4DD`)
  - Objective function: `YELLOW` (`#FFFF00`)
  - Gradient vectors: `RED` / `GREEN`
  - Optimal point: `WHITE` with a `Dot` flash
- **Never use `WHITE` text on `WHITE` background elements.** Always check contrast.

### Animations
- **`Write`** for equations appearing. **`Create`** for shapes/curves. **`FadeIn`** for supporting labels.
- **`FadeOut`** everything before a scene change — never just `self.remove()` mid-animation.
- **`Transform` / `ReplacementTransform`** to morph one equation into the next. This is the visual hook that makes math videos feel alive.
- **`self.play(FadeOut(*self.mobjects))`** is your scene wipe. Put it at the end of every major beat.
- **Avoid `AnimationGroup` until you're comfortable.** `LaggedStart` with a small `lag_ratio=0.15` is almost always better-looking and easier to reason about.

### Code Structure
- **One `Scene` class per beat or logical section.** Then stitch them together in a wrapper `Scene` by calling each section's logic as a method, or just render them separately and edit in post.
- **Name scenes descriptively:** `GradientIntro`, `ConstraintSetup`, `LagrangeReveal` — not `Scene1`, `Scene2`.
- **Extract repeated layout constants to the top of the file:**

```python
TITLE_Y     = UP * 5.5
CONTENT_Y   = UP * 1.0
BOTTOM_Y    = DOWN * 4.5
FONT_TITLE  = 80
FONT_BODY   = 52
FONT_LABEL  = 44
```

- **Use `config` at the top of your file, not in `manim.cfg`,** so the vertical format is self-contained:

```python
from manim import *
config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
```

### The Iteration Loop
- **Always prototype with `uv run short-low`** (480p, fast render).
- **Check last frame first with `uv run last-frame`** before watching the full animation.
- **Only run `uv run short-render` when the scene is locked.** 4K renders are slow.

---

## The Short: "Gradients & Lagrange Multipliers in 60 Seconds"

**Narrative arc:** Start with the intuition (gradient = direction of steepest ascent), introduce the constraint problem visually, show why unconstrained optimization fails, reveal the Lagrange condition geometrically, then write the equation.

**Total scenes: 8**
**Target runtime: ~58–62 seconds**

---

## Scene 1 — Hook (0s–5s)

**Goal:** Grab attention. One sharp question on screen.

**What's on screen:**
- Dark background
- Large bold question text, centered vertically in the top third

**Build sequence:**

```python
# Scene 1: Hook
class Hook(Scene):
    def construct(self):
        config.pixel_width  = 1080
        config.pixel_height = 1920
        config.frame_rate   = 60

        question = Text(
            "How do you find\nthe maximum\nunder a constraint?",
            font_size=72,
            line_spacing=1.4,
        ).move_to(UP * 2)

        sub = Text(
            "Lagrange multipliers.",
            font_size=56,
            color=YELLOW,
        ).next_to(question, DOWN, buff=1.2)

        # 1. Write the question word by word feel
        self.play(FadeIn(question, shift=UP * 0.3), run_time=1.2)
        self.wait(1.5)

        # 2. Answer drops in — creates tension/release
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # 3. Wipe to next scene
        self.play(FadeOut(question, sub), run_time=0.5)
```

**Transition into Scene 2:** Hard cut after FadeOut. The contrast of "abstract question → concrete visual" is the hook.

**Timing budget:** ~5s

---

## Scene 2 — What Is a Gradient? (5s–16s)

**Goal:** Define gradient visually. Show it as a vector pointing uphill on a surface — no equations yet.

**What's on screen:**
- A 2D filled contour-like representation using `NumberPlane` clipped to the frame width
- A dot at a point on the plane
- An arrow (the gradient vector) pointing in the direction of steepest ascent
- Label: "gradient = direction of steepest ascent"

**Build sequence:**

```python
class GradientIntro(Scene):
    def construct(self):
        # --- Layout constants ---
        TITLE_Y = UP * 5.5

        title = Text("The Gradient", font_size=80, color=YELLOW).move_to(TITLE_Y)

        # Compact plane — keep it within ~6 units wide so it fits the narrow canvas
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
        ).move_to(UP * 1.5)

        # A point somewhere on the plane
        point = plane.c2p(1, 0.5)
        dot = Dot(point, color=WHITE, radius=0.12)

        # Gradient vector at that point — for f(x,y) = x^2 + y^2, grad = (2x, 2y)
        # At (1, 0.5): grad = (2, 1), normalized and scaled for display
        grad_vec = Arrow(
            start=point,
            end=point + plane.c2p(1, 0.5) - plane.c2p(0, 0),  # direction (1, 0.5) scaled
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )

        label = Text("steepest ascent", font_size=48, color=RED).next_to(grad_vec, RIGHT, buff=0.2)

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
```

**Key technique:** Use `plane.c2p()` (coordinates to point) to position everything relative to the plane — don't use raw coordinates.

**Transition into Scene 3:** Wipe out everything, then immediately introduce the constraint curve with a `Create` animation. The plane stays in spirit but the constraint replaces it.

**Timing budget:** ~11s

---

## Scene 3 — The Constraint Problem (16s–24s)

**Goal:** Show the optimization problem visually. A curve (constraint) and level curves of the objective function. Establish the vocabulary: "maximize f subject to g = 0."

**What's on screen:**
- A `NumberPlane` (same size as before)
- A circular constraint curve `g(x,y) = x² + y² - 1 = 0` drawn in BLUE
- A few elliptical level curves of `f(x,y) = x + y` drawn as dashed lines in YELLOW
- Label on constraint: `g(x,y) = 0`
- Label on level curves: `f = c`
- Text at bottom: "find the highest level curve\nthat still touches the constraint"

**Build sequence:**

```python
class ConstraintSetup(Scene):
    def construct(self):
        title = Text("The Problem", font_size=80, color=YELLOW).move_to(UP * 5.5)

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=5.5,
        ).move_to(UP * 1.0)

        # Constraint: unit circle
        constraint = Circle(radius=plane.get_x_unit_size(), color=BLUE, stroke_width=5)
        constraint.move_to(plane.c2p(0, 0))

        g_label = MathTex(r"g(x,y)=0", font_size=48, color=BLUE)
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

        f_label = MathTex(r"f = c", font_size=48, color=YELLOW).move_to(plane.c2p(1.5, -1.2))

        insight = Text(
            "find the highest level curve\nthat still touches g = 0",
            font_size=44,
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
```

**Timing budget:** ~8s

---

## Scene 4 — Why Naive Gradient Ascent Fails (24s–31s)

**Goal:** Show that just following the gradient ignores the constraint. A dot walks off the constraint curve following the gradient — it "escapes" the feasible region.

**What's on screen:**
- The same plane + constraint circle from Scene 3
- A dot ON the constraint curve
- A gradient arrow pointing away (off the circle)
- An "❌" or red cross fading in
- Short label: "gradient alone ignores the constraint"

**Build sequence:**

```python
class NaiveGradientFails(Scene):
    def construct(self):
        title = Text("The Problem with\nJust Following ∇f",
                     font_size=64, line_spacing=1.3).move_to(UP * 5.2)

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=5.5,
        ).move_to(UP * 1.0)

        constraint = Circle(radius=plane.get_x_unit_size(), color=BLUE, stroke_width=5)
        constraint.move_to(plane.c2p(0, 0))

        # Start dot at (cos(225°), sin(225°)) ≈ (-0.7, -0.7) on the unit circle
        import numpy as np
        start_angle = 225 * DEGREES
        px, py = np.cos(start_angle), np.sin(start_angle)
        start_pt = plane.c2p(px, py)

        dot = Dot(start_pt, color=WHITE, radius=0.14)

        # For f = x + y, grad = (1, 1), normalized
        unit = plane.get_x_unit_size()
        grad_arrow = Arrow(
            start=start_pt,
            end=start_pt + np.array([unit * 0.8, unit * 0.8, 0]),
            buff=0,
            color=RED,
            stroke_width=6,
        )

        cross = Text("✗", font_size=120, color=RED).move_to(UP * 1.0)

        caption = Text(
            "gradient alone\nignores g = 0",
            font_size=48,
            line_spacing=1.3,
            color=RED,
        ).move_to(DOWN * 4.2)

        self.play(FadeIn(title), Create(plane), run_time=0.8)
        self.play(Create(constraint), FadeIn(dot), run_time=0.6)
        self.wait(0.3)
        self.play(GrowArrow(grad_arrow), run_time=0.7)
        self.wait(0.5)

        # Dot drifts off the constraint — animate along the arrow direction
        self.play(
            dot.animate.shift(np.array([unit * 0.8, unit * 0.8, 0])),
            run_time=0.8,
        )
        self.wait(0.3)
        self.play(FadeIn(cross), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(*self.mobjects), run_time=0.5)
```

**Timing budget:** ~7s

---

## Scene 5 — The Geometric Insight (31s–41s)

**Goal:** This is the core revelation. At the optimum, `∇f` and `∇g` are parallel — the level curve of f is tangent to the constraint curve. Show this visually before writing any equation.

**What's on screen:**
- Plane + constraint circle
- The optimal point highlighted (top-right of circle where x+y is maximized: `(1/√2, 1/√2)`)
- `∇f` arrow at that point (pointing up-right)
- `∇g` arrow at that point (pointing radially outward — same direction!)
- Both arrows flash/align
- Label: "at the optimum, ∇f ∥ ∇g"

**Build sequence:**

```python
class GeometricInsight(Scene):
    def construct(self):
        import numpy as np

        title = Text("The Key Insight", font_size=80, color=YELLOW).move_to(UP * 5.5)

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=5.5,
        ).move_to(UP * 1.0)

        constraint = Circle(radius=plane.get_x_unit_size(), color=BLUE, stroke_width=5)
        constraint.move_to(plane.c2p(0, 0))

        # Optimal point for max(x+y) on unit circle: (1/√2, 1/√2)
        ox, oy = 1 / np.sqrt(2), 1 / np.sqrt(2)
        opt_pt = plane.c2p(ox, oy)
        unit = plane.get_x_unit_size()

        opt_dot = Dot(opt_pt, color=WHITE, radius=0.16)
        opt_dot_glow = Dot(opt_pt, color=YELLOW, radius=0.28).set_opacity(0.4)

        # ∇f at optimum = (1, 1) normalized
        nf = np.array([1, 1]) / np.sqrt(2)
        arrow_f = Arrow(
            start=opt_pt,
            end=opt_pt + np.array([nf[0] * unit, nf[1] * unit, 0]),
            buff=0,
            color=RED,
            stroke_width=7,
        )
        label_f = MathTex(r"\nabla f", font_size=52, color=RED).next_to(arrow_f, RIGHT, buff=0.1)

        # ∇g at optimum = (2x, 2y) = (√2, √2) normalized = same direction
        ng = np.array([ox, oy]) / np.linalg.norm([ox, oy])
        arrow_g = Arrow(
            start=opt_pt,
            end=opt_pt + np.array([ng[0] * unit, ng[1] * unit, 0]),
            buff=0,
            color=GREEN,
            stroke_width=7,
        )
        label_g = MathTex(r"\nabla g", font_size=52, color=GREEN).next_to(arrow_g, LEFT, buff=0.1)

        parallel_label = MathTex(
            r"\nabla f \parallel \nabla g",
            font_size=68,
            color=WHITE,
        ).move_to(DOWN * 3.5)

        insight = Text("at the optimum", font_size=48, color=YELLOW).next_to(parallel_label, UP, buff=0.4)

        self.play(FadeIn(title), run_time=0.5)
        self.play(Create(plane), Create(constraint), run_time=0.8)
        self.wait(0.2)

        # Reveal the optimal point
        self.play(FadeIn(opt_dot_glow, opt_dot), run_time=0.6)
        self.wait(0.4)

        # Show ∇f
        self.play(GrowArrow(arrow_f), FadeIn(label_f), run_time=0.8)
        self.wait(0.4)

        # Show ∇g — it aligns!
        self.play(GrowArrow(arrow_g), FadeIn(label_g), run_time=0.8)
        self.wait(0.4)

        # Flash both to emphasize they're parallel
        self.play(
            arrow_f.animate.set_stroke(width=10),
            arrow_g.animate.set_stroke(width=10),
            run_time=0.4,
        )
        self.play(
            arrow_f.animate.set_stroke(width=7),
            arrow_g.animate.set_stroke(width=7),
            run_time=0.3,
        )

        # Drop the conclusion
        self.play(FadeIn(insight), Write(parallel_label), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(*self.mobjects), run_time=0.5)
```

**This is your climax scene.** Give it the most visual polish. The moment the two arrows align is the "aha" the viewer is here for.

**Timing budget:** ~10s

---

## Scene 6 — Writing the Lagrange Condition (41s–49s)

**Goal:** Translate the geometric insight into the equation. `∇f = λ∇g`. Introduce λ (lambda) as the scalar "how much bigger is one gradient than the other."

**What's on screen:**
- Clean dark background, no plane
- The parallel statement from Scene 5 fades in first as a reminder
- Then transforms into the equation
- λ is highlighted and labeled "Lagrange multiplier"

**Build sequence:**

```python
class LagrangeEquation(Scene):
    def construct(self):
        title = Text("The Equation", font_size=80, color=YELLOW).move_to(UP * 5.5)

        # Remind — parallel condition
        remind = MathTex(
            r"\nabla f \parallel \nabla g",
            font_size=72,
        ).move_to(UP * 2.5)

        # The Lagrange condition
        eq = MathTex(
            r"\nabla f = \lambda \nabla g",
            font_size=88,
        ).move_to(UP * 0.5)

        # Highlight lambda
        lambda_box = SurroundingRectangle(eq[0][7], color=YELLOW, buff=0.12)  # index of λ
        lambda_label = Text("Lagrange\nmultiplier", font_size=44, color=YELLOW, line_spacing=1.2)
        lambda_label.next_to(lambda_box, DOWN, buff=0.5)

        # The constraint reminder
        constraint_eq = MathTex(
            r"g(x,y) = 0",
            font_size=64,
            color=BLUE,
        ).move_to(DOWN * 2.5)

        plus_label = Text("subject to", font_size=44, color=GREY).next_to(constraint_eq, UP, buff=0.3)

        self.play(FadeIn(title), run_time=0.5)
        self.play(Write(remind), run_time=0.8)
        self.wait(0.5)

        # Transform parallel → equation
        self.play(
            ReplacementTransform(remind, eq),
            run_time=1.0,
        )
        self.wait(0.5)

        # Spotlight λ
        self.play(Create(lambda_box), run_time=0.5)
        self.play(FadeIn(lambda_label), run_time=0.5)
        self.wait(0.6)

        # Add constraint
        self.play(FadeIn(plus_label, constraint_eq), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(*self.mobjects), run_time=0.5)
```

**Note on MathTex indexing:** The index `[0][7]` for λ will depend on how ManimCE parses the LaTeX string. Always print `eq[0]` indices during development or use `eq.get_part_by_tex(r"\lambda")` to target it safely.

**Timing budget:** ~8s

---

## Scene 7 — The Full System (49s–55s)

**Goal:** Show the complete system of equations a student would actually solve. Three equations, stacked vertically, appearing one at a time.

**What's on screen:**
- Title: "Solve this system"
- Three equations appearing one by one:
  1. `∂f/∂x = λ ∂g/∂x`
  2. `∂f/∂y = λ ∂g/∂y`
  3. `g(x, y) = 0`
- A brace or bracket grouping them (optional — add only if timing allows)

**Build sequence:**

```python
class FullSystem(Scene):
    def construct(self):
        title = Text("Solve this system", font_size=72, color=YELLOW).move_to(UP * 5.5)

        eq1 = MathTex(r"\frac{\partial f}{\partial x} = \lambda\frac{\partial g}{\partial x}", font_size=72)
        eq2 = MathTex(r"\frac{\partial f}{\partial y} = \lambda\frac{\partial g}{\partial y}", font_size=72)
        eq3 = MathTex(r"g(x,\, y) = 0", font_size=72, color=BLUE)

        system = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.9).move_to(UP * 0.8)

        # Optional: left brace grouping
        brace = Brace(system, direction=LEFT, color=GREY)

        self.play(FadeIn(title), run_time=0.5)
        self.play(Write(eq1), run_time=0.8)
        self.play(Write(eq2), run_time=0.8)
        self.play(Write(eq3), run_time=0.8)
        self.wait(0.4)
        self.play(Create(brace), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(*self.mobjects), run_time=0.5)
```

**Timing budget:** ~6s

---

## Scene 8 — Outro / Call to Action (55s–60s)

**Goal:** Reinforce the concept in one line. Leave the viewer with the core takeaway and a reason to follow.

**What's on screen:**
- The core equation `∇f = λ∇g` large and centered
- One-line takeaway below it
- Optional: channel name or "follow for more" text at the bottom

**Build sequence:**

```python
class Outro(Scene):
    def construct(self):
        eq_final = MathTex(
            r"\nabla f = \lambda \nabla g",
            font_size=100,
            color=YELLOW,
        ).move_to(UP * 2.5)

        takeaway = Text(
            "when gradients align,\nyou've found the optimum.",
            font_size=52,
            line_spacing=1.4,
            color=WHITE,
        ).move_to(DOWN * 0.5)

        cta = Text(
            "follow for more math in 60s",
            font_size=40,
            color=GREY,
        ).move_to(DOWN * 4.5)

        self.play(Write(eq_final), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(takeaway, shift=UP * 0.2), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(cta), run_time=0.6)
        self.wait(1.5)
```

**Timing budget:** ~5s

---

## Scene Stitching — One File Approach

If you want to render the entire short as one video, wrap all scenes into a single `Scene` class and call each section's `construct` logic via methods. The cleaner approach for iteration is to keep them separate and stitch in a video editor (CapCut, DaVinci Resolve). Renders will be faster and you can swap individual scenes without re-rendering everything.

For a single-file render:

```python
from manim import *

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60

class GradientLagrangeShort(Scene):
    def construct(self):
        self._hook()
        self._gradient_intro()
        self._constraint_setup()
        self._naive_fails()
        self._geometric_insight()
        self._lagrange_equation()
        self._full_system()
        self._outro()

    def _hook(self):
        # ... paste Hook.construct body here
        pass

    def _gradient_intro(self):
        # ... paste GradientIntro.construct body here
        pass

    # etc.
```

Render with:
```bash
uv run short-render scenes/gradient_lagrange.py GradientLagrangeShort
```

---

## Runtime Tracker

| Scene | Description | Target |
|-------|-------------|--------|
| 1 | Hook | 5s |
| 2 | What is a gradient? | 11s |
| 3 | Constraint problem | 8s |
| 4 | Why naive gradient fails | 7s |
| 5 | Geometric insight (∇f ∥ ∇g) | 10s |
| 6 | The equation ∇f = λ∇g | 8s |
| 7 | Full system | 6s |
| 8 | Outro | 5s |
| **Total** | | **~60s** |
