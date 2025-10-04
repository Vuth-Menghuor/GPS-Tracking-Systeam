# 🚀 Render Deployment Guide

Your GPS Tracking System is ready to deploy on Render! Since Render has connected to your GitHub account, follow these steps:

## 🌐 **Step 1: Deploy Backend (Django) on Render**

### **Create Web Service**
1. **Go to your Render Dashboard** (render.com/dashboard)
2. **Click "New +"** → **"Web Service"**
3. **Connect Repository**: Select `GPS-Tracking-Systeam`
4. **Configure the service**:
   - **Name**: `gps-tracking-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn protrack.wsgi:application`

### **Environment Variables**
Add these in the Environment tab:
```
DEBUG=False
SECRET_KEY=gps-tracking-super-secret-key-change-2024
PROTRACK_API_TOKEN=your-protrack-api-token
PYTHON_VERSION=3.12.0
```

### **Add PostgreSQL Database**
1. **Click "New +"** → **"PostgreSQL"**
2. **Name**: `gps-tracking-db`
3. **Copy the Internal Database URL**
4. **Add to your web service environment variables**:
   ```
   DATABASE_URL=your-internal-database-url-from-render
   ```

## 🌐 **Step 2: Deploy Frontend (Nuxt.js) on Vercel**

1. **Go to [Vercel.com](https://vercel.com)**
2. **Import your GitHub repository**: `GPS-Tracking-Systeam`
3. **Set Root Directory**: `frontend/nuxt-app`
4. **Environment Variables**:
   ```
   NUXT_PUBLIC_API_BASE=https://your-render-backend-url.onrender.com/api
   ```
5. **Deploy!**

## 🔄 **Step 3: Final Configuration**

1. **Update Render backend** with frontend URL:
   ```
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```

2. **Redeploy both services**

## ✅ **Your URLs will be**:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-service.onrender.com`

## 🆓 **Free Tier Limits**:
- **Render Free**: 750 hours/month, sleeps after 15 min inactivity
- **Vercel Free**: Unlimited static sites, 100GB bandwidth

## 🛠️ **Troubleshooting**:
- **Cold starts**: Free tier services sleep, first request may be slow
- **Database**: Use internal URL for better performance
- **CORS**: Already configured for production