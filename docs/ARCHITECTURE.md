# Architecture Overview

## System Design

The AI Market Intelligence Dashboard follows a modern microservices architecture with clear separation of concerns.

```
┌─────────────────┐
│   Frontend      │  Next.js + React + Tailwind
│   (Port 3000)   │  - SWOT Analysis UI
└────────┬────────┘  - Trend Analysis UI
         │           - Data Visualization
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI + Python
│   (Port 8000)   │  - REST API Endpoints
└────────┬────────┘  - Business Logic
         │
    ┌────┴────┐
    ▼         ▼
┌─────┐   ┌──────────┐
│ LLM │   │ Vector   │  Pinecone
│     │   │ Database │  - Semantic Search
│OpenAI   └──────────┘  - Embeddings
└─────┘        │
    │          │
    └────┬─────┘
         ▼
    ┌─────────┐
    │ MongoDB │  Document Storage
    │         │  - Articles
    └─────────┘  - Analyses
```

## Tech Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **Lucide React**: Icon library

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **Motor/Beanie**: Async MongoDB ODM
- **OpenAI SDK**: LLM integration
- **Pinecone**: Vector database client
- **Python-Jose**: JWT authentication
- **Uvicorn**: ASGI server

### Databases
- **MongoDB**: Primary data store for documents and analyses
- **Pinecone**: Vector database for semantic search and RAG

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Component Architecture

### Backend Services

#### 1. LLM Service (`llm_service.py`)
Handles all interactions with OpenAI's GPT models:
- SWOT analysis generation
- Trend analysis
- Document summarization
- Text embeddings

**Key Features:**
- Structured JSON output
- Retry logic
- Temperature control
- Token optimization

#### 2. Vector Service (`vector_service.py`)
Manages vector embeddings and semantic search:
- Document embedding creation
- Similarity search
- Index management
- Metadata filtering

**RAG Pipeline:**
1. User query → Embedding
2. Similarity search in Pinecone
3. Retrieve top-k relevant documents
4. Context → LLM
5. Generate analysis

#### 3. Database Layer (`database.py`, Models)
- Async MongoDB connection
- Beanie ODM for document models
- Automatic indexing
- Connection pooling

### API Design

#### RESTful Endpoints

**Analysis Routes** (`/api/analyze`)
- `POST /swot`: Generate SWOT analysis
  - Input: company_name, industry, context
  - Output: Structured SWOT with recommendations
  
- `POST /trends`: Analyze market trends
  - Input: industry, time_period
  - Output: Emerging/declining trends, insights

- `GET /history/{type}`: Retrieve past analyses

**Document Routes** (`/api/documents`)
- `POST /ingest`: Add new documents
- `GET /`: List documents with filters
- `GET /{id}`: Get specific document
- `POST /search`: Semantic search

### Frontend Architecture

#### Page Structure
```
app/
├── page.tsx          # Main dashboard
└── layout.tsx        # Root layout

components/
├── SWOTAnalysis.tsx  # SWOT generation UI
└── TrendAnalysis.tsx # Trend analysis UI
```

#### State Management
- React Hooks (useState, useEffect)
- Local component state
- No global state manager (keeps it simple)

#### Data Flow
1. User input → Component state
2. API call via Axios
3. Loading state
4. Response → Update UI
5. Display results

## Data Models

### Document Model
```python
{
  "title": str,
  "content": str,
  "source": str,
  "url": str?,
  "category": str,  # news, report, analysis
  "industry": str,  # clean_tech, energy, etc.
  "embedding_id": str?,  # Pinecone vector ID
  "metadata": dict,
  "created_at": datetime
}
```

### SWOT Analysis Model
```python
{
  "company_name": str,
  "industry": str,
  "strengths": [str],
  "weaknesses": [str],
  "opportunities": [str],
  "threats": [str],
  "summary": str,
  "recommendations": [str],
  "source_documents": [str],  # Doc IDs used
  "created_at": datetime
}
```

### Trend Analysis Model
```python
{
  "industry": str,
  "time_period": str,
  "emerging_trends": [{
    "trend": str,
    "description": str,
    "impact": "high|medium|low"
  }],
  "declining_trends": [...],
  "summary": str,
  "key_insights": [str],
  "predictions": [str],
  "created_at": datetime
}
```

## Security Considerations

### API Security
- CORS middleware configured
- Environment-based secrets
- Input validation with Pydantic
- Rate limiting (recommended for production)

### Data Privacy
- No PII stored in vectors
- API keys in environment variables
- MongoDB access control (production)

## Performance Optimization

### Backend
- Async/await throughout
- Connection pooling
- Vector search caching
- Pagination on list endpoints

### Frontend
- Client-side rendering for interactivity
- Lazy loading components
- Optimized bundle size
- Image optimization (Next.js)

### Database
- Indexed fields (industry, category, created_at)
- Vector search optimized with metadata filters
- Efficient queries with Beanie

## Scalability

### Horizontal Scaling
- Stateless API (easily scalable)
- Docker containers
- Load balancer ready

### Vertical Scaling
- Async operations
- Efficient memory usage
- Optimized queries

### Database Scaling
- MongoDB replica sets
- Pinecone auto-scales
- Read replicas for analytics

## Error Handling

### Backend
- Try-catch blocks
- HTTPException with status codes
- Logging (production: use proper logger)
- Graceful degradation

### Frontend
- Error state management
- User-friendly error messages
- Retry mechanisms
- Loading states

## Testing Strategy

### Backend Testing
```bash
pytest
pytest --cov=app tests/
```

### Frontend Testing
```bash
npm test
npm run test:e2e
```

### Integration Testing
- API endpoint tests
- Database connection tests
- LLM mock tests (avoid costs)

## Monitoring & Observability

### Recommended (Production)
- **Logging**: Structured logging (JSON)
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry
- **Error Tracking**: Sentry
- **Uptime**: Status page

## Future Enhancements

1. **Authentication & Authorization**
   - User accounts
   - API key management
   - Role-based access

2. **Advanced Analytics**
   - Time-series analysis
   - Competitor comparison
   - Market sentiment analysis

3. **PDF Report Generation**
   - ReportLab integration
   - Custom templates
   - Email delivery

4. **Webhook Integration**
   - Real-time updates
   - Third-party integrations
   - Event-driven architecture

5. **Caching Layer**
   - Redis for API responses
   - Analysis result caching
   - Rate limiting

## Contributing

See `CONTRIBUTING.md` for development guidelines and architecture decisions.
