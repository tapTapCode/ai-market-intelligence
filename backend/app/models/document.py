from beanie import Document as BeanieDocument
from pydantic import Field
from typing import Optional, List
from datetime import datetime


class Document(BeanieDocument):
    """Model for storing market documents and articles."""
    
    title: str
    content: str
    source: str
    url: Optional[str] = None
    category: str  # e.g., "news", "report", "analysis"
    industry: str  # e.g., "clean_tech", "energy", "automotive"
    embedding_id: Optional[str] = None  # Pinecone vector ID
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "documents"
        indexes = [
            "title",
            "category",
            "industry",
            "created_at"
        ]
