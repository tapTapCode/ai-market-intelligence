from openai import AsyncOpenAI
from app.core.config import settings
from typing import List, Dict
import json


class LLMService:
    """Service for interacting with OpenAI LLM."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def generate_swot_analysis(
        self, 
        company_name: str, 
        industry: str, 
        context: str
    ) -> Dict:
        """Generate SWOT analysis using LLM."""
        
        prompt = f"""You are a business analyst. Generate a comprehensive SWOT analysis for {company_name} in the {industry} industry.

Context information:
{context}

Provide a structured SWOT analysis in the following JSON format:
{{
    "strengths": ["strength 1", "strength 2", ...],
    "weaknesses": ["weakness 1", "weakness 2", ...],
    "opportunities": ["opportunity 1", "opportunity 2", ...],
    "threats": ["threat 1", "threat 2", ...],
    "summary": "Brief summary of the analysis",
    "recommendations": ["recommendation 1", "recommendation 2", ...]
}}

Focus on actionable insights based on the context provided."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional business analyst specializing in strategic analysis."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    async def analyze_trends(
        self, 
        industry: str, 
        context: str,
        time_period: str = "current"
    ) -> Dict:
        """Analyze market trends using LLM."""
        
        prompt = f"""You are a market research analyst. Analyze market trends in the {industry} industry for {time_period}.

Context information:
{context}

Provide a structured trend analysis in the following JSON format:
{{
    "emerging_trends": [
        {{"trend": "trend name", "description": "detailed description", "impact": "high|medium|low"}},
        ...
    ],
    "declining_trends": [
        {{"trend": "trend name", "description": "detailed description", "impact": "high|medium|low"}},
        ...
    ],
    "summary": "Overall market summary",
    "key_insights": ["insight 1", "insight 2", ...],
    "predictions": ["prediction 1", "prediction 2", ...]
}}

Focus on data-driven insights and actionable predictions."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a market research analyst with deep industry expertise."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI."""
        
        response = await self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        
        return response.data[0].embedding
    
    async def summarize_document(self, content: str, max_words: int = 200) -> str:
        """Summarize document content."""
        
        prompt = f"""Summarize the following content in no more than {max_words} words:

{content}

Summary:"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()


llm_service = LLMService()
