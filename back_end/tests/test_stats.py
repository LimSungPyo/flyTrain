import pytest

from brain.stats import CREATION_POINTS, STAT_CAP, StatBlock, validate_creation


def test_creation_requires_all_points_spent():
    validate_creation(StatBlock(strength=10, luck=10))
    with pytest.raises(ValueError):
        validate_creation(StatBlock(strength=CREATION_POINTS - 1))


def test_level_bonus_raises_budget():
    validate_creation(StatBlock(strength=12, intelligence=10), bonus_points=2)


def test_stat_cap():
    with pytest.raises(ValueError):
        StatBlock(strength=STAT_CAP + 1)


def test_round_points_add_up():
    base = StatBlock(strength=10, reflex=10)
    assert base.plus(StatBlock(strength=5)).strength == 15
