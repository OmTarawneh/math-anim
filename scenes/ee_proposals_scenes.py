import math
from collections import Counter
from typing import cast

from base import NormalScene
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UR,
    Animation,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Transform,
    VGroup,
    Write,
)
from manim import Text as _ManimText
from theme import (
    ACCENT,
    ACCENT_3,
    BG,
    BUBBLE_BG,
    CREAM,
    FG,
    INFRA,
    INK,
    MERGED,
    MUTED,
    PROBLEM,
)


# Helvetica and Arial on macOS both trigger a ManimPango bug that halves
# the space advance after narrow glyph clusters ("Pls don'tdeploy",
# "at3pm"). Helvetica Neue does not — its space ratio measures ~0.96
# vs ~0.48 for Helvetica/Arial — and visually it is the closest cousin.
def Text(*args, **kwargs):
    kwargs.setdefault("font", "Helvetica Neue")
    return _ManimText(*args, **kwargs)


class EE00(NormalScene):
    def construct(self) -> None:
        title = Text(
            "Ephemeral Environments",
            color=FG,
            font_size=64,
            t2c={"Ephemeral": ACCENT},
        )
        subtitle = Text(
            "A proposal for the Hub team",
            color=MUTED,
            font_size=32,
            slant="ITALIC",
        )
        VGroup(title, subtitle).arrange(DOWN, buff=0.45)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            color=ACCENT,
            stroke_width=2.5,
        )

        self.wait(0.3)
        self.play(
            LaggedStart(
                *[FadeIn(ch, shift=UP * 0.25) for ch in title],
                lag_ratio=0.05,
            ),
            run_time=1.8,
        )
        self.play(Create(underline), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.7)
        self.wait(2.4)


class EE01(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # BEAT 1 (0–6s) — The team appears
        # ──────────────────────────────────────────────────────────
        def engineer(tag: str) -> VGroup:
            c = Circle(
                radius=0.20,
                color=INK,
                fill_color=CREAM,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            t = Text(tag, color=INK, font_size=15, weight="BOLD")
            t.move_to(c.get_center())
            return VGroup(c, t)

        fe_group = VGroup(*[engineer("FE") for _ in range(6)])
        fe_group.arrange(RIGHT, buff=0.22)

        be_group = VGroup(*[engineer("BE") for _ in range(7)])
        be_group.arrange(RIGHT, buff=0.22)

        qa_group = VGroup(*[engineer("QA") for _ in range(5)])
        qa_group.arrange(RIGHT, buff=0.22)

        team_row = VGroup(fe_group, be_group, qa_group).arrange(RIGHT, buff=0.85)
        team_row.move_to((0, 2.4, 0))

        fe_label = Text("FE × 6", color=MUTED, font_size=22, weight="MEDIUM")
        fe_label.next_to(fe_group, UP, buff=0.4)
        be_label = Text("BE × 7", color=MUTED, font_size=22, weight="MEDIUM")
        be_label.next_to(be_group, UP, buff=0.4)
        qa_label = Text("QA × 5", color=MUTED, font_size=22, weight="MEDIUM")
        qa_label.next_to(qa_group, UP, buff=0.4)

        all_eng = [*fe_group, *be_group, *qa_group]

        self.wait(0.3)
        self.play(
            LaggedStart(
                *[FadeIn(eng, shift=DOWN * 0.18) for eng in all_eng],
                lag_ratio=0.045,
            ),
            run_time=2.6,
        )
        self.play(
            FadeIn(fe_label, shift=DOWN * 0.12),
            FadeIn(be_label, shift=DOWN * 0.12),
            FadeIn(qa_label, shift=DOWN * 0.12),
            run_time=0.7,
        )
        self.wait(2.2)

        # ──────────────────────────────────────────────────────────
        # BEAT 2 (6–10s) — The shared resources appear
        # ──────────────────────────────────────────────────────────
        env_names = ["staging", "unify-staging", "training"]
        env_boxes = VGroup()
        for name in env_names:
            box = RoundedRectangle(
                width=3.7,
                height=1.5,
                corner_radius=0.18,
                color=INFRA,
                stroke_width=2.5,
                fill_color=INFRA,
                fill_opacity=0.12,
            )
            label = Text(name, color=INFRA, font_size=28, weight="MEDIUM")
            label.move_to(box.get_center())
            env_boxes.add(VGroup(box, label))
        env_boxes.arrange(RIGHT, buff=0.7)
        env_boxes.move_to((0, -2.1, 0))

        final_centers = [b.get_center().copy() for b in env_boxes]
        for b in env_boxes:
            b.shift(DOWN * 5)

        self.play(
            LaggedStart(
                *[
                    cast(Animation, b.animate.move_to(final_centers[i]))
                    for i, b in enumerate(env_boxes)
                ],
                lag_ratio=0.18,
            ),
            run_time=1.8,
        )
        self.wait(2.2)

        # ──────────────────────────────────────────────────────────
        # BEAT 3 (10–18s) — The collision
        # ──────────────────────────────────────────────────────────
        # (engineer index in all_eng, env index 0=staging, 1=unify-staging, 2=training)
        # all_eng layout: FE 0–5, BE 6–12, QA 13–17
        targets = [
            (0, 0),
            (1, 1),
            (2, 0),
            (3, 0),
            (4, 1),
            (6, 0),
            (7, 2),
            (8, 1),
            (9, 0),
            (10, 0),
            (11, 1),
            (13, 0),
            (14, 2),
            (15, 0),
            (16, 1),
            (17, 2),
        ]
        arrows = VGroup()
        arrow_env: list[int] = []
        for eng_idx, env_idx in targets:
            eng = all_eng[eng_idx]
            start = eng[0].get_bottom()
            end = env_boxes[env_idx][0].get_top() + DOWN * 0.02
            a = Arrow(
                start=start,
                end=end,
                color=MUTED,
                stroke_width=2.0,
                buff=0.08,
                tip_length=0.18,
                max_tip_length_to_length_ratio=0.08,
            )
            arrows.add(a)
            arrow_env.append(env_idx)

        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.10),
            run_time=2.4,
        )
        self.wait(0.3)

        # Contested = env with 2+ incoming arrows
        counts = Counter(arrow_env)
        contested = [i for i, c in counts.items() if c >= 2]
        contested_arrows = [a for a, ei in zip(arrows, arrow_env) if ei in contested]

        self.play(
            *[
                a.animate.set_color(PROBLEM).set_stroke(width=3.0)
                for a in contested_arrows
            ],
            run_time=0.6,
        )

        # Warning glyphs above contested envs (circle with diagonal slash, monochrome)
        warning_glyphs = VGroup()
        for ei in contested:
            ring = Circle(radius=0.20, color=PROBLEM, stroke_width=3.0, fill_opacity=0)
            slash = Line(
                start=(-0.14, 0.14, 0),
                end=(0.14, -0.14, 0),
                color=PROBLEM,
                stroke_width=3.0,
            )
            g = VGroup(ring, slash)
            g.next_to(env_boxes[ei], UP, buff=0.22)
            warning_glyphs.add(g)

        self.play(
            LaggedStart(
                *[FadeIn(g, scale=0.5) for g in warning_glyphs],
                lag_ratio=0.18,
            ),
            run_time=0.7,
        )

        # Jitter the contested arrows + glyphs
        for dx in (-0.07, 0.14, -0.14, 0.07):
            self.play(
                *[a.animate.shift(RIGHT * dx) for a in contested_arrows],
                *[g.animate.shift(RIGHT * dx) for g in warning_glyphs],
                run_time=0.08,
            )

        # Blink the warning glyphs once
        self.play(warning_glyphs.animate.set_opacity(0.25), run_time=0.25)
        self.play(warning_glyphs.animate.set_opacity(1.0), run_time=0.25)

        self.wait(2.4)

        # ──────────────────────────────────────────────────────────
        # BEAT 4 — The number lands, then leaves
        # ──────────────────────────────────────────────────────────
        scene_so_far = VGroup(
            fe_group,
            be_group,
            qa_group,
            fe_label,
            be_label,
            qa_label,
            env_boxes,
            arrows,
            warning_glyphs,
        )

        big_eng = VGroup(
            Text("18", color=ACCENT, font_size=88, weight="BOLD"),
            Text("engineers", color=FG, font_size=88, weight="BOLD"),
        ).arrange(RIGHT, buff=0.35)

        big_env = VGroup(
            Text("3", color=ACCENT, font_size=88, weight="BOLD"),
            Text("environments", color=FG, font_size=88, weight="BOLD"),
        ).arrange(RIGHT, buff=0.35)

        big_block = VGroup(big_eng, big_env).arrange(DOWN, buff=0.25)
        big_block.move_to(ORIGIN)

        self.play(FadeOut(scene_so_far), run_time=0.8)
        self.play(
            LaggedStart(
                FadeIn(big_eng, shift=UP * 0.3),
                FadeIn(big_env, shift=UP * 0.3),
                lag_ratio=0.4,
            ),
            run_time=1.6,
        )
        self.wait(3.5)
        self.play(FadeOut(big_block), run_time=1.0)
        self.wait(0.3)


def _engineer_circle(radius: float = 0.45) -> Circle:
    return Circle(
        radius=radius,
        color=INK,
        fill_color=CREAM,
        fill_opacity=1.0,
        stroke_width=1.5,
    )


def _speech_bubble(msg: str, font_size: int = 18) -> VGroup:
    text = Text(msg, color=INK, font_size=font_size)
    body = RoundedRectangle(
        width=text.width + 0.5,
        height=text.height + 0.32,
        corner_radius=0.16,
        color=INK,
        stroke_width=1.0,
        fill_color=BUBBLE_BG,
        fill_opacity=1.0,
    )
    text.move_to(body.get_center())
    return VGroup(body, text)


def _silhouette_pile() -> VGroup:
    eng = _engineer_circle(radius=0.20)
    bubbles = VGroup()
    for (dx, dy), w, h in [
        ((0.55, 0.35), 0.95, 0.24),
        ((-0.55, 0.30), 0.70, 0.22),
        ((0.30, -0.50), 0.80, 0.22),
    ]:
        b = RoundedRectangle(
            width=w,
            height=h,
            corner_radius=0.10,
            color=INK,
            stroke_width=1.0,
            fill_color=BUBBLE_BG,
            fill_opacity=1.0,
        )
        b.shift((dx, dy, 0))
        bubbles.add(b)
    return VGroup(eng, bubbles)


class EE02(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # BEAT 1 (0–8s) — One engineer, drowning in bubbles
        # ──────────────────────────────────────────────────────────
        engineer = _engineer_circle(radius=0.45)
        engineer.move_to(ORIGIN)

        messages = [
            "Anyone using staging?",
            "Pls don't deploy, testing X",
            "Can I grab unify-staging at 3pm?",
            "deploying after lunch — heads up",
            "is unify-staging free yet?",
        ]
        # Roughly ringed positions around the engineer (angle°, radius).
        # Radii sized so the longest messages don't collide with each other or
        # with the central engineer circle.
        ring = [(60, 2.8), (135, 3.2), (210, 2.8), (290, 2.7), (350, 2.5)]
        rotations = [0.04, -0.03, 0.05, -0.04, 0.02]  # radians

        bubbles = VGroup()
        for msg, (angle_deg, r), rot in zip(messages, ring, rotations):
            b = _speech_bubble(msg, font_size=18)
            angle = math.radians(angle_deg)
            b.move_to((r * math.cos(angle), r * math.sin(angle), 0))
            b.rotate(rot)
            bubbles.add(b)

        self.wait(0.2)
        self.play(FadeIn(engineer, shift=DOWN * 0.15), run_time=0.6)

        # Spawn bubbles one-by-one with a small float.
        # Intervals: (1.0, 1.6), (2.3, 2.9), (3.5, 4.1), (4.7, 5.3), (5.9, 6.5).
        # Per bubble: FadeIn (0.5s) then a small upward float (0.4s).
        for b in bubbles:
            self.play(FadeIn(b, shift=DOWN * 0.25), run_time=0.5)
            self.play(b.animate.shift(UP * 0.15), run_time=0.4)
            self.wait(0.25)
        # Cumulative: 0.2 + 0.6 + 5*(0.5+0.4+0.25) = 0.8 + 5*1.15 = 0.8 + 5.75 = 6.55
        self.wait(1.45)  # → ~8.0s

        # ──────────────────────────────────────────────────────────
        # BEAT 2 (8–16s) — Pull back: 13 engineers, each drowning
        # ──────────────────────────────────────────────────────────
        central = VGroup(engineer, bubbles)

        # Grid of 5 cols × 3 rows. Skip top-right (idx 4) and bottom-left (idx 10).
        grid_xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        grid_ys = [2.2, 0.0, -2.2]
        slots: list[tuple[float, float, float]] = []
        for y in grid_ys:
            for x in grid_xs:
                slots.append((x, y, 0))
        central_idx = 7  # row=1, col=2 → exact center
        skip_idxs = {4, 10}
        surrounding_idxs = [
            i for i in range(len(slots)) if i != central_idx and i not in skip_idxs
        ]

        # Pull-back: shrink and move central to its grid slot.
        self.play(
            central.animate.scale(0.32).move_to(slots[central_idx]),
            run_time=1.4,
        )

        # Build 12 silhouette piles at the surrounding slots
        surrounding = VGroup()
        for i in surrounding_idxs:
            pile = _silhouette_pile()
            pile.scale(0.85)
            pile.move_to(slots[i])
            surrounding.add(pile)

        self.play(
            LaggedStart(
                *[FadeIn(p, shift=DOWN * 0.15) for p in surrounding],
                lag_ratio=0.12,
            ),
            run_time=4.4,
        )
        # Six seconds of silence on the grid. Let the audience count the heads.
        self.wait(6.0)

        # ──────────────────────────────────────────────────────────
        # BEAT 3 — Counter builds the math against the silhouettes,
        # then the same number scales to fill the screen.
        # ──────────────────────────────────────────────────────────
        all_piles = VGroup(central, surrounding)

        counter = Text(
            "1.5 hrs/week per engineer",
            color=ACCENT,
            font_size=36,
            weight="BOLD",
        )
        counter.to_corner(UR, buff=0.6)

        self.play(FadeIn(counter, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # Show the multiplication explicitly — audience must see how 1.5 → 19.8.
        step_mult = Text(
            "1.5  ×  13 engineers",
            color=ACCENT,
            font_size=36,
            weight="BOLD",
        )
        step_mult.move_to(counter)
        self.play(Transform(counter, step_mult), run_time=0.6)
        self.wait(1.3)

        step_result = Text(
            "=  ~19.8 hrs/week",
            color=ACCENT,
            font_size=36,
            weight="BOLD",
        )
        step_result.move_to(counter)
        self.play(Transform(counter, step_result), run_time=0.6)
        self.wait(1.4)

        # The math is earned — dim the silhouettes and let the number scale up.
        self.play(all_piles.animate.set_opacity(0.06), run_time=0.6)

        big_number = Text(
            "~19.8 engineering hours/week",
            color=FG,
            font_size=58,
            weight="BOLD",
            t2c={"19.8": ACCENT},
        )
        big_number.move_to(ORIGIN + UP * 0.35)

        # Same number, scaled to the screen — small-to-big, not pop-in.
        self.play(Transform(counter, big_number), run_time=1.0)
        self.wait(3.0)


class EE03(NormalScene):
    def construct(self) -> None:
        # Single sustained metaphor: red hours fall into a pile, dollars follow.
        seg_w, seg_h, gap = 0.27, 0.62, 0.02
        red_count = 20  # 19.8 hrs ≈ 20 blocks

        col_x_left = -3.6
        col_x_right = 3.0
        pile_center_x = col_x_left
        pile_center_y = -0.3
        cell_w = seg_w + gap
        cell_h = seg_h + 0.04
        pile_rows, pile_cols = 4, 5
        pile_bottom_y = pile_center_y - (pile_rows - 1) / 2 * cell_h
        pile_targets: list[tuple[float, float, float]] = []
        for k in range(red_count):
            row = k // pile_cols
            col = k % pile_cols
            tx = pile_center_x + (col - (pile_cols - 1) / 2) * cell_w
            ty = pile_bottom_y + row * cell_h
            pile_targets.append((tx, ty, 0))

        spawn_y = 4.0
        red_segs: list[Rectangle] = []
        for i in range(red_count):
            block = Rectangle(
                width=seg_w,
                height=seg_h,
                color=PROBLEM,
                stroke_width=0.8,
                fill_color=PROBLEM,
                fill_opacity=1.0,
            )
            block.move_to((pile_targets[i][0], spawn_y, 0))
            red_segs.append(block)
            self.add(block)

        counter = Text("0 hrs lost", color=PROBLEM, font_size=44, weight="BOLD")
        counter.move_to((col_x_right, 2.4, 0))

        def make_counter(text: str):
            t = Text(text, color=PROBLEM, font_size=44, weight="BOLD")
            t.move_to(counter.get_center())
            return t

        def fall(seg: Rectangle, target: tuple[float, float, float]) -> Animation:
            return cast(Animation, seg.animate.move_to(target))

        self.wait(0.3)
        self.play(FadeIn(counter, shift=DOWN * 0.15), run_time=0.5)

        # Two phases — slow start, fast finish.
        self.play(
            LaggedStart(
                *[fall(red_segs[i], pile_targets[i]) for i in range(0, 3)],
                lag_ratio=0.45,
            ),
            run_time=1.8,
        )
        self.play(Transform(counter, make_counter("3 hrs lost")), run_time=0.3)
        self.play(
            LaggedStart(
                *[fall(red_segs[i], pile_targets[i]) for i in range(3, red_count)],
                lag_ratio=0.10,
            ),
            run_time=2.6,
        )
        self.play(Transform(counter, make_counter("19.8 hrs lost")), run_time=0.3)
        self.wait(1.0)

        # Money counter takes over the right column.
        self.play(FadeOut(counter, shift=UP * 0.2), run_time=0.4)

        money_y = 1.0
        money_states = ["$0", "$250", "$550", "$800", "$1000"]
        money = Text(money_states[0], color=PROBLEM, font_size=68, weight="BOLD")
        money.move_to((col_x_right, money_y, 0))

        self.play(FadeIn(money, shift=UP * 0.2), run_time=0.4)
        for s in money_states[1:]:
            new_money = Text(s, color=PROBLEM, font_size=68, weight="BOLD")
            new_money.move_to(money.get_center())
            self.play(Transform(money, new_money), run_time=0.32)

        money_full = VGroup(
            Text("~$1000", color=PROBLEM, font_size=68, weight="BOLD"),
            Text("/ month", color=MUTED, font_size=40, weight="MEDIUM"),
        ).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
        money_full.move_to((col_x_right, money_y, 0))

        self.play(Transform(money, money_full), run_time=0.7)

        # The math, not a tagline — earns its place.
        calc = Text(
            "19.8 hrs/week × ~$12/hr × 4 weeks",
            color=MUTED,
            font_size=22,
        )
        calc.move_to((0, -3.4, 0))
        self.play(FadeIn(calc, shift=UP * 0.08), run_time=0.6)
        self.wait(2.5)


class EE03B(NormalScene):
    def construct(self) -> None:
        # Trajectory: two repos share three envs. Migration is nearly done —
        # sale and profile are the core pages still on www-hub. When they
        # land in hub-next, the envs go red.

        TILE_W, TILE_H = 0.7, 0.30

        def page_tile(text: str = "", highlight: bool = False) -> VGroup:
            color = ACCENT if highlight else MUTED
            fill_op = 0.32 if highlight else 0.20
            tile = Rectangle(
                width=TILE_W,
                height=TILE_H,
                color=color,
                stroke_width=1.5 if highlight else 1.0,
                fill_color=color,
                fill_opacity=fill_op,
            )
            if text:
                t = Text(text, color=color, font_size=11, weight="BOLD")
                t.move_to(tile.get_center())
                return VGroup(tile, t)
            return VGroup(tile)

        # ──────────────────────────────────────────────────────────
        # BEAT 1 — Two repos, three shared envs
        # ──────────────────────────────────────────────────────────
        # www-hub (legacy, left)
        www_box = RoundedRectangle(
            width=3.2,
            height=1.9,
            corner_radius=0.14,
            color=MUTED,
            stroke_width=2.0,
            fill_color=BG,
            fill_opacity=1.0,
        )
        www_label = Text("www-hub", color=MUTED, font_size=22, weight="BOLD")
        www_label.move_to(www_box.get_top() + DOWN * 0.32)
        legacy_sub = Text("legacy", color=MUTED, font_size=14, slant="ITALIC")
        legacy_sub.next_to(www_label, DOWN, buff=0.04)
        www_card = VGroup(www_box, www_label, legacy_sub)
        www_card.move_to((-3.8, 1.8, 0))

        # hub-next (active, right)
        hub_box = RoundedRectangle(
            width=3.2,
            height=1.9,
            corner_radius=0.14,
            color=INFRA,
            stroke_width=2.0,
            fill_color=BG,
            fill_opacity=1.0,
        )
        hub_label = Text("hub-next", color=FG, font_size=22, weight="BOLD")
        hub_label.move_to(hub_box.get_top() + DOWN * 0.32)
        hub_card = VGroup(hub_box, hub_label)
        hub_card.move_to((3.8, 1.8, 0))

        # www-hub remaining pages: sale + profile
        sale_tile = page_tile("sale", highlight=True)
        profile_tile = page_tile("profile", highlight=True)
        www_pages_row = VGroup(sale_tile, profile_tile).arrange(RIGHT, buff=0.18)
        www_pages_row.move_to(www_box.get_center() + DOWN * 0.28)

        # hub-next: 8 generic tiles, already migrated
        hub_tiles = VGroup(*[page_tile() for _ in range(8)])
        hub_grid_rows = VGroup()
        for r in range(2):
            row = VGroup(*[hub_tiles[r * 4 + c] for c in range(4)]).arrange(
                RIGHT, buff=0.08
            )
            hub_grid_rows.add(row)
        hub_grid_rows.arrange(DOWN, buff=0.08)
        hub_grid_rows.move_to(hub_box.get_center() + DOWN * 0.22)

        # 3 shared envs
        env_names = ["staging", "unify-staging", "training"]
        env_groups: list[VGroup] = []
        env_boxes_only: list[RoundedRectangle] = []
        env_labels_only: list[Text] = []
        for name in env_names:
            box = RoundedRectangle(
                width=2.6,
                height=1.0,
                corner_radius=0.14,
                color=INFRA,
                stroke_width=2.2,
                fill_color=INFRA,
                fill_opacity=0.12,
            )
            lbl = Text(name, color=INFRA, font_size=18, weight="MEDIUM")
            lbl.move_to(box.get_center())
            env_groups.append(VGroup(box, lbl))
            env_boxes_only.append(box)
            env_labels_only.append(lbl)
        envs = VGroup(*env_groups)
        envs.arrange(RIGHT, buff=0.4)
        envs.move_to((0, -2.6, 0))

        # 6 arrows: each repo → each env
        www_arrows = VGroup(
            *[
                Line(
                    www_box.get_bottom(),
                    eb.get_top(),
                    color=MUTED,
                    stroke_width=1.0,
                )
                for eb in env_boxes_only
            ]
        )
        hub_arrows = VGroup(
            *[
                Line(
                    hub_box.get_bottom(),
                    eb.get_top(),
                    color=MUTED,
                    stroke_width=1.0,
                )
                for eb in env_boxes_only
            ]
        )

        # Stage envs offscreen for slide-up
        env_targets = [e.get_center().copy() for e in envs]
        for e in envs:
            e.shift(DOWN * 5)

        self.wait(0.3)
        self.play(
            FadeIn(www_card, shift=DOWN * 0.15),
            FadeIn(hub_card, shift=DOWN * 0.15),
            run_time=0.9,
        )
        self.play(
            FadeIn(www_pages_row, shift=DOWN * 0.05),
            LaggedStart(*[FadeIn(t) for t in hub_tiles], lag_ratio=0.04),
            run_time=1.0,
        )
        self.play(
            LaggedStart(
                *[
                    cast(Animation, e.animate.move_to(env_targets[i]))
                    for i, e in enumerate(envs)
                ],
                lag_ratio=0.18,
            ),
            run_time=1.4,
        )
        self.play(
            LaggedStart(
                *[Create(a) for a in [*www_arrows, *hub_arrows]],
                lag_ratio=0.05,
            ),
            run_time=1.0,
        )
        self.wait(0.8)

        # ──────────────────────────────────────────────────────────
        # BEAT 2 — Core pages callout
        # ──────────────────────────────────────────────────────────
        core_label = Text(
            "core pages remaining",
            color=ACCENT,
            font_size=15,
            slant="ITALIC",
        )
        core_label.next_to(www_box, DOWN, buff=0.22)
        self.play(FadeIn(core_label, shift=UP * 0.08), run_time=0.5)

        # Pulse sale + profile twice
        for _ in range(2):
            self.play(
                sale_tile[0].animate.set_fill(ACCENT, opacity=0.55),
                profile_tile[0].animate.set_fill(ACCENT, opacity=0.55),
                run_time=0.32,
            )
            self.play(
                sale_tile[0].animate.set_fill(ACCENT, opacity=0.32),
                profile_tile[0].animate.set_fill(ACCENT, opacity=0.32),
                run_time=0.32,
            )
        self.wait(0.3)

        # ──────────────────────────────────────────────────────────
        # BEAT 3 — Sale and profile cross to hub-next; envs go red
        # ──────────────────────────────────────────────────────────
        # Land them above the existing hub grid (visually distinct)
        target_sale = hub_box.get_center() + UP * 0.05 + LEFT * 0.55
        target_profile = hub_box.get_center() + UP * 0.05 + RIGHT * 0.55

        # Sale migrates first
        self.play(
            sale_tile.animate.move_to(target_sale),
            FadeOut(core_label, shift=DOWN * 0.1),
            run_time=1.2,
        )
        # Envs darken; hub arrows thicken & turn red
        env_first_pulse: list[Animation] = []
        for box, lbl in zip(env_boxes_only, env_labels_only):
            env_first_pulse.append(
                cast(
                    Animation,
                    box.animate.set_color(PROBLEM).set_fill(PROBLEM, opacity=0.20),
                )
            )
            env_first_pulse.append(cast(Animation, lbl.animate.set_color(PROBLEM)))
        hub_arrow_thicken: list[Animation] = [
            cast(Animation, a.animate.set_color(PROBLEM).set_stroke(width=2.5))
            for a in hub_arrows
        ]
        self.play(*env_first_pulse, *hub_arrow_thicken, run_time=0.6)

        # Profile migrates
        self.play(
            profile_tile.animate.move_to(target_profile),
            run_time=1.2,
        )
        # Envs spike harder + warning glyphs + www arrows fade
        warning_glyphs = VGroup()
        for eb in env_boxes_only:
            ring = Circle(radius=0.18, color=PROBLEM, stroke_width=3.0, fill_opacity=0)
            slash = Line(
                start=(-0.13, 0.13, 0),
                end=(0.13, -0.13, 0),
                color=PROBLEM,
                stroke_width=3.0,
            )
            wg = VGroup(ring, slash)
            wg.next_to(eb, UP, buff=0.18)
            warning_glyphs.add(wg)

        env_second_pulse: list[Animation] = [
            cast(
                Animation,
                b.animate.set_fill(PROBLEM, opacity=0.34).set_stroke(width=3.0),
            )
            for b in env_boxes_only
        ]
        thicker_hub_arrows: list[Animation] = [
            cast(Animation, a.animate.set_stroke(width=3.5)) for a in hub_arrows
        ]
        fade_www_arrows: list[Animation] = [
            cast(Animation, a.animate.set_stroke(opacity=0.25)) for a in www_arrows
        ]
        # www-hub greys out further (legacy goes silent)
        www_card_fade = cast(Animation, www_card.animate.set_opacity(0.4))

        self.play(
            *env_second_pulse,
            *thicker_hub_arrows,
            *fade_www_arrows,
            www_card_fade,
            LaggedStart(
                *[FadeIn(g, scale=0.6) for g in warning_glyphs],
                lag_ratio=0.18,
            ),
            run_time=0.9,
        )

        # ──────────────────────────────────────────────────────────
        # BEAT 4 — Hold on the contended state
        # ──────────────────────────────────────────────────────────
        self.wait(2.8)


class EE04(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # BEAT 1 (0–4s) — Question writes itself
        # ──────────────────────────────────────────────────────────
        line1 = Text(
            "What if every pull request",
            color=FG,
            font_size=48,
            t2c={"every pull request": ACCENT_3},
        )
        line2 = Text(
            "got its own environment?",
            color=FG,
            font_size=48,
        )
        question = VGroup(line1, line2).arrange(DOWN, buff=0.4)
        question.move_to(ORIGIN)

        self.wait(0.3)
        self.play(Write(question), run_time=2.2)
        self.wait(1.4)

        # ──────────────────────────────────────────────────────────
        # BEAT 2 (4–8s) — Question slides up; PR card appears below
        # ──────────────────────────────────────────────────────────
        self.play(
            question.animate.scale(0.55).move_to((0, 3.1, 0)),
            run_time=1.0,
        )

        card = RoundedRectangle(
            width=3.8,
            height=2.0,
            corner_radius=0.18,
            color=ACCENT_3,
            stroke_width=2.5,
            fill_color=ACCENT_3,
            fill_opacity=0.08,
        )
        status_dot = Circle(
            radius=0.10,
            color=ACCENT_3,
            fill_color=ACCENT_3,
            fill_opacity=1.0,
            stroke_width=0,
        )
        pr_label = Text("PR #1234", color=ACCENT_3, font_size=36, weight="BOLD")
        inner = VGroup(status_dot, pr_label).arrange(RIGHT, buff=0.22)
        inner.move_to(card.get_center())
        card_group = VGroup(card, inner)
        card_group.move_to(ORIGIN)

        self.play(FadeIn(card_group, scale=0.7), run_time=1.0)
        self.wait(2.0)


class EE05(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # Build the PR card (constant element across all 4 phases)
        # ──────────────────────────────────────────────────────────
        card_w, card_h = 7.0, 2.4
        card = RoundedRectangle(
            width=card_w,
            height=card_h,
            corner_radius=0.18,
            color=MUTED,
            stroke_width=1.8,
            fill_color=BG,
            fill_opacity=1.0,
        )

        title = Text(
            "feat: new search filter",
            color=FG,
            font_size=26,
            weight="BOLD",
        )

        def make_badge(text: str, color) -> VGroup:
            t = Text(text, color=color, font_size=18, weight="BOLD")
            pill = RoundedRectangle(
                width=t.width + 0.45,
                height=0.42,
                corner_radius=0.10,
                color=color,
                stroke_width=1.5,
                fill_color=color,
                fill_opacity=0.18,
            )
            t.move_to(pill.get_center())
            return VGroup(pill, t)

        status_badge = make_badge("Open", ACCENT_3)

        subtitle = Text(
            "#1234  ·  feature/search-filter",
            color=MUTED,
            font_size=18,
        )
        labels_text = Text("Labels:", color=MUTED, font_size=18)

        # Position card content (relative to card edges)
        x_left = card.get_left()[0]
        x_right = card.get_right()[0]
        y_top = card.get_top()[1]
        pad = 0.4

        title.move_to(
            (x_left + pad + title.width / 2, y_top - pad - title.height / 2, 0)
        )
        status_badge.move_to(
            (x_right - pad - status_badge.width / 2, y_top - pad - 0.21, 0)
        )
        subtitle.next_to(title, DOWN, buff=0.18, aligned_edge=LEFT)
        labels_text.next_to(subtitle, DOWN, buff=0.28, aligned_edge=LEFT)

        pr_card = VGroup(card, title, status_badge, subtitle, labels_text)
        pr_card.move_to((0, 1.4, 0))

        # ──────────────────────────────────────────────────────────
        # PHASE 1 — Open + label
        # ──────────────────────────────────────────────────────────
        pr_card.shift(LEFT * 14)  # off-screen-left start

        self.wait(0.3)
        self.play(pr_card.animate.shift(RIGHT * 14), run_time=1.2)
        self.wait(0.5)

        def make_chip(text: str, color) -> VGroup:
            t = Text(text, color=color, font_size=18, weight="MEDIUM")
            pill = RoundedRectangle(
                width=t.width + 0.5,
                height=t.height + 0.22,
                corner_radius=0.10,
                color=color,
                stroke_width=1.5,
                fill_color=color,
                fill_opacity=0.20,
            )
            t.move_to(pill.get_center())
            return VGroup(pill, t)

        preview_chip = make_chip("preview", PROBLEM)
        preview_chip.next_to(labels_text, RIGHT, buff=0.25)

        self.play(FadeIn(preview_chip, scale=0.6), run_time=0.7)
        self.wait(2.0)

        # ──────────────────────────────────────────────────────────
        # PHASE 2 — Build & deploy
        # ──────────────────────────────────────────────────────────

        # Build glyph: 3 horizontal short lines (code lines)
        def build_glyph() -> VGroup:
            return VGroup(
                Line((-0.18, 0.16, 0), (0.10, 0.16, 0), color=INFRA, stroke_width=2.0),
                Line((-0.18, 0.0, 0), (0.18, 0.0, 0), color=INFRA, stroke_width=2.0),
                Line(
                    (-0.18, -0.16, 0), (0.05, -0.16, 0), color=INFRA, stroke_width=2.0
                ),
            )

        # Registry glyph: 3 stacked rounded rect "layers"
        def registry_glyph() -> VGroup:
            return VGroup(
                *[
                    RoundedRectangle(
                        width=0.36,
                        height=0.10,
                        corner_radius=0.04,
                        color=INFRA,
                        stroke_width=1.5,
                        fill_color=INFRA,
                        fill_opacity=0.30,
                    ).shift(UP * dy)
                    for dy in (0.16, 0.0, -0.16)
                ]
            )

        # Deploy glyph: rightward triangle (forward motion)
        def deploy_glyph() -> Polygon:
            return Polygon(
                (-0.16, -0.18, 0),
                (-0.16, 0.18, 0),
                (0.18, 0, 0),
                color=INFRA,
                stroke_width=1.5,
                fill_color=INFRA,
                fill_opacity=0.30,
            )

        def make_infra_box(glyph_fn) -> VGroup:
            box = RoundedRectangle(
                width=0.85,
                height=0.85,
                corner_radius=0.12,
                color=INFRA,
                stroke_width=1.8,
                fill_color=INFRA,
                fill_opacity=0.10,
            )
            g = glyph_fn()
            g.move_to(box.get_center())
            return VGroup(box, g)

        ico_build = make_infra_box(build_glyph)
        ico_registry = make_infra_box(registry_glyph)
        ico_deploy = make_infra_box(deploy_glyph)

        infra_row = VGroup(ico_build, ico_registry, ico_deploy)
        infra_row.arrange(RIGHT, buff=1.4)
        infra_row.move_to((0, -2.7, 0))

        infra_line_bg = Line(
            ico_build.get_right(),
            ico_deploy.get_left(),
            color=MUTED,
            stroke_width=1.5,
        )
        infra_progress = Line(
            ico_build.get_right(),
            ico_deploy.get_left(),
            color=ACCENT_3,
            stroke_width=4.0,
        )
        # Lines sit behind the icons (they pass through registry's center)
        infra_line_bg.set_z_index(-1)
        infra_progress.set_z_index(-1)

        self.play(
            LaggedStart(
                FadeIn(ico_build, shift=UP * 0.15),
                FadeIn(ico_registry, shift=UP * 0.15),
                FadeIn(ico_deploy, shift=UP * 0.15),
                lag_ratio=0.35,
            ),
            FadeIn(infra_line_bg),
            run_time=1.4,
        )

        self.play(Create(infra_progress), run_time=2.5)
        self.wait(1.5)

        # ──────────────────────────────────────────────────────────
        # PHASE 3 — Live URL appears
        # ──────────────────────────────────────────────────────────

        comment_w, comment_h = 6.0, 1.4
        comment_card = RoundedRectangle(
            width=comment_w,
            height=comment_h,
            corner_radius=0.18,
            color=MUTED,
            stroke_width=1.5,
            fill_color=BG,
            fill_opacity=1.0,
        )

        # Monochrome ✓ glyph (two lines)
        check_glyph = VGroup(
            Line((-0.10, 0.0, 0), (-0.02, -0.10, 0), color=ACCENT_3, stroke_width=3.5),
            Line((-0.02, -0.10, 0), (0.16, 0.12, 0), color=ACCENT_3, stroke_width=3.5),
        )

        comment_header = Text(
            "Preview env ready",
            color=FG,
            font_size=20,
            weight="BOLD",
        )
        url_text = Text(
            "pr-1234.preview.hub.dev",
            color=ACCENT_3,
            font_size=22,
            weight="MEDIUM",
        )
        status_text = Text(
            "Build: passed  ·  Status: live",
            color=MUTED,
            font_size=16,
        )

        # Position content inside comment card (top-left anchor)
        c_x_left = comment_card.get_left()[0]
        c_y_top = comment_card.get_top()[1]
        check_glyph.move_to((c_x_left + 0.4, c_y_top - 0.4, 0))
        comment_header.next_to(check_glyph, RIGHT, buff=0.22)
        comment_header.set_y(check_glyph.get_center()[1])
        url_text.next_to(comment_header, DOWN, buff=0.18, aligned_edge=LEFT)
        status_text.next_to(url_text, DOWN, buff=0.12, aligned_edge=LEFT)

        comment_group = VGroup(
            comment_card,
            check_glyph,
            comment_header,
            url_text,
            status_text,
        )
        comment_group.move_to((0, -0.8, 0))

        self.play(FadeIn(comment_group, shift=UP * 0.3), run_time=1.0)

        # One pulse — twice was twee.
        self.play(url_text.animate.set_color(FG), run_time=0.3)
        self.play(url_text.animate.set_color(ACCENT_3), run_time=0.3)

        self.wait(3.0)

        # ──────────────────────────────────────────────────────────
        # PHASE 4 — Merge & auto teardown
        # ──────────────────────────────────────────────────────────

        # Status flips Open → Merged
        merged_badge = make_badge("Merged", MERGED)
        merged_badge.move_to(status_badge.get_center())

        self.play(
            Transform(status_badge, merged_badge),
            FadeOut(preview_chip, scale=0.7),
            run_time=0.8,
        )

        # Infra fades out reverse order (deploy → registry → build)
        self.play(
            LaggedStart(
                FadeOut(ico_deploy, shift=DOWN * 0.1),
                FadeOut(ico_registry, shift=DOWN * 0.1),
                FadeOut(ico_build, shift=DOWN * 0.1),
                FadeOut(infra_line_bg),
                FadeOut(infra_progress),
                lag_ratio=0.18,
            ),
            run_time=1.4,
        )

        # URL grays out + strikethrough
        strike = Line(
            url_text.get_left() + LEFT * 0.05,
            url_text.get_right() + RIGHT * 0.05,
            color=MUTED,
            stroke_width=2.0,
        )
        self.play(
            url_text.animate.set_color(MUTED),
            Create(strike),
            run_time=0.8,
        )

        # The strikethrough is the close. Hold on it.
        self.wait(2.5)


# Soft warning yellow for the trigger fire flash (not in theme — single-use).
WARN_YELLOW = "#E0B651"


def _label_glyph() -> VGroup:
    body = RoundedRectangle(
        width=0.42,
        height=0.26,
        corner_radius=0.06,
        color=FG,
        stroke_width=1.8,
        fill_opacity=0,
    )
    hole = Circle(radius=0.035, color=FG, stroke_width=1.5, fill_opacity=0)
    hole.move_to(body.get_left() + RIGHT * 0.08)
    return VGroup(body, hole)


def _merge_glyph() -> VGroup:
    junction: tuple[float, float, float] = (0, 0.0, 0)
    branch_left: tuple[float, float, float] = (-0.16, 0.20, 0)
    branch_right: tuple[float, float, float] = (0.16, 0.20, 0)
    trunk_bottom: tuple[float, float, float] = (0, -0.22, 0)
    return VGroup(
        Line(branch_left, junction, color=FG, stroke_width=2.0),
        Line(branch_right, junction, color=FG, stroke_width=2.0),
        Line(junction, trunk_bottom, color=FG, stroke_width=2.0),
        Dot(point=branch_left, radius=0.04, color=FG),
        Dot(point=branch_right, radius=0.04, color=FG),
        Dot(point=trunk_bottom, radius=0.04, color=FG),
    )


def _moon_glyph() -> VGroup:
    # Filled FG crescent: outer FG circle with offset BG cutout
    outer = Circle(
        radius=0.22,
        color=FG,
        stroke_width=1.8,
        fill_color=FG,
        fill_opacity=1.0,
    )
    cutout = Circle(
        radius=0.20,
        color=BG,
        stroke_width=0,
        fill_color=BG,
        fill_opacity=1.0,
    )
    cutout.shift(RIGHT * 0.10)
    return VGroup(outer, cutout)


def _calendar_glyph() -> VGroup:
    w, h = 0.42, 0.34
    outer = Rectangle(
        width=w,
        height=h,
        color=FG,
        stroke_width=1.8,
        fill_opacity=0,
    )
    v_mid = Line((0, h / 2, 0), (0, -h / 2, 0), color=FG, stroke_width=1.5)
    h_top = Line((-w / 2, h / 6, 0), (w / 2, h / 6, 0), color=FG, stroke_width=1.5)
    h_bot = Line((-w / 2, -h / 6, 0), (w / 2, -h / 6, 0), color=FG, stroke_width=1.5)
    return VGroup(outer, v_mid, h_top, h_bot)


def _hourglass_glyph() -> VGroup:
    top_tri = Polygon(
        (-0.18, 0.22, 0),
        (0.18, 0.22, 0),
        (0, 0, 0),
        color=FG,
        stroke_width=1.8,
        fill_opacity=0,
    )
    bot_tri = Polygon(
        (-0.18, -0.22, 0),
        (0.18, -0.22, 0),
        (0, 0, 0),
        color=FG,
        stroke_width=1.8,
        fill_opacity=0,
    )
    return VGroup(top_tri, bot_tri)


def _idle_glyph() -> VGroup:
    # Dotted circle: 8 dots arranged on a ring
    dots = VGroup()
    n, r = 8, 0.22
    for i in range(n):
        a = 2 * math.pi * i / n
        dots.add(
            Dot(point=(r * math.cos(a), r * math.sin(a), 0), radius=0.035, color=FG)
        )
    return dots


def _make_trigger(glyph: VGroup, title: str, sub: str) -> VGroup:
    title_text = Text(title, color=FG, font_size=20, weight="MEDIUM", font="Helvetica")
    sub_text = Text(sub, color=MUTED, font_size=15, font="Helvetica")
    label_block = VGroup(title_text, sub_text).arrange(DOWN, buff=0.08)
    return VGroup(glyph, label_block).arrange(DOWN, buff=0.18)


class EE06(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # BEAT 1 (0–6s) — Env in center, glowing
        # ──────────────────────────────────────────────────────────
        env_box = RoundedRectangle(
            width=1.6,
            height=0.7,
            corner_radius=0.16,
            color=ACCENT_3,
            stroke_width=2.5,
            fill_color=ACCENT_3,
            fill_opacity=0.18,
        )
        env_glow = RoundedRectangle(
            width=2.4,
            height=1.4,
            corner_radius=0.32,
            color=ACCENT_3,
            stroke_width=0,
            fill_color=ACCENT_3,
            fill_opacity=0.10,
        )
        env_label = Text(
            "pr-1234",
            color=ACCENT_3,
            font_size=22,
            weight="MEDIUM",
            font="Helvetica",
        )
        env_label.move_to(env_box.get_center())
        env_glow.set_z_index(-2)
        env_box.set_z_index(-1)

        env_group = VGroup(env_glow, env_box, env_label)
        env_group.move_to(ORIGIN)

        self.wait(0.3)
        self.play(
            FadeIn(env_glow),
            FadeIn(env_box),
            FadeIn(env_label),
            run_time=0.8,
        )
        # Soft pulse: 2 cycles of glow opacity
        for _ in range(2):
            self.play(
                env_glow.animate.set_fill(ACCENT_3, opacity=0.22),
                run_time=1.0,
            )
            self.play(
                env_glow.animate.set_fill(ACCENT_3, opacity=0.08),
                run_time=1.0,
            )
        self.wait(0.9)
        # Beat 1 cumulative: 0.3 + 0.8 + 4.0 + 0.9 = 6.0s ✓

        # ──────────────────────────────────────────────────────────
        # BEAT 2 (6–22s) — 6 triggers fire one at a time
        # ──────────────────────────────────────────────────────────
        # Type-A hexagon (no top/bottom, leaves vertical room for Beat 3 tagline)
        # Order: spec 1→6 mapped clockwise from upper-right.
        r = 2.7
        spec = [
            (60, _label_glyph, "Label removed", "instant teardown"),
            (0, _merge_glyph, "PR merged or closed", "automatic"),
            (300, _moon_glyph, "Nightly shutdown", "20:00 → 08:00"),
            (240, _calendar_glyph, "Weekend off", "Fri 20:00 → Mon 08:00"),
            (180, _hourglass_glyph, "Hard TTL", "7 days max"),
            (120, _idle_glyph, "Idle reaper", "scale to zero on low CPU"),
        ]

        triggers: list[tuple[VGroup, float]] = []
        for angle_deg, glyph_fn, title, sub in spec:
            t = _make_trigger(glyph_fn(), title, sub)
            angle = math.radians(angle_deg)
            t.move_to((r * math.cos(angle), r * math.sin(angle), 0))
            triggers.append((t, angle))

        for trigger, angle in triggers:
            # 1. Trigger appears
            self.play(FadeIn(trigger, scale=0.6), run_time=0.5)

            # 2. Fire line: from trigger toward env
            line_start = (0.7 * math.cos(angle), 0.7 * math.sin(angle), 0)
            line_end = (1.9 * math.cos(angle), 1.9 * math.sin(angle), 0)
            # Line(line_end, line_start) so Create draws from trigger toward env
            fire_line = Line(line_end, line_start, color=WARN_YELLOW, stroke_width=2.5)
            self.play(Create(fire_line), run_time=0.4)

            # 3. Env flashes yellow
            self.play(
                env_box.animate.set_color(WARN_YELLOW).set_fill(
                    WARN_YELLOW, opacity=0.22
                ),
                env_glow.animate.set_fill(WARN_YELLOW, opacity=0.22),
                env_label.animate.set_color(WARN_YELLOW),
                run_time=0.2,
            )
            self.wait(0.3)

            # 4. Env back to green; fade fire line
            self.play(
                env_box.animate.set_color(ACCENT_3).set_fill(ACCENT_3, opacity=0.18),
                env_glow.animate.set_fill(ACCENT_3, opacity=0.10),
                env_label.animate.set_color(ACCENT_3),
                FadeOut(fire_line),
                run_time=0.4,
            )
            self.wait(0.3)
        self.wait(0.5)

        # ──────────────────────────────────────────────────────────
        # BEAT 3 — Tagline. Main only; the subtitle was over-explaining.
        # ──────────────────────────────────────────────────────────
        tagline_main = Text(
            "Six shutdown paths, running in parallel.",
            color=FG,
            font_size=28,
            weight="BOLD",
            font="Helvetica",
        )
        tagline_main.move_to((0, -3.45, 0))

        self.play(FadeIn(tagline_main, shift=UP * 0.12), run_time=0.8)
        self.wait(3.5)


class EE07(NormalScene):
    def construct(self) -> None:
        # ──────────────────────────────────────────────────────────
        # Constants
        # ──────────────────────────────────────────────────────────
        Y_BASE = -2.7  # chart floor
        Y_PER_DOLLAR = 0.010  # $1 = 0.010 frame units; $600 → 6.0 tall
        BAR_W = 0.7
        FONT = "Helvetica"

        def y_for(d: float) -> float:
            return Y_BASE + d * Y_PER_DOLLAR

        def make_zero_bar(
            x: float,
            color,
            opacity: float = 0.75,
            w: float = BAR_W,
            y_offset: float = 0.0,
        ):
            r = Rectangle(
                width=w,
                height=0.001,
                fill_color=color,
                fill_opacity=opacity,
                stroke_width=0,
            )
            r.move_to((x, Y_BASE + y_offset + 0.0005, 0))
            return r

        def make_full_bar(
            x: float,
            height: float,
            color,
            opacity: float = 0.75,
            w: float = BAR_W,
            y_offset: float = 0.0,
        ):
            r = Rectangle(
                width=w,
                height=height,
                fill_color=color,
                fill_opacity=opacity,
                stroke_width=0,
            )
            r.move_to((x, Y_BASE + y_offset + height / 2, 0))
            return r

        def label(text: str, **kwargs):
            return Text(text, font=FONT, **kwargs)

        # X positions (Beat 3 onward)
        x_hub = -5.5
        x_fe = -3.8
        x_cons = -1.3
        x_real = -0.1
        x_heavy = 1.1
        x_worst = 2.3

        # Beat 1/2 hub bar position (slightly left of center, slides to x_hub in Beat 3)
        x_hub_init = -1.5

        # Heights
        active_h = 373.69 * Y_PER_DOLLAR
        idle_h = 226.80 * Y_PER_DOLLAR
        fe_h = 49.11 * Y_PER_DOLLAR
        h_hubnext = 16.61 * Y_PER_DOLLAR
        h_unifynext = 15.82 * Y_PER_DOLLAR
        h_training = 16.68 * Y_PER_DOLLAR
        h_cons = 4.0 * Y_PER_DOLLAR
        h_real = 8.0 * Y_PER_DOLLAR
        h_heavy = 25.0 * Y_PER_DOLLAR
        h_worst = 140.0 * Y_PER_DOLLAR

        y_threshold = y_for(226.80)

        # ──────────────────────────────────────────────────────────
        # BEAT 1 (0–10s) — Today's spend
        # ──────────────────────────────────────────────────────────
        # Two stacked bars, both initially gray (so the rising bar reads as one solid)
        active_bar = make_zero_bar(x_hub_init, MUTED, opacity=0.65)
        idle_bar = make_zero_bar(x_hub_init, MUTED, opacity=0.65, y_offset=active_h)
        active_target = make_full_bar(x_hub_init, active_h, MUTED, opacity=0.65)
        idle_target_gray = make_full_bar(
            x_hub_init, idle_h, MUTED, opacity=0.65, y_offset=active_h
        )

        self.wait(0.3)
        self.add(active_bar, idle_bar)
        self.play(
            Transform(active_bar, active_target),
            Transform(idle_bar, idle_target_gray),
            run_time=2.0,
        )
        self.wait(0.4)

        # Top portion turns red
        idle_target_red = make_full_bar(
            x_hub_init, idle_h, PROBLEM, opacity=0.78, y_offset=active_h
        )
        self.play(Transform(idle_bar, idle_target_red), run_time=0.7)

        # Labels
        label_total = label("$600/month", color=FG, font_size=22, weight="BOLD")
        label_total.move_to((x_hub_init, y_for(600) + 0.28, 0))

        label_idle_top = label("IDLE WASTE", color=PROBLEM, font_size=18, weight="BOLD")
        label_idle_amt = label("$226.80", color=PROBLEM, font_size=15)
        label_idle = VGroup(label_idle_top, label_idle_amt).arrange(DOWN, buff=0.06)
        label_idle.move_to(
            (x_hub_init + BAR_W / 2 + 1.1, Y_BASE + active_h + idle_h / 2, 0)
        )

        label_active_top = label(
            "Active workload", color=MUTED, font_size=18, weight="MEDIUM"
        )
        label_active_amt = label("$373.69", color=MUTED, font_size=15)
        label_active = VGroup(label_active_top, label_active_amt).arrange(
            DOWN, buff=0.06
        )
        label_active.move_to((x_hub_init + BAR_W / 2 + 1.1, Y_BASE + active_h / 2, 0))

        label_hub_name = label("hub namespace\ntoday", color=MUTED, font_size=14)
        label_hub_name.move_to((x_hub_init, Y_BASE - 0.32, 0))

        # Persistent data-source attribution — these real numbers are pulled
        # from Kubecost; pin a small caption top-right so the audience can tell
        # measured values from the projected scenarios in Beat 4.
        source_caption = label(
            "Source: Kubecost — hub staging, April 2026",
            color=MUTED,
            font_size=12,
            slant="ITALIC",
        )
        source_caption.move_to((6.55 - source_caption.width / 2, 3.75, 0))

        self.play(
            FadeIn(label_total, shift=DOWN * 0.1),
            FadeIn(label_idle, shift=LEFT * 0.1),
            FadeIn(label_active, shift=LEFT * 0.1),
            FadeIn(source_caption),
            run_time=0.8,
        )
        self.play(FadeIn(label_hub_name, shift=UP * 0.05), run_time=0.5)
        self.wait(2.5)

        # ──────────────────────────────────────────────────────────
        # BEAT 2 (10–18s) — Set the threshold first
        # ──────────────────────────────────────────────────────────
        dashed = DashedLine(
            start=(-6.5, y_threshold, 0),
            end=(+5.0, y_threshold, 0),
            color=PROBLEM,
            stroke_width=2.5,
            dash_length=0.18,
        )

        threshold_label = label(
            "Current idle waste — $226.80",
            color=PROBLEM,
            font_size=18,
            weight="MEDIUM",
        )
        threshold_label.next_to(dashed.get_end(), UP, buff=0.1)
        threshold_label.shift(LEFT * 1.5)  # nudge inward

        self.play(Create(dashed), run_time=1.5)
        self.play(FadeIn(threshold_label, shift=DOWN * 0.1), run_time=0.7)
        self.wait(2.5)

        # ──────────────────────────────────────────────────────────
        # BEAT 3 (18–25s) — Zooming into FE
        # ──────────────────────────────────────────────────────────
        # Slide hub bar (and its labels) to x_hub. Fade IDLE/ACTIVE labels (the dashed line carries it now).
        hub_shift = x_hub - x_hub_init
        hub_movables = VGroup(active_bar, idle_bar, label_total, label_hub_name)

        self.play(
            hub_movables.animate.shift(RIGHT * hub_shift),
            FadeOut(label_idle, shift=LEFT * 0.2),
            FadeOut(label_active, shift=LEFT * 0.2),
            run_time=1.0,
        )

        # Build FE bar with 3 stacked sub-segments (different INFRA shades)
        fe_seg1_zero = make_zero_bar(x_fe, INFRA, opacity=0.45)
        fe_seg2_zero = make_zero_bar(x_fe, INFRA, opacity=0.60, y_offset=h_hubnext)
        fe_seg3_zero = make_zero_bar(
            x_fe, INFRA, opacity=0.78, y_offset=h_hubnext + h_unifynext
        )
        fe_seg1_full = make_full_bar(x_fe, h_hubnext, INFRA, opacity=0.45)
        fe_seg2_full = make_full_bar(
            x_fe, h_unifynext, INFRA, opacity=0.60, y_offset=h_hubnext
        )
        fe_seg3_full = make_full_bar(
            x_fe, h_training, INFRA, opacity=0.78, y_offset=h_hubnext + h_unifynext
        )

        self.add(fe_seg1_zero, fe_seg2_zero, fe_seg3_zero)
        self.play(
            Transform(fe_seg1_zero, fe_seg1_full),
            Transform(fe_seg2_zero, fe_seg2_full),
            Transform(fe_seg3_zero, fe_seg3_full),
            run_time=1.2,
        )

        # FE bar value label (above) and breakdown
        label_fe_total = label("$49.11/mo", color=INFRA, font_size=18, weight="BOLD")
        label_fe_total.move_to((x_fe, Y_BASE + fe_h + 0.25, 0))

        label_fe_name = label("Frontend\nonly", color=MUTED, font_size=14)
        label_fe_name.move_to((x_fe, Y_BASE - 0.32, 0))

        # Per-segment breakdown to the right of FE bar
        fe_breakdown = VGroup(
            label("hub-next  $16.61", color=MUTED, font_size=11),
            label("unify-next  $15.82", color=MUTED, font_size=11),
            label("training  $16.68", color=MUTED, font_size=11),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        # Anchor LEFT edge of breakdown just right of the FE bar (not its center)
        fe_breakdown.move_to(
            (x_fe + BAR_W / 2 + 0.18 + fe_breakdown.width / 2, Y_BASE + fe_h / 2, 0)
        )

        self.play(
            FadeIn(label_fe_total, shift=DOWN * 0.1),
            FadeIn(label_fe_name, shift=UP * 0.05),
            run_time=0.6,
        )
        self.play(FadeIn(fe_breakdown, shift=LEFT * 0.1), run_time=0.6)
        self.wait(2.0)

        # ──────────────────────────────────────────────────────────
        # BEAT 4 (25–40s) — Four ephemeral env scenarios
        # ──────────────────────────────────────────────────────────
        ee_specs = [
            (x_cons, h_cons, "Conservative", "5 envs/mo", "$3–5"),
            (x_real, h_real, "Realistic", "10 envs/mo", "$6–10"),
            (x_heavy, h_heavy, "Heavy", "30 envs/mo", "$20–30"),
            (x_worst, h_worst, "Worst case", "no shutdown", "$120–160"),
        ]

        # Caveat that distinguishes the Kubecost-measured bars (left) from the
        # modeled scenarios (these four). Sits above the EE cluster and stays
        # for the rest of the scene.
        projected_caveat = label(
            "* projected — assumed env lifecycle × FE per-env cost",
            color=MUTED,
            font_size=12,
            slant="ITALIC",
        )
        projected_caveat.move_to(((x_cons + x_worst) / 2, Y_BASE + h_worst + 0.7, 0))
        self.play(FadeIn(projected_caveat, shift=DOWN * 0.05), run_time=0.5)

        for i, (x, h, name, sub, money) in enumerate(ee_specs):
            # Use ACCENT_3 (green = solution) for normal cases, but the worst case stays under threshold
            color = ACCENT_3
            opacity = 0.55 + i * 0.08  # gradient: lighter for tiny bars, denser for big

            bar_zero = make_zero_bar(x, color, opacity=opacity)
            bar_full = make_full_bar(x, h, color, opacity=opacity)
            self.add(bar_zero)

            # Label above bar (dollar range)
            money_label = label(money, color=ACCENT_3, font_size=14, weight="BOLD")
            money_label.move_to((x, Y_BASE + h + 0.20, 0))

            # Bar name below (2 lines)
            name_label = label(f"{name}\n{sub}", color=MUTED, font_size=12)
            name_label.move_to((x, Y_BASE - 0.32, 0))

            self.play(
                Transform(bar_zero, bar_full),
                FadeIn(money_label, shift=DOWN * 0.05),
                FadeIn(name_label, shift=UP * 0.05),
                run_time=1.2,
            )
            self.wait(0.4)
        # The bars-vs-threshold geometry is the argument. Hold briefly, then kicker.
        self.wait(2.0)

        # ──────────────────────────────────────────────────────────
        # BEAT 5 (40–45s) — The kicker
        # ──────────────────────────────────────────────────────────
        kicker = label(
            "Even our worst case is less than what we already waste sitting idle.",
            color=FG,
            font_size=22,
            weight="BOLD",
        )
        kicker.move_to((0, -3.45, 0))

        footnote = label(
            "Frontend scope. Backend has parallel scope; same math applies.",
            color=MUTED,
            font_size=13,
            slant="ITALIC",
        )
        footnote.move_to((0, -3.85, 0))

        self.play(FadeIn(kicker, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(footnote, shift=UP * 0.05), run_time=0.6)
        self.wait(3.4)
        # Beat 5 cumulative: 1.0 + 0.6 + 3.4 = 5.0s ✓
        # Total: 10 + 8 + 7 + 15 + 5 = 45s ✓


class EE07B(NormalScene):
    # Answers manager Q: "How often will the team use this?" and plants the
    # $0-if-unused floor as the bounded downside. Sits between EE07's cost
    # bars and EE08's resolution beat.
    def construct(self) -> None:
        FONT = "Helvetica"

        def label(text: str, **kwargs):
            return Text(text, font=FONT, **kwargs)

        # ──────────────────────────────────────────────────────────
        # Title + subtitle
        # ──────────────────────────────────────────────────────────
        title = label(
            "On-demand. Pay only for what we ship.",
            color=FG,
            font_size=36,
            weight="BOLD",
            t2c={"On-demand": ACCENT_3, "what we ship": ACCENT_3},
        )
        title.move_to((0, 3.45, 0))

        subtitle = label(
            "Usage scales with team velocity. Cost scales with usage.",
            color=MUTED,
            font_size=20,
            slant="ITALIC",
        )
        subtitle.move_to((0, 2.85, 0))

        self.wait(0.3)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(subtitle, shift=UP * 0.05), run_time=0.5)

        # ──────────────────────────────────────────────────────────
        # Inputs row — ~10 PRs/week (matches EE07 "Realistic" FE scenario)
        # ──────────────────────────────────────────────────────────
        inputs_label = label(
            "~10 PRs / week",
            color=FG,
            font_size=18,
            weight="MEDIUM",
        )
        inputs_label.move_to((0, 1.95, 0))

        def pr_glyph() -> VGroup:
            box = RoundedRectangle(
                width=0.55,
                height=0.42,
                corner_radius=0.08,
                color=ACCENT,
                stroke_width=1.5,
                fill_color=ACCENT,
                fill_opacity=0.10,
            )
            dot = Circle(
                radius=0.05,
                color=ACCENT,
                fill_color=ACCENT,
                fill_opacity=1.0,
                stroke_width=0,
            )
            dot.move_to(box.get_left() + RIGHT * 0.13)
            bar = Line(
                box.get_left() + RIGHT * 0.24,
                box.get_left() + RIGHT * 0.45,
                color=ACCENT,
                stroke_width=2.0,
            )
            return VGroup(box, dot, bar)

        pr_row = VGroup(*[pr_glyph() for _ in range(10)]).arrange(RIGHT, buff=0.18)
        pr_row.move_to((0, 1.45, 0))

        self.play(FadeIn(inputs_label, shift=DOWN * 0.05), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(g, scale=0.6) for g in pr_row],
                lag_ratio=0.06,
            ),
            run_time=1.2,
        )

        # ──────────────────────────────────────────────────────────
        # Arrow 1 — PR → env
        # ──────────────────────────────────────────────────────────
        arrow1 = Line((0, 1.05, 0), (0, 0.65, 0), color=MUTED, stroke_width=1.6)
        arrow1_head = Polygon(
            (-0.09, 0.72, 0),
            (0.09, 0.72, 0),
            (0, 0.55, 0),
            color=MUTED,
            stroke_width=0,
            fill_color=MUTED,
            fill_opacity=1.0,
        )
        arrow1_caption = label(
            "each PR spins one ephemeral env",
            color=MUTED,
            font_size=14,
        )
        arrow1_caption.move_to((2.8, 0.85, 0))

        self.play(
            Create(arrow1),
            FadeIn(arrow1_head),
            FadeIn(arrow1_caption, shift=LEFT * 0.1),
            run_time=0.6,
        )

        # ──────────────────────────────────────────────────────────
        # Outputs row — 10 env boxes (mirror PR count)
        # ──────────────────────────────────────────────────────────
        env_row = VGroup(
            *[
                RoundedRectangle(
                    width=0.55,
                    height=0.42,
                    corner_radius=0.10,
                    color=ACCENT_3,
                    stroke_width=1.8,
                    fill_color=ACCENT_3,
                    fill_opacity=0.22,
                )
                for _ in range(10)
            ]
        ).arrange(RIGHT, buff=0.18)
        env_row.move_to((0, 0.25, 0))

        self.play(
            LaggedStart(
                *[FadeIn(g, scale=0.6) for g in env_row],
                lag_ratio=0.06,
            ),
            run_time=1.2,
        )

        # ──────────────────────────────────────────────────────────
        # Arrow 2 — env → cost. Callback to EE06's 6 triggers.
        # ──────────────────────────────────────────────────────────
        arrow2 = Line((0, -0.18, 0), (0, -0.58, 0), color=MUTED, stroke_width=1.6)
        arrow2_head = Polygon(
            (-0.09, -0.50, 0),
            (0.09, -0.50, 0),
            (0, -0.68, 0),
            color=MUTED,
            stroke_width=0,
            fill_color=MUTED,
            fill_opacity=1.0,
        )
        arrow2_caption = label(
            "auto-teardown · 6 triggers (see EE06)",
            color=MUTED,
            font_size=14,
        )
        arrow2_caption.move_to((2.8, -0.38, 0))

        self.play(
            Create(arrow2),
            FadeIn(arrow2_head),
            FadeIn(arrow2_caption, shift=LEFT * 0.1),
            run_time=0.6,
        )

        # ──────────────────────────────────────────────────────────
        # Cost counter + floor/ceiling annotations.
        # The counter ramps $0 → ~$10 with floor caption pinned at the start
        # and ceiling caption appearing once it lands.
        # ──────────────────────────────────────────────────────────
        cost_caption = label("Cost / month", color=MUTED, font_size=16)
        cost_caption.move_to((0, -1.0, 0))

        spend = label("$0", color=FG, font_size=56, weight="BOLD")
        spend.move_to((0, -1.85, 0))

        self.play(
            FadeIn(cost_caption, shift=UP * 0.05),
            FadeIn(spend, shift=UP * 0.15),
            run_time=0.5,
        )

        floor_head = label("Floor: $0", color=ACCENT, font_size=28, weight="BOLD")
        floor_sub = label(
            "no PRs open → nothing runs → nothing bills",
            color=MUTED,
            font_size=12,
        )
        floor_block = VGroup(floor_head, floor_sub).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT
        )
        floor_block.move_to((-4.2, -1.85, 0))

        self.play(FadeIn(floor_block, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(0.6)

        # Counter ramps so the audience sees usage drive the spend.
        for s, color in [("$3", FG), ("$6", FG), ("~$10", ACCENT_3)]:
            new_spend = label(s, color=color, font_size=56, weight="BOLD")
            new_spend.move_to(spend.get_center())
            self.play(Transform(spend, new_spend), run_time=0.32)

        ceiling_head = label(
            "Realistic ceiling", color=ACCENT_3, font_size=20, weight="MEDIUM"
        )
        ceiling_amount = label(
            "~$10 / month  (FE)", color=ACCENT_3, font_size=18, weight="BOLD"
        )
        ceiling_source = label(
            "Source: EE07 · Kubecost Apr 2026",
            color=MUTED,
            font_size=11,
            slant="ITALIC",
        )
        ceiling_block = VGroup(
            ceiling_head, ceiling_amount, ceiling_source
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        ceiling_block.move_to((4.0, -1.85, 0))

        self.play(FadeIn(ceiling_block, shift=LEFT * 0.15), run_time=0.6)
        self.wait(1.2)

        # ──────────────────────────────────────────────────────────
        # Bottom strap
        # ──────────────────────────────────────────────────────────
        strap = label(
            "Pay-per-use. The downside is bounded.",
            color=FG,
            font_size=22,
            weight="BOLD",
            t2c={"Pay-per-use": ACCENT_3, "bounded": ACCENT_3},
        )
        strap.move_to((0, -3.55, 0))

        self.play(FadeIn(strap, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)


class EE07C(NormalScene):
    # Answers manager Q: "How will this improve velocity / delivery?"
    # 19.8 hrs/week recovered (from EE02–EE03) is the springboard; this scene
    # translates it into shipping outcomes that lead into EE08's resolution.
    def construct(self) -> None:
        FONT = "Helvetica"

        def label(text: str, **kwargs):
            return Text(text, font=FONT, **kwargs)

        # 3-lane glyph for "Independent deploys" — three parallel channels.
        def channels_glyph() -> VGroup:
            g = VGroup()
            for dy in (0.18, 0.0, -0.18):
                g.add(
                    Line(
                        (-0.20, dy, 0),
                        (0.20, dy, 0),
                        color=FG,
                        stroke_width=2.0,
                    )
                )
                g.add(Dot(point=(-0.20, dy, 0), radius=0.04, color=FG))
            return g

        # ──────────────────────────────────────────────────────────
        # Title + subtitle
        # ──────────────────────────────────────────────────────────
        title = label(
            "What 19.8 hrs/week buys us",
            color=FG,
            font_size=36,
            weight="BOLD",
            t2c={"19.8 hrs/week": ACCENT_3},
        )
        title.move_to((0, 3.45, 0))

        subtitle = label(
            "Hours reclaimed → velocity unlocked.",
            color=MUTED,
            font_size=20,
            slant="ITALIC",
        )
        subtitle.move_to((0, 2.85, 0))

        self.wait(0.3)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(subtitle, shift=UP * 0.05), run_time=0.5)

        # ──────────────────────────────────────────────────────────
        # 2×2 card grid using EE06's _make_trigger pattern, wrapped in
        # a soft ACCENT_3 card to match EE05's PR-card aesthetic.
        # ──────────────────────────────────────────────────────────
        cards_spec = [
            (_merge_glyph, "Parallel PR reviews",
             "Every PR gets its own env. No queue."),
            (_hourglass_glyph, "Faster QA cycles",
             "Env live the moment a PR opens."),
            (channels_glyph, "Independent deploys",
             "FE / BE / QA ship without a shared env."),
            (_idle_glyph, "Risk-free experiments",
             "Spikes & demos auto-vanish on merge."),
        ]

        def make_card(glyph_fn, title_text: str, sub_text: str) -> VGroup:
            inner = _make_trigger(glyph_fn(), title_text, sub_text)
            card = RoundedRectangle(
                width=5.4,
                height=1.9,
                corner_radius=0.18,
                color=ACCENT_3,
                stroke_width=1.5,
                fill_color=ACCENT_3,
                fill_opacity=0.06,
            )
            inner.move_to(card.get_center())
            return VGroup(card, inner)

        cards = [make_card(g, t, s) for g, t, s in cards_spec]
        positions = [(-2.85, 1.1), (2.85, 1.1), (-2.85, -1.05), (2.85, -1.05)]
        for c, (x, y) in zip(cards, positions):
            c.move_to((x, y, 0))

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.15) for c in cards],
                lag_ratio=0.20,
            ),
            run_time=2.0,
        )
        self.wait(3.0)

        # ──────────────────────────────────────────────────────────
        # Bottom strap — echoes into EE08's tag-line for continuity.
        # ──────────────────────────────────────────────────────────
        strap = label(
            "More PRs shipped · Less coordination · Migration unblocked",
            color=FG,
            font_size=22,
            weight="BOLD",
            t2c={"More PRs shipped": ACCENT_3, "Migration unblocked": ACCENT_3},
        )
        strap.move_to((0, -3.55, 0))

        self.play(FadeIn(strap, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)


class EE08(NormalScene):
    def construct(self) -> None:
        FONT = "Helvetica"

        def label(text: str, **kwargs):
            return Text(text, font=FONT, **kwargs)

        # Mirror of EE01 — 18 engineers, each paired 1:1 with their own env.
        # Same camera framing as EE01, no contention, no warnings.
        def engineer(tag: str) -> VGroup:
            c = Circle(
                radius=0.20,
                color=INK,
                fill_color=CREAM,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            t = Text(tag, color=INK, font_size=15, weight="BOLD", font=FONT)
            t.move_to(c.get_center())
            return VGroup(c, t)

        fe_group = VGroup(*[engineer("FE") for _ in range(6)]).arrange(RIGHT, buff=0.22)
        be_group = VGroup(*[engineer("BE") for _ in range(7)]).arrange(RIGHT, buff=0.22)
        qa_group = VGroup(*[engineer("QA") for _ in range(5)]).arrange(RIGHT, buff=0.22)
        team_row = VGroup(fe_group, be_group, qa_group).arrange(RIGHT, buff=0.85)
        team_row.move_to((0, 1.6, 0))

        all_eng = [*fe_group, *be_group, *qa_group]

        envs = VGroup()
        for eng in all_eng:
            env = RoundedRectangle(
                width=0.42,
                height=0.36,
                corner_radius=0.08,
                color=ACCENT_3,
                stroke_width=1.8,
                fill_color=ACCENT_3,
                fill_opacity=0.18,
            )
            env.move_to((eng[0].get_center()[0], -1.5, 0))
            envs.add(env)

        lines = VGroup()
        for eng, env in zip(all_eng, envs):
            ln = Line(
                eng[0].get_bottom(),
                env.get_top(),
                color=ACCENT_3,
                stroke_width=1.5,
            )
            lines.add(ln)

        self.wait(0.3)
        self.play(
            LaggedStart(
                *[FadeIn(eng, shift=DOWN * 0.18) for eng in all_eng],
                lag_ratio=0.045,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(
                *[FadeIn(env, shift=UP * 0.18) for env in envs],
                lag_ratio=0.045,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.04),
            run_time=1.5,
        )
        self.wait(1.5)

        # Stats land. The italic subtitle is cut — the picture is the argument.
        summary_main = label(
            "~19.8 hrs/week recovered.    ~$1000/mo back.",
            color=FG,
            font_size=30,
            weight="BOLD",
            t2c={"19.8": ACCENT_3, "$1000": ACCENT_3},
        )
        summary_main.move_to((0, -3.0, 0))

        velocity_tag = label(
            "More PRs shipped · No env collisions · Migration unblocked",
            color=MUTED,
            font_size=16,
        )
        velocity_tag.move_to((0, -3.55, 0))

        self.play(FadeIn(summary_main, shift=UP * 0.12), run_time=1.0)
        self.play(FadeIn(velocity_tag, shift=UP * 0.08), run_time=0.6)
        self.wait(2.6)


class EEFull(NormalScene):
    # Plays every EE beat in sequence as a single ~3-min video. Each scene's
    # construct body only uses inherited Scene methods (self.play/wait/add),
    # so calling EEnn.construct(self) on this scene reuses each beat verbatim.
    # Between beats we fade any residue and hold briefly — the next beat's
    # opening FadeIn completes the soft cross-dissolve.
    def construct(self) -> None:
        beats: list[type[NormalScene]] = [
            EE00,
            EE01,
            EE02,
            EE03,
            EE03B,
            EE04,
            EE05,
            EE06,
            EE07,
            EE07B,
            EE07C,
            EE08,
        ]
        for i, scene_cls in enumerate(beats):
            scene_cls.construct(self)  # type: ignore[arg-type]
            if i < len(beats) - 1:
                self._between_beats()

    def _between_beats(self, fade: float = 0.6, hold: float = 0.2) -> None:
        # Per-mobject FadeOut (not VGroup-wrapped) — some scenes leave
        # non-VMobject items on stage which VGroup rejects.
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=fade)
        self.wait(hold)
