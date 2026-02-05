# Frontend Requirements

## System Requirements

### Node.js & npm
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher

Check your versions:
```bash
node --version
npm --version
```

## Dependencies

All dependencies are listed in `package.json`. Install them with:

```bash
npm install
```

### Core Dependencies

#### Framework & Build Tools
- **react**: ^18.3.1 - UI framework
- **react-dom**: ^18.3.1 - React DOM renderer
- **vite**: ^6.3.5 - Build tool and dev server
- **typescript**: ^5.7.3 - Type safety

#### UI Components & Styling
- **@radix-ui/react-***: Various Radix UI components for accessible UI
- **tailwindcss**: ^4.1.0 - Utility-first CSS framework
- **lucide-react**: ^0.468.0 - Icon library
- **class-variance-authority**: ^0.7.1 - CSS variant management
- **clsx**: ^2.1.1 - Conditional className utility
- **tailwind-merge**: ^2.6.0 - Merge Tailwind classes

#### Data Visualization
- **recharts**: ^2.15.0 - Charting library for React

#### Animation
- **motion**: ^11.18.0 - Animation library (Framer Motion)

#### Form Handling
- **react-hook-form**: ^7.54.2 - Form state management
- **zod**: ^3.24.1 - Schema validation
- **@hookform/resolvers**: ^3.9.1 - Form validation resolvers

#### Date Handling
- **date-fns**: ^4.1.0 - Date utility library

#### Utilities
- **sonner**: ^1.7.3 - Toast notifications
- **vaul**: ^1.1.1 - Drawer component
- **cmdk**: ^1.0.4 - Command menu
- **embla-carousel-react**: ^8.5.2 - Carousel component
- **input-otp**: ^1.4.1 - OTP input component

### Development Dependencies

- **@types/react**: ^18.3.18 - React TypeScript types
- **@types/react-dom**: ^18.3.5 - React DOM TypeScript types
- **@vitejs/plugin-react**: ^4.3.4 - Vite React plugin
- **postcss**: ^8.4.49 - CSS processing
- **autoprefixer**: ^10.4.20 - CSS vendor prefixing
- **eslint**: ^9.18.0 - Code linting

## Environment Variables

Create a `.env.local` file with:

```env
VITE_API_BASE_URL=http://localhost:5000
```

For production, use `.env.production`:

```env
VITE_API_BASE_URL=https://your-production-api-url.com
```

## Browser Support

- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile browsers: iOS Safari 12+, Chrome Android

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git
   cd GDP_GROWTH_PREDICTION_MODEL-FRONTEND-
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.development .env.local
   # Edit .env.local with your backend API URL
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   ```
   http://localhost:5173
   ```

## Build Requirements

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

Build output will be in `dist/` folder.

### Preview Production Build
```bash
npm run preview
```

## Backend API Requirements

The frontend requires a Flask backend API with the following endpoints:

### Required Endpoints

1. **GET /api/countries**
   - Returns: Array of country names (203 countries)
   - Example: `["Albania", "Algeria", ...]`

2. **GET /api/history?country={name}**
   - Returns: Historical GDP data for the country (1972-2021)
   - Example:
     ```json
     [
       {
         "Country": "United States",
         "Year": 1972,
         "GDP_Growth": 5.3,
         "Exports_Growth": 4.2,
         "Imports_Growth": 3.8
       }
     ]
     ```

3. **POST /predict**
   - Request body:
     ```json
     {
       "Country": "United States",
       "Population": 1.1,
       "Exports": 5.2,
       "Imports": 4.8,
       "Investment": 3.5,
       "Consumption": 2.8,
       "Govt_Spend": 2.0
     }
     ```
   - Returns:
     ```json
     {
       "growth": 3.61,
       "method": "AI Model"
     }
     ```

### CORS Configuration

Backend must have CORS enabled:

```python
from flask_cors import CORS
CORS(app)
```

## Deployment Requirements

### Vercel
- Node.js 18+
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_BASE_URL`

### Netlify
- Node.js 18+
- Build command: `npm run build`
- Publish directory: `dist`
- Environment variable: `VITE_API_BASE_URL`

### Static Hosting (S3, GitHub Pages, etc.)
- Build the app: `npm run build`
- Upload `dist/` folder contents
- Configure environment variables before build

## Troubleshooting

### Installation Issues

**Problem**: `npm install` fails
```bash
# Solution 1: Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Solution 2: Use legacy peer deps
npm install --legacy-peer-deps
```

**Problem**: TypeScript errors
```bash
# Solution: Update TypeScript
npm install typescript@latest --save-dev
```

### Runtime Issues

**Problem**: White screen
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check browser console (F12) for errors
- Verify backend API is running

**Problem**: API connection fails
- Check `VITE_API_BASE_URL` in `.env.local`
- Verify backend CORS is enabled
- Test API: `curl http://localhost:5000/api/countries`

## Performance Optimization

### Production Build Optimization
- Code splitting enabled by default
- Tree shaking for unused code
- Minification and compression
- Asset optimization

### Recommended Settings
- Enable gzip/brotli compression on server
- Use CDN for static assets
- Implement caching headers
- Enable HTTP/2

## Security Considerations

- Never commit `.env.local` or `.env.production`
- Use HTTPS in production
- Implement Content Security Policy (CSP)
- Enable CORS only for trusted domains
- Sanitize user inputs
- Keep dependencies updated

## Updates & Maintenance

### Update Dependencies
```bash
# Check for updates
npm outdated

# Update all dependencies
npm update

# Update specific package
npm install package-name@latest
```

### Security Audit
```bash
npm audit
npm audit fix
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-/issues
- Check DEPLOYMENT.md for deployment guides
- Review package.json for exact versions

---

**Last Updated**: February 2026
