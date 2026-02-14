"""
Forms for the Hostel Management System.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import StudentProfile, Room, RoomAllocation, Complaint
import re


class StudentRegistrationForm(UserCreationForm):
    """Form for student registration."""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name',
    }))
    department = forms.ChoiceField(choices=StudentProfile.DEPARTMENT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    year = forms.ChoiceField(choices=StudentProfile.YEAR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number',
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'rows': 3,
    }))
    guardian_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Guardian Name',
    }))
    guardian_phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Guardian Phone (Optional)',
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'department', 
                  'year', 'phone_number', 'address', 'guardian_name', 'guardian_phone')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not re.match(r'^[0-9]{10}$', phone.replace('-', '').replace(' ', '')):
            raise ValidationError('Please enter a valid 10-digit phone number.')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                department=self.cleaned_data['department'],
                year=self.cleaned_data['year'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                guardian_name=self.cleaned_data['guardian_name'],
                guardian_phone=self.cleaned_data.get('guardian_phone', ''),
            )
        return user


class StudentLoginForm(AuthenticationForm):
    """Form for student login."""
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))


class RoomAllocationForm(forms.ModelForm):
    """Form for room allocation requests."""
    
    class Meta:
        model = RoomAllocation
        fields = []  # No fields needed, handled in view
    
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        if self.room and self.student:
            # Check if room is full
            if self.room.is_full:
                raise ValidationError('This room is currently full.')
            
            # Check if student already has a pending or approved allocation
            existing = RoomAllocation.objects.filter(
                student=self.student,
                status__in=['Pending', 'Approved']
            ).exists()
            if existing:
                raise ValidationError('You already have a pending or approved room allocation.')
        
        return self.cleaned_data


class ComplaintForm(forms.ModelForm):
    """Form for submitting complaints/feedback."""
    
    class Meta:
        model = Complaint
        fields = ('subject', 'description', 'priority')
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Complaint Subject',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your complaint or feedback...',
                'rows': 5,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class RoomForm(forms.ModelForm):
    """Form for room management (Admin)."""
    
    class Meta:
        model = Room
        fields = ('room_number', 'block_name', 'floor', 'capacity', 'room_type', 'status', 'amenities')
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room Number (e.g., A101)',
            }),
            'block_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Block Name (e.g., Block A)',
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4,
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Amenities (comma-separated)',
                'rows': 2,
            }),
        }


class RoomAllocationApprovalForm(forms.ModelForm):
    """Form for approving/rejecting room allocations (Admin)."""
    
    class Meta:
        model = RoomAllocation
        fields = ('status', 'rejection_reason')
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reason for rejection (if applicable)',
                'rows': 3,
            }),
        }


class ComplaintResolutionForm(forms.ModelForm):
    """Form for resolving complaints (Admin)."""
    
    class Meta:
        model = Complaint
        fields = ('status', 'resolution_notes')
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Resolution notes...',
                'rows': 3,
            }),
        }
