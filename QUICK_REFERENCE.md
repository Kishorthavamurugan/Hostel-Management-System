# Quick Reference Guide - Hostel Management System

## Essential Commands

### Setup & Initialization

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create admin
python manage.py createsuperuser

# Generate sample data
python manage.py generate_sample_data

# Collect static files
python manage.py collectstatic --noinput
```

### Running Application

```bash
# Development server
python manage.py runserver

# With specific port
python manage.py runserver 8001

# With specific host
python manage.py runserver 0.0.0.0:8000
```

### Database

```bash
# Database shell
python manage.py dbshell

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Migrate specific app
python manage.py migrate hostel_app

# Show migration plan
python manage.py showmigrations

# Reset database
python manage.py migrate hostel_app zero
```

### Django Administration

```bash
# Django shell
python manage.py shell

# Check configuration
python manage.py check

# Clear cache
python manage.py clear_cache
```

---

## Django Shell Commands

```python
# Import models
from django.contrib.auth.models import User
from hostel_app.models import StudentProfile, Room, RoomAllocation, Complaint

# View all users
User.objects.all()

# Create user
User.objects.create_user('username', 'email@example.com', 'password')

# Create student
StudentProfile.objects.create(
    user=user,
    full_name='Name',
    department='CSE',
    year=1,
    phone_number='1234567890',
    address='Address',
    guardian_name='Guardian'
)

# View rooms
Room.objects.all()

# Create room
Room.objects.create(
    room_number='A101',
    block_name='Block A',
    floor=1,
    capacity=2,
    room_type='Double',
    status='Available'
)

# Filter
Room.objects.filter(status='Available')
Room.objects.filter(block_name='Block A')

# Update
room = Room.objects.get(room_number='A101')
room.status = 'Full'
room.save()

# Delete
room.delete()

# Aggregate
from django.db.models import Count
Room.objects.aggregate(Count('id'))
```

---

## Common URLs

### Student URLs

- Register: `http://localhost:8000/register/`
- Login: `http://localhost:8000/login/`
- Dashboard: `http://localhost:8000/student/dashboard/`
- Rooms: `http://localhost:8000/rooms/`
- Applications: `http://localhost:8000/my-applications/`
- Complaints: `http://localhost:8000/complaints/`
- Logout: `http://localhost:8000/logout/`

### Admin URLs

- Dashboard: `http://localhost:8000/admin/dashboard/`
- Rooms: `http://localhost:8000/admin/rooms/`
- Add Room: `http://localhost:8000/admin/rooms/add/`
- Applications: `http://localhost:8000/admin/applications/`
- Students: `http://localhost:8000/admin/students/`
- Complaints: `http://localhost:8000/admin/complaints/`

### Django Admin

- Admin Panel: `http://localhost:8000/admin/`

---

## Test Credentials

### Admin

- **Username**: `admin`
- **Password**: `admin123`

### Students (after generate_sample_data)

- **student1** / password123
- **student2** / password123
- **student3** / password123
- **student4** / password123
- **student5** / password123

---

## .env Template

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-host.supabase.co
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Project Structure

```
hostel_project/
├── hostel_project/
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py
│   └── __init__.py
├── hostel_app/
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin config
│   ├── management/
│   │   └── commands/
│   │       └── generate_sample_data.py
│   └── __init__.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── room_list.html
│   ├── complaints.html
│   ├── admin_dashboard.html
│   └── admin_*.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── manage.py              # Django management
├── requirements.txt       # Dependencies
├── README.md
├── SETUP.md
├── QUICK_REFERENCE.md
└── .env.example
```

---

## Important File Locations

| File          | Purpose              |
| ------------- | -------------------- |
| `settings.py` | Django configuration |
| `models.py`   | Database schema      |
| `views.py`    | Business logic       |
| `forms.py`    | Input validation     |
| `urls.py`     | URL routing          |
| `admin.py`    | Admin panel config   |
| `templates/`  | HTML files           |
| `static/`     | CSS, JS, images      |

---

## Debugging Tips

### 1. Check Error Logs

```bash
python manage.py runserver > debug.log 2>&1
```

### 2. Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

Add to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]
```

### 3. Database Debugging

```python
# In Django shell
from django.db import connection
connection.queries  # View SQL queries
```

### 4. Print Debugging

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### 5. Browser Console

- Press F12 to open Developer Tools
- Check Console tab for JavaScript errors
- Check Network tab for HTTP requests

---

## Performance Tips

1. **Use `select_related()` for ForeignKey**

   ```python
   allocations = RoomAllocation.objects.select_related('student', 'room')
   ```

2. **Use `prefetch_related()` for Reverse Lookups**

   ```python
   rooms = Room.objects.prefetch_related('room_allocations')
   ```

3. **Add Database Indexes**

   ```python
   class Room(models.Model):
       room_number = models.CharField(max_length=20, unique=True, db_index=True)
   ```

4. **Pagination for Large Datasets**
   ```python
   from django.core.paginator import Paginator
   paginator = Paginator(queryset, 25)
   ```

---

## Security Checklist

- [ ] Change DEBUG to False in production
- [ ] Generate new SECRET_KEY
- [ ] Set ALLOWED_HOSTS properly
- [ ] Use HTTPS (set CSRF_COOKIE_SECURE = True)
- [ ] Validate all user inputs
- [ ] Use CSRF tokens in forms
- [ ] Hash passwords properly
- [ ] Set strong database password
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data

---

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup database backups
- [ ] Configure email service
- [ ] Setup error logging
- [ ] Configure static file serving
- [ ] Setup SSL/HTTPS
- [ ] Test all features
- [ ] Setup monitoring
- [ ] Plan maintenance schedule

---

## Support & Resources

- Django Docs: https://docs.djangoproject.com/
- Supabase Docs: https://supabase.com/docs
- Bootstrap Docs: https://getbootstrap.com/docs/
- Python Docs: https://docs.python.org/

---

**Last Updated**: February 2026
**Version**: 1.0.0
