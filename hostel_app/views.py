"""
Views for the Hostel Management System.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from .models import StudentProfile, Room, RoomAllocation, Complaint
from .forms import (
    StudentRegistrationForm, StudentLoginForm, RoomAllocationForm,
    ComplaintForm, RoomForm, RoomAllocationApprovalForm, ComplaintResolutionForm
)


# ==================== Helper Functions ====================

def is_admin(user):
    """Check if user is admin."""
    return user.is_staff and user.is_superuser


def is_student(user):
    """Check if user is a student."""
    return user.is_active and not user.is_staff


# ==================== Authentication Views ====================

@require_http_methods(["GET", "POST"])
def register(request):
    """Student registration view."""
    if request.user.is_authenticated:
        return redirect('student_dashboard' if is_student(request.user) else 'admin_dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Student login view."""
    if request.user.is_authenticated:
        return redirect('student_dashboard' if is_student(request.user) else 'admin_dashboard')
    
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if is_admin(user):
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('login')


# ==================== Student Views ====================

@login_required(login_url='login')
def student_dashboard(request):
    """Student dashboard view."""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('logout')
    
    # Get allocated room if any
    allocation = RoomAllocation.objects.filter(
        student=request.user,
        status='Approved'
    ).first()
    
    allocated_room = allocation.room if allocation else None
    
    # Get pending applications
    pending_applications = RoomAllocation.objects.filter(
        student=request.user,
        status='Pending'
    ).count()
    
    # Get complaints
    complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')[:5]
    
    # Get available rooms count
    available_rooms = Room.objects.filter(status='Available')
    
    context = {
        'student_profile': student_profile,
        'allocated_room': allocated_room,
        'pending_applications': pending_applications,
        'complaints': complaints,
        'available_rooms_count': available_rooms.count(),
    }
    
    return render(request, 'student_dashboard.html', context)


@login_required(login_url='login')
def room_list(request):
    """List available rooms for students."""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    
    # Get search query
    search_query = request.GET.get('search', '')
    room_type_filter = request.GET.get('room_type', '')
    
    # Base queryset
    rooms = Room.objects.all()
    
    # Apply filters
    if search_query:
        rooms = rooms.filter(
            Q(room_number__icontains=search_query) |
            Q(block_name__icontains=search_query)
        )
    
    if room_type_filter:
        rooms = rooms.filter(room_type=room_type_filter)
    
    # Only show available or full rooms (not maintenance)
    rooms = rooms.exclude(status='Maintenance').order_by('block_name', 'floor')
    
    # Pagination
    paginator = Paginator(rooms, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get student's current application
    student_application = RoomAllocation.objects.filter(
        student=request.user,
        status__in=['Pending', 'Approved']
    ).first()
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj.object_list,
        'search_query': search_query,
        'room_type_filter': room_type_filter,
        'room_types': Room.ROOM_TYPE_CHOICES,
        'student_application': student_application,
    }
    
    return render(request, 'room_list.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def apply_room(request, room_id):
    """Apply for a room."""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    
    room = get_object_or_404(Room, id=room_id)
    
    # Check if room is full
    if room.is_full:
        messages.error(request, 'This room is currently full.')
        return redirect('room_list')
    
    # Check if student already has a pending or approved allocation
    existing = RoomAllocation.objects.filter(
        student=request.user,
        status__in=['Pending', 'Approved']
    ).first()
    
    if existing:
        messages.warning(request, f'You already have a {existing.status.lower()} application for {existing.room.room_number}.')
        return redirect('room_list')
    
    # Check if already allocated to this room
    if RoomAllocation.objects.filter(student=request.user, room=room, status='Approved').exists():
        messages.info(request, 'You are already allocated to this room.')
        return redirect('room_list')
    
    # Create allocation
    allocation = RoomAllocation.objects.create(student=request.user, room=room)
    messages.success(request, f'Application for Room {room.room_number} submitted successfully!')
    
    return redirect('student_dashboard')


@login_required(login_url='login')
def my_applications(request):
    """View student's room applications."""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    
    applications = RoomAllocation.objects.filter(student=request.user).order_by('-applied_date')
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'applications': page_obj.object_list,
    }
    
    return render(request, 'my_applications.html', context)


@login_required(login_url='login')
def complaints(request):
    """View and submit complaints."""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            
            # Auto-assign room if student has allocated room
            allocation = RoomAllocation.objects.filter(
                student=request.user,
                status='Approved'
            ).first()
            if allocation:
                complaint.room = allocation.room
            
            complaint.save()
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('complaints')
        else:
            messages.error(request, 'There was an error submitting your complaint.')
    else:
        form = ComplaintForm()
    
    # Get student's complaints
    student_complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(student_complaints, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'complaints': page_obj.object_list,
    }
    
    return render(request, 'complaints.html', context)


# ==================== Admin Views ====================

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def admin_dashboard(request):
    """Admin dashboard view."""
    # Get statistics
    total_students = StudentProfile.objects.count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='Available').count()
    occupied_rooms = Room.objects.filter(status='Full').count()
    maintenance_rooms = Room.objects.filter(status='Maintenance').count()
    
    pending_applications = RoomAllocation.objects.filter(status='Pending').count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    in_progress_complaints = Complaint.objects.filter(status='In Progress').count()
    
    # Get recent applications
    recent_applications = RoomAllocation.objects.filter(
        status='Pending'
    ).order_by('-applied_date')[:5]
    
    # Get recent complaints
    recent_complaints = Complaint.objects.filter(
        status__in=['Pending', 'In Progress']
    ).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'maintenance_rooms': maintenance_rooms,
        'pending_applications': pending_applications,
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'recent_applications': recent_applications,
        'recent_complaints': recent_complaints,
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def manage_rooms(request):
    """Manage rooms (Admin)."""
    search_query = request.GET.get('search', '')
    
    rooms = Room.objects.all()
    if search_query:
        rooms = rooms.filter(
            Q(room_number__icontains=search_query) |
            Q(block_name__icontains=search_query)
        )
    
    rooms = rooms.order_by('block_name', 'floor')
    
    # Pagination
    paginator = Paginator(rooms, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj.object_list,
        'search_query': search_query,
    }
    
    return render(request, 'admin_manage_rooms.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["GET", "POST"])
def add_room(request):
    """Add a new room (Admin)."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully!')
            return redirect('manage_rooms')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RoomForm()
    
    return render(request, 'admin_add_room.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["GET", "POST"])
def edit_room(request, room_id):
    """Edit a room (Admin)."""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('manage_rooms')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'admin_edit_room.html', {'form': form, 'room': room})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["POST"])
def delete_room(request, room_id):
    """Delete a room (Admin)."""
    room = get_object_or_404(Room, id=room_id)
    
    # Check if room has allocations
    if room.room_allocations.filter(status='Approved').exists():
        messages.error(request, 'Cannot delete a room with active allocations.')
        return redirect('manage_rooms')
    
    room.delete()
    messages.success(request, 'Room deleted successfully!')
    return redirect('manage_rooms')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def manage_applications(request):
    """Manage room applications (Admin)."""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    applications = RoomAllocation.objects.all()
    
    if search_query:
        applications = applications.filter(
            Q(student__username__icontains=search_query) |
            Q(student__student_profile__full_name__icontains=search_query) |
            Q(room__room_number__icontains=search_query)
        )
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    applications = applications.order_by('-applied_date')
    
    # Pagination
    paginator = Paginator(applications, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'applications': page_obj.object_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': RoomAllocation.STATUS_CHOICES,
    }
    
    return render(request, 'admin_manage_applications.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["POST"])
def approve_application(request, allocation_id):
    """Approve a room application (Admin)."""
    allocation = get_object_or_404(RoomAllocation, id=allocation_id)
    
    if allocation.approve():
        messages.success(request, f'Application approved! Room {allocation.room.room_number} allocated to {allocation.student.username}.')
    else:
        messages.error(request, 'Cannot approve: Room is full.')
    
    return redirect('manage_applications')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["POST"])
def reject_application(request, allocation_id):
    """Reject a room application (Admin)."""
    allocation = get_object_or_404(RoomAllocation, id=allocation_id)
    
    reason = request.POST.get('reason', '')
    allocation.reject(reason)
    
    messages.success(request, f'Application rejected.')
    return redirect('manage_applications')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def manage_students(request):
    """Manage students (Admin)."""
    search_query = request.GET.get('search', '')
    
    students = StudentProfile.objects.all()
    
    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    students = students.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(students, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'students': page_obj.object_list,
        'search_query': search_query,
    }
    
    return render(request, 'admin_manage_students.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def student_detail(request, student_id):
    """View student details (Admin)."""
    student_profile = get_object_or_404(StudentProfile, user_id=student_id)
    
    allocations = RoomAllocation.objects.filter(student_id=student_id).order_by('-applied_date')
    complaints = Complaint.objects.filter(student_id=student_id).order_by('-created_at')
    
    context = {
        'student': student_profile,
        'allocations': allocations,
        'complaints': complaints,
    }
    
    return render(request, 'admin_student_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
@require_http_methods(["POST"])
def remove_allocation(request, allocation_id):
    """Remove a room allocation (Admin)."""
    allocation = get_object_or_404(RoomAllocation, id=allocation_id)
    
    if allocation.status == 'Approved':
        allocation.status = 'Rejected'
        allocation.rejection_reason = 'Removed by admin'
        allocation.save()
        allocation.room.update_occupancy()
        messages.success(request, f'Allocation for Room {allocation.room.room_number} removed.')
    else:
        allocation.delete()
        messages.success(request, 'Application removed.')
    
    return redirect('manage_applications')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def manage_complaints(request):
    """Manage complaints (Admin)."""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    complaints = Complaint.objects.all()
    
    if search_query:
        complaints = complaints.filter(
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(student__username__icontains=search_query) |
            Q(student__student_profile__full_name__icontains=search_query)
        )
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    
    complaints = complaints.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(complaints, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'complaints': page_obj.object_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': Complaint.STATUS_CHOICES,
        'priority_choices': Complaint.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_manage_complaints.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='student_dashboard')
def complaint_detail(request, complaint_id):
    """View complaint details (Admin)."""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintResolutionForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint updated successfully!')
            return redirect('manage_complaints')
    else:
        form = ComplaintResolutionForm(instance=complaint)
    
    context = {
        'complaint': complaint,
        'form': form,
    }
    
    return render(request, 'admin_complaint_detail.html', context)


# ==================== Home View ====================

def home(request):
    """Home/index view."""
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('login')
