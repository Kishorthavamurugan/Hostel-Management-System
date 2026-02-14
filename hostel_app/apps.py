"""
Application configuration for hostel_app.
"""

from django.apps import AppConfig


class HostelAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel_app'
    verbose_name = 'Hostel Management System'
