# Quick Start Guide 🚀

Get the AI Market Intelligence Dashboard running in **5 minutes**!

## 📋 What You'll Need

1. **API Keys** (Get these first):
   - [OpenAI API Key](https://platform.openai.com/api-keys) - $5 minimum credit
   - [Pinecone API Key](https://www.pinecone.io/) - Free tier available

2. **Software** (If not using Docker):
   - Node.js 18+
   - Python 3.11+
   - MongoDB (or use Docker)

## ⚡ Option 1: Docker (Recommended)

```bash
# 1. Clone and navigate
cd ~/ai-market-intelligence

# 2. Set up environment
cp backend/.env.example backend/.env

# 3. Edit backend/.env with your keys
# Add your OPENAI_API_KEY and PINECONE_API_KEY

# 4. Start everything
docker-compose up --build

# Done! Visit http://localhost:3000
```

## 💻 Option 2: Local Development

```bash
# 1. Navigate to project
cd ~/ai-market-intelligence

# 2. Run setup script
./scripts/setup.sh

# 3. Edit backend/.env with your API keys
nano backend/.env  # or use your favorite editor

# 4. Start MongoDB
docker-compose up mongodb -d

# 5. Start backend (Terminal 1)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 6. Start frontend (Terminal 2)
cd frontend
npm run dev

# Visit http://localhost:3000
```

## 🎯 First Steps

### 1. Try SWOT Analysis
- Click **"SWOT Analysis"** tab
- Enter company: **Tesla**
- Enter industry: **clean_tech**
- Click **"Generate SWOT Analysis"**

### 2. Try Trend Analysis
- Click **"Trend Analysis"** tab
- Enter industry: **clean_tech**
- Time period: **Q1 2024**
- Click **"Analyze Trends"**

## 📊 Add Sample Data (Optional)

```bash
cd backend
source venv/bin/activate
python ../scripts/seed_data.py
```

This adds 5 sample articles about clean tech and EVs.

## 🔧 Troubleshooting

### "Connection refused" error
- Check if MongoDB is running: `docker ps`
- Start it: `docker-compose up mongodb -d`

### "Invalid API key" error
- Double-check your `.env` file has the correct keys
- Restart the backend after editing `.env`

### Port already in use
```bash
# Kill port 8000
lsof -ti:8000 | xargs kill -9

# Kill port 3000
lsof -ti:3000 | xargs kill -9
```

## 📚 Next Steps

- **Read full docs**: `docs/GETTING_STARTED.md`
- **Understand architecture**: `docs/ARCHITECTURE.md`
- **API docs**: http://localhost:8000/docs

## 🎓 What You Built

✅ Full-stack AI application  
✅ LLM integration (GPT-4)  
✅ RAG with vector database  
✅ Modern frontend (Next.js)  
✅ RESTful API (FastAPI)  
✅ Docker deployment  
✅ Production-ready structure  

Perfect for your **Enki.ai portfolio**! 🎉

## 🚀 Push to GitHub

```bash
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-market-intelligence.git
git branch -M main
git push -u origin main
```

**Update README.md** with your GitHub username before pushing!
