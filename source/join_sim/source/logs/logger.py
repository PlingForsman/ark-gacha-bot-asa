import logging

from logger.logger import logger, LOG_PATH  # noqa: F401 - re-exported for old imports

TEMPLATE_LEVEL = 5
logging.addLevelName(TEMPLATE_LEVEL, "TEMPLATE")


def template(self, message, *args, **kwargs):
    if self.isEnabledFor(TEMPLATE_LEVEL):
        self._log(TEMPLATE_LEVEL, message, args, **kwargs)


logging.Logger.template = template