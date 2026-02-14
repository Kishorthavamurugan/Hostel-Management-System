"""
Models for the Hostel Management System.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class StudentProfile(models.Model):
    """Student profile information linked to Django User model."""
    
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        ('EN', 'Engineering'),
        ('SC', 'Science'),
        ('AR', 'Arts'),
        ('CO', 'Commerce'),
        ('OTHER', 'Other'),
    ]
    
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.full_name} ({self.user.username})"
    
    @property
    def has_allocated_room(self):
        """Check if student has an approved room allocation."""
        return self.user.room_allocations.filter(status='Approved').exists()
    
    @property
    def allocated_room(self):
        """Get the allocated room if any."""
        allocation = self.user.room_allocations.filter(status='Approved').first()
        return allocation.room if allocation else None


class Room(models.Model):
    """Model for hostel rooms."""
    
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Shared', 'Shared Room (3-4 students)'),
    ]
    
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Maintenance', 'Under Maintenance'),
    ]
    
    room_number = models.CharField(max_length=20, unique=True)
    block_name = models.CharField(max_length=50)
    floor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    current_occupancy = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    amenities = models.TextField(blank=True, help_text="Comma-separated list of amenities")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['block_name', 'floor', 'room_number']
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"Room {self.room_number} - Block {self.block_name}"
    
    @property
    def available_slots(self):
        """Calculate available slots in the room."""
        return self.capacity - self.current_occupancy
    
    @property
    def occupancy_percentage(self):
        """Calculate occupancy percentage."""
        if self.capacity == 0:
            return 0
        return (self.current_occupancy / self.capacity) * 100
    
    @property
    def is_full(self):
        """Check if room is full."""
        return self.current_occupancy >= self.capacity
    
    def update_occupancy(self):
        """Update occupancy based on approved allocations."""
        approved_count = self.room_allocations.filter(status='Approved').count()
        self.current_occupancy = approved_count
        if self.current_occupancy >= self.capacity:
            self.status = 'Full'
        elif self.status == 'Full' and self.current_occupancy < self.capacity:
            self.status = 'Available'
        self.save()


class RoomAllocation(models.Model):
    """Model for room allocation requests and approvals."""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_allocations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    allocated_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ('student', 'room')
    
    def __str__(self):
        student_profile = StudentProfile.objects.filter(user=self.student).first()
        student_name = student_profile.full_name if student_profile else self.student.username
        return f"{student_name} - Room {self.room.room_number}"
    
    def approve(self):
        """Approve the room allocation."""
        if not self.room.is_full:
            self.status = 'Approved'
            self.allocated_date = timezone.now()
            self.save()
            self.room.update_occupancy()
            return True
        return False
    
    def reject(self, reason=""):
        """Reject the room allocation."""
        self.status = 'Rejected'
        self.rejection_reason = reason
        self.save()


class Complaint(models.Model):
    """Model for student complaints and feedback."""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Complaints'
    
    def __str__(self):
        student_profile = StudentProfile.objects.filter(user=self.student).first()
        student_name = student_profile.full_name if student_profile else self.student.username
        return f"{self.subject} - {student_name}"
    
    def resolve(self):
        """Mark complaint as resolved."""
        self.status = 'Resolved'
        self.resolved_at = timezone.now()
        self.save()
