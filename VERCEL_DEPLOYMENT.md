# Deploying GDP Forecaster to Vercel

## 🚀 Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Backend API deployed and accessible

### Step-by-Step Deployment

#### 1. Prepare Frontend

The frontend is already configured for Vercel with:
- ✅ `vercel.json` - Vercel configuration
- ✅ `.env.production` - Production environment variables
- ✅ `package.json` - Build scripts

#### 2. Deploy to Vercel

**Option A: Using Vercel Dashboard (Recommended)**

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your GitHub repository:
   ```
   https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git
   ```
4. Configure project:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

5. Add Environment Variable:
   - Key: `VITE_API_BASE_URL`
   - Value: Your backend URL (see backend deployment section)
   
6. Click "Deploy"

7. Wait for deployment (usually 2-3 minutes)

8. Your app will be live at: `https://your-project-name.vercel.app`

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? gdp-forecaster (or your choice)
# - Directory? ./
# - Override settings? No

# Add environment variable
vercel env add VITE_API_BASE_URL production

# Deploy to production
vercel --prod
```

#### 3. Configure Environment Variables

After deploying backend, update the environment variable:

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Edit `VITE_API_BASE_URL` with your backend URL
4. Click "Save"
5. Redeploy: Go to "Deployments" → Click "..." → "Redeploy"

#### 4. Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (up to 48 hours)

## 🐍 Backend Deployment Options

**Important**: Vercel has limited Python support. For production, use one of these alternatives:

### Option 1: Heroku (Recommended for Python)

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-gdp-api

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Your backend URL: https://your-gdp-api.herokuapp.com
```

### Option 2: Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select backend repository
4. Railway auto-detects Python
5. Deploy!
6. Get URL from dashboard

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Deploy
6. Get URL from dashboard

### Option 4: Vercel Serverless (Limited)

**Note**: Vercel Python support is limited. Model file (57MB) may be too large.

Create `api/index.py`:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simplified version - full model may not work due to size limits

@app.route('/')
def home():
    return jsonify({"status": "running"})

# Add other endpoints...

# Vercel serverless handler
def handler(request):
    return app(request)
```

Create `vercel.json` in backend:
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

**Limitations**:
- 50MB deployment size limit (model is 57MB)
- 10-second execution timeout
- Limited memory

**Recommendation**: Use Heroku, Railway, or Render for backend.

## 🔗 Connecting Frontend to Backend

After deploying both:

1. **Get Backend URL**:
   - Heroku: `https://your-app-name.herokuapp.com`
   - Railway: `https://your-app-name.up.railway.app`
   - Render: `https://your-app-name.onrender.com`

2. **Update Frontend Environment Variable**:
   ```bash
   # In Vercel dashboard
   Settings → Environment Variables → VITE_API_BASE_URL
   # Set to your backend URL
   ```

3. **Update Backend CORS**:
   ```python
   # In app.py
   CORS(app, origins=[
       "https://your-frontend.vercel.app",
       "https://your-custom-domain.com"
   ])
   ```

4. **Redeploy Both**:
   - Backend: `git push heroku main` (or your platform)
   - Frontend: Vercel auto-redeploys on git push

## ✅ Deployment Checklist

### Frontend (Vercel)
- [ ] Repository pushed to GitHub
- [ ] Vercel project created
- [ ] Build settings configured
- [ ] Environment variable `VITE_API_BASE_URL` set
- [ ] Deployment successful
- [ ] Custom domain configured (optional)

### Backend (Heroku/Railway/Render)
- [ ] Repository pushed to GitHub
- [ ] Platform account created
- [ ] Project deployed
- [ ] Backend URL obtained
- [ ] CORS configured with frontend URL
- [ ] API endpoints tested

### Integration
- [ ] Frontend environment variable updated with backend URL
- [ ] Backend CORS allows frontend domain
- [ ] Test API connection from frontend
- [ ] Test all features (country list, historical data, predictions)

## 🧪 Testing Deployment

### Test Frontend
```bash
# Open in browser
https://your-project.vercel.app

# Check console (F12) for errors
# Test country selection
# Test prediction functionality
```

### Test Backend
```bash
# Health check
curl https://your-backend-url.com/

# Countries list
curl https://your-backend-url.com/api/countries

# Historical data
curl "https://your-backend-url.com/api/history?country=United%20States"

# Prediction
curl -X POST https://your-backend-url.com/predict \
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

## 🐛 Troubleshooting

### Frontend Issues

**White Screen**
- Check browser console for errors
- Verify `VITE_API_BASE_URL` is set correctly
- Hard refresh: Ctrl+Shift+R

**API Connection Failed**
- Verify backend is running
- Check CORS configuration
- Verify environment variable

### Backend Issues

**Model Not Loading**
- Check file size limits on platform
- Consider using external storage for model
- Verify all dependencies installed

**CORS Errors**
- Update CORS origins in `app.py`
- Redeploy backend
- Clear browser cache

## 💰 Cost Estimates

### Free Tier Limits

**Vercel (Frontend)**
- ✅ 100 GB bandwidth/month
- ✅ Unlimited projects
- ✅ Automatic HTTPS
- ✅ Custom domains

**Heroku (Backend)**
- ✅ 550-1000 dyno hours/month (free)
- ⚠️ Sleeps after 30 min inactivity
- ⚠️ 512 MB RAM

**Railway (Backend)**
- ✅ $5 free credit/month
- ✅ No sleep
- ✅ 512 MB RAM

**Render (Backend)**
- ✅ 750 hours/month free
- ⚠️ Spins down after inactivity
- ✅ 512 MB RAM

## 🚀 Production Recommendations

1. **Frontend**: Vercel ✅ (Perfect for React/Vite)
2. **Backend**: Railway or Render (Better Python support than Vercel)
3. **Database**: Not needed (using CSV files)
4. **Monitoring**: Add Sentry for error tracking
5. **Analytics**: Add Google Analytics or Vercel Analytics

## 📞 Support

- **Frontend Repo**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git
- **Backend Repo**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-.git
- **Vercel Docs**: https://vercel.com/docs
- **Heroku Docs**: https://devcenter.heroku.com/

---

**Last Updated**: February 2026
