# Fix: ModuleNotFoundError - Installation Guide

## 🔧 Problem
The installation failed because `psycopg2-binary` requires PostgreSQL development files that aren't installed on Windows.

## ✅ Solution (Choose One)

### **Option 1: Use the Fixed Batch Script (EASIEST)**

```powershell
cd D:\project-mini\college-placement-portal\python-rag
.\install_dependencies.bat
```

This installs packages one by one to avoid build issues.

---

### **Option 2: Manual Step-by-Step (If Option 1 Fails)**

Open PowerShell in `python-rag` folder:

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 3. Install packages individually
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install requests==2.31.0
pip install colorama==0.4.6

# 4. Install ChromaDB and ML libraries
pip install chromadb==0.4.22
pip install sentence-transformers==2.2.2

# 5. Install psycopg2 (PostgreSQL driver)
pip install psycopg2-binary --no-build-isolation
```

---

### **Option 3: Alternative PostgreSQL Driver (If psycopg2 keeps failing)**

If `psycopg2-binary` still fails, use `psycopg` (newer version):

```powershell
# Skip psycopg2-binary, install everything else
pip install fastapi uvicorn[standard] python-dotenv pydantic requests chromadb sentence-transformers colorama

# Then install psycopg (Python 3.6+)
pip install psycopg[binary]
```

Then update `knowledge_sync.py` line 5:
```python
# Change from:
import psycopg2

# To:
import psycopg as psycopg2
```

---

## 🧪 Verify Installation

After installation, test:

```powershell
# Test imports
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
python -c "import chromadb; print('ChromaDB OK')"
python -c "import psycopg2; print('PostgreSQL driver OK')"
```

All should print "OK" without errors.

---

## 🚀 Start the Service

Once installed successfully:

```powershell
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## 🐛 Still Having Issues?

### Issue: "No module named 'chromadb'"
```powershell
pip install chromadb==0.4.22 --no-deps
pip install sentence-transformers==2.2.2
```

### Issue: "Microsoft Visual C++ 14.0 is required"
This affects psycopg2. Use Option 3 above (psycopg instead).

### Issue: "ImportError: DLL load failed"
```powershell
# Reinstall with fresh venv
cd ..
Remove-Item -Recurse -Force python-rag\venv
cd python-rag
python -m venv venv
.\venv\Scripts\Activate.ps1
.\install_dependencies.bat
```

---

## ✅ Quick Fix Commands (Copy & Paste)

```powershell
# Complete fresh install
cd D:\project-mini\college-placement-portal\python-rag
if (Test-Path venv) { Remove-Item -Recurse -Force venv }
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] python-dotenv pydantic requests chromadb sentence-transformers colorama psycopg2-binary --no-build-isolation
python main.py
```

---

## 📋 Installed Packages Checklist

After successful installation, you should have:

- ✅ fastapi (0.104.1)
- ✅ uvicorn (0.24.0)
- ✅ python-dotenv (1.0.0)
- ✅ pydantic (2.5.0)
- ✅ requests (2.31.0)
- ✅ psycopg2-binary (2.9.9) OR psycopg
- ✅ chromadb (0.4.22)
- ✅ sentence-transformers (2.2.2)
- ✅ colorama (0.4.6)

Check with: `pip list | findstr "fastapi uvicorn chromadb psycopg"`

---

**Status:** Installation fix provided  
**Next:** Run one of the options above, then `python main.py`

