import logging
from logging.handlers import RotatingFileHandler

from ..core.config import config

config.get_logs_dir().mkdir(parents=True, exist_ok=True)

handler = RotatingFileHandler(
    config.get_logs_dir() / "app.log", maxBytes=1000000, backupCount=5, encoding="utf-8"
)

console_handler = logging.StreamHandler()

if config.parameters.get("debug", False):
    log_level = logging.DEBUG
else:
    log_level = logging.INFO


logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[handler, console_handler],
)

logger = logging.getLogger(__name__)
