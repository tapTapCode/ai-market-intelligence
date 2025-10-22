# Getting Started

This guide will help you set up and run the AI Market Intelligence Dashboard locally.

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **MongoDB** (or use Docker)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
- **Pinecone API Key** - [Sign up here](https://www.pinecone.io/)

## Quick Start with Docker

The easiest way to run the entire stack:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-market-intelligence.git
cd ai-market-intelligence

# 2. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 3. Start all services
docker-compose up --build
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Local Development Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 3. Database Setup

#### Option A: Docker MongoDB

```bash
docker-compose up mongodb -d
```

#### Option B: Local MongoDB

Install MongoDB locally or use MongoDB Atlas (cloud).

Update `MONGODB_URL` in `backend/.env`:
```
MONGODB_URL=mongodb://localhost:27017
# Or for Atlas:
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/
```

## Seeding Sample Data

To populate the database with sample documents for testing:

```bash
cd backend
source venv/bin/activate
python ../scripts/seed_data.py
```

This will create:
- 5 sample market documents
- Vector embeddings in Pinecone
- MongoDB document records

## Environment Variables

### Backend (.env)

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Pinecone
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=us-west1-gcp  # Your Pinecone region
PINECONE_INDEX_NAME=market-intelligence

# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=market_intelligence

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing the Application

### 1. SWOT Analysis

1. Navigate to the dashboard
2. Click "SWOT Analysis" tab
3. Enter:
   - Company: "Tesla"
   - Industry: "clean_tech"
4. Click "Generate SWOT Analysis"

### 2. Trend Analysis

1. Click "Trend Analysis" tab
2. Enter:
   - Industry: "clean_tech"
   - Time Period: "Q1 2024"
3. Click "Analyze Trends"

## API Endpoints

### Analysis

- `POST /api/analyze/swot` - Generate SWOT analysis
- `POST /api/analyze/trends` - Analyze market trends
- `GET /api/analyze/history/{type}` - Get analysis history

### Documents

- `POST /api/documents/ingest` - Ingest new document
- `GET /api/documents/` - List documents
- `GET /api/documents/{id}` - Get document by ID
- `POST /api/documents/search` - Semantic search

Visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

### MongoDB Connection Issues

If you get connection errors:
1. Ensure MongoDB is running
2. Check `MONGODB_URL` in `.env`
3. For Docker: `docker-compose up mongodb -d`

### Pinecone Errors

1. Verify API key in `.env`
2. Check Pinecone environment/region
3. Ensure index is created (auto-created on first run)

### OpenAI API Errors

1. Verify API key has credits
2. Check rate limits
3. Ensure model name is correct

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## Next Steps

1. **Add More Documents**: Use the document ingestion API to add your own data
2. **Customize Analysis**: Modify LLM prompts in `backend/app/services/llm_service.py`
3. **Deploy**: See `docs/DEPLOYMENT.md` for deployment guides
4. **Contribute**: Check `CONTRIBUTING.md` for contribution guidelines

## Support

- **GitHub Issues**: [Report bugs](https://github.com/YOUR_USERNAME/ai-market-intelligence/issues)
- **Documentation**: [Full docs](https://github.com/YOUR_USERNAME/ai-market-intelligence/tree/main/docs)
