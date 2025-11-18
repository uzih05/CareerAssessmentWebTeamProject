-- 전주대학교 전공 유형 검사 데이터베이스 스키마
-- SQLite3 사용

-- 질문 테이블
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    aptitude_type VARCHAR(50) NOT NULL,  -- 측정하는 적성 (언어능력, 논리/분석력 등)
    is_reverse BOOLEAN DEFAULT FALSE,    -- 역채점 여부 (True면 5→1, 4→2 등)
    question_order INTEGER NOT NULL,     -- 질문 순서 (1-20)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 적성 타입 인덱스 (검색 최적화)
CREATE INDEX IF NOT EXISTS idx_questions_aptitude ON questions(aptitude_type);

-- 학과 테이블
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    aptitude_scores TEXT NOT NULL,       -- JSON 문자열: "[7,8,6,9,5,4,7,8,6,7]"
    description TEXT,                    -- 학과 설명
    url TEXT,                            -- 학과 홈페이지 URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 학과명 인덱스 (검색 최적화)
CREATE INDEX IF NOT EXISTS idx_departments_name ON departments(name);

-- 결과 저장 테이블 (공유 기능용)
CREATE TABLE IF NOT EXISTS test_results (
    id VARCHAR(20) PRIMARY KEY,          -- 짧은 공유 ID (예: "a1b2c3d4")
    user_answers TEXT NOT NULL,          -- JSON 문자열: "[5,4,3,5,2,4,...]" (20개)
    user_scores TEXT NOT NULL,           -- JSON 문자열: "[7,8,6,9,...]" (10개 적성 점수)
    top_departments TEXT NOT NULL,       -- JSON 문자열: 상위 3개 학과 정보
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP                 -- 만료 시간 (선택)
);

-- 생성일 인덱스 (만료된 결과 정리용)
CREATE INDEX IF NOT EXISTS idx_results_created ON test_results(created_at);

-- 10가지 적성 리스트 (참고용 주석)
/*
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
*/