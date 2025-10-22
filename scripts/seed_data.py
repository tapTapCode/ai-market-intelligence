"""
Sample data seeder for AI Market Intelligence Dashboard
Run this to populate the database with sample documents for testing
"""

import asyncio
import sys
sys.path.append('./backend')

from app.models.document import Document
from app.services.vector_service import vector_service
from app.core.database import connect_to_mongo, close_mongo_connection


SAMPLE_DOCUMENTS = [
    {
        "title": "Tesla's Battery Innovation Breakthrough",
        "content": "Tesla has announced a major breakthrough in battery technology, achieving 20% higher energy density and 30% faster charging times. This advancement positions Tesla as a leader in the EV market and could accelerate the transition to sustainable transportation.",
        "source": "Tech News Daily",
        "url": "https://example.com/tesla-battery",
        "category": "news",
        "industry": "clean_tech",
    },
    {
        "title": "Clean Energy Investment Surge in Q1 2024",
        "content": "Global clean energy investments reached $150 billion in Q1 2024, a 40% increase from the previous year. Solar and wind projects dominated, with emerging markets showing strong growth.",
        "source": "Energy Market Report",
        "category": "report",
        "industry": "clean_tech",
    },
    {
        "title": "AI Integration in Renewable Energy Management",
        "content": "Artificial intelligence is revolutionizing renewable energy management. Smart grids powered by AI can predict energy demand, optimize distribution, and reduce waste by up to 25%.",
        "source": "AI Energy Journal",
        "category": "analysis",
        "industry": "clean_tech",
    },
    {
        "title": "Electric Vehicle Market Share Reaches 18%",
        "content": "Electric vehicles now account for 18% of global car sales, up from 12% last year. China leads adoption, followed by Europe and North America.",
        "source": "Automotive Insights",
        "category": "news",
        "industry": "automotive",
    },
    {
        "title": "Green Hydrogen Production Costs Drop 30%",
        "content": "Green hydrogen production costs have decreased by 30% due to improved electrolysis technology and cheaper renewable electricity. This makes hydrogen a viable alternative for heavy industry decarbonization.",
        "source": "Energy Transition Report",
        "category": "report",
        "industry": "clean_tech",
    },
]


async def seed_documents():
    """Seed the database with sample documents."""
    
    print("🌱 Seeding database with sample documents...")
    
    await connect_to_mongo()
    await vector_service.initialize()
    
    for doc_data in SAMPLE_DOCUMENTS:
        # Create document
        document = Document(**doc_data)
        await document.insert()
        
        # Create vector embedding
        vector_id = await vector_service.upsert_document(
            doc_id=str(document.id),
            content=doc_data["content"],
            metadata={
                "title": doc_data["title"],
                "source": doc_data["source"],
                "category": doc_data["category"],
                "industry": doc_data["industry"]
            }
        )
        
        # Update document with embedding ID
        document.embedding_id = vector_id
        await document.save()
        
        print(f"✅ Created: {doc_data['title']}")
    
    await close_mongo_connection()
    print("🎉 Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_documents())
