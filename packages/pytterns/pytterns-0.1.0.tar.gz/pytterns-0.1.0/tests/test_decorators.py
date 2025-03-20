import pytest
from pytterns.core.decorators import strategy, STRATEGIES, chain, CHAINS

def test_strategy_decorator():
    @strategy("test_group")
    class TestStrategy:
        def check(self, value):
            return value == "test"

    assert "test_group" in STRATEGIES
    assert len(STRATEGIES["test_group"]) == 1
    assert STRATEGIES["test_group"][0].check("test") is True

def test_chain_decorator():
    @chain("test_group", 1)
    class TestChain:
        def handle(self, value):
            return value

    assert "test_group" in CHAINS
    assert len(CHAINS["test_group"]) == 1
    assert CHAINS["test_group"][0][0] == 1
    assert CHAINS["test_group"][0][1].handle("test") == "test"