"""
Django Admin configuration for hostel_app.
"""

from django.contrib import admin
from .models import StudentProfile, Room, RoomAllocation, Complaint


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'department', 'year', 'phone_number', 'created_at')
    list_filter = ('department', 'year', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Account', {'fields': ('user',)}),
        ('Personal Information', {'fields': ('full_name', 'phone_number', 'address')}),
        ('Academic Information', {'fields': ('department', 'year')}),
        ('Guardian Information', {'fields': ('guardian_name', 'guardian_phone')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'block_name', 'floor', 'capacity', 'current_occupancy', 'room_type', 'status')
    list_filter = ('status', 'room_type', 'block_name', 'floor')
    search_fields = ('room_number', 'block_name')
    readonly_fields = ('created_at', 'updated_at', 'occupancy_percentage')
    fieldsets = (
        ('Room Details', {'fields': ('room_number', 'block_name', 'floor', 'room_type')}),
        ('Capacity', {'fields': ('capacity', 'current_occupancy', 'occupancy_percentage')}),
        ('Status', {'fields': ('status',)}),
        ('Additional', {'fields': ('amenities',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'status', 'applied_date', 'allocated_date')
    list_filter = ('status', 'applied_date', 'room__block_name')
    search_fields = ('student__username', 'student__student_profile__full_name', 'room__room_number')
    readonly_fields = ('applied_date', 'allocated_date')
    fieldsets = (
        ('Allocation Details', {'fields': ('student', 'room', 'status')}),
        ('Dates', {'fields': ('applied_date', 'allocated_date')}),
        ('Rejection', {'fields': ('rejection_reason',)}),
    )


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at', 'room')
    search_fields = ('subject', 'description', 'student__username', 'student__student_profile__full_name')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    fieldsets = (
        ('Complaint Information', {'fields': ('subject', 'description', 'student', 'room')}),
        ('Status', {'fields': ('status', 'priority', 'resolution_notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at'), 'classes': ('collapse',)}),
    )
