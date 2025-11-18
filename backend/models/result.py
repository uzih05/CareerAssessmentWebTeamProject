"""
Result Model - 검사 결과 데이터 및 요약 생성
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class TestResult:
    """검사 결과 데이터"""
    id: str  # 공유용 짧은 ID (예: "k3m9x2a7")
    user_answers: List[int]  # 20개 답변 (1-5)
    user_scores: List[float]  # 10개 적성 점수 (1-5)
    interest_tags: List[str]  # 관심사 태그
    personality_type: str  # 성향 ("논리형", "창의형" 등)

    # 매칭 결과
    top_departments: List[Dict]  # Top 3 학과
    worst_departments: List[Dict]  # Worst 3 학과
    similar_departments: List[Dict]  # 관심사 기반 추천

    # 메타 정보
    created_at: str  # ISO 형식 시간

    def to_dict(self) -> Dict:
        """딕셔너리로 변환 (JSON 직렬화용)"""
        return asdict(self)

    def to_json(self) -> str:
        """JSON 문자열로 변환"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict) -> 'TestResult':
        """딕셔너리에서 복원"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'TestResult':
        """JSON 문자열에서 복원"""
        return cls.from_dict(json.loads(json_str))


class ResultSummary:
    """결과 요약 및 맞춤 문구 생성"""

    def __init__(self, result: TestResult):
        self.result = result

    def generate_personality_summary(self) -> str:
        """
        성향 기반 요약 문구 생성

        Returns:
            "당신은 논리적 사고와 분석을 잘하는 학생입니다"
        """
        personality_templates = {
            "논리형": "당신은 논리적 사고와 분석을 잘하는",
            "창의형": "당신은 창의적이고 새로운 아이디어를 내는",
            "탐구형": "당신은 호기심이 많고 깊이 파고드는",
            "사회형": "당신은 사람들과 소통하고 공감을 잘하는",
            "리더형": "당신은 주도적이고 리더십이 있는",
            "활동형": "당신은 활동적이고 에너지가 넘치는",
            "예술형": "당신은 예술적 감각과 표현력이 뛰어난",
            "체계형": "당신은 계획적이고 체계적으로 일하는",
            "실행형": "당신은 문제를 해결하고 실행하는",
            "언어형": "당신은 언어 능력과 표현력이 뛰어난",
        }

        personality = self.result.personality_type
        template = personality_templates.get(personality, "당신은 다재다능한")

        return f"{template} 학생입니다"

    def generate_strength_summary(self) -> str:
        """
        강점 적성 요약

        Returns:
            "논리력과 문제해결능력이 특히 뛰어납니다"
        """
        from .question import APTITUDE_NAMES

        # 강점 찾기 (4.0 이상)
        strong = []
        for i, score in enumerate(self.result.user_scores):
            if score >= 4.0:
                strong.append(APTITUDE_NAMES[i])

        if not strong:
            return "전반적으로 균형잡힌 적성을 보입니다"

        # 상위 2-3개만
        strong = strong[:3]

        if len(strong) == 1:
            return f"{strong[0]}이(가) 특히 뛰어납니다"
        elif len(strong) == 2:
            return f"{strong[0]}과(와) {strong[1]}이(가) 특히 뛰어납니다"
        else:
            return f"{', '.join(strong[:-1])}과(와) {strong[-1]}이(가) 특히 뛰어납니다"

    def generate_interest_summary(self) -> Optional[str]:
        """
        관심사 기반 요약

        Returns:
            "IT와 코딩에 관심이 있는 학생이시군요!"
            None (관심사 태그가 없으면)
        """
        tags = self.result.interest_tags

        if not tags:
            return None

        # 상위 3개만
        tags = tags[:3]

        if len(tags) == 1:
            tag_text = tags[0]
        elif len(tags) == 2:
            tag_text = f"{tags[0]}와(과) {tags[1]}"
        else:
            tag_text = f"{', '.join(tags[:-1])}와(과) {tags[-1]}"

        return f"{tag_text}에 관심이 있는 학생이시군요!"

    def generate_full_summary(self) -> Dict[str, str]:
        """
        전체 요약 문구 생성

        Returns:
            {
                "personality": "당신은 논리적 사고와...",
                "strength": "논리력과 문제해결능력이...",
                "interest": "IT와 코딩에 관심이..." (Optional)
            }
        """
        summary = {
            "personality": self.generate_personality_summary(),
            "strength": self.generate_strength_summary()
        }

        interest = self.generate_interest_summary()
        if interest:
            summary["interest"] = interest

        return summary

    def generate_top_department_summary(self) -> str:
        """
        1순위 학과 추천 문구

        Returns:
            "컴퓨터공학과가 95% 일치하며, 당신의 논리력과..."
        """
        if not self.result.top_departments:
            return "추천할 학과가 없습니다"

        top = self.result.top_departments[0]
        dept_name = top["department"]["name"]
        match_pct = top["match_percentage"]
        reason = top["reason"]

        return f"{dept_name}가 {match_pct}% 일치하며, {reason}"

    def generate_similar_departments_summary(self) -> Optional[str]:
        """
        관심사 기반 추가 추천 문구

        Returns:
            "함께 고려해볼 학과: 인공지능학과, 소프트웨어학과"
            None (추가 추천이 없으면)
        """
        similar = self.result.similar_departments

        if not similar:
            return None

        dept_names = [s["department"]["name"] for s in similar]

        if len(dept_names) == 1:
            return f"함께 고려해볼 학과: {dept_names[0]}"
        else:
            return f"함께 고려해볼 학과: {', '.join(dept_names)}"

    def get_share_message(self) -> str:
        """
        공유용 간단 메시지

        Returns:
            "전주대 전공검사 결과\n나는 컴퓨터공학과 95% 일치!\nhttps://..."
        """
        if not self.result.top_departments:
            dept_text = "결과 확인"
        else:
            top = self.result.top_departments[0]
            dept_name = top["department"]["name"]
            match_pct = top["match_percentage"]
            dept_text = f"{dept_name} {match_pct}% 일치"

        url = f"https://major-test.jj.ac.kr/result/{self.result.id}"

        return f"""전주대 전공 유형 검사 결과
나는 {dept_text}!
{url}"""


def create_test_result(
    result_id: str,
    answers: List[int],
    scores: List[float],
    tags: List[str],
    personality: str,
    top_depts: List[Dict],
    worst_depts: List[Dict],
    similar_depts: List[Dict]
) -> TestResult:
    """
    TestResult 객체 생성 헬퍼 함수
    """
    return TestResult(
        id=result_id,
        user_answers=answers,
        user_scores=scores,
        interest_tags=tags,
        personality_type=personality,
        top_departments=top_depts,
        worst_departments=worst_depts,
        similar_departments=similar_depts,
        created_at=datetime.now().isoformat()
    )