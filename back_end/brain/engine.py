"""뇌 엔진 인터페이스.

미니게임은 뇌 내부를 모른다. 감각 입력을 넣고 행동을 돌려받을 뿐이다.
처음에는 가짜 뇌(규칙 기반)로 게임을 만들고, 나중에 커넥톰 LIF 뇌로 바꿔 끼운다.
"""

from dataclasses import dataclass, field
from typing import Protocol

import numpy as np

from brain.stats import StatBlock


@dataclass
class SensoryInput:
    """어떤 감각 뉴런 그룹을 얼마나 세게 자극할지. 키는 뉴런 그룹 이름."""

    stimuli: dict[str, float] = field(default_factory=dict)


@dataclass
class Action:
    """뇌가 고른 행동과, 연출용으로 쓸 뉴런 활동 요약."""

    name: str
    confidence: float = 0.0
    activity: dict[str, float] = field(default_factory=dict)


class Brain(Protocol):
    def decide(
        self, sensory: SensoryInput, stats: StatBlock, rng: np.random.Generator
    ) -> Action:
        """감각 입력을 받아 행동을 고른다. 무작위는 반드시 rng로만 쓴다(재현성)."""
        ...

    def reward(self, signal: float) -> None:
        """보상(+)·벌(-)을 도파민 뉴런 자극으로 바꿔 버섯체 연결을 바꾼다."""
        ...
