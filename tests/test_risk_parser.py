from nl2sql_assistant.chains.risk_classifier import parse_risk_json


def test_parse_risk_json_valid():
    raw = """
    {
      "risk_level": "low",
      "flags": [{"type": "none", "message": "ok"}],
      "suggestions": ["run it"]
    }
    """.strip()
    r = parse_risk_json(raw)
    assert r.risk_level == "low"
    assert len(r.flags) == 1
    assert r.flags[0].type == "none"
    assert r.suggestions == ["run it"]


def test_parse_risk_json_invalid_fallback():
    raw = "NOT JSON"
    r = parse_risk_json(raw)
    assert r.risk_level == "medium"
    assert r.flags[0].type == "json_parse_error"
