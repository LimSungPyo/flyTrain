"""미니게임 플러그인 인터페이스.

새 종목은 MiniGame을 구현해 games/ 아래에 추가한다.
서버가 시드를 고정해 라운드를 끝까지 돌리고, 그 기록(리플레이)을 프론트가 재생한다.
"""

from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from brain.engine import Action, SensoryInput


@dataclass
class ReplayEvent:
    """프론트가 그릴 한 순간. 해설(Claude)도 이 기록을 보고 만든다."""

    tick: int
    side: str  # "a" | "b"
    kind: str  # 예: "punch", "dodge", "choose", "slap_bell"
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class RoundResult:
    winner: str | None  # "a" | "b" | None(무승부)
    score_a: float
    score_b: float
    replay: list[ReplayEvent]


class MiniGame(Protocol):
    key: str  # 예: "rps", "kickbox", "bell"
    rounds: int  # 기본 5

    def new_round(self, rng: np.random.Generator) -> Any:
        """라운드 상태를 새로 만든다."""
        ...

    def observe(self, state: Any, side: str) -> SensoryInput:
        """한쪽 초파리가 지금 느끼는 감각 입력."""
        ...

    def step(self, state: Any, action_a: Action, action_b: Action) -> Any:
        """두 초파리의 행동을 반영해 상태를 한 틱 진행한다."""
        ...

    def is_over(self, state: Any) -> bool: ...

    def result(self, state: Any) -> RoundResult: ...
