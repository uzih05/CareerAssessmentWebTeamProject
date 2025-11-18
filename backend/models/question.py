"""
Question Model - 질문 및 점수 계산 로직
"""
from typing import List, Dict, Tuple
from dataclasses import dataclass


# 10가지 적성 이름 (순서 고정)
APTITUDE_NAMES = [
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


@dataclass
class Question:
    """개별 질문 데이터"""
    id: int
    question_text: str
    aptitude_type: str  # "언어능력", "논리/분석력" 등
    is_reverse: bool    # 역채점 여부
    tags: List[str]     # 관심사 태그 (예: ["코딩", "IT"])

    def calculate_answer_score(self, answer: int) -> int:
        """
        답변을 점수로 변환 (1-5점)
        역채점 질문은 6 - answer
        """
        if self.is_reverse:
            return 6 - answer
        return answer


class QuestionSet:
    """20개 질문 관리 및 점수 계산"""

    def __init__(self, questions: List[Question]):
        self.questions = questions

        # 적성별 질문 인덱스 매핑
        self.aptitude_question_map = self._build_aptitude_map()

    def _build_aptitude_map(self) -> Dict[str, List[int]]:
        """적성별로 질문 인덱스 매핑"""
        mapping = {apt: [] for apt in APTITUDE_NAMES}

        for i, q in enumerate(self.questions):
            if q.aptitude_type in mapping:
                mapping[q.aptitude_type].append(i)

        return mapping

    def calculate_score(self, answers: List[int]) -> Dict:
        """
        사용자 답변 → 적성 점수 + 관심사 태그

        Args:
            answers: 20개 질문의 답변 (1-5점)

        Returns:
            {
                "aptitude_scores": [7, 8, 6, 9, ...],  # 10개 적성 점수
                "interest_tags": ["코딩", "IT", ...]   # 관심사 태그
            }
        """
        if len(answers) != len(self.questions):
            raise ValueError(f"답변 개수가 맞지 않습니다. 필요: {len(self.questions)}, 입력: {len(answers)}")

        # 1. 각 적성별 점수 계산 (평균)
        aptitude_scores = []

        for aptitude in APTITUDE_NAMES:
            question_indices = self.aptitude_question_map[aptitude]

            if not question_indices:
                # 해당 적성 질문이 없으면 0
                aptitude_scores.append(0)
                continue

            # 해당 적성 질문들의 점수 평균
            scores = []
            for idx in question_indices:
                question = self.questions[idx]
                user_answer = answers[idx]
                score = question.calculate_answer_score(user_answer)
                scores.append(score)

            avg_score = sum(scores) / len(scores)
            aptitude_scores.append(round(avg_score, 1))

        # 2. 관심사 태그 추출 (4점 이상 답변한 질문의 태그)
        interest_tags = self._extract_interest_tags(answers)

        return {
            "aptitude_scores": aptitude_scores,
            "interest_tags": interest_tags
        }

    def _extract_interest_tags(self, answers: List[int]) -> List[str]:
        """
        높은 점수를 받은 질문의 태그 추출
        4점 이상 답변한 질문의 태그만 추출
        """
        tags = []

        for i, answer in enumerate(answers):
            question = self.questions[i]

            # 역채점 질문은 낮은 답변이 높은 점수
            actual_score = question.calculate_answer_score(answer)

            if actual_score >= 4 and question.tags:
                tags.extend(question.tags)

        # 중복 제거
        return list(set(tags))

    def analyze_personality(self, scores: List[float]) -> str:
        """
        적성 점수로 성향 분석

        Args:
            scores: 10개 적성 점수

        Returns:
            "논리형", "창의형" 등의 성향 문자열
        """
        if len(scores) != 10:
            raise ValueError("적성 점수는 10개여야 합니다")

        # 가장 높은 점수 2개의 적성 찾기
        indexed_scores = [(score, idx) for idx, score in enumerate(scores)]
        indexed_scores.sort(reverse=True)

        top1_idx = indexed_scores[0][1]
        top2_idx = indexed_scores[1][1]

        # 성향 매핑
        personality_map = {
            0: "언어형",      # 언어능력
            1: "논리형",      # 논리/분석력
            2: "창의형",      # 창의력
            3: "사회형",      # 사회성/공감능력
            4: "리더형",      # 주도성/리더십
            5: "활동형",      # 신체-활동성
            6: "예술형",      # 예술감각/공간지각
            7: "체계형",      # 체계성/꼼꼼함
            8: "탐구형",      # 탐구심
            9: "실행형"       # 문제해결능력
        }

        # 1순위 적성 기준
        return personality_map.get(top1_idx, "균형형")

    def get_strong_aptitudes(self, scores: List[float], threshold: float = 4.0) -> List[Tuple[str, float]]:
        """
        강점 적성 추출 (threshold 이상)

        Returns:
            [("논리/분석력", 8.5), ("문제해결능력", 9.0)]
        """
        strong = []

        for i, score in enumerate(scores):
            if score >= threshold:
                strong.append((APTITUDE_NAMES[i], score))

        # 점수 높은 순 정렬
        strong.sort(key=lambda x: x[1], reverse=True)

        return strong

    def get_weak_aptitudes(self, scores: List[float], threshold: float = 3.0) -> List[Tuple[str, float]]:
        """
        약점 적성 추출 (threshold 이하)

        Returns:
            [("신체-활동성", 2.5), ("예술감각", 2.0)]
        """
        weak = []

        for i, score in enumerate(scores):
            if score <= threshold:
                weak.append((APTITUDE_NAMES[i], score))

        # 점수 낮은 순 정렬
        weak.sort(key=lambda x: x[1])

        return weak

    def get_aptitude_name(self, index: int) -> str:
        """인덱스로 적성 이름 조회"""
        if 0 <= index < len(APTITUDE_NAMES):
            return APTITUDE_NAMES[index]
        return "알 수 없음"