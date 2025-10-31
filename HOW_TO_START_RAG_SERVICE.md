# 🤖 How to Start the RAG Service

## Quick Start (Recommended)

### **Step 1: Open Terminal**
```bash
cd d:\project-mini\college-placement-portal
```

### **Step 2: Start RAG Service**

**Option A: Using Batch File (Easiest)**
```bash
START_RAG_SERVICE.bat
```

**Option B: Manual Start**
```bash
cd python-rag
python main.py
```

### **Step 3: Verify It's Running**

You should see:
```
Starting RAG Service (OpenRouter)
Port: 8001
Mode: OpenRouter RAG with Database Sync

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

---

## ✅ How to Test If It's Working

### Test 1: Health Check
Open browser and go to:
```
http://localhost:8001/health
```

Should see: `{"status": "healthy"}`

### Test 2: Test Query
```bash
cd python-rag
python test_rag.py
```

---

## 🔧 Troubleshooting

### Problem: "Module not found" Error

**Solution:** Activate virtual environment first
```bash
cd python-rag
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac
python main.py
```

### Problem: "Port 8001 already in use"

**Solution:** Kill existing process
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Then restart
START_RAG_SERVICE.bat
```

### Problem: "OpenRouter API Error"

**Solution:** Check your API key in `python-rag/config.env`
```env
OPENROUTER_API_KEY=your_key_here
```

---

## 📊 Service Ports

| Service | Port | URL |
|---------|------|-----|
| Laravel App | 8000 | http://localhost:8000 |
| RAG Service | 8001 | http://localhost:8001 |

---

## 🔗 Integration with Laravel

Once RAG service is running, your chatbot in the Laravel app will automatically connect to it.

**Test the chatbot:**
1. Login to student dashboard
2. Click the chatbot icon (bottom right)
3. Ask: "Show me available assessments"

---

## 🛑 How to Stop the Service

Press `Ctrl + C` in the terminal where RAG service is running.

---

## 📝 Service Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Send chat query |
| `/knowledge/sync` | POST | Sync knowledge base |
| `/student/{id}/context` | GET | Get student context |

---

## 🔄 Running Both Services Together

### Terminal 1: Laravel App
```bash
cd d:\project-mini\college-placement-portal
php artisan serve
```

### Terminal 2: RAG Service
```bash
cd d:\project-mini\college-placement-portal
START_RAG_SERVICE.bat
```

Now both services are running and the chatbot will work!

---

## ⚡ Quick Commands Reference

```bash
# Start Laravel
php artisan serve

# Start RAG Service
START_RAG_SERVICE.bat

# Test RAG Service
cd python-rag && python test_rag.py

# Check if RAG is running
curl http://localhost:8001/health

# View RAG logs
cd python-rag && type rag_service.log
```

---

## 💡 Tips

1. **Keep both terminals open** - One for Laravel, one for RAG
2. **Check logs** if chatbot doesn't work - Look at `python-rag/rag_service.log`
3. **Restart after code changes** - Press Ctrl+C and restart both services
4. **Update knowledge base** - Service auto-syncs with database every 5 minutes

---

## 🎯 Success Indicators

✅ RAG service shows "Uvicorn running on http://0.0.0.0:8001"
✅ Laravel app shows "Laravel development server started"
✅ Chatbot icon visible on student dashboard
✅ Chatbot responds to queries
✅ No errors in logs

---

## 📞 Need Help?

If you see errors, check:
1. Is Python installed? `python --version`
2. Are dependencies installed? `cd python-rag && pip install -r requirements.txt`
3. Is virtual environment activated? (You should see `(venv)` in terminal)
4. Is port 8001 free? Check with `netstat -ano | findstr :8001`

---

**Status:** ✅ Ready to use
**Last Updated:** October 16, 2025

