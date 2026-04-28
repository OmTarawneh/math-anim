# math-anim

Manim animations with a Claude-themed palette.

## Layout

- `scenes/base.py` — `ShortScene` (1080×1920), `NormalScene` (1920×1080), `NormalThreeDScene`. Each pins resolution and applies the dark Claude background.
- `scenes/theme.py` — Claude palette (`BG`, `FG`, `ACCENT`, `MUTED`, `ACCENT_2`, `ACCENT_3`).
- `scenes/demo_short.py`, `scenes/demo_normal.py` — minimal demos for each mode.

## Running

```
uv run poe high scenes/demo_short.py ShortDemo
uv run poe high scenes/demo_normal.py NormalDemo
```

Poe tasks (`pyproject.toml`): `scene` (default), `low` (-ql, 15 fps for fast iteration), `high` (-qh, 60 fps), `last-frame` (-ps), `render` (-qh, write only). Output goes to `media/videos/<file>/<pixel_height>p<fps>/<Scene>.mp4`.

## Verifying output dimensions

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 media/videos/demo_short/1920p60/ShortDemo.mp4
# → 1080,1920

ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 media/videos/demo_normal/1080p60/NormalDemo.mp4
# → 1920,1080
```
