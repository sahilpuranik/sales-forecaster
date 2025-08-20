# 🚀 Deployment Guide

This guide covers deploying the SalesForecaster application to production environments.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Server with at least 2GB RAM
- Domain name (optional but recommended)

## 🐳 Docker Deployment (Recommended)

### 1. Create Dockerfile

```dockerfile
# Use multi-stage build for smaller image
FROM python:3.11-slim as backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY App/ ./App/
COPY FlaskBackend/ ./FlaskBackend/
COPY data/ ./data/

EXPOSE 5000
CMD ["python", "FlaskBackend/run.py"]

# Frontend build
FROM node:18-alpine as frontend

WORKDIR /app
COPY ReactFrontEnd/package*.json ./
RUN npm ci --only=production

COPY ReactFrontEnd/ ./
RUN npm run build

# Production image
FROM nginx:alpine
COPY --from=frontend /app/dist /usr/share/nginx/html
COPY --from=backend /app /app/backend

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

### 2. Create nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server localhost:5000;
    }

    server {
        listen 80;
        server_name localhost;

        # Serve frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Proxy API calls to backend
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 3. Create docker-compose.yml

```yaml
version: '3.8'

services:
  salesforecaster:
    build: .
    ports:
      - "80:80"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    restart: unless-stopped
```

### 4. Deploy

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   ```bash
   # Ubuntu 22.04 LTS, t3.medium or larger
   # Security group: HTTP (80), HTTPS (443), SSH (22)
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nodejs npm nginx
   ```

3. **Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd SalesForecaster
   ```

4. **Setup Backend**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Setup Frontend**
   ```bash
   cd ReactFrontEnd
   npm install
   npm run build
   ```

6. **Configure Nginx**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/salesforecaster
   sudo ln -s /etc/nginx/sites-available/salesforecaster /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **Setup Systemd Service**
   ```bash
   sudo cp salesforecaster.service /etc/systemd/system/
   sudo systemctl enable salesforecaster
   sudo systemctl start salesforecaster
   ```

### Heroku Deployment

1. **Create Procfile**
   ```
   web: gunicorn FlaskBackend.run:app
   ```

2. **Update requirements.txt**
   ```
   gunicorn==21.2.0
   ```

3. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

## 🔧 Environment Configuration

### Production Settings

Create `.env` file:
```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/salesforecaster
```

### Security Considerations

1. **HTTPS Setup**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Get SSL certificate
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Firewall Configuration**
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

3. **Database Setup** (Optional)
   ```bash
   # PostgreSQL
   sudo apt install postgresql postgresql-contrib
   sudo -u postgres createdb salesforecaster
   ```

## 📊 Monitoring & Logging

### Application Logs
```bash
# View logs
sudo journalctl -u salesforecaster -f

# Log rotation
sudo logrotate /etc/logrotate.d/salesforecaster
```

### Performance Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor resources
htop
df -h
free -h
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest tests/
      
      - name: Deploy to Server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          script: |
            cd /path/to/app
            git pull origin main
            docker-compose up -d --build
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Permission Errors**
   ```bash
   sudo chown -R $USER:$USER /path/to/app
   chmod +x scripts/deploy.sh
   ```

3. **Memory Issues**
   ```bash
   # Increase swap
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Health Checks

```bash
# Check if services are running
sudo systemctl status nginx
sudo systemctl status salesforecaster

# Test API endpoints
curl http://localhost:5000/
curl http://localhost:5000/docs
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ALB, nginx)
- Multiple application instances
- Database clustering

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layer (Redis)

### Performance Optimization
```python
# Add caching
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis'})

@app.route('/forecast')
@cache.cached(timeout=300)  # Cache for 5 minutes
def forecast():
    # Your forecast logic
    pass
```

## 🔐 Security Checklist

- [ ] HTTPS enabled
- [ ] Firewall configured
- [ ] Regular security updates
- [ ] Database backups
- [ ] Environment variables secured
- [ ] Rate limiting implemented
- [ ] Input validation
- [ ] Error handling

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify environment configuration
3. Test locally first
4. Review security settings
5. Contact system administrator
