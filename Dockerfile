
FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt .
COPY fastAPI.py .
COPY BestModel.pkl .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "fastAPI:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]