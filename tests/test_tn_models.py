"""Tests for trade_negotiation.models -- to_dict/from_dict roundtrips."""

import pytest
from simulations.trade_negotiation.models import (
    TradePartner,
    TradeIssue,
    TradeDeal,
    NegotiationState,
)


class TestTradePartnerRoundtrip:
    def test_default_roundtrip(self):
        p = TradePartner(id="p1", name="TestLand",
                         economy_size="medium",
                         development_level="emerging",
                         leverage=55.0)
        d = p.to_dict()
        p2 = TradePartner.from_dict(d)
        assert p2.id == p.id
        assert p2.name == p.name
        assert p2.economy_size == p.economy_size
        assert p2.leverage == p.leverage
        assert p2.to_dict() == d

    def test_full_roundtrip(self):
        p = TradePartner(
            id="p2", name="FullLand",
            economy_size="large", development_level="developed",
            leverage=85.0, priority_issues=["ip", "tech"],
            trust_level=72.0, deals_completed=["deal_001"],
            vulnerability=15.0,
        )
        d = p.to_dict()
        p2 = TradePartner.from_dict(d)
        assert p2.trust_level == 72.0
        assert p2.deals_completed == ["deal_001"]
        assert p2.to_dict() == d


class TestTradeIssueRoundtrip:
    def test_default_roundtrip(self):
        i = TradeIssue(name="tariff_p1", type="tariff")
        d = i.to_dict()
        i2 = TradeIssue.from_dict(d)
        assert i2.name == i.name
        assert i2.type == i.type
        assert i2.to_dict() == d

    def test_full_roundtrip(self):
        i = TradeIssue(
            name="ip_p2", type="ip",
            your_position=70.0, partner_position=40.0,
            importance_to_you=80.0, importance_to_partner=60.0,
        )
        d = i.to_dict()
        i2 = TradeIssue.from_dict(d)
        assert i2.your_position == 70.0
        assert i2.partner_position == 40.0
        assert i2.to_dict() == d


class TestTradeDealRoundtrip:
    def test_default_roundtrip(self):
        deal = TradeDeal(id="deal_001", partner_id="p1")
        d = deal.to_dict()
        deal2 = TradeDeal.from_dict(d)
        assert deal2.id == "deal_001"
        assert deal2.partner_id == "p1"
        assert deal2.to_dict() == d

    def test_full_roundtrip(self):
        deal = TradeDeal(
            id="deal_002", partner_id="p2",
            round_agreed=5,
            issues={"tariff_p2": 60.0, "ip_p2": 45.0},
            your_benefit=25.5, partner_benefit=18.3,
            terms=["tariff=60", "ip=45"],
            implemented=True,
            reneged_items=["ip_p2"],
        )
        d = deal.to_dict()
        deal2 = TradeDeal.from_dict(d)
        assert deal2.round_agreed == 5
        assert deal2.issues == {"tariff_p2": 60.0, "ip_p2": 45.0}
        assert deal2.implemented is True
        assert deal2.reneged_items == ["ip_p2"]
        assert deal2.to_dict() == d


class TestNegotiationStateRoundtrip:
    def test_default_roundtrip(self):
        ns = NegotiationState(round=3, reputation=65.0)
        d = ns.to_dict()
        ns2 = NegotiationState.from_dict(d)
        assert ns2.round == 3
        assert ns2.reputation == 65.0
        assert ns2.to_dict() == d

    def test_with_partners_roundtrip(self):
        partner = TradePartner(
            id="p1", name="TestLand",
            economy_size="small", development_level="developing",
            leverage=30.0,
        )
        deal = TradeDeal(id="deal_001", partner_id="p1", round_agreed=2)
        ns = NegotiationState(
            round=5,
            partners={"p1": partner},
            active_negotiations=["p1"],
            completed_deals=[deal],
            your_portfolio_value=100.0,
            reputation=70.0,
            total_deal_value=200.0,
            promises_made=["tariff_cut"],
            promises_kept=["tariff_cut"],
        )
        d = ns.to_dict()
        ns2 = NegotiationState.from_dict(d)
        assert ns2.round == 5
        assert "p1" in ns2.partners
        assert ns2.partners["p1"].name == "TestLand"
        assert len(ns2.completed_deals) == 1
        assert ns2.completed_deals[0].id == "deal_001"
        assert ns2.promises_made == ["tariff_cut"]
        assert ns2.promises_kept == ["tariff_cut"]
