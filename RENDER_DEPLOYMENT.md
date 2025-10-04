# 🚀 Render Deployment Guide

## Backend Deployment on Render (FREE)

### Step 1: After Account Confirmation

1. **Go to Render Dashboard**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**: `GPS-Tracking-Systeam`

### Step 2: Configure Web Service

**Basic Settings:**

- **Name**: `gps-tracking-backend`
- **Region**: Select closest to you
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**Build & Deploy:**

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn protrack.wsgi:application`

### Step 3: Environment Variables

Add these in the "Environment" section:

```
DEBUG=False
SECRET_KEY=gps-tracking-super-secret-key-render-2024
PROTRACK_API_TOKEN=your-protrack-token-here
```

### Step 4: Add PostgreSQL Database

1. **In Render Dashboard**: Click "New +" → "PostgreSQL"
2. **Name**: `gps-tracking-db`
3. **Copy the Internal Database URL**
4. **Add to your web service environment variables**:
   ```
   DATABASE_URL=postgresql://username:password@hostname:port/database
   ```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Your backend will be live** at: `https://your-service-name.onrender.com`

## Render vs Railway Benefits

✅ **FREE Forever** (no trial period)
✅ **Automatic HTTPS**
✅ **PostgreSQL included**
✅ **750 hours/month** (enough for small projects)
✅ **No credit card required**

## After Backend Deployment

1. **Copy your Render URL**
2. **Deploy frontend to Vercel** with:
   ```
   NUXT_PUBLIC_API_BASE=https://your-render-url.onrender.com/api
   ```
