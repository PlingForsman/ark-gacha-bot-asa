# Display formatting shared by everything that puts a count in front of a
# user - the on-screen stat cards and the resource image rendered for
# Discord. Kept out of UI.py so the image renderer doesn't have to import
# the whole UI (and Tk with it) just to format a number.


def format_count(n):
    """Compact a raw count for the stat cards: 950 -> '950',
    14_320 -> '14.32k', 2_000_000 -> '2m', 1_234_000_000 -> '1.23b'.
    Two decimals at most; trailing zeros are dropped ('2.00k' and '14.30k'
    read worse than '2k' and '14.3k')."""
    n = int(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    tiers = ((1_000_000_000, "b"), (1_000_000, "m"), (1_000, "k"))
    for i, (div, suffix) in enumerate(tiers):
        if n >= div:
            value = round(n / div, 2)
            # 999_995+ would round to '1000k' - promote it a tier to '1m'
            if value >= 1000 and i:
                div, suffix = tiers[i - 1]
                value = round(n / div, 2)
            text = f"{value:.2f}".rstrip("0").rstrip(".")
            return f"{sign}{text}{suffix}"
    return f"{sign}{n}"
