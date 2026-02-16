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
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Room Management
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage-rooms/add/', views.add_room, name='add_room'),
    path('manage-rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('manage-rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    
    
    # Application Management
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    path('manage-applications/<int:allocation_id>/approve/', views.approve_application, name='approve_application'),
    path('manage-applications/<int:allocation_id>/reject/', views.reject_application, name='reject_application'),
    path('manage-allocations/<int:allocation_id>/remove/', views.remove_allocation, name='remove_allocation'),
    
    # Student Management
    path('manage-students/', views.manage_students, name='manage_students'),
    path('manage-students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Complaint Management
    path('manage-complaints/', views.manage_complaints, name='manage_complaints'),
    path('manage-complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    
]
