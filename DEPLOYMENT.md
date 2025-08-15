# KickCast Deployment Guide

## Current Status
Your application is currently deployed to GitHub Pages, but it needs a backend server to function properly.

## Issues with Current Deployment
- GitHub Pages only serves static files (HTML, CSS, JS)
- Your Flask backend API calls won't work on GitHub Pages
- The 404 errors you're seeing are because the backend isn't available

## Solutions

### Option 1: Deploy Backend to Render (Recommended)

1. **Create a Render account** at https://render.com
2. **Connect your GitHub repository**
3. **Create a new Web Service**
4. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
5. **Add environment variables if needed**
6. **Deploy**

### Option 2: Deploy Backend to Railway

1. **Create a Railway account** at https://railway.app
2. **Connect your GitHub repository**
3. **Railway will auto-detect Python and deploy**
4. **Get your deployment URL**

### Option 3: Deploy Backend to Heroku

1. **Create a Heroku account**
2. **Install Heroku CLI**
3. **Create a `Procfile`** with: `web: python app.py`
4. **Deploy using Heroku CLI**

## Update Frontend Configuration

After deploying your backend, update the `API_BASE` URL in `static/script.js`:

```javascript
const API_BASE = isLocal ? 'http://127.0.0.1:5000' : 'https://your-backend-url.onrender.com';
```

## Quick Fix for Testing

For now, you can test the frontend locally:

1. **Start your Flask server locally:**
   ```bash
   source .venv/bin/activate
   python3 app.py
   ```

2. **Access at:** `http://localhost:5000`

## Next Steps

1. Choose a backend deployment option
2. Deploy your Flask app
3. Update the API_BASE URL in the frontend
4. Push changes to GitHub
5. Your GitHub Pages site will now work with the deployed backend

## Alternative: Static-Only Version

If you want to deploy without a backend, we can modify the app to use only static JSON data, but this will limit functionality.
