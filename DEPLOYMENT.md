# 🚀 Deployment Guide - MediAlert Pro

This guide covers deployment options for the MediAlert Pro emergency medical system.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Environment Variables](#environment-variables)
6. [Security Considerations](#security-considerations)

## 🏠 Local Development

### Quick Start

```bash
# Install dependencies
uv sync

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
uv run python app.py
```

Access at: `http://localhost:5000`

## 🌐 Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
```bash
uv add gunicorn
```

2. **Create Gunicorn configuration**
```python
# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "logs/error.log"
accesslog = "logs/access.log"
loglevel = "info"
```

3. **Run with Gunicorn**
```bash
gunicorn -c gunicorn_config.py app:app
```

### Using uWSGI

1. **Install uWSGI**
```bash
uv add uwsgi
```

2. **Create uWSGI configuration**
```ini
# uwsgi.ini
[uwsgi]
module = app:app
master = true
processes = 4
socket = /tmp/medialert.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

3. **Run with uWSGI**
```bash
uwsgi --ini uwsgi.ini
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t medialert-pro .

# Run container
docker run -d -p 5000:5000 --env-file .env medialert-pro

# Or use Docker Compose
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
eb init -p python-3.11 medialert-pro
```

3. **Create environment**
```bash
eb create medialert-prod
```

4. **Deploy**
```bash
eb deploy
```

### Heroku

1. **Create Procfile**
```
web: gunicorn app:app
```

2. **Deploy**
```bash
heroku create medialert-pro
git push heroku main
heroku config:set GROQ_API_KEY=your_key_here
```

### Google Cloud Run

1. **Create cloudbuild.yaml**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/medialert-pro', '.']
images:
  - 'gcr.io/$PROJECT_ID/medialert-pro'
```

2. **Deploy**
```bash
gcloud run deploy medialert-pro \
  --image gcr.io/PROJECT_ID/medialert-pro \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

1. **Create Azure Web App**
```bash
az webapp create \
  --resource-group medialert-rg \
  --plan medialert-plan \
  --name medialert-pro \
  --runtime "PYTHON:3.11"
```

2. **Deploy**
```bash
az webapp up --name medialert-pro
```

## 🔐 Environment Variables

### Required Variables

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your_secret_key_here

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Security
API_RATE_LIMIT=1000
ALLOWED_ORIGINS=https://yourdomain.com
```

### Optional Variables

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/medialert/app.log

# Performance
WORKERS=4
TIMEOUT=120

# Features
ENABLE_API_DOCS=true
ENABLE_ADMIN_PANEL=true
```

## 🛡️ Security Considerations

### 1. HTTPS/SSL

Always use HTTPS in production:

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name medialert-pro.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. API Key Protection

Never commit API keys:

```bash
# .gitignore
.env
*.key
secrets/
```

### 3. Rate Limiting

Implement rate limiting:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.headers.get('X-API-Key'),
    default_limits=["1000 per hour"]
)
```

### 4. Input Validation

Always validate user input:

```python
from flask import request
from werkzeug.exceptions import BadRequest

@app.route('/api/alert', methods=['POST'])
def create_alert():
    data = request.get_json()
    
    if not data.get('symptomes'):
        raise BadRequest('Symptoms are required')
    
    # Process alert...
```

### 5. CORS Configuration

Configure CORS properly:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 📊 Monitoring

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      
      - name: Run tests
        run: uv run pytest
      
      - name: Deploy to production
        run: |
          # Your deployment commands
```

## 📈 Performance Optimization

### 1. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/api/hospitals')
@cache.cached(timeout=300)
def get_hospitals():
    # Cached for 5 minutes
    return jsonify(hospitals_data)
```

### 2. Database Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### 3. Async Processing

```python
from celery import Celery

celery = Celery('medialert', broker='redis://localhost:6379/0')

@celery.task
def process_emergency_alert(data):
    # Process alert asynchronously
    pass
```

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

2. **Permission denied**
```bash
# Fix file permissions
chmod +x app.py
```

3. **Module not found**
```bash
# Reinstall dependencies
uv sync --force
```

## 📞 Support

For deployment issues:
- GitHub Issues: https://github.com/ZouhairChoufa/medical-emergency-ai-system/issues
- Email: support@medialert-pro.com
- Documentation: http://localhost:5000/api-docs

---

**Last Updated**: 2024
**Version**: 1.0.0
