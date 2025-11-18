"""
Department Model - 학과 정보 및 매칭 알고리즘
"""
from typing import List, Dict, Tuple
from dataclasses import dataclass
import math


@dataclass
class Department:
    """학과 정보"""
    id: int
    name: str
    aptitude_scores: List[int]  # 10개 적성 점수 (1-10)
    description: str
    url: str
    tags: List[str]  # 학과 관심사 태그 (예: ["코딩", "프로그래밍"])
    category: str  # 계열 (예: "이공계", "인문사회")

    def __post_init__(self):
        """점수 개수 검증"""
        if len(self.aptitude_scores) != 10:
            raise ValueError(f"적성 점수는 10개여야 합니다. 현재: {len(self.aptitude_scores)}")


class DepartmentMatcher:
    """학과 매칭 알고리즘"""

    def __init__(self, departments: List[Department]):
        self.departments = departments

    def match_departments(
        self,
        user_scores: List[float],
        user_tags: List[str] = None,
        top_n: int = 3,
        worst_n: int = 3
    ) -> Dict:
        """
        사용자 점수로 학과 매칭

        Args:
            user_scores: 사용자 10개 적성 점수 (1-5)
            user_tags: 사용자 관심사 태그
            top_n: 추천할 상위 학과 수
            worst_n: 보여줄 하위 학과 수

        Returns:
            {
                "top": [...],     # Top 3 학과
                "worst": [...],   # Worst 3 학과
                "similar": [...], # 관심사 기반 추천
            }
        """
        if len(user_scores) != 10:
            raise ValueError("사용자 점수는 10개여야 합니다")

        # 사용자 점수를 1-10 스케일로 변환 (학과 점수와 동일 스케일)
        user_scores_scaled = [score * 2 for score in user_scores]

        # 모든 학과와 매칭률 계산
        matches = []
        for dept in self.departments:
            match_percentage = self.calculate_match_percentage(
                user_scores_scaled,
                dept.aptitude_scores
            )

            reason = self.generate_match_reason(
                user_scores_scaled,
                dept
            )

            matches.append({
                "department": dept,
                "match_percentage": match_percentage,
                "reason": reason
            })

        # 매칭률 순 정렬
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)

        # Top N
        top_matches = matches[:top_n]

        # Worst N
        worst_matches = matches[-worst_n:]
        worst_matches.reverse()  # 낮은 순으로

        # Worst에 미스매치 이유 추가
        for match in worst_matches:
            match["mismatch_reason"] = self.generate_mismatch_reason(
                user_scores_scaled,
                match["department"]
            )

        # 관심사 기반 추천 (태그가 있을 경우)
        similar_by_tags = []
        if user_tags:
            similar_by_tags = self.find_similar_by_tags(
                user_tags,
                exclude_ids=[m["department"].id for m in top_matches]
            )[:3]

        return {
            "top": top_matches,
            "worst": worst_matches,
            "similar": similar_by_tags
        }

    def calculate_match_percentage(
        self,
        user_scores: List[float],
        dept_scores: List[int]
    ) -> float:
        """
        유클리드 거리로 매칭률 계산

        거리가 0이면 100%, 최대 거리면 0%
        """
        # 유클리드 거리
        distance = math.sqrt(
            sum((u - d) ** 2 for u, d in zip(user_scores, dept_scores))
        )

        # 최대 거리 (10개 적성에서 각각 최대 차이 9)
        max_distance = math.sqrt(10 * (9 ** 2))  # √810 ≈ 28.46

        # 일치율 = (1 - 정규화된 거리) × 100
        match_rate = (1 - (distance / max_distance)) * 100

        return round(max(0, min(100, match_rate)), 1)  # 0-100 범위로 제한

    def generate_match_reason(
        self,
        user_scores: List[float],
        dept: Department
    ) -> str:
        """
        매칭 이유 문구 생성

        "당신의 논리력(9/10)과 문제해결능력(10/10)이 뛰어나며..."
        """
        from .question import APTITUDE_NAMES

        # 강점 적성 찾기 (사용자 점수 7 이상 && 학과 점수 7 이상)
        strong_matches = []

        for i, (user, dept_score) in enumerate(zip(user_scores, dept.aptitude_scores)):
            if user >= 7 and dept_score >= 7:
                strong_matches.append((
                    APTITUDE_NAMES[i],
                    round(user / 2, 1)  # 1-10 → 1-5 스케일로 표시
                ))

        if not strong_matches:
            return "전반적으로 적성이 잘 맞습니다"

        # 상위 2개만
        strong_matches = strong_matches[:2]

        # 문구 생성
        aptitude_text = ", ".join([
            f"{name}({score}/5)"
            for name, score in strong_matches
        ])

        return f"당신의 {aptitude_text}이(가) 뛰어나며 이 학과와 잘 맞습니다"

    def generate_mismatch_reason(
        self,
        user_scores: List[float],
        dept: Department
    ) -> str:
        """
        미스매치 이유 문구 생성

        "신체활동성(3/10)이 낮아 적응에 어려움이 있을 수 있어요"
        """
        from .question import APTITUDE_NAMES

        # 약점 찾기 (사용자 낮음 && 학과 높음)
        weaknesses = []

        for i, (user, dept_score) in enumerate(zip(user_scores, dept.aptitude_scores)):
            # 차이가 5 이상이고 사용자가 낮을 때
            if dept_score - user >= 5:
                weaknesses.append((
                    APTITUDE_NAMES[i],
                    round(user / 2, 1)
                ))

        if not weaknesses:
            return "전반적으로 적성이 맞지 않습니다"

        # 가장 차이 큰 1개
        apt_name, apt_score = weaknesses[0]

        # 적성별 맞춤 문구
        reason_templates = {
            "신체-활동성": "신체 활동이 많은 학과라 체력 부담이 있을 수 있어요",
            "예술감각/공간지각": "미적 감각과 표현력이 중요한 학과예요",
            "사회성/공감능력": "사람들과의 소통이 많아 부담을 느낄 수 있어요",
            "언어능력": "언어 능력이 중요하게 요구되는 학과예요",
            "논리/분석력": "논리적 사고와 분석이 많이 필요한 학과예요",
            "창의력": "창의적 발상과 아이디어가 중요한 학과예요",
            "주도성/리더십": "리더십과 주도적 역할이 많이 요구되는 학과예요",
            "체계성/꼼꼼함": "세밀한 작업과 정확성이 중요한 학과예요",
            "탐구심": "깊이 있는 연구와 탐구가 필요한 학과예요",
            "문제해결능력": "복잡한 문제 해결이 자주 필요한 학과예요"
        }

        reason = reason_templates.get(
            apt_name,
            "학과 특성과 적성이 잘 맞지 않아요"
        )

        return f"{apt_name}({apt_score}/5)이(가) 낮아 {reason}"

    def find_similar_by_tags(
        self,
        user_tags: List[str],
        exclude_ids: List[int] = None,
        min_common_tags: int = 1
    ) -> List[Dict]:
        """
        관심사 태그 기반 학과 추천

        Args:
            user_tags: 사용자 관심사 태그
            exclude_ids: 제외할 학과 ID (이미 추천된 학과)
            min_common_tags: 최소 공통 태그 수

        Returns:
            [{department, common_tags, tag_match_count}, ...]
        """
        exclude_ids = exclude_ids or []
        similar = []

        for dept in self.departments:
            if dept.id in exclude_ids:
                continue

            # 공통 태그
            common = set(user_tags) & set(dept.tags)

            if len(common) >= min_common_tags:
                similar.append({
                    "department": dept,
                    "common_tags": list(common),
                    "tag_match_count": len(common)
                })

        # 공통 태그 많은 순 정렬
        similar.sort(key=lambda x: x["tag_match_count"], reverse=True)

        return similar

    def get_department_by_id(self, dept_id: int) -> Department:
        """ID로 학과 조회"""
        for dept in self.departments:
            if dept.id == dept_id:
                return dept
        return None