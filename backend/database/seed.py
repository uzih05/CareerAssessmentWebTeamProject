"""
Seed Data - 초기 데이터 삽입 (질문 20개 + 학과 70개)
"""
import json
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import get_db, init_database

# 질문 20개 데이터 (questions_design.md 기반)
QUESTIONS_DATA = [
    # 1. 언어능력 (2문항)
    {
        "question_text": "책을 읽거나 글을 쓰는 것을 좋아한다.",
        "aptitude_type": "언어능력",
        "is_reverse": False,
        "question_order": 1,
        "tags": ["독서", "글쓰기", "문학"]
    },
    {
        "question_text": "다른 사람에게 내 생각을 말이나 글로 표현하는 것이 어렵다.",
        "aptitude_type": "언어능력",
        "is_reverse": True,
        "question_order": 2,
        "tags": []
    },

    # 2. 논리/분석력 (2문항)
    {
        "question_text": "복잡한 문제를 단계별로 분석하고 해결하는 것을 좋아한다.",
        "aptitude_type": "논리/분석력",
        "is_reverse": False,
        "question_order": 3,
        "tags": ["논리", "분석", "문제해결"]
    },
    {
        "question_text": "숫자나 데이터를 다루는 일은 나와 맞지 않는다.",
        "aptitude_type": "논리/분석력",
        "is_reverse": True,
        "question_order": 4,
        "tags": []
    },

    # 3. 창의력 (2문항)
    {
        "question_text": "새로운 아이디어나 독창적인 방법을 생각해내는 것을 즐긴다.",
        "aptitude_type": "창의력",
        "is_reverse": False,
        "question_order": 5,
        "tags": ["창의", "아이디어", "기획"]
    },
    {
        "question_text": "정해진 틀이나 규칙을 따르는 것이 더 편하다.",
        "aptitude_type": "창의력",
        "is_reverse": True,
        "question_order": 6,
        "tags": []
    },

    # 4. 사회성/공감능력 (2문항)
    {
        "question_text": "다른 사람의 감정을 잘 이해하고 공감할 수 있다.",
        "aptitude_type": "사회성/공감능력",
        "is_reverse": False,
        "question_order": 7,
        "tags": ["소통", "공감", "사회성"]
    },
    {
        "question_text": "혼자 일하는 것이 다른 사람과 협력하는 것보다 편하다.",
        "aptitude_type": "사회성/공감능력",
        "is_reverse": True,
        "question_order": 8,
        "tags": []
    },

    # 5. 주도성/리더십 (2문항)
    {
        "question_text": "팀 프로젝트에서 리더 역할을 맡는 것을 선호한다.",
        "aptitude_type": "주도성/리더십",
        "is_reverse": False,
        "question_order": 9,
        "tags": ["리더십", "주도", "팀워크"]
    },
    {
        "question_text": "다른 사람을 이끌거나 설득하는 것이 부담스럽다.",
        "aptitude_type": "주도성/리더십",
        "is_reverse": True,
        "question_order": 10,
        "tags": []
    },

    # 6. 신체-활동성 (2문항)
    {
        "question_text": "운동이나 신체 활동을 하는 것을 좋아한다.",
        "aptitude_type": "신체-활동성",
        "is_reverse": False,
        "question_order": 11,
        "tags": ["운동", "활동", "체육"]
    },
    {
        "question_text": "오래 앉아서 일하는 것이 나에게 더 잘 맞는다.",
        "aptitude_type": "신체-활동성",
        "is_reverse": True,
        "question_order": 12,
        "tags": []
    },

    # 7. 예술감각/공간지각 (2문항)
    {
        "question_text": "그림, 음악, 디자인 등 예술적인 활동에 관심이 많다.",
        "aptitude_type": "예술감각/공간지각",
        "is_reverse": False,
        "question_order": 13,
        "tags": ["예술", "디자인", "미술"]
    },
    {
        "question_text": "색상이나 형태의 조화를 생각하는 것이 어렵다.",
        "aptitude_type": "예술감각/공간지각",
        "is_reverse": True,
        "question_order": 14,
        "tags": []
    },

    # 8. 체계성/꼼꼼함 (2문항)
    {
        "question_text": "일을 계획적이고 체계적으로 처리하는 것을 선호한다.",
        "aptitude_type": "체계성/꼼꼼함",
        "is_reverse": False,
        "question_order": 15,
        "tags": ["체계", "계획", "꼼꼼"]
    },
    {
        "question_text": "세부적인 것보다 큰 그림을 보는 것이 더 중요하다고 생각한다.",
        "aptitude_type": "체계성/꼼꼼함",
        "is_reverse": True,
        "question_order": 16,
        "tags": []
    },

    # 9. 탐구심 (2문항)
    {
        "question_text": "새로운 지식을 배우고 연구하는 것을 좋아한다.",
        "aptitude_type": "탐구심",
        "is_reverse": False,
        "question_order": 17,
        "tags": ["연구", "학습", "탐구"]
    },
    {
        "question_text": "'왜 그럴까?'라는 의문을 가지고 깊이 파고드는 것이 번거롭게 느껴진다.",
        "aptitude_type": "탐구심",
        "is_reverse": True,
        "question_order": 18,
        "tags": []
    },

    # 10. 문제해결능력 (2문항)
    {
        "question_text": "어려운 문제에 부딪혔을 때 포기하지 않고 해결 방법을 찾는다.",
        "aptitude_type": "문제해결능력",
        "is_reverse": False,
        "question_order": 19,
        "tags": ["문제해결", "끈기", "도전"]
    },
    {
        "question_text": "예상치 못한 상황이 생기면 당황하고 어떻게 대처해야 할지 모르겠다.",
        "aptitude_type": "문제해결능력",
        "is_reverse": True,
        "question_order": 20,
        "tags": []
    },
]


def extract_department_tags(aptitude_list: list) -> list:
    """
    학과 적성 설명에서 키워드 태그 추출

    예: "영어 교사 목표" → ["영어", "교사", "교육"]
    """
    keywords_map = {
        "교사": ["교육", "교사", "교직"],
        "교수": ["교육", "교수", "학문"],
        "의사": ["의료", "건강", "치료"],
        "간호": ["의료", "간호", "돌봄"],
        "컴퓨터": ["IT", "컴퓨터", "기술"],
        "프로그램": ["IT", "코딩", "프로그래밍"],
        "코딩": ["IT", "코딩", "프로그래밍"],
        "디자인": ["디자인", "미술", "창작"],
        "예술": ["예술", "창작", "표현"],
        "경영": ["경영", "비즈니스", "관리"],
        "금융": ["금융", "경제", "투자"],
        "법": ["법", "법률", "정의"],
        "건축": ["건축", "설계", "공간"],
        "체육": ["체육", "운동", "스포츠"],
        "음악": ["음악", "예술", "공연"],
        "언어": ["언어", "외국어", "소통"],
        "영어": ["영어", "외국어", "언어"],
        "일본": ["일본", "일본어", "외국어"],
        "중국": ["중국", "중국어", "외국어"],
        "역사": ["역사", "인문", "문화"],
        "문화": ["문화", "인문", "예술"],
        "과학": ["과학", "연구", "실험"],
        "공학": ["공학", "기술", "엔지니어링"],
        "AI": ["AI", "인공지능", "기술"],
        "게임": ["게임", "콘텐츠", "개발"],
    }

    tags = set()
    text = " ".join(aptitude_list).lower()

    for keyword, tag_list in keywords_map.items():
        if keyword.lower() in text:
            tags.update(tag_list)

    return list(tags)


def insert_questions(db):
    """질문 20개 삽입"""
    print("\n📝 질문 데이터 삽입 중...")

    for q in QUESTIONS_DATA:
        db.execute("""
                   INSERT INTO questions
                       (question_text, aptitude_type, is_reverse, question_order)
                   VALUES (?, ?, ?, ?)
                   """, (
                       q["question_text"],
                       q["aptitude_type"],
                       q["is_reverse"],
                       q["question_order"]
                   ))

    count = db.get_table_count("questions")
    print(f"✅ 질문 {count}개 삽입 완료!")


def insert_departments(db, json_path: str):
    """학과 70개 삽입"""
    print("\n🏫 학과 데이터 삽입 중...")

    with open(json_path, 'r', encoding='utf-8') as f:
        departments = json.load(f)

    for dept in departments:
        # 태그 자동 생성
        tags = extract_department_tags(dept["적성"])

        db.execute("""
                   INSERT INTO departments
                       (name, aptitude_scores, description, url)
                   VALUES (?, ?, ?, ?)
                   """, (
                       dept["학과"],
                       json.dumps(dept["적성점수"]),
                       json.dumps(dept["적성"], ensure_ascii=False),
                       dept["URL"]
                   ))

    count = db.get_table_count("departments")
    print(f"✅ 학과 {count}개 삽입 완료!")


def seed_database(json_path: str = None, reset: bool = False):
    """
    데이터베이스 초기 데이터 삽입

    Args:
        json_path: 학과 JSON 파일 경로
        reset: True면 기존 데이터 삭제 후 삽입
    """
    # DB 초기화
    db = init_database(reset=reset)

    # 기본 JSON 경로
    if json_path is None:
        json_path = Path(__file__).parent.parent.parent / "jj_departments_with_scores.json"

    # 데이터 삽입
    try:
        insert_questions(db)
        insert_departments(db, json_path)

        print("\n" + "=" * 50)
        print("✅ 초기 데이터 삽입 완료!")
        print("=" * 50)
        print(f"📝 질문: {db.get_table_count('questions')}개")
        print(f"🏫 학과: {db.get_table_count('departments')}개")
        print(f"📊 결과: {db.get_table_count('test_results')}개")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    # 실행: python -m database.seed

    # JSON 파일 경로 찾기
    json_path = "/mnt/user-data/uploads/jj_departments_with_scores.json"

    print("=" * 50)
    print("🚀 데이터베이스 초기화 시작")
    print("=" * 50)

    seed_database(json_path=json_path, reset=True)