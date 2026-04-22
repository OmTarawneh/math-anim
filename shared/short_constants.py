from manim import DOWN, UP

# ==========================================
# 1. VIDEO RESOLUTION & FRAME SETUP
# ==========================================
# Use these to configure your scene before rendering
RES_WIDTH = 1080
RES_HEIGHT = 1920
FPS = 60

# Expanded coordinate system for vertical video
FRAME_WIDTH = 9.0
FRAME_HEIGHT = 16.0

# ==========================================
# 2. TYPOGRAPHY & FONTS
# ==========================================
# Recommended Sans-Serif fonts for readability on mobile screens
FONT_PRIMARY = "Comic Sans MS"
FONT_SECONDARY = "Inter"
FONT_CODE = "Fira Code"

# Font Sizes (Calibrated for the 9x16 frame width)
FONT_SIZE_XL = 48  # Hooks, main questions, big impact text
FONT_SIZE_L = 36  # Subtitles, secondary text
FONT_SIZE_M = 28  # Standard body text, lists, equations
FONT_SIZE_S = 22  # Citations, footnotes, small labels

# Line Spacing
SPACING_TIGHT = 1.0
SPACING_NORMAL = 1.2  # Best for large hooks
SPACING_LOOSE = 1.4  # Best for dense body text

# ==========================================
# 3. SAFE ZONES & POSITIONING
# ==========================================
# With frame_height=16 (Y goes from -8 to 8) and frame_width=9 (X goes from -4.5 to 4.5)

# Y-Axis Constraints (Vertical)
SAFE_TOP = 5.5  # Do not place text above this (avoids top UI)
SAFE_BOTTOM = -3.5  # Do not place text below this (avoids captions/description)

# X-Axis Constraints (Horizontal)
SAFE_LEFT = -3.5  # Margin for left edge
SAFE_RIGHT = 3.5  # Margin for right edge (avoids like/share buttons)

# Anchor Points
POS_HOOK_TOP = UP * 3.5  # Standard placement for top hooks
POS_CENTER = UP * 0  # Center of the screen
POS_SUB_BOTTOM = DOWN * 2.5  # Lowest safe point for text

# Buffs (Spacing between elements)
BUFF_SMALL = 0.5
BUFF_NORMAL = 1.0
BUFF_LARGE = 1.5

# ==========================================
# 4. COLORS
# ==========================================
# Standardized palette for consistency across videos
COLOR_TEXT_MAIN = "#FFFFFF"  # Pure white
COLOR_TEXT_SUB = "#E0E0E0"  # Light grey
COLOR_ACCENT = "#FADB5F"  # Attention-grabbing Yellow
COLOR_HIGHLIGHT = "#FF5A5F"  # Punchy Red/Pink for contrast
COLOR_BG = "#0A0A0A"  # Deep black/grey background

# ==========================================
# 5. ANIMATION TIMINGS
# ==========================================
# Use these for consistent pacing
TIME_SNAPPY = 0.4  # Quick pops, UI elements
TIME_NORMAL = 0.8  # Standard fade-ins, drawing text
TIME_SLOW = 1.5  # Emphasized reveals, complex equations
