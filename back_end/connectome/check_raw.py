"""data/raw에 커넥톰 원본 파일이 있는지 확인한다.

실행: python -m connectome.check_raw
내려받는 방법은 docs/CONNECTOME.md 참고.
"""

import sys
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

# FlyWire v783 기준 파일. 출처는 docs/CONNECTOME.md. 이름이 바뀌면 여기만 고친다.
REQUIRED = [
    "Connectivity_783.parquet",  # 연결 + 흥분/억제 부호 (Shiu et al. 2024)
    "Completeness_783.csv",  # 시뮬레이션에 쓰는 뉴런 목록과 순서 (Shiu et al. 2024)
    "Supplemental_file1_neuron_annotations.tsv",  # 세포 유형·분류 (Schlegel et al. 2024)
]


def main() -> int:
    missing = [name for name in REQUIRED if not (RAW_DIR / name).exists()]
    if missing:
        print(f"[없음] {RAW_DIR} 에 다음 파일이 필요하다:")
        for name in missing:
            print(f"  - {name}")
        return 1
    print("[확인] 커넥톰 원본 파일이 모두 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
