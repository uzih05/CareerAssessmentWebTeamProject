"""
ID Generator - 결과 공유용 짧은 ID 생성
"""
import secrets
import string
from typing import Set

# 생성된 ID 저장 (중복 방지) - 실제로는 DB 조회로 확인
_generated_ids: Set[str] = set()


def generate_result_id(length: int = 8) -> str:
    """
    공유용 짧은 ID 생성

    Args:
        length: ID 길이 (기본 8자리)

    Returns:
        소문자 + 숫자로 구성된 랜덤 ID (예: "k3m9x2a7")

    Note:
        - 8자리 기준 충돌 확률: 2.8조 분의 1
        - 소문자(26) + 숫자(10) = 36가지 문자
        - 36^8 = 2,821,109,907,456 가지 조합
    """
    alphabet = string.ascii_lowercase + string.digits

    # ID 생성 (중복 방지)
    while True:
        result_id = ''.join(secrets.choice(alphabet) for _ in range(length))

        # 중복 체크 (실제로는 DB에서 확인)
        if result_id not in _generated_ids:
            _generated_ids.add(result_id)
            return result_id


def is_valid_id(result_id: str, length: int = 8) -> bool:
    """
    ID 유효성 검사

    Args:
        result_id: 검사할 ID
        length: 예상 ID 길이

    Returns:
        True if 유효, False otherwise
    """
    if not result_id or len(result_id) != length:
        return False

    # 소문자 + 숫자만 허용
    allowed = set(string.ascii_lowercase + string.digits)
    return all(c in allowed for c in result_id)


def clear_id_cache():
    """생성된 ID 캐시 초기화 (테스트용)"""
    global _generated_ids
    _generated_ids.clear()


# 사용 예시
if __name__ == "__main__":
    # 테스트
    print("🔑 ID 생성 테스트\n")

    # 10개 ID 생성
    for i in range(10):
        result_id = generate_result_id()
        is_valid = is_valid_id(result_id)
        print(f"{i + 1}. {result_id} - Valid: {is_valid}")

    # 유효성 검사 테스트
    print("\n✅ 유효성 검사 테스트\n")
    test_cases = [
        ("k3m9x2a7", True),
        ("ABC123EF", False),  # 대문자 포함
        ("k3m9", False),  # 길이 부족
        ("k3m9x2a7!", False),  # 특수문자 포함
    ]

    for test_id, expected in test_cases:
        result = is_valid_id(test_id)
        status = "✅" if result == expected else "❌"
        print(f"{status} {test_id}: {result} (expected: {expected})")