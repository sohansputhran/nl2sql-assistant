"""
config.py
------------
Purpose:
- Define the application configuration.

"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    app_name: str = "nl2sql-assistant"
    stage: str = "0"


CONFIG = AppConfig()
