# 🌍 GPS Tracking System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-v4.0+-green.svg)](https://www.djangoproject.com/)
[![Nuxt.js](https://img.shields.io/badge/nuxt.js-v3.0+-brightgreen.svg)](https://nuxt.com/)
[![Vue.js](https://img.shields.io/badge/vue.js-v3.0+-4FC08D.svg)](https://vuejs.org/)

A professional full-stack GPS tracking system built with Django (backend) and Nuxt.js (frontend) for real-time monitoring and management of GPS devices. Designed for fleet management, device tracking, and location-based services.

![GPS Tracking Dashboard](https://via.placeholder.com/800x400/0EA5E9/FFFFFF?text=GPS+Tracking+Dashboard)

> **🎯 Perfect for:** Fleet management companies, logistics providers, device monitoring services, and any organization requiring real-time GPS tracking capabilities.

## 🌟 Features

### Backend (Django)

- **Real-time GPS Data Fetching**: Automated data collection from ProTrack365 API
- **Smart Data Management**: Automatic cleanup of old tracking logs (keeps latest 3 runs)
- **Real-time Time Calculations**: Dynamic "time since update" calculations using Unix timestamps
- **RESTful API**: Complete API for device data, statistics, and operations
- **Database Management**: PostgreSQL/SQLite support with Django ORM
- **Management Commands**: Custom Django commands for data operations

### Frontend (Nuxt.js)

- **Real-time Dashboard**: Live GPS tracking dashboard with auto-refresh
- **Interactive Interface**: Modern, responsive UI with real-time updates
- **Auto-refresh System**: Smart auto-refresh with GPS data fetching every 2.5 minutes
- **Data Export**: CSV export functionality
- **Statistics Display**: Device counts, GPS availability, and status overview
- **Pagination**: Efficient data display with pagination support

### Key Improvements

- **Intelligent Auto-refresh**: Updates display every 30 seconds + fetches new GPS data every 2.5 minutes
- **Automatic Cleanup**: Removes old tracking logs automatically, keeping only the 3 most recent
- **Real-time Calculations**: Time since last update calculated in real-time from Unix timestamps
- **Enhanced UI**: Visual feedback for all operations with loading states and notifications

## 🏗️ Project Structure

```
GPS_Tracking_System/
├── backend/                    # Django backend
│   ├── api/                   # Main API application
│   │   ├── management/        # Custom Django commands
│   │   │   └── commands/      # Management commands
│   │   ├── migrations/        # Database migrations
│   │   ├── services/          # External API services
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   └── urls.py            # URL routing
│   ├── protrack/              # Django project settings
│   ├── scripts/               # Utility scripts
│   │   ├── utils/             # Helper utilities
│   │   └── main.py            # Main data collection script
│   ├── response_logs/         # GPS data logs (auto-cleaned)
│   └── manage.py              # Django management script
├── frontend/                  # Nuxt.js frontend
│   └── nuxt-app/             # Nuxt application
│       ├── pages/            # Vue.js pages
│       ├── components/       # Vue.js components
│       ├── public/           # Static assets
│       └── nuxt.config.ts    # Nuxt configuration
└── README.md                 # This file
```

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/Vuth-Menghuor/GPS-Tracking-Systeam.git
cd GPS-Tracking-Systeam

# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install django djangorestframework django-cors-headers requests pandas
python manage.py migrate
python manage.py runserver

# Frontend setup (new terminal)
cd frontend/nuxt-app
npm install
npm run dev
```

🌐 **Access your application:**

- **Backend API**: http://localhost:8000
- **Frontend Dashboard**: http://localhost:3000

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git
- ProTrack365 API access (for GPS data)

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd GPS_Tracking_System/backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install django djangorestframework django-cors-headers requests pandas
   ```

4. **Configure database**

   ```bash
   python manage.py migrate
   ```

5. **Run backend server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend**

   ```bash
   cd ../frontend/nuxt-app
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

## 📋 API Endpoints

### Device Management

- `GET /devices/` - Get paginated device list
- `GET /stats/` - Get dashboard statistics
- `GET /export-csv/` - Export data to CSV

### Data Operations

- `POST /fetch-tracking/` - Fetch new GPS data from API
- `POST /load-database/` - Load GPS data to database
- `GET /logs/` - Get recent tracking logs

## 🔧 Configuration

### Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
PROTRACK_API_TOKEN=your-api-token
```

**Frontend (.env)**

```
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

## 🛠️ Management Commands

### Fetch GPS Data

```bash
python manage.py fetch_tracking_data
```

### Load Data to Database

```bash
python manage.py load_device_data path/to/data.json --clear-existing
```

### Update Relative Times

```bash
python manage.py update_relative_times
```

### Clear Device Data

```bash
python manage.py clear_device_data
```

## 📊 Features in Detail

### Auto-refresh System

- **Display Updates**: Every 30 seconds for real-time "time since update"
- **GPS Data Fetching**: Every 2.5 minutes (5 refresh cycles)
- **Automatic Database Loading**: New GPS data automatically loaded
- **User Control**: Toggle auto-refresh on/off

### Data Management

- **Smart Cleanup**: Automatically removes old tracking logs
- **Configurable Retention**: Keep latest N tracking runs (default: 3)
- **Real-time Calculations**: Time since update calculated dynamically
- **Export Functionality**: CSV export with all device data

### User Interface

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live data updates without page refresh
- **Visual Feedback**: Loading states and notifications
- **Pagination**: Efficient handling of large datasets

## 🔄 Data Flow

1. **GPS Data Collection**: ProTrack365 API → Django backend
2. **Data Processing**: Raw GPS data processed and stored
3. **Real-time Display**: Frontend fetches and displays data
4. **Auto-refresh**: System automatically updates with new GPS data
5. **Cleanup**: Old tracking logs automatically removed

## 🏃‍♂️ Development

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend/nuxt-app
npm run test
```

### Development Mode

- Backend: `python manage.py runserver` (http://localhost:8000)
- Frontend: `npm run dev` (http://localhost:3000)

## 📈 Recent Improvements

- ✅ Implemented automatic cleanup of old tracking logs
- ✅ Enhanced auto-refresh with intelligent GPS data fetching
- ✅ Added real-time time calculations using Unix timestamps
- ✅ Improved UI with better visual feedback and notifications
- ✅ Added countdown display for next GPS fetch
- ✅ Enhanced error handling and user experience

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please open an issue in the repository.

---

**Built with ❤️ for efficient GPS tracking and monitoring**
