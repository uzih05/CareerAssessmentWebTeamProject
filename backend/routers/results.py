"""
Results Router - 검사 결과 처리 API
✅ tags와 category를 DB에서 직접 읽기 (완벽한 버전)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict, Optional
import json
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import get_db
from models.question import Question, QuestionSet, APTITUDE_NAMES
from models.department import Department, DepartmentMatcher
from models.result import TestResult, ResultSummary, create_test_result
from utils.id_generator import generate_result_id, is_valid_id

router = APIRouter(
    prefix="/api/results",
    tags=["results"]
)


# Request/Response 모델
class TestSubmission(BaseModel):
    """검사 제출 요청"""
    answers: List[int]

    @validator('answers')
    def validate_answers(cls, v):
        if len(v) != 20:
            raise ValueError("답변은 정확히 20개여야 합니다")

        for i, answer in enumerate(v):
            if not 1 <= answer <= 5:
                raise ValueError(f"답변 {i + 1}번: 1-5 사이의 값이어야 합니다 (입력: {answer})")

        return v


class DepartmentInfo(BaseModel):
    """학과 정보"""
    id: int
    name: str


class MatchedDepartment(BaseModel):
    """매칭된 학과"""
    department: DepartmentInfo
    match_percentage: float
    reason: str
    mismatch_reason: Optional[str] = None


class TestResultResponse(BaseModel):
    """검사 결과 응답"""
    id: str
    url: str
    scores: List[float]
    interest_tags: List[str]
    personality: str
    summary: Dict[str, str]
    top_departments: List[Dict]
    worst_departments: List[Dict]
    similar_departments: List[Dict]
    created_at: str


# 헬퍼 함수
def load_questions_from_db() -> List[Question]:
    """데이터베이스에서 질문 로드 (✅ tags 포함)"""
    db = get_db()

    query = """
            SELECT id, question_text, aptitude_type, is_reverse, question_order, tags
            FROM questions
            ORDER BY question_order ASC
            """

    rows = db.fetchall(query)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="질문 데이터가 없습니다"
        )

    questions = []
    for row in rows:
        # ✅ DB에서 tags 읽기
        tags = []
        if row["tags"]:
            try:
                tags = json.loads(row["tags"])
            except (json.JSONDecodeError, TypeError):
                tags = []

        questions.append(Question(
            id=row["id"],
            question_text=row["question_text"],
            aptitude_type=row["aptitude_type"],
            is_reverse=bool(row["is_reverse"]),
            tags=tags  # ✅ DB에서 가져온 tags
        ))

    return questions


def load_departments_from_db() -> List[Department]:
    """
    데이터베이스에서 학과 로드
    ✅ tags와 category를 DB에서 직접 읽기 (완벽한 버전)
    """
    db = get_db()

    query = """
            SELECT id, name, aptitude_scores, description, url, tags, category
            FROM departments
            """

    rows = db.fetchall(query)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="학과 데이터가 없습니다"
        )

    departments = []
    for row in rows:
        try:
            # JSON 파싱
            scores = json.loads(row["aptitude_scores"])
            desc_list = json.loads(row["description"]) if row["description"] else []

            # ✅ DB에서 tags와 category 직접 읽기 (None 체크 강화)
            tags = []
            if row["tags"]:
                try:
                    tags = json.loads(row["tags"])
                except (json.JSONDecodeError, TypeError):
                    tags = []

            category = row["category"] if row["category"] else "기타"

            departments.append(Department(
                id=row["id"],
                name=row["name"],
                aptitude_scores=scores,
                description=" / ".join(desc_list) if desc_list else "",
                url=row["url"] or "",
                tags=tags,  # ✅ DB에서 가져온 값
                category=category  # ✅ DB에서 가져온 값
            ))
        except Exception as e:
            print(f"⚠️ 학과 '{row['name']}' 로드 중 오류: {e}")
            continue

    return departments


def save_result_to_db(result: TestResult) -> bool:
    """결과를 DB에 저장"""
    try:
        db = get_db()

        query = """
                INSERT INTO test_results
                    (id, user_answers, user_scores, top_departments, created_at)
                VALUES (?, ?, ?, ?, ?)
                """

        db.execute(query, (
            result.id,
            json.dumps(result.user_answers),
            json.dumps(result.user_scores),
            json.dumps(result.top_departments, ensure_ascii=False),
            result.created_at
        ))

        return True

    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")
        return False


# API 엔드포인트
@router.post("", response_model=TestResultResponse)
async def submit_test(submission: TestSubmission):
    """
    검사 제출 및 결과 생성

    Args:
        submission: 20개 답변 (1-5)

    Returns:
        검사 결과 (ID, 점수, 추천 학과 등)
    """
    try:
        # 1. 질문 로드
        questions = load_questions_from_db()
        question_set = QuestionSet(questions)

        # 2. 점수 계산
        score_result = question_set.calculate_score(submission.answers)
        user_scores = score_result["aptitude_scores"]
        interest_tags = score_result["interest_tags"]

        # 3. 성향 분석
        personality = question_set.analyze_personality(user_scores)

        # 4. 학과 로드 및 매칭
        departments = load_departments_from_db()
        matcher = DepartmentMatcher(departments)

        match_result = matcher.match_departments(
            user_scores=user_scores,
            user_tags=interest_tags,
            top_n=3,
            worst_n=3
        )

        # 5. 결과 ID 생성
        result_id = generate_result_id()

        # 6. 결과 객체 생성
        def format_department_match(match: Dict) -> Dict:
            """매칭 결과를 직렬화 가능한 형태로 변환"""
            dept = match["department"]
            return {
                "department": {
                    "id": dept.id,
                    "name": dept.name,
                    "url": dept.url,
                    "description": dept.description
                },
                "match_percentage": match["match_percentage"],
                "reason": match["reason"],
                "mismatch_reason": match.get("mismatch_reason")
            }

        top_depts = [format_department_match(m) for m in match_result["top"]]
        worst_depts = [format_department_match(m) for m in match_result["worst"]]

        # ✅ similar는 다른 구조라서 별도 처리
        def format_similar_department(match: Dict) -> Dict:
            """관심사 기반 추천 포맷"""
            dept = match["department"]
            return {
                "department": {
                    "id": dept.id,
                    "name": dept.name,
                    "url": dept.url,
                    "description": dept.description
                },
                "common_tags": match["common_tags"],
                "tag_match_count": match["tag_match_count"]
            }

        similar_depts = [format_similar_department(m) for m in match_result["similar"]]

        test_result = create_test_result(
            result_id=result_id,
            answers=submission.answers,
            scores=user_scores,
            tags=interest_tags,
            personality=personality,
            top_depts=top_depts,
            worst_depts=worst_depts,
            similar_depts=similar_depts
        )

        # 7. 요약 문구 생성
        summary_gen = ResultSummary(test_result)
        summary = summary_gen.generate_full_summary()

        # 8. DB 저장
        save_result_to_db(test_result)

        # 9. 응답 반환
        return TestResultResponse(
            id=result_id,
            url=f"/result/{result_id}",
            scores=user_scores,
            interest_tags=interest_tags,
            personality=personality,
            summary=summary,
            top_departments=top_depts,
            worst_departments=worst_depts,
            similar_departments=similar_depts,
            created_at=test_result.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"결과 생성 중 오류 발생: {str(e)}"
        )


@router.get("/{result_id}", response_model=TestResultResponse)
async def get_result(result_id: str):
    """
    저장된 결과 조회 (공유 기능)

    Args:
        result_id: 결과 ID (8자리)

    Returns:
        저장된 검사 결과
    """
    try:
        # ID 유효성 검사
        if not is_valid_id(result_id):
            raise HTTPException(
                status_code=400,
                detail="유효하지 않은 결과 ID입니다"
            )

        # DB 조회
        db = get_db()

        query = """
                SELECT id, user_answers, user_scores, top_departments, created_at
                FROM test_results
                WHERE id = ?
                """

        row = db.fetchone(query, (result_id,))

        if not row:
            raise HTTPException(
                status_code=404,
                detail="결과를 찾을 수 없습니다"
            )

        # JSON 파싱
        user_answers = json.loads(row["user_answers"])
        user_scores = json.loads(row["user_scores"])
        top_departments = json.loads(row["top_departments"])

        # 질문 로드하여 성향 재계산
        questions = load_questions_from_db()
        question_set = QuestionSet(questions)
        personality = question_set.analyze_personality(user_scores)

        # 응답 구성 (간소화 버전)
        return TestResultResponse(
            id=row["id"],
            url=f"/result/{row['id']}",
            scores=user_scores,
            interest_tags=[],  # 저장하지 않음
            personality=personality,
            summary={},  # 요약도 간소화
            top_departments=top_departments,
            worst_departments=[],  # Worst는 공유 안 함
            similar_departments=[],
            created_at=row["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"결과 조회 중 오류 발생: {str(e)}"
        )


@router.delete("/{result_id}")
async def delete_result(result_id: str):
    """
    결과 삭제 (관리자용)

    Args:
        result_id: 결과 ID

    Returns:
        삭제 성공 메시지
    """
    try:
        if not is_valid_id(result_id):
            raise HTTPException(
                status_code=400,
                detail="유효하지 않은 결과 ID입니다"
            )

        db = get_db()

        # 존재 확인
        check_query = "SELECT id FROM test_results WHERE id = ?"
        row = db.fetchone(check_query, (result_id,))

        if not row:
            raise HTTPException(
                status_code=404,
                detail="결과를 찾을 수 없습니다"
            )

        # 삭제
        delete_query = "DELETE FROM test_results WHERE id = ?"
        db.execute(delete_query, (result_id,))

        return {
            "message": "결과가 삭제되었습니다",
            "deleted_id": result_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"결과 삭제 중 오류 발생: {str(e)}"
        )


@router.get("/stats/summary")
async def get_results_stats():
    """
    결과 통계 정보

    Returns:
        총 결과 수, 최근 생성 시간 등
    """
    try:
        db = get_db()

        # 총 결과 수
        count_query = "SELECT COUNT(*) as count FROM test_results"
        count_row = db.fetchone(count_query)
        total_count = count_row["count"] if count_row else 0

        # 최근 결과
        recent_query = """
                       SELECT created_at
                       FROM test_results
                       ORDER BY created_at DESC LIMIT 1
                       """
        recent_row = db.fetchone(recent_query)
        last_created = recent_row["created_at"] if recent_row else None

        return {
            "total_results": total_count,
            "last_created_at": last_created
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"통계 조회 중 오류 발생: {str(e)}"
        )