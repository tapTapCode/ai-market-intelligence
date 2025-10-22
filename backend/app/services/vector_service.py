from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from app.services.llm_service import llm_service
from typing import List, Dict
import hashlib


class VectorService:
    """Service for vector database operations using Pinecone."""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.index = None
    
    async def initialize(self):
        """Initialize Pinecone index."""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            
            if self.index_name not in [idx.name for idx in existing_indexes]:
                # Create index if it doesn't exist
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI ada-002 embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=settings.PINECONE_ENVIRONMENT
                    )
                )
                print(f"✅ Created Pinecone index: {self.index_name}")
            
            self.index = self.pc.Index(self.index_name)
            print(f"✅ Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            print(f"❌ Error initializing Pinecone: {e}")
            raise
    
    def _generate_id(self, text: str) -> str:
        """Generate unique ID for vector."""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def upsert_document(
        self, 
        doc_id: str,
        content: str, 
        metadata: Dict
    ) -> str:
        """Store document embedding in vector database."""
        
        # Generate embedding
        embedding = await llm_service.generate_embedding(content)
        
        # Generate unique vector ID
        vector_id = self._generate_id(f"{doc_id}_{content[:100]}")
        
        # Upsert to Pinecone
        self.index.upsert(
            vectors=[
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        **metadata,
                        "doc_id": doc_id,
                        "content_preview": content[:200]
                    }
                }
            ]
        )
        
        return vector_id
    
    async def search_similar(
        self, 
        query: str, 
        top_k: int = 5,
        filter_dict: Dict = None
    ) -> List[Dict]:
        """Search for similar documents using semantic search."""
        
        # Generate query embedding
        query_embedding = await llm_service.generate_embedding(query)
        
        # Search in Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        # Format results
        similar_docs = []
        for match in results.matches:
            similar_docs.append({
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            })
        
        return similar_docs
    
    async def delete_document(self, vector_id: str):
        """Delete document from vector database."""
        self.index.delete(ids=[vector_id])


vector_service = VectorService()
