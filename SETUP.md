# 🚀 Setup Guide - Hostel Management System

Complete step-by-step setup instructions for the Hostel Management System.

---

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Database Configuration](#database-configuration)
3. [Django Setup](#django-setup)
4. [Running the Application](#running-the-application)
5. [Initial Data Setup](#initial-data-setup)

---

## Environment Setup

### Step 1: Install Python

Ensure Python 3.8+ is installed:

```bash
python --version
```

### Step 2: Create Virtual Environment

Navigate to project directory and create a virtual environment:

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Configuration

### Step 1: Create Supabase Account

1. Visit [Supabase](https://supabase.com)
2. Click "Sign Up"
3. Create account with email/GitHub
4. Create a new organization

### Step 2: Create New Project

1. Click "New Project"
2. Fill in project details:
   - Name: `hostel-management`
   - Password: `your-secure-password` (save this!)
   - Region: Choose closest region
3. Wait for project to initialize (2-3 minutes)

### Step 3: Get Database Credentials

1. Go to Project Settings (bottom left)
2. Click "Database"
3. Copy connection information:
   - Host: `your-project.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: (from setup)

### Step 4: Setup Environment File

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
```

**Windows (Notepad):**

```bash
notepad .env
```

**Linux/macOS (nano):**

```bash
nano .env
```

**Update these values:**

```
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=your-project.supabase.co
DB_PORT=5432
```

---

## Django Setup

### Step 1: Generate Secret Key

```bash
python manage.py shell
```

Inside the shell:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the key and update `.env`

### Step 2: Create Database Tables

```bash
# Generate migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

Expected output:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hostel_app, sessions
Running migrations:
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_options... OK
  ...
  Applying hostel_app.0001_initial... OK
```

### Step 3: Create Admin Account

```bash
python manage.py createsuperuser
```

Enter prompts:

```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

### Step 4: Create Student Test Account

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from hostel_app.models import StudentProfile

# Create user
user = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='student123'
)

# Create student profile
StudentProfile.objects.create(
    user=user,
    full_name='John Doe',
    department='CSE',
    year=1,
    phone_number='9876543210',
    address='123 Main St, City, State 12345',
    guardian_name='Jane Doe',
    guardian_phone='9876543210'
)

print("Student account created successfully!")
```

### Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Running the Application

### Development Server

```bash
python manage.py runserver
```

Access at: `http://localhost:8000/`

### Access Applications

- **Student Dashboard**: `http://localhost:8000/student/dashboard/`
- **Admin Dashboard**: `http://localhost:8000/admin/dashboard/`
- **Django Admin**: `http://localhost:8000/admin/`
- **Register Page**: `http://localhost:8000/register/`
- **Login Page**: `http://localhost:8000/login/`

### Test Accounts

**Admin:**

- Username: `admin`
- Password: `admin123`

**Student:**

- Username: `student1`
- Password: `student123`

---

## Initial Data Setup

### Create Sample Rooms

```bash
python manage.py shell
```

```python
from hostel_app.models import Room

# Create Block A rooms
Block_A_rooms = [
    {"room_number": "A101", "floor": 1, "capacity": 2, "type": "Double"},
    {"room_number": "A102", "floor": 1, "capacity": 3, "type": "Shared"},
    {"room_number": "A201", "floor": 2, "capacity": 2, "type": "Double"},
    {"room_number": "A202", "floor": 2, "capacity": 1, "type": "Single"},
]

# Create Block B rooms
Block_B_rooms = [
    {"room_number": "B101", "floor": 1, "capacity": 3, "type": "Shared"},
    {"room_number": "B102", "floor": 1, "capacity": 1, "type": "Single"},
    {"room_number": "B201", "floor": 2, "capacity": 2, "type": "Double"},
    {"room_number": "B202", "floor": 2, "capacity": 3, "type": "Shared"},
]

# Insert Block A
for room_data in Block_A_rooms:
    Room.objects.create(
        room_number=room_data["room_number"],
        block_name="Block A",
        floor=room_data["floor"],
        capacity=room_data["capacity"],
        room_type=room_data["type"],
        status="Available",
        amenities="WiFi, Fan, Bed, Study Table, Wardrobe"
    )

# Insert Block B
for room_data in Block_B_rooms:
    Room.objects.create(
        room_number=room_data["room_number"],
        block_name="Block B",
        floor=room_data["floor"],
        capacity=room_data["capacity"],
        room_type=room_data["type"],
        status="Available",
        amenities="WiFi, Fan, Bed, Study Table, Wardrobe"
    )

print(f"Created {Room.objects.count()} rooms successfully!")
```

### Exit Shell

```python
exit()
```

---

## Verification

### Check Database Connection

```bash
python manage.py dbshell
```

```sql
SELECT 1;
```

Should output `1` confirming connection.

Exit with: `\q`

### Check Django Setup

```bash
python manage.py check
```

Should output: `System check identified no issues (0 silenced).`

### Verify Users

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
print(f"Total users: {User.objects.count()}")
print(f"Superusers: {User.objects.filter(is_superuser=True).count()}")
print("\nAll Users:")
for user in User.objects.all():
    print(f"  - {user.username} (Admin: {user.is_staff})")
```

---

## Common Issues & Solutions

### Issue 1: Import Error with psycopg2

**Error**: `psycopg2: No module named 'psycopg2'`

**Solution**:

```bash
pip install psycopg2-binary
```

### Issue 2: Database Connection Refused

**Error**: `FATAL: remaining connection slots are reserved`

**Solution**:

- Check Supabase project status
- Verify credentials in `.env`
- Check firewall/network settings

### Issue 3: Static Files Not Found

**Error**: 404 on CSS/JS files

**Solution**:

```bash
python manage.py collectstatic --clear
python manage.py runserver
```

### Issue 4: Port Already in Use

**Error**: `Address already in use`

**Solution**:

```bash
# Use different port
python manage.py runserver 8001
```

### Issue 5: Secret Key Error

**Error**: `ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**Solution**:

- Regenerate secret key
- Add to `.env`
- Update `settings.py` to read from .env

---

## Testing the Application

### Test Student Flow

1. Visit `http://localhost:8000/register/`
2. Register new student account
3. Login with credentials
4. Browse rooms
5. Apply for a room
6. Submit complaint

### Test Admin Flow

1. Login with admin credentials
2. Access `http://localhost:8000/admin/dashboard/`
3. Review room applications
4. Approve/reject applications
5. View complaints
6. Manage rooms

---

## Next Steps

### For Development

1. Customize templates
2. Add more features
3. Implement API endpoints
4. Add tests

### For Production

1. Set `DEBUG = False`
2. Use production database
3. Set up email notifications
4. Configure SSL/HTTPS
5. Use production server (Gunicorn + Nginx)
6. Set up backups
7. Configure monitoring

---

## Support

For issues:

1. Check error messages carefully
2. Review logs: `python manage.py runserver > debug.log 2>&1`
3. Check `.env` file format
4. Verify database connection

---

**Setup completed! Happy coding! 🎉**
