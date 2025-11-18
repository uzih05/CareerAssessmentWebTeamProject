"""
Result Model - 검사 결과 관리 클래스

역할: 검사 결과 저장 및 공유 관리
- 결과 ID 생성
- 결과 저장/조회
"""

from dataclasses import dataclass
from typing import List, Dict
import json
import random
import string
from datetime import datetime, timedelta


@dataclass
class TestResult:
    """검사 결과 모델"""

    id: str  # 공유용 짧은 ID (예: "a1b2c3d4")
    user_answers: List[int]  # 20개 답변 (1-5점)
    user_scores: List[float]  # 10개 적성 점수 (1-5점)
    top_departments: List[Dict]  # 상위 3개 학과 정보
    created_at: datetime = None

    @staticmethod
    def generate_short_id(length: int = 8) -> str:
        """
        공유용 짧은 ID 생성

        Args:
            length: ID 길이 (기본 8자)

        Returns:
            랜덤 ID (예: "a1b2c3d4")
        """
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))

    @classmethod
    def create(
            cls,
            user_answers: List[int],
            user_scores: List[float],
            top_departments: List[Dict]
    ) -> 'TestResult':
        """
        새 결과 생성

        Args:
            user_answers: 사용자 답변
            user_scores: 적성 점수
            top_departments: 매칭된 학과 정보

        Returns:
            TestResult 객체
        """
        return cls(
            id=cls.generate_short_id(),
            user_answers=user_answers,
            user_scores=user_scores,
            top_departments=top_departments,
            created_at=datetime.now()
        )

    def to_dict(self) -> Dict:
        """API 응답용 딕셔너리로 변환"""
        return {
            "id": self.id,
            "user_scores": self.user_scores,
            "top_departments": self.top_departments,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def to_db_tuple(self) -> tuple:
        """
        DB 삽입용 튜플로 변환

        Returns:
            (id, user_answers_json, user_scores_json, top_departments_json, created_at)
        """
        return (
            self.id,
            json.dumps(self.user_answers),
            json.dumps(self.user_scores),
            json.dumps(self.top_departments),
            self.created_at or datetime.now()
        )

    @classmethod
    def from_db_row(cls, row: tuple) -> 'TestResult':
        """
        DB 쿼리 결과를 TestResult 객체로 변환

        Args:
            row: (id, user_answers_json, user_scores_json, top_departments_json, created_at, expires_at)

        Returns:
            TestResult 객체
        """
        return cls(
            id=row[0],
            user_answers=json.loads(row[1]),
            user_scores=json.loads(row[2]),
            top_departments=json.loads(row[3]),
            created_at=datetime.fromisoformat(row[4]) if isinstance(row[4], str) else row[4]
        )

    def get_share_url(self, base_url: str = "https://example.com") -> str:
        """
        공유 URL 생성

        Args:
            base_url: 베이스 URL

        Returns:
            공유 링크 (예: "https://example.com/result/a1b2c3d4")
        """
        return f"{base_url}/result/{self.id}"

    def is_expired(self, days: int = 30) -> bool:
        """
        결과 만료 여부 확인

        Args:
            days: 만료 기간 (기본 30일)

        Returns:
            만료 여부
        """
        if not self.created_at:
            return False

        expiry_date = self.created_at + timedelta(days=days)
        return datetime.now() > expiry_date


class ResultSummary:
    """결과 요약 - 통계 정보 제공"""

    @staticmethod
    def get_aptitude_summary(user_scores: List[float]) -> Dict[str, any]:
        """
        적성 점수 요약 통계

        Args:
            user_scores: 10개 적성 점수

        Returns:
            통계 정보 (평균, 최고, 최저)
        """
        aptitude_names = [
            "언어능력", "논리/분석력", "창의력", "사회성/공감능력",
            "주도성/리더십", "신체-활동성", "예술감각/공간지각",
            "체계성/꼼꼼함", "탐구심", "문제해결능력"
        ]

        scores_with_names = [
            {"name": name, "score": score}
            for name, score in zip(aptitude_names, user_scores)
        ]

        # 점수 높은 순으로 정렬
        sorted_scores = sorted(scores_with_names, key=lambda x: x['score'], reverse=True)

        return {
            "average": round(sum(user_scores) / len(user_scores), 2),
            "top_3": sorted_scores[:3],
            "bottom_3": sorted_scores[-3:],
            "all": scores_with_names
        }

    @staticmethod
    def get_match_summary(top_departments: List[Dict]) -> Dict[str, any]:
        """
        매칭 결과 요약

        Args:
            top_departments: 매칭된 학과 리스트

        Returns:
            매칭 요약 정보
        """
        if not top_departments:
            return {"status": "no_match"}

        return {
            "best_match": top_departments[0],
            "match_count": len(top_departments),
            "average_score": round(
                sum(d['match_score'] for d in top_departments) / len(top_departments),
                1
            )
        }


# 사용 예시
if __name__ == "__main__":
    # 결과 생성 예시
    result = TestResult.create(
        user_answers=[5, 2, 4, 3, 5, 1, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2],
        user_scores=[4.5, 5.0, 4.0, 2.5, 3.0, 2.0, 2.5, 4.5, 4.5, 5.0],
        top_departments=[
            {"name": "컴퓨터공학과", "match_score": 85.3},
            {"name": "소프트웨어학과", "match_score": 82.1},
            {"name": "인공지능학과", "match_score": 80.5}
        ]
    )

    print("결과 ID:", result.id)
    print("공유 URL:", result.get_share_url())
    print("\n적성 요약:")
    summary = ResultSummary.get_aptitude_summary(result.user_scores)
    print(f"- 평균: {summary['average']}")
    print(f"- 강점: {summary['top_3'][0]['name']} ({summary['top_3'][0]['score']}점)")