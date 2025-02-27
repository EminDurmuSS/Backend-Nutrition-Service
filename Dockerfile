FROM python:3.12-slim

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run with optimized settings
CMD ["gunicorn","-k", "uvicorn.workers.UvicornWorker","--bind", "0.0.0.0:5000", "--timeout", "1000", "--keep-alive", "1000", "--preload", "main:main"]