# GDP Forecaster Dashboard - Deployment Guide

## 🚀 Quick Start

This is the frontend for the GDP Growth Prediction Model. It's a React + TypeScript application built with Vite.

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend API running (Flask server)

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.development .env.local
```

## ⚙️ Environment Configuration

Create a `.env.local` file (or `.env.production` for production):

```env
VITE_API_BASE_URL=http://localhost:5000
```

For production, update to your backend API URL:
```env
VITE_API_BASE_URL=https://your-backend-api.com
```

## 🏃 Running Locally

```bash
# Development mode with hot reload
npm run dev

# Open http://localhost:5173
```

## 🏗️ Building for Production

```bash
# Build the application
npm run build

# Preview the production build
npm run preview
```

The build output will be in the `dist/` folder.

## 🌐 Deployment Options

### Option 1: Vercel (Recommended)

1. Push code to GitHub (already done!)
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Add environment variable: `VITE_API_BASE_URL`
5. Deploy!

### Option 2: Netlify

1. Go to [netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Add environment variable: `VITE_API_BASE_URL`
6. Deploy!

### Option 3: Static Hosting (AWS S3, GitHub Pages, etc.)

```bash
# Build the app
npm run build

# Upload the dist/ folder to your hosting service
```

## 🔗 Backend Integration

This frontend connects to a Flask backend API. Make sure your backend is deployed and accessible.

### Required Backend Endpoints:

- `GET /api/countries` - Get list of all countries
- `GET /api/history?country={name}` - Get historical GDP data
- `POST /predict` - Submit prediction request

### CORS Configuration

Ensure your backend has CORS enabled for your frontend domain:

```python
from flask_cors import CORS
CORS(app, origins=["https://your-frontend-domain.com"])
```

## 📊 Features

- **203 Countries**: Select from all countries in the training dataset
- **Historical Data**: View GDP growth from 1972-2021
- **AI Predictions**: Get ML-powered GDP forecasts for 2022-2023
- **Interactive Charts**: Visualize trends with Recharts
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Hot module replacement in development

## 🧪 Testing

```bash
# Run tests (if configured)
npm test

# Type checking
npm run type-check
```

## 📦 Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Radix UI** - Accessible components

## 🐛 Troubleshooting

### White Screen Issue
- Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
- Check browser console for errors (F12)
- Verify backend API is running and accessible

### API Connection Issues
- Check `VITE_API_BASE_URL` in environment variables
- Verify CORS is enabled on backend
- Test API directly: `curl http://your-api-url/api/countries`

### Build Errors
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `rm -rf dist .vite`
- Update dependencies: `npm update`

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:5000` |

## 🔒 Security Notes

- Never commit `.env.local` or `.env.production` files
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting on backend API

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Repository**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git

**Last Updated**: February 2026
