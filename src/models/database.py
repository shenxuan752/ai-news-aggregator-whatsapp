import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.article import Base, Article
from pathlib import Path


class Database:
    """Database manager for the news aggregator"""

    def __init__(self, database_url: str = None):
        if database_url is None:
            # Default to SQLite in data directory
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            database_url = f"sqlite:///{data_dir}/news_aggregator.db"

        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    def drop_tables(self):
        """Drop all tables (use with caution)"""
        Base.metadata.drop_all(bind=self.engine)


# Global database instance
db = Database()


def init_db():
    """Initialize the database"""
    db.create_tables()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
