# 🚀 Deployment Guide

This guide will help you deploy your GPS Tracking System to the web for free using Vercel (frontend) and Railway (backend).

## 📋 Prerequisites

- GitHub account
- Vercel account (free)
- Railway account (free)
- Your code pushed to a GitHub repository

## 🔧 Backend Deployment (Railway)

### Step 1: Prepare Your Backend

1. **Push your code to GitHub** (if not already done)
2. **Install additional dependencies** (already added to requirements.txt):
   ```bash
   cd backend
   pip install dj-database-url whitenoise gunicorn
   ```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)** and sign up with GitHub
2. **Create a New Project**
3. **Select "Deploy from GitHub repo"**
4. **Choose your GPS tracking repository**
5. **Add a PostgreSQL database**:
   - In your project dashboard, click "New"
   - Select "Database" → "PostgreSQL"
6. **Configure environment variables**:
   - Go to your app service → Variables
   - Add these variables:
     ```
     DEBUG=False
     SECRET_KEY=your-super-secret-key-here
     PROTRACK_API_TOKEN=your-protrack-api-token
     ```
   - Railway will automatically set `DATABASE_URL`

### Step 3: Configure Deployment

1. **Set the root directory** (if needed):

   - In Settings → General
   - Set "Root Directory" to `backend`

2. **Your app should automatically deploy!**
   - Railway will detect the `Procfile` and `requirements.txt`
   - Wait for deployment to complete
   - Note your Railway URL (e.g., `https://your-app-name.railway.app`)

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Your Frontend

1. **Update the API URL**:
   - Create `.env` file in `frontend/nuxt-app/`:
     ```
     NUXT_PUBLIC_API_BASE=https://your-backend-railway-url.railway.app/api
     ```

### Step 2: Deploy to Vercel

1. **Go to [Vercel.com](https://vercel.com)** and sign up with GitHub
2. **Import your project**:
   - Click "New Project"
   - Select your GPS tracking repository
   - Set "Root Directory" to `frontend/nuxt-app`
3. **Configure environment variables**:
   - In project settings, add:
     ```
     NUXT_PUBLIC_API_BASE=https://your-backend-railway-url.railway.app/api
     ```
4. **Deploy!**
   - Click "Deploy"
   - Your frontend will be available at `https://your-project.vercel.app`

## 🔄 Update Backend CORS Settings

After deployment, update your backend settings:

1. **Go to Railway dashboard**
2. **Add your Vercel URL to environment variables**:

   ```
   FRONTEND_URL=https://your-project.vercel.app
   ```

3. **Or update CORS settings in Django settings** (already configured for production)

## 🎉 You're Done!

Your GPS tracking system is now live!

- **Frontend**: `https://your-project.vercel.app`
- **Backend API**: `https://your-app-name.railway.app`

## 🔧 Alternative Deployment Options

### Free Alternatives:

1. **Netlify + Render** (similar to Vercel + Railway)
2. **GitHub Pages + PythonAnywhere** (for simpler projects)
3. **Heroku** (has free tier limitations)

### Professional Options:

1. **DigitalOcean App Platform** ($12-25/month)
2. **AWS Elastic Beanstalk + S3** ($20-50/month)
3. **Google Cloud Run + Cloud Storage** ($15-40/month)

## 📝 Deployment Checklist

- [ ] Backend deployed to Railway
- [ ] PostgreSQL database connected
- [ ] Environment variables configured
- [ ] Frontend deployed to Vercel
- [ ] API URL updated in frontend
- [ ] CORS settings configured
- [ ] SSL certificates enabled (automatic)
- [ ] Custom domain configured (optional)

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure your frontend URL is in CORS_ALLOWED_ORIGINS
2. **Database Connection**: Verify DATABASE_URL is set correctly
3. **Static Files**: Whitenoise should handle this automatically
4. **Environment Variables**: Double-check all required variables are set

### Useful Commands:

```bash
# Check Railway logs
railway logs

# Local testing
python manage.py collectstatic
python manage.py migrate
```

## 🚀 Next Steps

1. **Custom Domain**: Add your own domain in Vercel/Railway settings
2. **Monitoring**: Set up error tracking (Sentry)
3. **Analytics**: Add Google Analytics to track usage
4. **CDN**: Consider using Cloudflare for better performance
5. **Backup**: Set up database backups in Railway
