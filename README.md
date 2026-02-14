# 🏠 Hostel Management System

A modern, full-stack **Hostel Management System** built with Django and Supabase PostgreSQL. Designed for college-level hostel administration with separate student and admin dashboards.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.8-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ Features

### 🎯 For Students

- ✅ User registration and authentication
- ✅ Browse available hostel rooms
- ✅ Apply for room allocation
- ✅ Track application status
- ✅ View allocated room details
- ✅ Submit complaints and feedback
- ✅ Dashboard with quick stats

### 👨‍💼 For Administrators

- ✅ Comprehensive admin dashboard
- ✅ Room management (add, edit, delete)
- ✅ Review room allocation requests
- ✅ Approve or reject applications
- ✅ Manage student records
- ✅ Monitor hostel occupancy
- ✅ Handle complaints and feedback
- ✅ Generate reports

---

## 🏗️ Tech Stack

| Component          | Technology                           |
| ------------------ | ------------------------------------ |
| **Backend**        | Django 4.2.8                         |
| **Database**       | Supabase PostgreSQL                  |
| **Frontend**       | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Authentication** | Django Built-in Auth                 |
| **ORM**            | Django ORM                           |
| **Server**         | Gunicorn, WhiteNoise                 |

---

## 📁 Project Structure

```
hostel_project/
│
├── hostel_project/           # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
├── hostel_app/              # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   └── __init__.py
│
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── navbar.html
│   ├── footer.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── room_list.html
│   ├── complaints.html
│   ├── admin_dashboard.html
│   ├── admin_manage_rooms.html
│   ├── admin_manage_applications.html
│   ├── admin_manage_students.html
│   └── admin_manage_complaints.html
│
├── static/                  # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Supabase PostgreSQL account
- Virtual environment (recommended)

### Installation Steps

#### 1. Clone or Download the Project

```bash
cd hostel_project
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your Supabase credentials
nano .env
```

#### 5. Database Setup with Supabase

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Get your connection details from Project Settings > Database
4. Update `.env` with:
   ```
   DB_HOST=your-project.supabase.co
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_NAME=postgres
   DB_PORT=5432
   ```

#### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Follow the prompts to create admin credentials
```

#### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 9. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🔐 Default Access

### Admin Login

- **URL**: `http://localhost:8000/login/`
- **Username**: admin (created via createsuperuser)
- **Dashboard**: `http://localhost:8000/admin/dashboard/`

### Student Registration

- **URL**: `http://localhost:8000/register/`
- **Login**: `http://localhost:8000/login/`

---

## 📊 Database Models

### StudentProfile

- user (OneToOne → User)
- full_name
- department
- year
- phone_number
- address
- guardian_name

### Room

- room_number (unique)
- block_name
- floor
- capacity
- current_occupancy
- room_type (Single/Double/Shared)
- status (Available/Full/Maintenance)
- amenities

### RoomAllocation

- student (ForeignKey → User)
- room (ForeignKey → Room)
- status (Pending/Approved/Rejected)
- applied_date
- allocated_date
- rejection_reason

### Complaint

- student (ForeignKey → User)
- subject
- description
- status (Pending/In Progress/Resolved)
- priority (Low/Medium/High)
- room (ForeignKey → Room, optional)
- resolution_notes
- created_at

---

## 📋 API Endpoints

### Student Routes

| Endpoint              | Method    | Purpose                |
| --------------------- | --------- | ---------------------- |
| `/register/`          | GET, POST | Student registration   |
| `/login/`             | GET, POST | Student login          |
| `/student/dashboard/` | GET       | Student dashboard      |
| `/rooms/`             | GET       | Browse rooms           |
| `/rooms/<id>/apply/`  | POST      | Apply for room         |
| `/my-applications/`   | GET       | View applications      |
| `/complaints/`        | GET, POST | View/submit complaints |

### Admin Routes

| Endpoint                  | Method    | Purpose           |
| ------------------------- | --------- | ----------------- |
| `/admin/dashboard/`       | GET       | Admin dashboard   |
| `/admin/rooms/`           | GET       | Manage rooms      |
| `/admin/rooms/add/`       | GET, POST | Add room          |
| `/admin/rooms/<id>/edit/` | GET, POST | Edit room         |
| `/admin/applications/`    | GET       | View applications |
| `/admin/students/`        | GET       | View students     |
| `/admin/complaints/`      | GET       | View complaints   |

---

## ⚙️ Configuration

### settings.py

Key configurations you might need to adjust:

```python
# Secret Key (CHANGE IN PRODUCTION)
SECRET_KEY = 'your-secret-key'

# Debug Mode
DEBUG = True  # False in production

# Allowed Hosts
ALLOWED_HOSTS = ['*']  # Restrict in production

# Database (Supabase)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'your-supabase-host',
        'PORT': '5432',
    }
}
```

---

## 🧪 Sample Test Data

### Add Sample Admin

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### Create Sample Rooms

```bash
python manage.py shell
```

```python
from hostel_app.models import Room

# Block A
Room.objects.create(
    room_number="A101",
    block_name="Block A",
    floor=1,
    capacity=2,
    room_type="Double",
    status="Available",
    amenities="WiFi, Fan, Bed, Study Table"
)

Room.objects.create(
    room_number="A201",
    block_name="Block A",
    floor=2,
    capacity=3,
    room_type="Shared",
    status="Available",
    amenities="WiFi, Fan, Beds, Study Tables"
)
```

---

## 📦 Production Deployment

### Recommended Hosting Platforms

- **Heroku** (Free tier available)
- **PythonAnywhere**
- **Digital Ocean**
- **AWS** (Elastic Beanstalk)

### Key Production Changes

1. Set `DEBUG = False`
2. Generate a new `SECRET_KEY`
3. Set `ALLOWED_HOSTS` properly
4. Use environment-specific settings
5. Enable HTTPS
6. Use a production-grade server (Gunicorn + Nginx)
7. Configure static files serving (WhiteNoise or CDN)

### Deployment Checklist

- [ ] Update `.env` for production
- [ ] Run `collectstatic`
- [ ] Set up database backups
- [ ] Configure email service
- [ ] Enable security headers
- [ ] Set up monitoring/logging
- [ ] Test all features

---

## 🐛 Troubleshooting

### Issue: PostgreSQL connection failed

**Solution**:

- Verify Supabase credentials in `.env`
- Check network connection to Supabase
- Ensure firewall allows connections

### Issue: Static files not loading

**Solution**:

```bash
python manage.py collectstatic --noinput --clear
```

### Issue: Migrations not applied

**Solution**:

```bash
python manage.py migrate --run-syncdb
```

### Issue: CSRF token errors

**Solution**:

- Ensure `{% csrf_token %}` in all POST forms
- Check `CSRF_COOKIE_SECURE` setting

---

## 📚 Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Developed by**: Your Name/Organization

---

## 📞 Support

For issues or questions, please:

- Create an issue in the repository
- Check existing documentation
- Contact: support@hostelhub.edu

---

## 🎉 Changelog

### Version 1.0.0 (Initial Release)

- ✅ Full hostel management system
- ✅ Student authentication and dashboard
- ✅ Room allocation system
- ✅ Complaint management
- ✅ Admin dashboard
- ✅ Modern responsive UI

---

**Built with ❤️ for College Hostel Management**
