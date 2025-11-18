"""
Database Connection - SQLite 연결 및 관리
"""
import sqlite3
import os
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class DatabaseConnection:
    """SQLite 데이터베이스 연결 관리 클래스"""
    
    def __init__(self, db_path: str = "major_test.db"):
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
            # Row 객체로 결과 반환 (딕셔너리처럼 사용 가능)
            self.connection.row_factory = sqlite3.Row
        
        return self.connection
    
    def close(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        SQL 쿼리 실행
        
        Args:
            query: SQL 쿼리
            params: 파라미터 튜플
        
        Returns:
            Cursor 객체
        """
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
        """
        스키마 초기화 (테이블 생성)
        
        Args:
            schema_path: schema.sql 파일 경로
        """
        if schema_path is None:
            # 기본 경로: database/schema.sql
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
        """데이터베이스 초기화 (모든 데이터 삭제 후 스키마 재생성)"""
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
    
    Returns:
        DatabaseConnection 인스턴스
    """
    global _db_instance
    
    if _db_instance is None:
        _db_instance = DatabaseConnection()
        _db_instance.connect()
    
    return _db_instance


@contextmanager
def get_db_cursor():
    """
    Context manager로 DB cursor 사용
    
    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM questions")
            results = cursor.fetchall()
    """
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


def init_database(db_path: str = "major_test.db", reset: bool = False):
    """
    데이터베이스 초기화 헬퍼 함수
    
    Args:
        db_path: DB 파일 경로
        reset: True면 기존 데이터 삭제 후 재생성
    """
    global _db_instance
    _db_instance = DatabaseConnection(db_path)
    
    if reset:
        _db_instance.reset_database()
    else:
        # 테이블이 없으면 생성
        if not _db_instance.check_table_exists("questions"):
            _db_instance.initialize_schema()
    
    return _db_instance


# 사용 예시
if __name__ == "__main__":
    # 테스트
    db = init_database("test.db", reset=True)
    
    print(f"Questions table exists: {db.check_table_exists('questions')}")
    print(f"Departments table exists: {db.check_table_exists('departments')}")
    print(f"Test results table exists: {db.check_table_exists('test_results')}")
    
    db.close()
