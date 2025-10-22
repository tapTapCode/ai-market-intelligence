from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service
from app.models.analysis import SWOTAnalysis, TrendAnalysis, AnalysisType
from app.models.document import Document

router = APIRouter(prefix="/analyze", tags=["analysis"])


class SWOTRequest(BaseModel):
    company_name: str
    industry: str
    context: Optional[str] = None
    use_rag: bool = True  # Whether to use RAG for context


class TrendRequest(BaseModel):
    industry: str
    time_period: Optional[str] = "current"
    use_rag: bool = True


@router.post("/swot", response_model=dict)
async def generate_swot_analysis(request: SWOTRequest):
    """Generate SWOT analysis for a company."""
    
    try:
        context = request.context or ""
        
        # Use RAG to get relevant context
        if request.use_rag:
            similar_docs = await vector_service.search_similar(
                query=f"{request.company_name} {request.industry}",
                top_k=5,
                filter_dict={"industry": request.industry}
            )
            
            # Combine context from similar documents
            rag_context = "\n\n".join([
                doc["metadata"].get("content_preview", "") 
                for doc in similar_docs
            ])
            context = f"{context}\n\n{rag_context}"
        
        # Generate SWOT analysis
        analysis_data = await llm_service.generate_swot_analysis(
            company_name=request.company_name,
            industry=request.industry,
            context=context
        )
        
        # Save to database
        swot = SWOTAnalysis(
            company_name=request.company_name,
            industry=request.industry,
            strengths=analysis_data["strengths"],
            weaknesses=analysis_data["weaknesses"],
            opportunities=analysis_data["opportunities"],
            threats=analysis_data["threats"],
            summary=analysis_data["summary"],
            recommendations=analysis_data.get("recommendations", [])
        )
        await swot.insert()
        
        return {
            "id": str(swot.id),
            "company_name": swot.company_name,
            "industry": swot.industry,
            "analysis": {
                "strengths": swot.strengths,
                "weaknesses": swot.weaknesses,
                "opportunities": swot.opportunities,
                "threats": swot.threats,
                "summary": swot.summary,
                "recommendations": swot.recommendations
            },
            "created_at": swot.created_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trends", response_model=dict)
async def analyze_market_trends(request: TrendRequest):
    """Analyze market trends for an industry."""
    
    try:
        context = ""
        
        # Use RAG to get relevant context
        if request.use_rag:
            similar_docs = await vector_service.search_similar(
                query=f"{request.industry} market trends {request.time_period}",
                top_k=10,
                filter_dict={"industry": request.industry}
            )
            
            context = "\n\n".join([
                doc["metadata"].get("content_preview", "") 
                for doc in similar_docs
            ])
        
        # Generate trend analysis
        analysis_data = await llm_service.analyze_trends(
            industry=request.industry,
            context=context,
            time_period=request.time_period
        )
        
        # Save to database
        trend = TrendAnalysis(
            industry=request.industry,
            time_period=request.time_period,
            emerging_trends=analysis_data["emerging_trends"],
            declining_trends=analysis_data.get("declining_trends", []),
            summary=analysis_data["summary"],
            key_insights=analysis_data["key_insights"],
            predictions=analysis_data.get("predictions", [])
        )
        await trend.insert()
        
        return {
            "id": str(trend.id),
            "industry": trend.industry,
            "time_period": trend.time_period,
            "analysis": {
                "emerging_trends": trend.emerging_trends,
                "declining_trends": trend.declining_trends,
                "summary": trend.summary,
                "key_insights": trend.key_insights,
                "predictions": trend.predictions
            },
            "created_at": trend.created_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{analysis_type}")
async def get_analysis_history(analysis_type: str, limit: int = 10):
    """Get historical analyses."""
    
    try:
        if analysis_type == "swot":
            analyses = await SWOTAnalysis.find().limit(limit).to_list()
            return [
                {
                    "id": str(a.id),
                    "company_name": a.company_name,
                    "industry": a.industry,
                    "created_at": a.created_at.isoformat()
                }
                for a in analyses
            ]
        elif analysis_type == "trend":
            analyses = await TrendAnalysis.find().limit(limit).to_list()
            return [
                {
                    "id": str(a.id),
                    "industry": a.industry,
                    "time_period": a.time_period,
                    "created_at": a.created_at.isoformat()
                }
                for a in analyses
            ]
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
