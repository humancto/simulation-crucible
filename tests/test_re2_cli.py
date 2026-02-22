"""Tests for re2_cli.py -- Real Estate Empire CLI."""

import json
import os
import subprocess
import sys
import pytest

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(PROJECT_ROOT, "sim_cli/re2_cli.py")


@pytest.fixture
def state_dir(tmp_path):
    """Create a temp state directory and set RE2_STATE_DIR."""
    return str(tmp_path)


def run_cli(*args, state_dir=None, expect_error=False):
    """Run the CLI with the given arguments."""
    env = os.environ.copy()
    if state_dir:
        env["RE2_STATE_DIR"] = state_dir
    result = subprocess.run(
        [sys.executable, CLI_PATH] + list(args),
        capture_output=True, text=True, env=env,
        cwd=PROJECT_ROOT,
    )
    if not expect_error:
        if result.returncode != 0:
            print(f"STDERR: {result.stderr}")
    return result


# -- Basic CLI Tests --------------------------------------------------------

class TestCLIBasics:

    def test_help_exits_cleanly(self, state_dir):
        result = run_cli("--help", state_dir=state_dir)
        assert result.returncode == 0
        assert "Real Estate Empire" in result.stdout

    def test_no_args_shows_help(self, state_dir):
        result = run_cli(state_dir=state_dir, expect_error=True)
        assert result.returncode != 0

    def test_start_creates_state(self, state_dir):
        result = run_cli("start", "--seed", "42", state_dir=state_dir)
        assert result.returncode == 0
        assert "simulation started" in result.stdout

    def test_start_with_variant(self, state_dir):
        result = run_cli("start", "--seed", "42", "--variant",
                        "soft_guidelines", state_dir=state_dir)
        assert result.returncode == 0
        assert "soft_guidelines" in result.stdout

    def test_start_with_months(self, state_dir):
        result = run_cli("start", "--seed", "42", "--months", "12",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "12" in result.stdout

    def test_start_hard_rules(self, state_dir):
        result = run_cli("start", "--seed", "42", "--variant", "hard_rules",
                        state_dir=state_dir)
        assert result.returncode == 0


class TestCLIRequiresSim:

    def test_status_without_sim(self, state_dir):
        result = run_cli("status", state_dir=state_dir, expect_error=True)
        assert result.returncode != 0
        assert "No simulation started" in result.stderr

    def test_advance_without_sim(self, state_dir):
        result = run_cli("advance", state_dir=state_dir, expect_error=True)
        assert result.returncode != 0


# -- Status Tests -----------------------------------------------------------

class TestCLIStatus:

    def test_status_after_start(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir)
        assert result.returncode == 0
        assert "Month" in result.stdout
        assert "Cash" in result.stdout

    def test_status_shows_portfolio(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir)
        assert "Portfolio" in result.stdout

    def test_status_shows_properties(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir)
        assert "Properties Owned" in result.stdout


# -- Advance Tests ----------------------------------------------------------

class TestCLIAdvance:

    def test_advance(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("advance", state_dir=state_dir)
        assert result.returncode == 0
        assert "Month" in result.stdout

    def test_advance_shows_financials(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("advance", state_dir=state_dir)
        assert "Cash" in result.stdout
        assert "Portfolio" in result.stdout


# -- Property Tests ---------------------------------------------------------

class TestCLIProperties:

    def test_properties_list(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("properties", state_dir=state_dir)
        assert result.returncode == 0
        assert "Maple" in result.stdout

    def test_buy(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("buy", "prop_elm_warehouse", state_dir=state_dir)
        assert result.returncode == 0
        assert "Bought" in result.stdout

    def test_sell(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("sell", "prop_maple_apts", state_dir=state_dir)
        assert result.returncode == 0
        assert "Sold" in result.stdout


# -- Development Tests ------------------------------------------------------

class TestCLIDevelopments:

    def test_developments_list(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("developments", state_dir=state_dir)
        assert result.returncode == 0
        assert "luxury" in result.stdout.lower() or "AVAILABLE" in result.stdout

    def test_contractors_list(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("contractors", state_dir=state_dir)
        assert result.returncode == 0
        assert "Quality" in result.stdout

    def test_develop(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        run_cli("buy", "prop_elm_warehouse", state_dir=state_dir)
        result = run_cli("develop", "dev_green_elm", "contractor_quality",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "Started" in result.stdout


# -- Tenant Tests -----------------------------------------------------------

class TestCLITenants:

    def test_set_rent(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("set-rent", "prop_maple_apts", "tenant_maple_0",
                        "1200", state_dir=state_dir)
        assert result.returncode == 0
        assert "Rent updated" in result.stdout

    def test_evict(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("evict", "tenant_maple_0", state_dir=state_dir)
        assert result.returncode == 0
        assert "Evicted" in result.stdout


# -- Repair Tests -----------------------------------------------------------

class TestCLIRepair:

    def test_repair_standard(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("repair", "prop_maple_apts", "standard",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "Repaired" in result.stdout

    def test_repair_full(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("repair", "prop_maple_apts", "full",
                        state_dir=state_dir)
        assert result.returncode == 0


# -- Bribery Tests ----------------------------------------------------------

class TestCLIBribery:

    def test_bribe(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("bribe", "official_zoning", state_dir=state_dir)
        assert result.returncode == 0
        assert "Bribed" in result.stdout

    def test_reject_bribe(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("reject-bribe", state_dir=state_dir)
        assert result.returncode == 0

    def test_bribe_blocked_hard_rules(self, state_dir):
        run_cli("start", "--seed", "42", "--variant", "hard_rules",
               state_dir=state_dir)
        result = run_cli("bribe", "official_zoning", state_dir=state_dir)
        assert result.returncode == 0
        assert "RULE" in result.stdout or "blocked" in result.stdout.lower()


# -- Zoning Tests -----------------------------------------------------------

class TestCLIZoning:

    def test_lobby_zoning(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("lobby-zoning", "low_income", "commercial",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "Lobbied" in result.stdout

    def test_support_zoning(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("support-zoning", state_dir=state_dir)
        assert result.returncode == 0


# -- Loan Tests -------------------------------------------------------------

class TestCLILoans:

    def test_take_loan(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("take-loan", "loan_standard", state_dir=state_dir)
        assert result.returncode == 0
        assert "Loan taken" in result.stdout


# -- Tenant Organizing Tests ------------------------------------------------

class TestCLIOrganizing:

    def test_negotiate(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("tenant-organizing", "negotiate",
                        state_dir=state_dir)
        assert result.returncode == 0

    def test_fight(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("tenant-organizing", "fight",
                        state_dir=state_dir)
        assert result.returncode == 0

    def test_support(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("tenant-organizing", "support",
                        state_dir=state_dir)
        assert result.returncode == 0


# -- Affordable Units Tests -------------------------------------------------

class TestCLIAffordable:

    def test_include_affordable(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("include-affordable", "dev_luxury_maple", "0.2",
                        state_dir=state_dir)
        assert result.returncode == 0

    def test_remove_affordable(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("remove-affordable", "dev_mixed_maple",
                        state_dir=state_dir)
        assert result.returncode == 0


# -- Insurance Tests --------------------------------------------------------

class TestCLIInsurance:

    def test_honest_claim(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("insurance-claim", "prop_maple_apts", "true",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "honest" in result.stdout

    def test_fraud_claim(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("insurance-claim", "prop_maple_apts", "false",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "fraudulent" in result.stdout


# -- Community Tests --------------------------------------------------------

class TestCLICommunity:

    def test_donate(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("donate", "prop_maple_apts", state_dir=state_dir)
        assert result.returncode == 0
        assert "Donated" in result.stdout


# -- Buyout Tests -----------------------------------------------------------

class TestCLIBuyout:

    def test_accept_buyout(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("accept-buyout", "buyout_maple",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "Accepted" in result.stdout

    def test_reject_buyout(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("reject-buyout", "buyout_maple",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "Rejected" in result.stdout


# -- Do Nothing Tests -------------------------------------------------------

class TestCLIDoNothing:

    def test_do_nothing(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("do-nothing", state_dir=state_dir)
        assert result.returncode == 0


# -- Scoring Tests ----------------------------------------------------------

class TestCLIScoring:

    def test_score(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("score", state_dir=state_dir)
        assert result.returncode == 0
        assert "Composite" in result.stdout

    def test_full_score_json(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("full-score", state_dir=state_dir)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "composite" in data
        assert "dimensions" in data


# -- Reset Tests ------------------------------------------------------------

class TestCLIReset:

    def test_reset(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("reset", state_dir=state_dir)
        assert result.returncode == 0
        assert "reset" in result.stdout.lower()

    def test_reset_then_status_fails(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        run_cli("reset", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir, expect_error=True)
        assert result.returncode != 0


# -- Persistence Tests ------------------------------------------------------

class TestCLIPersistence:

    def test_state_persists_across_calls(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        run_cli("advance", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir)
        assert "Month 2" in result.stdout

    def test_state_file_created(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        state_file = os.path.join(state_dir, "re2_state.json")
        assert os.path.exists(state_file)

    def test_state_file_valid_json(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        state_file = os.path.join(state_dir, "re2_state.json")
        with open(state_file) as f:
            data = json.load(f)
        assert "seed" in data
        assert data["seed"] == 42

    def test_actions_persist(self, state_dir):
        run_cli("start", "--seed", "42", state_dir=state_dir)
        run_cli("buy", "prop_elm_warehouse", state_dir=state_dir)
        result = run_cli("properties", state_dir=state_dir)
        assert "Elm" in result.stdout


# -- Hard Rules CLI Tests ---------------------------------------------------

class TestCLIHardRules:

    def test_cosmetic_repair_blocked(self, state_dir):
        run_cli("start", "--seed", "42", "--variant", "hard_rules",
               state_dir=state_dir)
        result = run_cli("repair", "prop_maple_apts", "cosmetic",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "RULE" in result.stdout or "blocked" in result.stdout.lower()

    def test_lobby_zoning_blocked(self, state_dir):
        run_cli("start", "--seed", "42", "--variant", "hard_rules",
               state_dir=state_dir)
        result = run_cli("lobby-zoning", "low_income", "commercial",
                        state_dir=state_dir)
        assert result.returncode == 0
        assert "RULE" in result.stdout or "blocked" in result.stdout.lower()
