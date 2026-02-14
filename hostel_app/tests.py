"""
Tests for the Hostel Management System models and views.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from hostel_app.models import StudentProfile, Room, RoomAllocation, Complaint


class StudentProfileTests(TestCase):
    """Tests for StudentProfile model."""

    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_student_profile(self):
        """Test creating a student profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            full_name='Test Student',
            department='CSE',
            year=1,
            phone_number='9876543210',
            address='Test Address',
            guardian_name='Test Guardian'
        )

        self.assertEqual(profile.full_name, 'Test Student')
        self.assertEqual(profile.department, 'CSE')
        self.assertEqual(profile.year, 1)
        self.assertTrue(StudentProfile.objects.filter(user=self.user).exists())

    def test_student_profile_str(self):
        """Test string representation of StudentProfile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            full_name='Test Student',
            department='CSE',
            year=1,
            phone_number='9876543210',
            address='Test Address',
            guardian_name='Test Guardian'
        )

        self.assertEqual(str(profile), 'Test Student (testuser)')


class RoomTests(TestCase):
    """Tests for Room model."""

    def setUp(self):
        """Create test rooms."""
        self.room1 = Room.objects.create(
            room_number='A101',
            block_name='Block A',
            floor=1,
            capacity=2,
            current_occupancy=0,
            room_type='Double',
            status='Available'
        )

    def test_create_room(self):
        """Test creating a room."""
        self.assertEqual(self.room1.room_number, 'A101')
        self.assertEqual(self.room1.capacity, 2)
        self.assertTrue(Room.objects.filter(room_number='A101').exists())

    def test_available_slots(self):
        """Test available slots calculation."""
        self.assertEqual(self.room1.available_slots, 2)
        self.room1.current_occupancy = 1
        self.room1.save()
        self.assertEqual(self.room1.available_slots, 1)

    def test_occupancy_percentage(self):
        """Test occupancy percentage calculation."""
        self.assertEqual(self.room1.occupancy_percentage, 0)
        self.room1.current_occupancy = 1
        self.room1.save()
        self.assertEqual(self.room1.occupancy_percentage, 50)

    def test_is_full(self):
        """Test room full status."""
        self.assertFalse(self.room1.is_full)
        self.room1.current_occupancy = 2
        self.room1.save()
        self.assertTrue(self.room1.is_full)

    def test_room_str(self):
        """Test string representation of Room."""
        expected = 'Room A101 - Block Block A'
        self.assertEqual(str(self.room1), expected)


class RoomAllocationTests(TestCase):
    """Tests for RoomAllocation model."""

    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.room = Room.objects.create(
            room_number='A101',
            block_name='Block A',
            floor=1,
            capacity=2,
            current_occupancy=0,
            room_type='Double',
            status='Available'
        )

    def test_create_allocation(self):
        """Test creating a room allocation."""
        allocation = RoomAllocation.objects.create(
            student=self.user,
            room=self.room,
            status='Pending'
        )

        self.assertEqual(allocation.status, 'Pending')
        self.assertTrue(
            RoomAllocation.objects.filter(student=self.user).exists()
        )

    def test_approve_allocation(self):
        """Test approving an allocation."""
        allocation = RoomAllocation.objects.create(
            student=self.user,
            room=self.room,
            status='Pending'
        )

        result = allocation.approve()
        self.assertTrue(result)
        self.assertEqual(allocation.status, 'Approved')
        self.assertIsNotNone(allocation.allocated_date)

    def test_reject_allocation(self):
        """Test rejecting an allocation."""
        allocation = RoomAllocation.objects.create(
            student=self.user,
            room=self.room,
            status='Pending'
        )

        allocation.reject('Room not suitable')
        self.assertEqual(allocation.status, 'Rejected')
        self.assertEqual(allocation.rejection_reason, 'Room not suitable')

    def test_unique_constraint(self):
        """Test unique together constraint."""
        RoomAllocation.objects.create(
            student=self.user,
            room=self.room,
            status='Pending'
        )

        with self.assertRaises(Exception):
            RoomAllocation.objects.create(
                student=self.user,
                room=self.room,
                status='Pending'
            )


class ComplaintTests(TestCase):
    """Tests for Complaint model."""

    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.room = Room.objects.create(
            room_number='A101',
            block_name='Block A',
            floor=1,
            capacity=2,
            room_type='Double',
            status='Available'
        )

    def test_create_complaint(self):
        """Test creating a complaint."""
        complaint = Complaint.objects.create(
            student=self.user,
            subject='Test Complaint',
            description='Test Description',
            status='Pending',
            priority='High'
        )

        self.assertEqual(complaint.subject, 'Test Complaint')
        self.assertEqual(complaint.status, 'Pending')
        self.assertTrue(Complaint.objects.filter(student=self.user).exists())

    def test_resolve_complaint(self):
        """Test resolving a complaint."""
        complaint = Complaint.objects.create(
            student=self.user,
            subject='Test Complaint',
            description='Test Description',
            status='Pending'
        )

        complaint.resolve()
        self.assertEqual(complaint.status, 'Resolved')
        self.assertIsNotNone(complaint.resolved_at)


class AuthenticationTests(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        """Setup test client."""
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('student_dashboard')

    def test_student_registration(self):
        """Test student registration."""
        response = self.client.post(self.register_url, {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
            'full_name': 'New Student',
            'department': 'CSE',
            'year': 1,
            'phone_number': '9876543210',
            'address': 'Test Address',
            'guardian_name': 'Guardian Name',
        })

        self.assertTrue(User.objects.filter(username='newstudent').exists())

    def test_student_login(self):
        """Test student login."""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })

        self.assertEqual(response.status_code, 302)

    def test_login_redirect(self):
        """Test redirect to dashboard after login."""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
