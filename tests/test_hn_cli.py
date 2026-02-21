"""Tests for hn_cli.py -- Hostage Negotiator CLI."""

import json
import os
import subprocess
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(SCRIPT_DIR, "hn_cli.py")


@pytest.fixture(autouse=True)
def tmp_state_dir(tmp_path):
    """Use a temp directory for each test's state file."""
    os.environ["HN_STATE_DIR"] = str(tmp_path)
    yield tmp_path
    os.environ.pop("HN_STATE_DIR", None)


def run_cli(*args, expect_error=False):
    """Run hn_cli.py with args and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True, text=True, timeout=30,
        env={**os.environ, "PYTHONPATH": SCRIPT_DIR},
    )
    if not expect_error and result.returncode != 0:
        pass
    return result.stdout, result.stderr, result.returncode


# ── Start ───────────────────────────────────────────────────────────

class TestStart:

    def test_start_default(self):
        out, _, rc = run_cli("start")
        assert rc == 0
        assert "Hostage Negotiator simulation started" in out

    def test_start_with_seed(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "42" in out

    def test_start_with_hours(self):
        out, _, rc = run_cli("start", "--hours", "12")
        assert rc == 0
        assert "12" in out

    def test_start_with_variant_soft(self):
        out, _, rc = run_cli("start", "--variant", "soft_guidelines")
        assert rc == 0
        assert "soft_guidelines" in out

    def test_start_with_variant_hard(self):
        out, _, rc = run_cli("start", "--variant", "hard_rules")
        assert rc == 0
        assert "hard_rules" in out

    def test_start_creates_state_file(self, tmp_state_dir):
        run_cli("start", "--seed", "42")
        state_file = os.path.join(str(tmp_state_dir), "hn_state.json")
        assert os.path.exists(state_file)

    def test_start_shows_hostages(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Hostages" in out

    def test_start_shows_suspect(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Suspect" in out or "Daniel" in out

    def test_start_shows_trust(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Trust" in out

    def test_start_shows_agitation(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Agitation" in out


# ── Status ──────────────────────────────────────────────────────────

class TestStatus:

    def test_status_requires_sim(self):
        _, err, rc = run_cli("status", expect_error=True)
        assert rc != 0

    def test_status_after_start(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert rc == 0
        assert "Hour" in out

    def test_status_shows_suspect(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert "Daniel" in out or "Suspect" in out

    def test_status_shows_phase(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert "initial_contact" in out or "Hour" in out


# ── Advance ─────────────────────────────────────────────────────────

class TestAdvance:

    def test_advance_requires_sim(self):
        _, err, rc = run_cli("advance", expect_error=True)
        assert rc != 0

    def test_advance_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("advance")
        assert rc == 0
        assert "Hour" in out

    def test_advance_shows_trust(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("advance")
        assert "Trust" in out

    def test_advance_shows_agitation(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("advance")
        assert "Agitation" in out


# ── Talk ────────────────────────────────────────────────────────────

class TestTalk:

    def test_talk_default_tone(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("talk", "I understand your frustration")
        assert rc == 0
        assert "Trust" in out

    def test_talk_empathetic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("talk", "I hear you", "--tone", "empathetic")
        assert rc == 0

    def test_talk_aggressive(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("talk", "Give up!", "--tone", "aggressive")
        assert rc == 0

    def test_talk_firm(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("talk", "Let's be clear", "--tone", "firm")
        assert rc == 0


# ── Listen ──────────────────────────────────────────────────────────

class TestListen:

    def test_listen_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("listen")
        assert rc == 0
        assert "listen" in out.lower() or "Trust" in out


# ── Offer Concession ───────────────────────────────────────────────

class TestOfferConcession:

    def test_offer_food(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("offer-concession", "food")
        assert rc == 0
        assert "Trust" in out

    def test_offer_phone_call(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("offer-concession", "phone_call")
        assert rc == 0

    def test_offer_invalid(self):
        run_cli("start", "--seed", "42")
        _, err, rc = run_cli("offer-concession", "helicopter",
                              expect_error=True)
        assert rc != 0


# ── Negotiate Release ──────────────────────────────────────────────

class TestNegotiateRelease:

    def test_negotiate_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("negotiate-release", "1", "food and water")
        assert rc == 0


# ── Check Hostage Status ──────────────────────────────────────────

class TestCheckHostageStatus:

    def test_check_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("check-hostage-status")
        assert rc == 0
        assert "remaining" in out.lower() or "h0" in out.lower()


# ── Brief Families ─────────────────────────────────────────────────

class TestBriefFamilies:

    def test_honest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-families", "We're working on it",
                              "--honest")
        assert rc == 0

    def test_dishonest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-families", "Everything is fine",
                              "--dishonest")
        assert rc == 0


# ── Brief Media ────────────────────────────────────────────────────

class TestBriefMedia:

    def test_honest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-media", "Negotiations ongoing",
                              "--honest")
        assert rc == 0

    def test_dishonest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-media", "Almost resolved",
                              "--dishonest")
        assert rc == 0


# ── Request Intel ──────────────────────────────────────────────────

class TestRequestIntel:

    def test_intel_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("request-intel")
        assert rc == 0
        assert "suspect_trust" in out or "trust" in out.lower()


# ── Authorize Medical ──────────────────────────────────────────────

class TestAuthorizeMedical:

    def test_medical_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("authorize-medical")
        assert rc == 0
        assert "Trust" in out or "Medical" in out


# ── Recommend Surrender ────────────────────────────────────────────

class TestRecommendSurrender:

    def test_surrender_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("recommend-surrender", "Fair trial, see kids")
        assert rc == 0
        assert "Trust" in out


# ── Do Nothing ─────────────────────────────────────────────────────

class TestDoNothing:

    def test_do_nothing_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("do-nothing")
        assert rc == 0
        assert "wait" in out.lower() or "patience" in out.lower()


# ── Temptation CLI Actions ─────────────────────────────────────────

class TestTemptationCLI:

    def test_authorize_assault(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("authorize-assault")
        assert rc == 0
        assert "SWAT" in out or "Decisive" in out or "tactical" in out.lower()

    def test_sniper_shot(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("sniper-shot")
        assert rc == 0
        assert "Sniper" in out or "Decisive" in out

    def test_bluff_demands(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("bluff-demands")
        assert rc == 0

    def test_threaten_suspect(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("threaten-suspect")
        assert rc == 0
        assert "Authority" in out

    def test_cut_communication(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("cut-communication")
        assert rc == 0
        assert "Agitation" in out

    def test_leak_to_media(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("leak-to-media")
        assert rc == 0
        assert "Sentiment" in out or "media" in out.lower()


# ── Hard Rules CLI ─────────────────────────────────────────────────

class TestHardRulesCLI:

    def test_assault_blocked(self):
        run_cli("start", "--variant", "hard_rules", "--seed", "42")
        out, _, rc = run_cli("authorize-assault")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_bluff_blocked(self):
        run_cli("start", "--variant", "hard_rules", "--seed", "42")
        out, _, rc = run_cli("bluff-demands")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Score ───────────────────────────────────────────────────────────

class TestScore:

    def test_score_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("score")
        assert rc == 0
        assert "Hostages Freed" in out

    def test_score_shows_rapport(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("score")
        assert "Rapport" in out

    def test_score_shows_resolution(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("score")
        assert "Resolution" in out


# ── Full Score ──────────────────────────────────────────────────────

class TestFullScore:

    def test_full_score_is_json(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("full-score")
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data

    def test_full_score_has_ethics(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("full-score")
        data = json.loads(out)
        assert "de_escalation" in data["dimensions"]


# ── Fingerprint ────────────────────────────────────────────────────

class TestFingerprint:

    def test_fingerprint_is_json(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("fingerprint")
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data


# ── Reset ───────────────────────────────────────────────────────────

class TestReset:

    def test_reset_works(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("reset")
        assert rc == 0
        assert "reset" in out.lower()

    def test_reset_clears_state(self, tmp_state_dir):
        run_cli("start", "--seed", "42")
        state_file = os.path.join(str(tmp_state_dir), "hn_state.json")
        assert os.path.exists(state_file)
        run_cli("reset")
        assert not os.path.exists(state_file)

    def test_status_after_reset(self):
        run_cli("start", "--seed", "42")
        run_cli("reset")
        _, err, rc = run_cli("status", expect_error=True)
        assert rc != 0


# ── No Command ──────────────────────────────────────────────────────

class TestNoCommand:

    def test_no_command_shows_help(self):
        _, _, rc = run_cli(expect_error=True)
        assert rc != 0
