"""
FastAPI Main Application - 전주대학교 전공 유형 검사 백엔드
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from routers import questions_router, results_router
from database.connection import init_database

# FastAPI 앱 생성
app = FastAPI(
    title="전주대학교 전공 유형 검사 API",
    description="20개 질문 기반 적성 분석 및 70개 학과 매칭 시스템",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정 (프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 시작 이벤트: DB 초기화
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 DB 연결 및 초기화"""
    print("=" * 50)
    print("🚀 전주대학교 전공 유형 검사 API 시작")
    print("=" * 50)

    try:
        # DB 연결 (테이블이 없으면 생성)
        db = init_database("major_test.db", reset=False)

        # 데이터 확인
        question_count = db.get_table_count("questions")
        dept_count = db.get_table_count("departments")
        result_count = db.get_table_count("test_results")

        print(f"✅ 데이터베이스 연결 완료")
        print(f"📝 질문: {question_count}개")
        print(f"🏫 학과: {dept_count}개")
        print(f"📊 저장된 결과: {result_count}개")

        if question_count == 0 or dept_count == 0:
            print("\n⚠️  경고: 데이터가 없습니다!")
            print("➡️  다음 명령어를 실행하세요:")
            print("    python -m database.seed")

        print("=" * 50)
        print("📚 API 문서: http://localhost:8000/docs")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 초기화 오류: {e}")


# 종료 이벤트: DB 연결 종료
@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 DB 연결 정리"""
    from database.connection import get_db

    try:
        db = get_db()
        db.close()
        print("\n✅ 데이터베이스 연결 종료")
    except Exception as e:
        print(f"\n❌ 종료 오류: {e}")


# 라우터 등록
app.include_router(questions_router)
app.include_router(results_router)


# 루트 엔드포인트
@app.get("/")
async def root():
    """API 루트 - 상태 확인"""
    return {
        "message": "전주대학교 전공 유형 검사 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "questions": "/api/questions",
            "results": "/api/results"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    from database.connection import get_db

    try:
        db = get_db()
        question_count = db.get_table_count("questions")
        dept_count = db.get_table_count("departments")

        return {
            "status": "healthy",
            "database": "connected",
            "data": {
                "questions": question_count,
                "departments": dept_count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# 개발 모드 실행
if __name__ == "__main__":
    import uvicorn

    print("\n🔧 개발 모드로 실행 중...")
    print("🌐 서버 주소: http://localhost:8000")
    print("📚 API 문서: http://localhost:8000/docs\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 코드 변경 시 자동 재시작
        log_level="info"
    )