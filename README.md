# flyTrain 🪰

**진짜 초파리 뇌지도로 만든 내 초파리를 키워서, 남의 초파리를 이기는 예능 RPG.**

초파리 성체 뇌의 뉴런 약 14만 개를 전부 이은 [FlyWire 커넥톰](https://flywire.ai)으로 초파리의 뇌를 시뮬레이션합니다.
플레이어는 트레이너입니다. 초파리를 만들어 스탯을 찍어 주고, 경기를 지켜보며 잔소리를 할 수 있습니다.
초파리는 진짜 학습 회로인 버섯체로 상대의 버릇을 배웁니다. 가끔은 끝까지 못 배우기도 합니다.

> 🚧 개발 초기 단계입니다. 진행 상황은 [로드맵](docs/ROADMAP.md)에서 볼 수 있습니다.

## 어떻게 노나요

1. **초파리 만들기**: 힘·민첩·반응속도·지능·지구력·운에 20포인트를 나눠 찍고, 콧수염과 선글라스를 달아 줍니다.
2. **도전하기**: 랭크전으로 비슷한 실력의 초파리와 매칭되거나, 마음에 안 드는 초파리를 골라 직접 도전합니다.
3. **5라운드 경기**: 가위바위보, 킥복싱, 과일 종 치기 중 하나를 고릅니다. 라운드가 끝날 때마다 받는 5포인트로 그 경기 동안만 쓸 수 있는 스탯을 올립니다.
4. **성장**: 경기에서 배운 것의 일부가 뇌에 영구히 남습니다. 많이 싸운 초파리일수록 정말로 경험 많은 뇌가 됩니다.

## 구조

```
flyTrain/
├─ front_end/   # Next.js (App Router) + TypeScript + Tailwind
├─ back_end/    # FastAPI — 웹 API + 뇌 엔진(brain/) + 미니게임(games/) + 커넥톰 전처리(connectome/)
├─ data/        # 커넥톰 원본·전처리 결과 (git 제외)
└─ docs/        # 설계 문서
```

| 문서 | 내용 |
|---|---|
| [GAME_DESIGN](docs/GAME_DESIGN.md) | 게임 규칙, 스탯, 미니게임, 대전 방식, 예능 장치 |
| [BRAIN](docs/BRAIN.md) | 커넥톰을 판단·학습에 쓰는 방법 |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | 시스템 구성, 경기 흐름, 데이터 모델 |
| [CONNECTOME](docs/CONNECTOME.md) | 커넥톰 데이터 받는 법, 라이선스 |
| [ROADMAP](docs/ROADMAP.md) | 개발 단계 |

## 기술 스택

- **프론트엔드**: Next.js 16, React 19, TypeScript, Tailwind CSS 4, PixiJS(예정)
- **백엔드**: Python 3.12, FastAPI, numpy / scipy(희소 행렬 LIF 시뮬레이션)
- **DB**: PostgreSQL (Supabase)
- **AI**: Claude API (경기 중계, 이름 짓기, 코칭 해석. 승패에는 관여하지 않습니다)

## 로컬 실행

```bash
# 백엔드 (http://localhost:8100)
cd back_end
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/python -m uvicorn app.main:app --reload --port 8100

# 프론트엔드 (http://localhost:3100)
cd front_end
npm install
cp .env.example .env.local
npm run dev
```

커넥톰 데이터 준비는 [docs/CONNECTOME.md](docs/CONNECTOME.md)를 참고하세요.

### 검사

```bash
cd back_end && .venv/bin/ruff format --check . && .venv/bin/ruff check . && .venv/bin/pytest
cd front_end && npm run format:check && npm run lint && npm run test && npm run build
```

## 크레딧

- 커넥톰 데이터: FlyWire Consortium — Dorkenwald et al. (2024), Schlegel et al. (2024), *Nature*
- 뇌 모델 참고: Shiu et al. (2024), *Nature*

데이터는 각 출처의 라이선스를 따릅니다.
