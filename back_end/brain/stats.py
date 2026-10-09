"""초파리 스탯 정의와 배분 규칙.

스탯마다 실제로 손대는 뇌 회로가 정해져 있다(docs/BRAIN.md 참고).
수치는 아직 임시값이며, 밸런스는 Phase 1에서 다시 잡는다.
"""

from enum import StrEnum

from pydantic import BaseModel, model_validator


class Stat(StrEnum):
    STRENGTH = "strength"  # 힘 — 운동 하강뉴런 출력 증폭
    AGILITY = "agility"  # 민첩 — 보행·비행 회로
    REFLEX = "reflex"  # 반응속도 — 시각 탈출 회로(LPLC2·자이언트 파이버)
    INTELLIGENCE = "intelligence"  # 지능 — 버섯체 학습률
    STAMINA = "stamina"  # 지구력 — 뉴런 피로·적응
    LUCK = "luck"  # 운 — 시뮬레이션 노이즈


CREATION_POINTS = 20  # 초파리를 처음 만들 때 주는 포인트
ROUND_POINTS = 5  # 라운드가 끝날 때마다 주는 포인트 (그 경기에서만 유효)
STAT_CAP = 30  # 한 스탯에 넣을 수 있는 최대치 (경기 중 포인트 포함)


class StatBlock(BaseModel):
    strength: int = 0
    agility: int = 0
    reflex: int = 0
    intelligence: int = 0
    stamina: int = 0
    luck: int = 0

    @model_validator(mode="after")
    def _check_range(self) -> "StatBlock":
        for stat in Stat:
            value = getattr(self, stat.value)
            if not 0 <= value <= STAT_CAP:
                raise ValueError(f"{stat.value}는 0~{STAT_CAP} 사이여야 한다: {value}")
        return self

    def total(self) -> int:
        return sum(getattr(self, stat.value) for stat in Stat)

    def plus(self, other: "StatBlock") -> "StatBlock":
        return StatBlock(
            **{s.value: getattr(self, s.value) + getattr(other, s.value) for s in Stat}
        )


def validate_creation(stats: StatBlock, bonus_points: int = 0) -> None:
    """생성 포인트(+레벨 보너스)를 정확히 다 썼는지 확인한다."""
    budget = CREATION_POINTS + bonus_points
    if stats.total() != budget:
        raise ValueError(
            f"포인트를 {budget}개 모두 배분해야 한다: {stats.total()}개 사용"
        )
