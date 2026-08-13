"""Backwards-compatible shim for old code that imports
`source.logs.gachalogs.logger`. Not a separate logger - this just re-exports
the one shared instance from logger/logger.py, so old and new code write to
the same logs.log and the same on-screen Event Log.

The TEMPLATE level (used for template-matching debug output, which is
noisy enough to break the Discord bot if left on DEBUG) is registered here
rather than in logger/logger.py, since it's specific to this older code
path - registering it on logging.Logger still makes logger.template(...)
work on the shared instance, since it's a logging.Logger subclass."""
import logging

from logger.logger import logger, LOG_PATH  

TEMPLATE_LEVEL = 5
logging.addLevelName(TEMPLATE_LEVEL, "TEMPLATE")

def template(self, message, *args, **kwargs):
    if self.isEnabledFor(TEMPLATE_LEVEL):
        self._log(TEMPLATE_LEVEL, message, args, **kwargs)

logging.Logger.template = template