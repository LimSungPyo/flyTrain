# 아키텍처

> 상태: 초안 (2026-10-09)

## 1. 시스템

```
[Vercel] Next.js (front_end)  ──REST──▶  [Render/Fly] FastAPI (back_end)  ──▶  [Supabase] PostgreSQL
  · 로비·랭킹·프로필                       · 인증, 매칭, 레이팅(Glicko-2)          · 유저·초파리·경기·라운드
  · 초파리 생성·커스텀                      · 경기 진행 (라운드 단위)                · 레이팅 기록
  · 리플레이 재생 (PixiJS 예정)              · 뇌 엔진 + 미니게임 시뮬레이션
                                            │
                                            ├──▶ [Supabase Storage] 초파리별 뇌 가중치 변화량
                                            ├──▶ data/processed  커넥톰 하위 회로 (서버 이미지에 포함)
                                            └──▶ [Claude API] 중계·이름 짓기·코칭 해석
```

- 백엔드는 하나의 FastAPI 앱이다. 시뮬레이션이 무거워지면 `brain/`·`games/`를 별도 워커(큐)로 떼어 낸다. 그래서 이 둘은 처음부터 `app/`(웹 계층)에 의존하지 않게 만든다.

## 2. 경기 흐름 (서버 권위 · 비동기)

```
POST /matches                  매칭(랭크전) 또는 직접 도전 → 양쪽 초파리 스냅샷 + 시드 저장
POST /matches/{id}/rounds      서버가 라운드 1개 시뮬레이션 → 리플레이 반환
  (프론트: 리플레이 재생 → 포인트 5개 배분 + 코칭 입력)
POST /matches/{id}/allocate    배분 저장 (상대는 자동 배분 성향으로 배분)
  … 5라운드 반복 …
POST /matches/{id}/finish      레이팅·경험치·기억 고정 반영
```

- 라운드 시드는 `경기 시드 + 라운드 번호`로 만든다. 같은 입력이면 같은 리플레이다.
- 리플레이는 `ReplayEvent` 목록이다(`back_end/games/base.py`). 프론트는 이것만 보고 그린다.
- 중계(Claude)는 리플레이를 받은 뒤 비동기로 만들고, 실패해도 경기는 진행된다.

## 3. 데이터 모델 (초안)

| 테이블 | 주요 컬럼 |
|---|---|
| `users` | id(UUID), email, nickname |
| `flies` | id, owner_id, name, bio, base_stats(JSON), appearance(JSON), auto_alloc_style, level, xp, brain_ref(Storage 경로), rating, rd, volatility |
| `matches` | id, game_key, fly_a_id, fly_b_id, fly_a_snapshot, fly_b_snapshot, seed, kind(ranked/challenge), status, winner |
| `rounds` | match_id, no, alloc_a, alloc_b, coaching_a, result, replay(JSON), commentary |
| `rating_history` | fly_id, match_id, before, after |

## 4. 디렉터리

```
flyTrain/
├─ front_end/            Next.js (App Router) + TypeScript + Tailwind
│  └─ src/
│     ├─ app/            화면 (로비, 생성, 경기, 랭킹, 프로필)
│     ├─ components/     공용 UI
│     ├─ game/           리플레이 렌더러 (PixiJS 예정)
│     ├─ lib/            API 클라이언트
│     └─ types/          백엔드와 맞춘 타입
├─ back_end/             FastAPI
│  ├─ app/               웹 계층 (라우터, 설정, DB)
│  ├─ brain/             뇌 엔진 — 스탯, LIF, 버섯체 학습 (웹 계층 의존 금지)
│  ├─ games/             미니게임 플러그인 (웹 계층 의존 금지)
│  ├─ connectome/        커넥톰 원본 → 하위 회로 전처리 스크립트
│  └─ tests/
├─ data/                 커넥톰 원본·전처리 결과 (git 제외)
└─ docs/                 설계 문서
```

## 5. 의존 방향

```
app/  ──▶  games/  ──▶  brain/
  └──────────────────────▲
connectome/ ──▶ data/processed ──▶ brain/ (로드)
```

`brain/`은 아무것도 모르고, `games/`는 `brain/`의 인터페이스만 안다.
