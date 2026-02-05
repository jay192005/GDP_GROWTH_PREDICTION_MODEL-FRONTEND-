# Backend Deployment Guide

## 🚀 Quick Deploy

### Prerequisites
- Python 3.13+
- pip
- Git

### Local Setup

```bash
# Clone repository
git clone https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-.git
cd GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server will be available at: `http://127.0.0.1:5000`

## 🌐 Production Deployment

### Option 1: Heroku (Recommended)

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Add Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

3. **Add gunicorn to requirements**
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

4. **Deploy**
   ```bash
   heroku login
   heroku create your-gdp-api
   git push heroku main
   ```

5. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

6. **Open app**
   ```bash
   heroku open
   ```

### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t2.micro (free tier) or t2.small
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect to instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. **Clone and setup**
   ```bash
   git clone https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-.git
   cd GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Run with gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

6. **Setup Nginx (optional)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Setup systemd service**
   ```bash
   sudo nano /etc/systemd/system/gdp-api.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=GDP Prediction API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-
   Environment="PATH=/home/ubuntu/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-/venv/bin"
   ExecStart=/home/ubuntu/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable gdp-api
   sudo systemctl start gdp-api
   ```

### Option 3: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.13-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["python", "app.py"]
   ```

2. **Build image**
   ```bash
   docker build -t gdp-prediction-api .
   ```

3. **Run container**
   ```bash
   docker run -d -p 5000:5000 --name gdp-api gdp-prediction-api
   ```

4. **Deploy to Docker Hub**
   ```bash
   docker tag gdp-prediction-api your-username/gdp-api:latest
   docker push your-username/gdp-api:latest
   ```

### Option 4: Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Add environment variables if needed
6. Get your deployment URL

### Option 5: Render

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Deploy!

## ⚙️ Environment Configuration

### Production Settings

Update `app.py` for production:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### CORS Configuration

For production, restrict CORS to your frontend domain:

```python
from flask_cors import CORS

# Development
CORS(app)

# Production
CORS(app, origins=[
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com"
])
```

### Environment Variables

Set these in production:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000
```

## 🔒 Security Checklist

- [ ] Disable debug mode in production
- [ ] Restrict CORS to specific domains
- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Add rate limiting
- [ ] Implement authentication for sensitive endpoints
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable logging and monitoring
- [ ] Set up firewall rules
- [ ] Regular security audits

## 📊 Monitoring

### Health Check Endpoint

```bash
curl https://your-api-url.com/
```

Should return:
```json
{
  "status": "running",
  "model_loaded": true,
  "encoder_loaded": true
}
```

### Logging

Add logging to `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Performance Monitoring

Consider adding:
- **New Relic**: Application performance monitoring
- **Sentry**: Error tracking
- **Datadog**: Infrastructure monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.13'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_api.py
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 🧪 Testing in Production

```bash
# Test health
curl https://your-api-url.com/

# Test countries
curl https://your-api-url.com/api/countries

# Test historical data
curl "https://your-api-url.com/api/history?country=United%20States"

# Test prediction
curl -X POST https://your-api-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Country": "United States",
    "Population": 1.1,
    "Exports": 5.2,
    "Imports": 4.8,
    "Investment": 3.5,
    "Consumption": 2.8,
    "Govt_Spend": 2.0
  }'
```

## 📈 Scaling

### Horizontal Scaling

- Use load balancer (AWS ELB, Nginx)
- Deploy multiple instances
- Use Redis for caching
- Implement request queuing

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize model loading
- Use model caching
- Implement database connection pooling

## 🐛 Troubleshooting

### Model File Too Large

GitHub has a 50MB file size limit. The model is 57.56 MB.

**Solution 1: Git LFS**
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add gdp_model.pkl
git commit -m "Add model with Git LFS"
git push
```

**Solution 2: External Storage**
- Upload model to S3/Google Cloud Storage
- Download on server startup
- Update `app.py` to load from URL

### Port Issues

If port 5000 is in use:
```bash
# Change port in app.py
app.run(port=8000)

# Or use environment variable
PORT=8000 python app.py
```

### Memory Issues

If server runs out of memory:
- Increase server RAM
- Optimize model (reduce estimators)
- Use model compression
- Implement lazy loading

## 📞 Support

- **Issues**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-/issues
- **Frontend**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git

---

**Repository**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-.git
**Last Updated**: February 2026
