"""Đọc cấu hình từ file .env (nằm cạnh file này) và biến môi trường."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

REQUIRED_VARS = (
    "SECRET_KEY",
    "MYSQL_HOST",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DATABASE",
)


class ConfigError(RuntimeError):
    pass


def load_config():
    missing = [name for name in REQUIRED_VARS if not os.getenv(name)]
    if missing:
        raise ConfigError(
            "Thiếu biến môi trường: " + ", ".join(missing)
            + f". Hãy tạo file {BASE_DIR / '.env'} từ .env.example."
        )

    return {
        "SECRET_KEY": os.environ["SECRET_KEY"],
        "MYSQL_HOST": os.environ["MYSQL_HOST"],
        "MYSQL_PORT": int(os.getenv("MYSQL_PORT", "3306")),
        "MYSQL_USER": os.environ["MYSQL_USER"],
        "MYSQL_PASSWORD": os.environ["MYSQL_PASSWORD"],
        "MYSQL_DATABASE": os.environ["MYSQL_DATABASE"],
    }
