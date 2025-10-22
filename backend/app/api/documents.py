from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.document import Document
from app.services.vector_service import vector_service

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    title: str
    content: str
    source: str
    url: Optional[str] = None
    category: str
    industry: str
    metadata: dict = {}


@router.post("/ingest", response_model=dict)
async def ingest_document(doc: DocumentCreate):
    """Ingest a new document and create vector embeddings."""
    
    try:
        # Create document in MongoDB
        document = Document(
            title=doc.title,
            content=doc.content,
            source=doc.source,
            url=doc.url,
            category=doc.category,
            industry=doc.industry,
            metadata=doc.metadata
        )
        await document.insert()
        
        # Store embedding in vector database
        vector_id = await vector_service.upsert_document(
            doc_id=str(document.id),
            content=doc.content,
            metadata={
                "title": doc.title,
                "source": doc.source,
                "category": doc.category,
                "industry": doc.industry
            }
        )
        
        # Update document with embedding ID
        document.embedding_id = vector_id
        await document.save()
        
        return {
            "id": str(document.id),
            "title": document.title,
            "embedding_id": vector_id,
            "message": "Document ingested successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}")
async def get_document(document_id: str):
    """Retrieve a document by ID."""
    
    try:
        document = await Document.get(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": str(document.id),
            "title": document.title,
            "content": document.content,
            "source": document.source,
            "url": document.url,
            "category": document.category,
            "industry": document.industry,
            "created_at": document.created_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_documents(
    industry: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
):
    """List documents with optional filters."""
    
    try:
        query = Document.find()
        
        if industry:
            query = query.find(Document.industry == industry)
        if category:
            query = query.find(Document.category == category)
        
        documents = await query.limit(limit).to_list()
        
        return [
            {
                "id": str(doc.id),
                "title": doc.title,
                "source": doc.source,
                "category": doc.category,
                "industry": doc.industry,
                "created_at": doc.created_at.isoformat()
            }
            for doc in documents
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def semantic_search(query: str, industry: Optional[str] = None, top_k: int = 5):
    """Perform semantic search across documents."""
    
    try:
        filter_dict = {"industry": industry} if industry else None
        
        results = await vector_service.search_similar(
            query=query,
            top_k=top_k,
            filter_dict=filter_dict
        )
        
        return {
            "query": query,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
