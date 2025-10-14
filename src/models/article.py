from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    """Article model for storing news articles"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    source = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # tech or investment
    subtopic = Column(String(100), nullable=True)

    # Content
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)

    # AI-generated fields
    summary = Column(Text, nullable=True)
    key_points = Column(Text, nullable=True)  # JSON string of bullet points
    relevance_score = Column(Integer, default=50)  # 0-100

    # Metadata
    published_date = Column(DateTime, nullable=True)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    author = Column(String(200), nullable=True)

    # Filtering
    is_duplicate = Column(Boolean, default=False)
    is_filtered = Column(Boolean, default=False)  # True if filtered out

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...', source='{self.source}')>"

    def to_dict(self):
        """Convert article to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "subtopic": self.subtopic,
            "description": self.description,
            "summary": self.summary,
            "key_points": self.key_points,
            "relevance_score": self.relevance_score,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "fetched_date": self.fetched_date.isoformat() if self.fetched_date else None,
            "author": self.author,
            "is_duplicate": self.is_duplicate,
            "is_filtered": self.is_filtered,
        }
