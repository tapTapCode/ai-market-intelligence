# AI Market Intelligence Dashboard

An AI-powered market intelligence platform that analyzes industry trends, generates SWOT analyses, and provides actionable insights using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **📊 Interactive Dashboard**: Real-time data visualization with trends and insights
- **🤖 AI-Powered Analysis**: LLM-driven SWOT analysis and market trend detection
- **🔍 Semantic Search**: RAG-based document search using vector embeddings
- **📈 Data Visualization**: Beautiful charts and graphs using Recharts
- **📄 Report Generation**: Export insights as PDF reports
- **🔐 Secure API**: RESTful API with authentication and rate limiting

## 🏗️ Architecture

```
ai-market-intelligence/
├── backend/           # FastAPI + Python microservice
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Configuration & utilities
│   │   ├── models/    # Database models
│   │   ├── services/  # Business logic & LLM integration
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          # Next.js + React dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenAI API**: GPT-4 for analysis and insights
- **Pinecone**: Vector database for semantic search
- **MongoDB**: Document storage
- **LangChain**: LLM orchestration framework

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Recharts**: Data visualization library
- **Tailwind CSS**: Utility-first styling
- **Axios**: API client

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- Docker & Docker Compose (optional)
- MongoDB instance
- OpenAI API key
- Pinecone API key

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-market-intelligence.git
cd ai-market-intelligence
```

2. **Set up backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

3. **Set up frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with backend API URL
npm run dev
```

### Docker Deployment

```bash
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔑 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=market_intelligence
SECRET_KEY=your_secret_key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📖 API Documentation

Once running, visit `/docs` for interactive API documentation (Swagger UI).

### Key Endpoints

- `POST /api/analyze/swot` - Generate SWOT analysis
- `POST /api/analyze/trends` - Detect market trends
- `POST /api/search/semantic` - Semantic search over documents
- `GET /api/reports/{id}` - Retrieve analysis report
- `POST /api/documents/ingest` - Ingest new documents

## 🎯 Use Cases

- **Market Research**: Analyze competitor strategies and market trends
- **Investment Analysis**: Generate insights for investment decisions
- **Strategic Planning**: Create SWOT analyses for business planning
- **Trend Detection**: Identify emerging patterns in industry data

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚢 Deployment

Deploy to cloud platforms:
- **Backend**: AWS Lambda, Google Cloud Run, Railway
- **Frontend**: Vercel, Netlify, AWS Amplify
- **Database**: MongoDB Atlas, AWS DocumentDB

## 📝 License

MIT License

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

Built as a portfolio project demonstrating:
- LLM integration and prompt engineering
- RAG implementation with vector databases
- Full-stack development with modern frameworks
- Production-ready architecture and deployment
