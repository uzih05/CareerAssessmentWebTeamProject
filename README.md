# 전주대학교 전공 유형 검사

20개 질문 기반 적성 분석 및 70개 학과 매칭 시스템

## 프로젝트 구조

```
CareerAssessmentWebTeamProject/
├── jj_departments_with_scores.json    # 학과 데이터 (필수)
├── backend/                            # FastAPI 백엔드
│   ├── main.py                        # 서버 엔트리포인트
│   ├── database/                      # DB 관리
│   ├── models/                        # 데이터 모델
│   ├── routers/                       # API 라우터
│   └── utils/                         # 유틸리티
└── frontend/                          # SPA 프론트엔드
    ├── index.html                     # 메인 페이지
    ├── pages/                         # 검사/결과 페이지
    ├── css/                           # 스타일시트
    └── js/                            # JavaScript
```

## 빠른 시작

### 1. 의존성 설치
```bash
pip install fastapi uvicorn --break-system-packages
```

### 2. DB 초기화
```bash
cd backend
python -m database.seed
```

### 3. 백엔드 실행
```bash
python main.py
```

### 4. 프론트엔드 실행 (다른 터미널)
```bash
cd ../frontend
python -m http.server 3000
```

### 5. 브라우저 접속
- 메인: http://localhost:3000
- API 문서: http://localhost:8000/docs

## 주요 기능

### 백엔드
- FastAPI 기반 RESTful API
- SQLite 데이터베이스 (질문 20개, 학과 70개)
- 유클리드 거리 기반 학과 매칭 알고리즘
- 점수 계산 및 성향 분석
- 결과 공유 기능

### 프론트엔드
- Vanilla JavaScript SPA
- Chart.js 레이더 차트
- Glassmorphism UI 디자인
- 반응형 레이아웃
- 키보드 네비게이션

## API 엔드포인트

### 질문
- `GET /api/questions` - 전체 질문 조회
- `GET /api/questions/{id}` - 개별 질문 조회

### 결과
- `POST /api/results` - 검사 제출
- `GET /api/results/{id}` - 결과 조회
- `DELETE /api/results/{id}` - 결과 삭제

## 데이터 구조

### 적성 타입 (10개)
1. 언어능력
2. 논리/분석력
3. 창의력
4. 사회성/공감능력
5. 주도성/리더십
6. 신체-활동성
7. 예술감각/공간지각
8. 체계성/꼼꼼함
9. 탐구심
10. 문제해결능력

### 질문 구조
- 총 20문항 (적성당 2문항)
- 리커트 5점 척도 (1: 전혀 그렇지 않다 ~ 5: 매우 그렇다)
- 역채점 문항 포함

### 학과 데이터
- 70개 학과
- 각 학과당 10개 적성 점수 (1-10점)
- 자동 생성 태그 및 계열 분류

## 알고리즘

### 점수 계산
```python
# 역채점 처리
score = 6 - answer if is_reverse else answer

# 적성별 평균
aptitude_score = sum(scores) / 2  # 적성당 2문항
```

### 학과 매칭
```python
# 유클리드 거리
distance = sqrt(sum((user - dept)^2))

# 일치율 (0-100%)
match_rate = (1 - distance / max_distance) * 100
```

## 문제 해결

### 백엔드 서버 실행 실패
```bash
# 포트 충돌
lsof -i :8000
kill -9 <PID>
```

### 데이터 없음
```bash
cd backend
python -m database.seed
```

### CORS 에러
- `main.py`에서 CORS 설정 확인
- 백엔드 서버 실행 중인지 확인

### JSON 파일 경로
- `jj_departments_with_scores.json`이 프로젝트 루트에 있는지 확인

## 기술 스택

### 백엔드
- Python 3.8+
- FastAPI
- SQLite3
- Pydantic

### 프론트엔드
- HTML5 / CSS3
- Vanilla JavaScript (ES6+)
- Chart.js 4.4.0

## 브라우저 지원
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 개발 팀
- 강민석
- 유지헌
- 조현우

## 라이선스
전주대학교 전공 유형 검사 프로젝트

---

**제작**: 2025년  
**학교**: 전주대학교