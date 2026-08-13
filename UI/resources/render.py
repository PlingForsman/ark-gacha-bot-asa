"""Draw the resource counts as a standalone image, for sending out over
Discord.

The cards are the dashboard's loot cards, rebuilt in Pillow. Nothing here
touches Tk, so an image can be produced with the window minimized, buried
behind a fullscreen game, or not open at all - which is the point, since the
request arrives from Discord while the user is doing something else.

The background is transparent, and stays that way: the cards carry their own
dark fill, which is what keeps their near-white text readable whatever theme
the viewer is on. A static PNG can't adapt to that theme - everyone in the
channel is served the same file - so self-contained cards on transparency is
as theme-independent as this gets. Don't "fix" the fill by removing it.

Card geometry below mirrors DashboardPage's mini stat cards (a StatCard built
with height=STAT_ROW_H, icon_size=48, icon_pad=14, title_size=11,
value_size=22) at the 288x80 they actually lay out to on screen. The two are
matched by measurement, not wired together: UI.py owns the on-screen look,
and importing it here would drag Tk into a module whose whole point is not
needing it. If a card changes there, it has to be re-matched here by hand.
"""
import os
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

from tools.format import format_count
from UI.resources import store
from UI.theme import (
    COLOR_BG, COLOR_CRYSTAL, COLOR_CYAN, COLOR_ELECTRONICS, COLOR_METAL,
    COLOR_PASTE, COLOR_PEARL, COLOR_SUBTEXT, COLOR_TEXT,
)

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

CARD_W, CARD_H = 288, 80
CARD_GAP = 16
CARD_RADIUS = 12
ACCENT_W = 5      # width of the colored strip down the card's left edge
TEXT_X = 20
ICON_SIZE = 48
ICON_PAD = 14     # gap between the icon and the card's right edge
TITLE_SIZE = 11
VALUE_SIZE = 22

# Everything is drawn at this multiple and scaled back down at the end.
# Pillow draws shapes with hard edges, so a rounded corner at final size
# comes out visibly stepped; oversampling is what smooths them.
SUPERSAMPLE = 4

# Font files rather than family names: PIL resolves these out of the Windows
# font directory, and there's no name-to-file lookup to go through.
TITLE_FONT = "segoeuib.ttf"  # Segoe UI Bold - the UI's FONT_FAMILY, bold
VALUE_FONT = "segoeuib.ttf"

# (store key, label, icon file, accent color) - order and colors match the
# dashboard, with the two headline counts leading.
CARDS = [
    ("crystals_opened", "Crystals Opened", "gacha_crystal.png", COLOR_CYAN),
    ("dust_collected", "Dust Collected", "element_dust.png", COLOR_CYAN),
    ("black_pearls", "Black Pearls", "black_pearls.png", COLOR_PEARL),
    ("metal_ingots", "Metal Ingots", "metal_ingot.png", COLOR_METAL),
    ("cementing_paste", "Cementing Paste", "cementing_paste.png", COLOR_PASTE),
    ("electronics", "Electronics", "electronics.png", COLOR_ELECTRONICS),
    ("crystal", "Crystal", "crystal.png", COLOR_CRYSTAL),
]


@lru_cache(maxsize=None)
def _font(filename, size):
    """Load a font, falling back to PIL's built-in one. A missing Segoe UI
    should cost the image its typography, not cost the user their image.
    Cached because every card asks for the same two fonts."""
    try:
        return ImageFont.truetype(filename, size)
    except OSError:
        try:
            return ImageFont.load_default(size)
        except TypeError:
            # Pillow only learned to size its built-in font in 10.1.
            return ImageFont.load_default()


def _draw_card(label, count, icon_file, accent, scale):
    """One resource card, on its own transparent tile, drawn `scale` times
    larger than final size (the caller downsamples the finished sheet)."""
    width, height = CARD_W * scale, CARD_H * scale
    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # The card body and the accent strip are painted as plain rectangles and
    # then cut to shape by the rounded mask, which is what keeps the strip
    # tracing the card's own corner curve instead of bulging past it.
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, width, height), fill=COLOR_BG)
    draw.rectangle((0, 0, ACCENT_W * scale, height), fill=accent)

    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1),
                                            radius=CARD_RADIUS * scale, fill=255)
    card.putalpha(mask)

    if icon_file:
        icon = Image.open(os.path.join(IMAGES_DIR, icon_file)).convert("RGBA")
        size = ICON_SIZE * scale
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        # Right-aligned, vertically centered - as the dashboard anchors it.
        card.alpha_composite(icon, (width - ICON_PAD * scale - size,
                                    (height - size) // 2))

    draw = ImageDraw.Draw(card)
    # The dashboard anchors its text at 34% and 68% of the card height, by
    # the text's own vertical center ("m" anchor: middle baseline-box).
    draw.text((TEXT_X * scale, height * 0.34), label.upper(), anchor="lm",
              font=_font(TITLE_FONT, TITLE_SIZE * scale), fill=COLOR_SUBTEXT)
    draw.text((TEXT_X * scale, height * 0.68), format_count(count), anchor="lm",
              font=_font(VALUE_FONT, VALUE_SIZE * scale), fill=COLOR_TEXT)
    return card


def render_resources(counts=None, columns=2) -> Image.Image:
    """Return the resource cards as a transparent RGBA image.

        image = render_resources()
        buffer = io.BytesIO()
        image.save(buffer, "PNG")   # PNG - transparency needs it
        buffer.seek(0)

    `counts` defaults to whatever is saved in resources.json, so this can be
    called without the app running at all. Note the dashboard saves on a
    throttle, so the file can trail the numbers on screen by up to a second;
    pass a dict of the same shape (store.DEFAULTS) - the dashboard's own
    `_stats`, or a session's totals - when that matters.

    `columns` reflows the grid: 1 gives a tall strip, 2 a squarer block that
    sits better in a Discord message."""
    if counts is None:
        counts = store.load()
    columns = max(1, columns)

    scale = SUPERSAMPLE
    rows = -(-len(CARDS) // columns)  # ceiling division
    width = columns * CARD_W + (columns - 1) * CARD_GAP
    height = rows * CARD_H + (rows - 1) * CARD_GAP
    sheet = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))

    for i, (key, label, icon_file, accent) in enumerate(CARDS):
        card = _draw_card(label, counts.get(key, 0), icon_file, accent, scale)
        column, row = i % columns, i // columns
        sheet.alpha_composite(card, (column * (CARD_W + CARD_GAP) * scale,
                                     row * (CARD_H + CARD_GAP) * scale))

    return sheet.resize((width, height), Image.Resampling.LANCZOS)
