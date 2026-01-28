"""
test_smoke.py
--------------
Purpose:
- Ensure the app config is correctly loaded.

"""

from nl2sql_assistant.config import CONFIG


def test_config_smoke():
    assert CONFIG.app_name == "nl2sql-assistant"
    assert CONFIG.stage == "0"
