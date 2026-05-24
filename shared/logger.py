from loguru import logger
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger.add(
    "logs/robot.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO"
)

def get_logger():
    return logger