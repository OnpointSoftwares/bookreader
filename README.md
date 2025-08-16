# BookReader

A modern, feature-rich digital book reading platform built with Django and PDF.js. BookReader provides an immersive reading experience with features like reading progress tracking, bookmarks, and responsive design that works across all devices.

## 🚀 Features

- 📖 PDF document viewer with smooth page navigation
- 📱 Responsive design for desktop, tablet, and mobile devices
- 🔖 Bookmark your favorite books and track reading progress
- 📊 Reading statistics and analytics
- 🔍 Full-text search functionality
- 🌙 Dark/Light mode support
- 📱 Touch gestures for mobile navigation
- 📊 Reading progress synchronization across devices

## 🛠️ Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **PDF Rendering**: PDF.js
- **Database**: SQLite (Development), PostgreSQL (Production-ready)
- **Styling**: Bootstrap 5 with custom theming
- **Icons**: Bootstrap Icons
- **Deployment**: Docker-ready configuration

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for frontend assets)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OnpointSoftwares/bookreader.git
   cd bookreader
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 📚 Project Structure

```
bookreader/
├── bookreader/               # Main project configuration
├── core/                     # Main application
│   ├── migrations/           # Database migrations
│   ├── static/               # Static files (CSS, JS, images)
│   ├── templates/            # HTML templates
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── urls.py              # URL routing
│   └── views.py             # View functions
├── media/                    # User-uploaded files
├── static/                   # Collected static files
├── templates/                # Base templates
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── manage.py                # Django management script
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## 🌐 Deployment

### Production

For production deployment, it's recommended to use:
- Gunicorn or uWSGI as the application server
- Nginx as the reverse proxy
- PostgreSQL as the database
- Redis for caching (optional)

### Docker

A `Dockerfile` and `docker-compose.yml` are provided for containerized deployment:

```bash
docker-compose up --build
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework used
- [PDF.js](https://mozilla.github.io/pdf.js/) - PDF rendering library
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
