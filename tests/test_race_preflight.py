"""Tests for race/preflight.py helper functions."""

from race import preflight as race_preflight


def test_check_api_key_supports_explicit_env_map():
    agent_defs = {"codex": {"env_key": "OPENAI_API_KEY"}}

    has_key, key_name = race_preflight.check_api_key(
        agent_defs,
        "codex",
        env={"OPENAI_API_KEY": "sk-test"},
    )
    assert (has_key, key_name) == (True, "OPENAI_API_KEY")

    has_key, key_name = race_preflight.check_api_key(
        agent_defs,
        "codex",
        env={},
    )
    assert (has_key, key_name) == (False, "OPENAI_API_KEY")

    assert race_preflight.check_api_key(agent_defs, "unknown", env={}) == (False, "")


def test_run_preflight_reports_availability_and_auth_lines():
    lines = []
    agent_defs = {
        "codex": {"display": "OpenAI Codex"},
        "gemini": {"display": "Google Gemini"},
    }

    def check_agent_available(agent_type):
        if agent_type == "codex":
            return True, "codex 1.2.3", ""
        return False, "", "not installed"

    def check_api_key(agent_type):
        if agent_type == "codex":
            return False, "OPENAI_API_KEY"
        return True, "GEMINI_API_KEY"

    def detect_model(agent_type):
        if agent_type == "codex":
            return "o4-mini", "from test"
        return "gemini-2.5-pro", "from test"

    results = race_preflight.run_preflight(
        agent_defs,
        ["gemini", "codex", "codex"],
        check_agent_available_cb=check_agent_available,
        check_api_key_cb=check_api_key,
        detect_model_cb=detect_model,
        print_fn=lines.append,
    )

    assert results == [
        ("codex", True, "o4-mini"),
        ("gemini", False, "not installed"),
    ]
    assert any("PRE-FLIGHT CHECKS" in line for line in lines)
    assert any("[OK]" in line and "OpenAI Codex" in line for line in lines)
    assert any("Auth: checking login status..." in line for line in lines)
    assert any("[MISS]" in line and "Google Gemini" in line for line in lines)


def test_build_final_agent_lists_filters_unavailable_types():
    final_names, final_types, final_models, missing_agents = race_preflight.build_final_agent_lists(
        raw_names=["claude", "codex", "codex-2", "gemini"],
        agent_types=["claude", "codex", "codex", "gemini"],
        model_overrides=[None, "o4-mini", "o4-mini-high"],
        preflight_rows=[
            ("claude", True, "claude (auto)"),
            ("codex", False, "missing"),
            ("gemini", True, "gemini-2.5-pro"),
        ],
    )

    assert final_names == ["claude", "gemini"]
    assert final_types == ["claude", "gemini"]
    assert final_models == [None, None]
    assert missing_agents == [("codex", "codex"), ("codex-2", "codex")]

