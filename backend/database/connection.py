"""
Database Connection - SQLite 연결 및 관리
"""
import sqlite3
import os
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# [중요] 이 부분이 클래스나 함수 정의보다 *위*에 있어야 합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "major_test.db"

class DatabaseConnection:
    """SQLite 데이터베이스 연결 관리 클래스"""

    # [수정 1] 클래스 초기화 시에도 절대 경로를 기본값으로 사용하도록 변경
    def __init__(self, db_path: str = str(DEFAULT_DB_PATH)):
        """
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """데이터베이스 연결"""
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False  # FastAPI에서 여러 스레드 사용
            )
            self.connection.row_factory = sqlite3.Row

        return self.connection

    def close(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """SQL 쿼리 실행"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    def fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """단일 행 조회"""
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query: str, params: tuple = ()) -> list:
        """모든 행 조회"""
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def initialize_schema(self, schema_path: str = None):
        """스키마 초기화 (테이블 생성)"""
        if schema_path is None:
            current_dir = Path(__file__).parent
            schema_path = current_dir / "schema.sql"

        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        conn = self.connect()
        conn.executescript(schema_sql)
        conn.commit()

        print(f"✅ Database schema initialized: {self.db_path}")

    def check_table_exists(self, table_name: str) -> bool:
        """테이블 존재 여부 확인"""
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.fetchone(query, (table_name,))
        return result is not None

    def get_table_count(self, table_name: str) -> int:
        """테이블 행 개수 조회"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.fetchone(query)
        return result["count"] if result else 0

    def clear_table(self, table_name: str):
        """테이블 데이터 삭제 (구조는 유지)"""
        self.execute(f"DELETE FROM {table_name}")
        print(f"✅ Table cleared: {table_name}")

    def drop_table(self, table_name: str):
        """테이블 완전 삭제"""
        self.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"✅ Table dropped: {table_name}")

    def reset_database(self):
        """데이터베이스 초기화"""
        tables = ["test_results", "departments", "questions"]
        for table in tables:
            self.drop_table(table)
        self.initialize_schema()
        print("✅ Database reset complete")


# 싱글톤 인스턴스
_db_instance: Optional[DatabaseConnection] = None


def get_db() -> DatabaseConnection:
    """
    데이터베이스 연결 싱글톤 인스턴스 반환
    """
    global _db_instance

    if _db_instance is None:
        # 여기서 인자 없이 호출하면 클래스의 __init__ 기본값(절대경로)이 사용됨
        _db_instance = DatabaseConnection()
        _db_instance.connect()

    return _db_instance


@contextmanager
def get_db_cursor():
    """Context manager로 DB cursor 사용"""
    db = get_db()
    conn = db.connect()
    cursor = conn.cursor()

    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

# [수정 2] 함수 인자의 기본값도 절대 경로로 변경
def init_database(db_path: str = str(DEFAULT_DB_PATH), reset: bool = False):
    """
    데이터베이스 초기화 헬퍼 함수
    """
    global _db_instance
    _db_instance = DatabaseConnection(db_path)

    if reset:
        _db_instance.reset_database()
    else:
        if not _db_instance.check_table_exists("questions"):
            _db_instance.initialize_schema()

    return _db_instance


# 사용 예시
if __name__ == "__main__":
    # 테스트용 DB도 절대 경로와 동일한 폴더에 생성하고 싶다면 아래처럼 경로 지정 가능
    # (단, 테스트 목적이면 그냥 test.db 유지해도 무방함)
    test_db_path = BASE_DIR / "test.db"
    db = init_database(str(test_db_path), reset=True)

    print(f"Questions table exists: {db.check_table_exists('questions')}")
    print(f"Departments table exists: {db.check_table_exists('departments')}")
    print(f"Test results table exists: {db.check_table_exists('test_results')}")

    db.close()