"""
Department Model - 학과 데이터 관리 클래스

역할: 학과 정보와 매칭 로직 관리
- 학과 데이터 CRUD
- 유사도 계산
"""

from dataclasses import dataclass
from typing import List, Dict
import json
import math


@dataclass
class Department:
    """학과 모델 - 개별 학과 하나를 표현"""

    id: int
    name: str
    aptitude_scores: List[int]  # 10개 적성 점수 (1-10점)
    description: str = ""
    url: str = ""

    def calculate_match_score(self, user_scores: List[float]) -> float:
        """
        사용자 점수와의 유사도 계산 (유클리드 거리 기반)

        Args:
            user_scores: 사용자 10개 적성 점수 (1-5점)

        Returns:
            일치율 (0-100%)
        """
        if len(user_scores) != 10:
            raise ValueError(f"적성 점수는 10개여야 합니다 (현재: {len(user_scores)}개)")

        # 사용자 점수를 1-10 스케일로 변환
        user_scores_scaled = [score * 2 for score in user_scores]

        # 유클리드 거리 계산
        distance = math.sqrt(
            sum((u - d) ** 2 for u, d in zip(user_scores_scaled, self.aptitude_scores))
        )

        # 최대 거리 (모든 점수가 정반대일 때)
        # 최소 1점 vs 최대 10점 = 9점 차이
        # 10개 항목: sqrt(10 * 9^2) = sqrt(810) ≈ 28.46
        max_distance = math.sqrt(10 * 9 ** 2)

        # 일치율 계산 (거리가 가까울수록 높음)
        match_percentage = (1 - distance / max_distance) * 100

        return round(match_percentage, 1)

    def to_dict(self, include_scores: bool = False) -> Dict:
        """API 응답용 딕셔너리로 변환"""
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url
        }

        if include_scores:
            result["aptitude_scores"] = self.aptitude_scores

        return result

    def to_match_result(self, user_scores: List[float]) -> Dict:
        """매칭 결과 형식으로 변환"""
        match_score = self.calculate_match_score(user_scores)

        return {
            "id": self.id,
            "name": self.name,
            "match_score": match_score,
            "description": self.description,
            "url": self.url
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Department':
        """
        DB 쿼리 결과를 Department 객체로 변환

        Args:
            row: (id, name, aptitude_scores_json, description, url, created_at)

        Returns:
            Department 객체
        """
        return cls(
            id=row[0],
            name=row[1],
            aptitude_scores=json.loads(row[2]),  # JSON 문자열 → 리스트
            description=row[3] or "",
            url=row[4] or ""
        )


class DepartmentMatcher:
    """학과 매칭 관리 - 모든 학과와 사용자 비교"""

    def __init__(self, departments: List[Department]):
        self.departments = departments

    def find_best_matches(
            self,
            user_scores: List[float],
            top_n: int = 3
    ) -> List[Dict]:
        """
        사용자 점수와 가장 잘 맞는 학과 찾기

        Args:
            user_scores: 사용자 10개 적성 점수 (1-5점)
            top_n: 반환할 상위 학과 개수 (기본 3개)

        Returns:
            매칭 결과 리스트 (일치율 높은 순)
        """
        # 모든 학과의 매칭 점수 계산
        matches = [dept.to_match_result(user_scores) for dept in self.departments]

        # 일치율 높은 순으로 정렬
        matches.sort(key=lambda x: x['match_score'], reverse=True)

        # 상위 N개 반환
        return matches[:top_n]

    def find_worst_matches(
            self,
            user_scores: List[float],
            bottom_n: int = 3
    ) -> List[Dict]:
        """
        사용자 점수와 가장 안 맞는 학과 찾기

        Args:
            user_scores: 사용자 10개 적성 점수 (1-5점)
            bottom_n: 반환할 하위 학과 개수 (기본 3개)

        Returns:
            매칭 결과 리스트 (일치율 낮은 순)
        """
        # 모든 학과의 매칭 점수 계산
        matches = [dept.to_match_result(user_scores) for dept in self.departments]

        # 일치율 낮은 순으로 정렬
        matches.sort(key=lambda x: x['match_score'])

        # 하위 N개 반환
        return matches[:bottom_n]

    def get_all_matches(self, user_scores: List[float]) -> List[Dict]:
        """모든 학과의 매칭 결과 반환 (정렬됨)"""
        matches = [dept.to_match_result(user_scores) for dept in self.departments]
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches


# 사용 예시
if __name__ == "__main__":
    # 예시 학과 생성
    comp_sci = Department(
        id=1,
        name="컴퓨터공학과",
        aptitude_scores=[6, 10, 9, 5, 6, 4, 5, 9, 9, 10],
        description="소프트웨어 개발 전문가 양성",
        url="https://iphak.jj.ac.kr/computer"
    )

    nursing = Department(
        id=2,
        name="간호학과",
        aptitude_scores=[7, 8, 6, 10, 7, 8, 5, 9, 8, 8],
        description="전문 간호사 양성",
        url="https://iphak.jj.ac.kr/nursing"
    )

    # 사용자 점수 (1-5점)
    # [언어, 논리, 창의, 사회성, 주도성, 신체, 예술, 체계성, 탐구, 문제해결]
    user_scores = [3.5, 5.0, 4.5, 2.5, 3.0, 2.0, 2.5, 4.5, 4.5, 5.0]

    # 개별 매칭 테스트
    print("컴퓨터공학과 일치율:", comp_sci.calculate_match_score(user_scores), "%")
    print("간호학과 일치율:", nursing.calculate_match_score(user_scores), "%")

    # 매처 테스트
    matcher = DepartmentMatcher([comp_sci, nursing])
    best = matcher.find_best_matches(user_scores, top_n=1)

    print("\n가장 잘 맞는 학과:")
    print(f"- {best[0]['name']}: {best[0]['match_score']}%")