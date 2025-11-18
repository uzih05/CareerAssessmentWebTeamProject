"""
Questions Router - 질문 조회 API
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import get_db

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"]
)


@router.get("", response_model=Dict)
async def get_questions():
    """
    전체 질문 조회 (20개)

    Returns:
        {
            "questions": [
                {
                    "id": 1,
                    "text": "책을 읽거나 글을 쓰는 것을 좋아한다.",
                    "order": 1
                },
                ...
            ],
            "total": 20
        }
    """
    try:
        db = get_db()

        # 질문 조회 (순서대로)
        query = """
                SELECT id, question_text, question_order
                FROM questions
                ORDER BY question_order ASC \
                """

        rows = db.fetchall(query)

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="질문 데이터가 없습니다. python -m database.seed 를 실행하세요."
            )

        # 응답 데이터 구성
        questions = []
        for row in rows:
            questions.append({
                "id": row["id"],
                "text": row["question_text"],
                "order": row["question_order"]
            })

        return {
            "questions": questions,
            "total": len(questions)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 조회 중 오류 발생: {str(e)}"
        )


@router.get("/{question_id}", response_model=Dict)
async def get_question_by_id(question_id: int):
    """
    특정 질문 조회

    Args:
        question_id: 질문 ID

    Returns:
        {
            "id": 1,
            "text": "책을 읽거나...",
            "order": 1,
            "aptitude_type": "언어능력"
        }
    """
    try:
        db = get_db()

        query = """
                SELECT id, question_text, question_order, aptitude_type
                FROM questions
                WHERE id = ? \
                """

        row = db.fetchone(query, (question_id,))

        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"질문 ID {question_id}를 찾을 수 없습니다"
            )

        return {
            "id": row["id"],
            "text": row["question_text"],
            "order": row["question_order"],
            "aptitude_type": row["aptitude_type"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 조회 중 오류 발생: {str(e)}"
        )


@router.get("/aptitude/{aptitude_type}", response_model=Dict)
async def get_questions_by_aptitude(aptitude_type: str):
    """
    특정 적성의 질문들 조회

    Args:
        aptitude_type: 적성 타입 (예: "언어능력", "논리/분석력")

    Returns:
        {
            "aptitude_type": "언어능력",
            "questions": [...],
            "count": 2
        }
    """
    try:
        db = get_db()

        query = """
                SELECT id, question_text, question_order, is_reverse
                FROM questions
                WHERE aptitude_type = ?
                ORDER BY question_order ASC \
                """

        rows = db.fetchall(query, (aptitude_type,))

        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"적성 타입 '{aptitude_type}'의 질문을 찾을 수 없습니다"
            )

        questions = []
        for row in rows:
            questions.append({
                "id": row["id"],
                "text": row["question_text"],
                "order": row["question_order"],
                "is_reverse": bool(row["is_reverse"])
            })

        return {
            "aptitude_type": aptitude_type,
            "questions": questions,
            "count": len(questions)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 조회 중 오류 발생: {str(e)}"
        )


@router.get("/stats/summary", response_model=Dict)
async def get_questions_stats():
    """
    질문 통계 정보

    Returns:
        {
            "total_questions": 20,
            "aptitude_types": ["언어능력", "논리/분석력", ...],
            "questions_per_aptitude": 2
        }
    """
    try:
        db = get_db()

        # 전체 질문 수
        total_query = "SELECT COUNT(*) as count FROM questions"
        total_row = db.fetchone(total_query)
        total = total_row["count"] if total_row else 0

        # 적성 타입 목록
        aptitude_query = """
                         SELECT DISTINCT aptitude_type
                         FROM questions
                         ORDER BY aptitude_type \
                         """
        aptitude_rows = db.fetchall(aptitude_query)
        aptitude_types = [row["aptitude_type"] for row in aptitude_rows]

        return {
            "total_questions": total,
            "aptitude_types": aptitude_types,
            "aptitude_count": len(aptitude_types),
            "questions_per_aptitude": total // len(aptitude_types) if aptitude_types else 0
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"통계 조회 중 오류 발생: {str(e)}"
        )