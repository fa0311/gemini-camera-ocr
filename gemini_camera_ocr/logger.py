import json
import logging
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LoggingSettings:
    level: str
    format: str
    json: bool


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(s: LoggingSettings) -> None:
    root = logging.getLogger()
    root.handlers.clear()

    level = getattr(logging, s.level.upper(), logging.INFO)
    root.setLevel(level)

    handler = logging.StreamHandler()

    if s.json:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(s.format))

    root.addHandler(handler)


logger = logging.getLogger(__name__)
