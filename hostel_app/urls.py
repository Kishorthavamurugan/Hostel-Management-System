"""
URL configuration for hostel_app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student Views
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/apply/', views.apply_room, name='apply_room'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('complaints/', views.complaints, name='complaints'),
    
    # Admin Views
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Room Management
    path('admin/rooms/', views.manage_rooms, name='manage_rooms'),
    path('admin/rooms/add/', views.add_room, name='add_room'),
    path('admin/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('admin/rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    
    # Application Management
    path('admin/applications/', views.manage_applications, name='manage_applications'),
    path('admin/applications/<int:allocation_id>/approve/', views.approve_application, name='approve_application'),
    path('admin/applications/<int:allocation_id>/reject/', views.reject_application, name='reject_application'),
    path('admin/allocations/<int:allocation_id>/remove/', views.remove_allocation, name='remove_allocation'),
    
    # Student Management
    path('admin/students/', views.manage_students, name='manage_students'),
    path('admin/students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Complaint Management
    path('admin/complaints/', views.manage_complaints, name='manage_complaints'),
    path('admin/complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]
