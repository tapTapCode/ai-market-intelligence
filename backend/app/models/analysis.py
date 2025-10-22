from beanie import Document
from pydantic import Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class AnalysisType(str, Enum):
    SWOT = "swot"
    TREND = "trend"
    COMPETITOR = "competitor"
    MARKET = "market"


class SWOTAnalysis(Document):
    """Model for SWOT analysis results."""
    
    company_name: str
    industry: str
    analysis_type: AnalysisType = AnalysisType.SWOT
    
    # SWOT Components
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    threats: List[str] = Field(default_factory=list)
    
    # Summary
    summary: str
    recommendations: List[str] = Field(default_factory=list)
    
    # Metadata
    source_documents: List[str] = Field(default_factory=list)  # Document IDs
    confidence_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "swot_analyses"


class TrendAnalysis(Document):
    """Model for market trend analysis."""
    
    industry: str
    analysis_type: AnalysisType = AnalysisType.TREND
    time_period: str  # e.g., "Q1 2024"
    
    # Trends
    emerging_trends: List[Dict[str, str]] = Field(default_factory=list)
    # [{"trend": "...", "description": "...", "impact": "high|medium|low"}]
    
    declining_trends: List[Dict[str, str]] = Field(default_factory=list)
    
    # Insights
    summary: str
    key_insights: List[str] = Field(default_factory=list)
    predictions: List[str] = Field(default_factory=list)
    
    # Metadata
    source_documents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "trend_analyses"


class Analysis(Document):
    """Generic analysis model for all types."""
    
    analysis_type: AnalysisType
    title: str
    industry: str
    data: Dict  # Flexible data structure for any analysis type
    summary: str
    source_documents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "analyses"
