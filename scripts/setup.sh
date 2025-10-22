#!/bin/bash

echo "🚀 Setting up AI Market Intelligence Dashboard..."

# Check if .env files exist
if [ ! -f backend/.env ]; then
    echo "⚠️  Creating backend/.env from example..."
    cp backend/.env.example backend/.env
    echo "✅ Please edit backend/.env with your API keys"
fi

if [ ! -f frontend/.env.local ]; then
    echo "⚠️  Creating frontend/.env.local from example..."
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ frontend/.env.local created"
fi

echo ""
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env with your API keys (OpenAI, Pinecone)"
echo "2. Start MongoDB: docker-compose up mongodb -d"
echo "3. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "4. Start frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker Compose:"
echo "docker-compose up --build"
