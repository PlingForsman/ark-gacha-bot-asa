"""Reads and writes resources.json - how much the bot has farmed, kept
across restarts.

Written from two places: the dashboard, which throttles saves to at most one
a second while counts are climbing (DashboardPage._schedule_stats_save), and
whatever flushes on the way out. Read by the dashboard at startup and by
UI/resources/render.py when it draws the counts for Discord.

Sibling of settings/store.py, with the same corrupt-file handling."""
import json
import os

from logger.logger import logger
from tools.recovery import quarantine

RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "resources.json"
)
ARCHIVE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "resources_archive.json"
)
# Defaults + canonical key set, used both to seed a fresh resources.json and
# to backfill any keys missing from an older one on load. Keys match the
# dashboard's stat card keys (DashboardPage.stat_cards).
DEFAULTS = {
    "crystals_opened": 0,
    "dust_collected": 0,
    "black_pearls": 0,
    "metal_ingots": 0,
    "flint": 0,
    "electronics": 0,
    "crystal": 0,
}


def load() -> dict:
    """Load resources.json, backfilling missing keys with 0 and dropping
    any stale keys a newer build no longer tracks.

    The app ships without a resources.json at all, so a missing file is
    the normal first-launch case - and a corrupt one must not crash the
    app either. Both fall back to all-zero counts and write them to disk.

    Because a missing file is created here, calling this is never purely a
    read - it can write resources.json and log that it did."""
    data = dict(DEFAULTS)
    try:
        with open(RESOURCES_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
        data.update({k: int(v) for k, v in saved.items() if k in DEFAULTS})
    except FileNotFoundError:
        save(data)
        logger.info("resources.json not found - created it with zeroed counts.")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        backup = quarantine(RESOURCES_PATH)
        save(data)
        recovered = (f"the old file was saved to {backup}" if backup
                     else "the old file could not be backed up")
        logger.warning(f"resources.json unreadable ({error}) - "
                       f"reset to zeroed counts; {recovered}.")
    return data


def save(data: dict) -> None:
    """Write resources.json. Only the keys in DEFAULTS are written, in that
    order, so the file stays canonical no matter what it's handed."""
    with open(RESOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump({k: int(data.get(k, 0)) for k in DEFAULTS}, f, indent=4)

def on_start() -> None:
    #on start write current data to an archieve of resources and reset currently tracked resources to 0 
    current = {k: int(load().get(k, 0)) for k in DEFAULTS}

    if os.path.exists(ARCHIVE_PATH):
        try:
            with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
            if not isinstance(existing, dict):
                existing = {}
        except (OSError, json.JSONDecodeError):
            existing = {}
    else:
        existing = {}

    merged = dict(existing)
    for key, value in current.items():
        merged[key] = merged.get(key, 0) + value

    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4)

    save(DEFAULTS)