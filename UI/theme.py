# ----------------------------------------------------------------------------
# THEME / COLOR TOKENS
# ----------------------------------------------------------------------------
# Single source of truth for the app's look: every color used anywhere in
# the UI is named here, so restyling never means hunting hex codes through
# widget code.
#
# The resource accents (COLOR_PEARL down to COLOR_CRYSTAL) are sampled from
# each item's own artwork in UI/resources/images/, which is why several of
# them are muted rather than vivid - they're meant to read as that item, not
# to stand out on their own. UI/resources/render.py draws the same accents
# into the image sent to Discord, so changing one here changes both.

COLOR_BG = "#0d0d12"          # app background
COLOR_SIDEBAR = "#131319"     # sidebar background
COLOR_RAIL = "#0f0f15"        # settings category rail - darker than the
                                # sidebar so the two navbars read as separate
COLOR_CARD = "#1b1b24"        # card / panel background
COLOR_CARD_HOVER = "#22222d"
COLOR_ROW_ALT = "#16161f"     # zebra-stripe row background in the event log
COLOR_BORDER = "#26262f"
COLOR_TEXT = "#f2f2f5"
COLOR_SUBTEXT = "#8f8f9c"
COLOR_ACCENT = "#ff3d78"      # pink/magenta accent
COLOR_ACCENT_HOVER = "#e5326a"
COLOR_GREEN = "#3ddc84"
COLOR_GREEN_HOVER = "#31c473"
COLOR_RED = "#ff5c5c"
COLOR_RED_HOVER = "#e14d4d"
COLOR_BLUE = "#5b8dff"
COLOR_CYAN = "#22d3ee"        # dust collected accent
COLOR_PEARL = "#4B3C58"       # black pearls accent - dark desaturated purple
COLOR_METAL = "#C7C3C5"       # metal ingots accent - brushed aluminum grey
COLOR_PASTE = "#444444"       # cementing paste accent - neutral dark grey
COLOR_ELECTRONICS = "#938F5D" # electronics accent - dull olive gold, off the
                                # circuit board art
COLOR_CRYSTAL = "#CDD3D3"     # crystal accent - pale ice

FONT_FAMILY = "Segoe UI"