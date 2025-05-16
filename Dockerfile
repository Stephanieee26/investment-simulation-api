FROM python:3.10-slim

# 建立工作目錄
WORKDIR /app

# 複製需求檔與程式碼
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 啟動 FastAPI + Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
