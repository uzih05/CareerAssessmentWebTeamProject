"""
Question Model - 질문 데이터 관리 클래스

역할: DB와 API 사이의 중간 다리
- 질문 생성, 조회, 수정 간편화
- 점수 계산 로직 캡슐화
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Question:
    """질문 모델 - 개별 질문 하나를 표현"""

    id: int
    question_text: str
    aptitude_type: str  # '언어능력', '논리/분석력' 등
    is_reverse: bool  # 역채점 여부
    question_order: int

    def calculate_score(self, user_answer: int) -> int:
        """
        사용자 답변을 적성 점수로 변환

        Args:
            user_answer: 1-5점 (리커트 척도)

        Returns:
            변환된 점수 1-5점
        """
        if self.is_reverse:
            # 역채점: 5 → 1, 4 → 2, 3 → 3, 2 → 4, 1 → 5
            return 6 - user_answer
        else:
            # 정채점: 그대로 반환
            return user_answer

    def to_dict(self) -> Dict:
        """API 응답용 딕셔너리로 변환"""
        return {
            "id": self.id,
            "question_text": self.question_text,
            "aptitude_type": self.aptitude_type,
            "question_order": self.question_order
            # is_reverse는 클라이언트에 노출하지 않음 (보안)
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Question':
        """
        DB 쿼리 결과를 Question 객체로 변환

        Args:
            row: (id, question_text, aptitude_type, is_reverse, question_order, created_at)

        Returns:
            Question 객체
        """
        return cls(
            id=row[0],
            question_text=row[1],
            aptitude_type=row[2],
            is_reverse=bool(row[3]),
            question_order=row[4]
        )


class QuestionSet:
    """질문 세트 관리 - 20개 질문 전체를 관리"""

    def __init__(self, questions: List[Question]):
        self.questions = sorted(questions, key=lambda q: q.question_order)

    def get_all(self) -> List[Dict]:
        """모든 질문을 API 응답 형식으로 반환"""
        return [q.to_dict() for q in self.questions]

    def calculate_aptitude_scores(self, user_answers: List[int]) -> Dict[str, float]:
        """
        사용자 답변을 10개 적성 점수로 변환

        Args:
            user_answers: 20개 답변 (1-5점 리스트)

        Returns:
            적성별 평균 점수 딕셔너리 (1-5점)
            예: {"언어능력": 4.5, "논리/분석력": 3.0, ...}
        """
        if len(user_answers) != len(self.questions):
            raise ValueError(f"답변 개수 불일치: {len(user_answers)}개 (예상: {len(self.questions)}개)")

        # 적성별로 점수 그룹화
        aptitude_scores = {}
        aptitude_counts = {}

        for question, answer in zip(self.questions, user_answers):
            # 답변 검증 (1-5 범위)
            if not 1 <= answer <= 5:
                raise ValueError(f"잘못된 답변: {answer} (1-5 범위여야 함)")

            # 점수 계산 (역채점 처리 포함)
            score = question.calculate_score(answer)
            aptitude = question.aptitude_type

            # 적성별 합산
            if aptitude not in aptitude_scores:
                aptitude_scores[aptitude] = 0
                aptitude_counts[aptitude] = 0

            aptitude_scores[aptitude] += score
            aptitude_counts[aptitude] += 1

        # 평균 계산
        result = {
            aptitude: aptitude_scores[aptitude] / aptitude_counts[aptitude]
            for aptitude in aptitude_scores
        }

        return result

    def calculate_aptitude_scores_list(self, user_answers: List[int]) -> List[float]:
        """
        사용자 답변을 10개 적성 점수 리스트로 변환 (순서 보장)

        Args:
            user_answers: 20개 답변 (1-5점 리스트)

        Returns:
            10개 적성 점수 리스트 (1-5점)
            순서: [언어, 논리, 창의, 사회성, 주도성, 신체, 예술, 체계성, 탐구, 문제해결]
        """
        scores_dict = self.calculate_aptitude_scores(user_answers)

        # 고정된 순서로 리스트 생성
        aptitude_order = [
            "언어능력",
            "논리/분석력",
            "창의력",
            "사회성/공감능력",
            "주도성/리더십",
            "신체-활동성",
            "예술감각/공간지각",
            "체계성/꼼꼼함",
            "탐구심",
            "문제해결능력"
        ]

        return [scores_dict.get(apt, 3.0) for apt in aptitude_order]


# 사용 예시
if __name__ == "__main__":
    # 예시 질문 생성
    q1 = Question(
        id=1,
        question_text="책을 읽거나 글을 쓰는 것을 좋아한다.",
        aptitude_type="언어능력",
        is_reverse=False,
        question_order=1
    )

    q2 = Question(
        id=2,
        question_text="다른 사람에게 내 생각을 표현하는 것이 어렵다.",
        aptitude_type="언어능력",
        is_reverse=True,
        question_order=2
    )

    # 정채점 테스트
    print("Q1 (정채점) - 답변 5점:", q1.calculate_score(5))  # 5

    # 역채점 테스트
    print("Q2 (역채점) - 답변 5점:", q2.calculate_score(5))  # 1
    print("Q2 (역채점) - 답변 1점:", q2.calculate_score(1))  # 5

    # 질문 세트 테스트
    question_set = QuestionSet([q1, q2])
    user_answers = [5, 2]  # Q1: 5점, Q2: 2점

    scores = question_set.calculate_aptitude_scores(user_answers)
    print("\n적성 점수:", scores)
    # 언어능력 = (5 + (6-2)) / 2 = 4.5