import logging
from logging.handlers import RotatingFileHandler

from core.config import config

handler = RotatingFileHandler(
    config.get_logs_dir() / "app.log", maxBytes=1000000, backupCount=5, encoding="utf-8"
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[handler],
)

logger = logging.getLogger(__name__)
