import os
import shutil
from datetime import datetime

# Corrupt savefiles are moved here (project root) instead of being deleted,
# so the user can still open them and recover their values by hand after
# the app has reset the live file to defaults.
CORRUPTED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "CORRUPTED_SAVEFILES"
)


def quarantine(path: str):
    """Move a corrupt savefile into CORRUPTED_SAVEFILES/, timestamping the
    name so repeated corruption never overwrites an earlier backup.
    Returns the backup path, or None if the file couldn't be moved (the
    caller should still proceed with its reset - a stuck corrupt file must
    not keep the app from starting)."""
    try:
        os.makedirs(CORRUPTED_DIR, exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(path))
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        target = os.path.join(CORRUPTED_DIR, f"{name}_{stamp}{ext}")
        shutil.move(path, target)
        return target
    except OSError:
        return None
