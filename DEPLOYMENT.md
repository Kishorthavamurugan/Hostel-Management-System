# 📦 Deployment Guide - Hostel Management System

Complete guide for deploying the Hostel Management System to production.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Deployment Options](#deployment-options)
4. [Post-Deployment](#post-deployment)

---

## Pre-Deployment Checklist

### Code Quality

- [ ] Remove debug code and print statements
- [ ] Run tests: `python manage.py test`
- [ ] Check for security issues: `python manage.py check --deploy`
- [ ] Review all settings in settings.py
- [ ] Update all dependencies in requirements.txt
- [ ] Test all user workflows

### Security

- [ ] Set `DEBUG = False`
- [ ] Generate new `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure CSRF settings
- [ ] Enable HTTPS/SSL
- [ ] Update email settings
- [ ] Review permission settings
- [ ] Check password validators

### Database

- [ ] Backup production database
- [ ] Test migrations on staging
- [ ] Setup automated backups
- [ ] Configure database user with limited permissions
- [ ] Test recovery procedures

### Static Files

- [ ] Collect all static files
- [ ] Configure CDN if needed
- [ ] Test CSS and JavaScript loading
- [ ] Optimize image sizes

### Monitoring

- [ ] Setup error logging (Sentry)
- [ ] Setup application monitoring
- [ ] Configure email alerts
- [ ] Setup database monitoring
- [ ] Create monitoring dashboard

---

## Environment Setup

### 1. Production settings.py

```python
# settings.py - Production Configuration

import os
from decouple import config

# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = config('SECRET_KEY')

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database (Supabase Production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/hostel/error.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

### 2. Production .env

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=strong-password-here
DB_HOST=your-supabase-host.supabase.co
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Deployment Options

### Option 1: Heroku (Easiest)

#### Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed

#### Steps

1. **Create Heroku App**

```bash
heroku create hostel-management-system
```

2. **Add Buildpacks**

```bash
heroku buildpacks:add heroku/python
```

3. **Create Procfile**

```
web: gunicorn hostel_project.wsgi --log-file -
release: python manage.py migrate
```

4. **Set Environment Variables**

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
# Set all other required variables
```

5. **Deploy**

```bash
git push heroku main
```

6. **Create Admin**

```bash
heroku run python manage.py createsuperuser
```

7. **Generate Sample Data**

```bash
heroku run python manage.py generate_sample_data
```

---

### Option 2: AWS Elastic Beanstalk

#### Prerequisites

- AWS account
- AWS CLI configured
- EB CLI installed

#### Steps

1. **Initialize EB Application**

```bash
eb init -p python-3.11 hostel-management
```

2. **Create Environment**

```bash
eb create hostel-prod
```

3. **Create .ebextensions/django.config**

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: hostel_project.wsgi:application

commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate"
    leader_only: true
  02_createadmin:
    command: "source /var/app/venv/*/bin/activate && python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>/dev/null || true"
    leader_only: true
  03_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
```

4. **Set Environment Variables**

```bash
eb setenv SECRET_KEY=your-secret-key DEBUG=False
```

5. **Deploy**

```bash
eb deploy
```

---

### Option 3: DigitalOcean App Platform

#### Prerequisites

- DigitalOcean account
- GitHub repository connected

#### Steps

1. **Create App**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Connect GitHub repository

2. **Configure App**
   - Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Set run command: `gunicorn hostel_project.wsgi`
   - Add environment variables

3. **Configure Database**
   - Create managed PostgreSQL database
   - Update connection string

4. **Deploy**
   - Push to GitHub
   - App Platform automatically deploys

---

### Option 4: Manual VPS (Ubuntu 20.04)

#### Prerequisites

- VPS with Ubuntu 20.04
- SSH access
- Domain name

#### Steps

1. **Update System**

```bash
sudo apt update
sudo apt upgrade -y
```

2. **Install Dependencies**

```bash
sudo apt install -y python3-pip python3-venv postgresql nginx supervisor
```

3. **Setup Application**

```bash
# Create user
sudo useradd -m hostel

# Clone repository
cd /home/hostel
git clone your-repo.git
cd hostel-management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

4. **Configure Gunicorn**

Create `/home/hostel/hostel.conf`:

```
[program:hostel]
directory=/home/hostel/hostel-management
command=/home/hostel/hostel-management/venv/bin/gunicorn hostel_project.wsgi:application --bind 127.0.0.1:8000
user=hostel
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hostel/gunicorn.log
```

5. **Configure Nginx**

Create `/etc/nginx/sites-available/hostel`:

```nginx
upstream hostel {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static {
        alias /home/hostel/hostel-management/staticfiles;
    }

    location / {
        proxy_pass http://hostel;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

6. **Enable Nginx Site**

```bash
sudo ln -s /etc/nginx/sites-available/hostel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup SSL with Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

8. **Start Application**

```bash
sudo systemctl start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start hostel
```

---

## Post-Deployment

### Testing

```bash
# Test all URLs
curl https://yourdomain.com/
curl https://yourdomain.com/admin/

# Check status
curl -I https://yourdomain.com/
```

### Monitoring Setup

1. **Sentry for Error Tracking**

```bash
pip install sentry-sdk
```

In settings.py:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=False
)
```

2. **Setup Automated Backups**

```bash
# Supabase automatic backups are enabled by default
# For additional backups, use:
pg_dump postgresql://user:password@host/database > backup.sql
```

### Performance Optimization

1. **Enable Caching**

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

2. **Compress Static Files**

```bash
pip install django-compressor
python manage.py compress
```

3. **Use CDN**
   - Use Cloudflare or AWS CloudFront for static files

### Maintenance

1. **Regular Backups**
   - Daily database backups
   - Test restore procedures monthly

2. **Update Dependencies**
   - Update packages monthly
   - Test updates in staging first

3. **Monitor Logs**
   - Check error logs daily
   - Monitor application performance
   - Review security logs

4. **Performance Monitoring**
   - Monitor response times
   - Track database queries
   - Monitor CPU/memory usage

---

## Troubleshooting

### Issue: 500 Internal Server Error

- Check error logs
- Verify environment variables
- Check database connection
- Test migrations

### Issue: Static Files Not Found

- Run `collectstatic`
- Check Nginx configuration
- Verify file permissions

### Issue: Database Connection Failed

- Verify connection string
- Check Supabase status
- Test network connection
- Check firewall rules

### Issue: Email Not Sending

- Verify email credentials
- Check email configuration
- Test with Django shell

---

## Security Hardening

1. **Enable CORS**

```python
CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

2. **Set Security Headers**

```python
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}
```

3. **Rate Limit Requests**

```bash
pip install django-ratelimit
```

4. **Two-Factor Authentication**

```bash
pip install django-otp qrcode
```

---

## Production Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY changed
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Database backups setup
- [ ] Error monitoring setup
- [ ] Static files optimized
- [ ] Email configured
- [ ] Admin created
- [ ] Logs configured
- [ ] Performance monitoring setup
- [ ] Security headers configured
- [ ] CORS configured
- [ ] Rate limiting enabled

---

**Deployment Complete! 🚀**
