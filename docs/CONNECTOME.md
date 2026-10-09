# 커넥톰 데이터 준비

## 1. 내려받기

FlyWire Codex(https://codex.flywire.ai)의 다운로드는 로그인한 브라우저에서만 되고, 터미널로는 받을 수 없다(로그인 페이지 HTML이 내려온다). 그래서 **로그인 없이 받을 수 있는 v783 공개 사본**을 쓴다.

```bash
cd data/raw
curl -fL -O https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/Connectivity_783.parquet
curl -fL -O https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/Completeness_783.csv
curl -fL -O https://raw.githubusercontent.com/flyconnectome/flywire_annotations/main/supplemental_files/Supplemental_file1_neuron_annotations.tsv
```

| 파일 | 크기 | 내용 | 출처 |
|---|---|---|---|
| `Connectivity_783.parquet` | 약 100MB | 뉴런 쌍 약 1,509만 개. 시냅스 수(`Connectivity`), 흥분 +1 / 억제 −1(`Excitatory`), 둘의 곱. `Presynaptic_Index`·`Postsynaptic_Index`는 아래 뉴런 목록의 순서다 | Shiu et al. 2024 GitHub (MIT) |
| `Completeness_783.csv` | 약 3MB | 시뮬레이션 뉴런 목록 138,639개(root_id). 이 순서가 행렬 인덱스다 | Shiu et al. 2024 GitHub (MIT) |
| `Supplemental_file1_neuron_annotations.tsv` | 약 32MB | 뉴런 139,248개의 `super_class`, `cell_class`, `cell_type`, 신경전달물질 예측(`top_nt`), 좌우(`side`) | Schlegel et al. 2024 GitHub |

- 확인: `cd back_end && .venv/bin/python -m connectome.check_raw`
- 두 출처의 root_id는 같은 v783이다. 뉴런 목록의 99.99%가 주석 파일과 맞물린다(2026-10-10 확인).
- 더 자세한 원본이 필요하면 Zenodo의 `proofread_connections_783.feather`(약 850MB, CC BY 4.0, record 10676866)를 쓴다. 지금은 필요 없다.

### 확인된 주요 세포 수 (주석 파일 기준)

| 구분 | 수 | 쓰는 곳 |
|---|---|---|
| Kenyon cell (`cell_class == Kenyon_Cell`) | 5,177 | 버섯체 학습 |
| MBON | 96 | 행동 선택 출력 |
| DAN (PAM·PPL1 등) | 331 | 보상·벌 신호 |
| ALPN (후각 투사 뉴런) | 685 | 게임 상황 입력("냄새") |
| `LPLC2` | 210 | 반응속도 (시각 탈출) |
| `DNp01` (자이언트 파이버) | 2 | 반응속도 출력 |

## 2. 참고 모델

Shiu et al.(2024)의 전뇌 LIF 모델 코드(GitHub `philshiu/Drosophila_brain_model`)가 우리 엔진의 기준이다. 위 연결 파일이 바로 그 모델의 입력이므로, 같은 자극을 주면 같은 결과가 나오는지 비교할 수 있다. 코드는 이 저장소에 넣지 않는다.

## 3. 라이선스와 출처 표기

- Shiu 모델 저장소: MIT License (Copyright (c) 2023 Philip Shiu and Nico Spiller)
- FlyWire 커넥톰 데이터: CC BY 4.0 (Zenodo record 10676866 기준). 출처 표기가 필수다.
- `flywire_annotations` 저장소에는 LICENSE 파일이 없다. 논문(Schlegel et al. 2024)과 FlyWire 인용 가이드에 따라 출처를 표기한다. 공개 배포 전에 FlyWire(flywire@princeton.edu)의 인용 가이드를 다시 확인한다.
- 원본은 저장소에 커밋하지 않는다(용량, 재배포 조건).
- 게임 안 크레딧 화면과 README에 FlyWire 컨소시엄과 논문을 출처로 표기한다.

## 4. 전처리 (Phase 0에서 작성)

`back_end/connectome/`에 아래 스크립트를 만든다.

- `check_raw.py` — 원본 파일 확인 (있음)
- `extract.py` — 세포 유형 기준으로 하위 회로(BRAIN.md §2)를 추출해 `data/processed/<회로>.npz` + 메타데이터 저장 (예정)
