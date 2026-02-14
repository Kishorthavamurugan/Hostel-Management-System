"""
Management command to generate sample data for the Hostel Management System.

Usage: python manage.py generate_sample_data
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from hostel_app.models import StudentProfile, Room, RoomAllocation, Complaint
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Generate sample data for testing the Hostel Management System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()

        try:
            self.create_admin()
            self.create_students()
            self.create_rooms()
            self.create_allocations()
            self.create_complaints()
            
            self.stdout.write(
                self.style.SUCCESS('✓ Sample data generated successfully!')
            )
        except Exception as e:
            raise CommandError(f'Error generating sample data: {str(e)}')

    def clear_data(self):
        """Clear existing data"""
        self.stdout.write('Clearing existing data...')
        
        User.objects.filter(is_superuser=False).delete()
        Room.objects.all().delete()
        RoomAllocation.objects.all().delete()
        Complaint.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('✓ Data cleared'))

    def create_admin(self):
        """Create admin user"""
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('⚠ Admin user already exists'))
            return

        admin = User.objects.create_superuser(
            username='admin',
            email='admin@hostelhub.edu',
            password='admin123'
        )
        self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        self.stdout.write(f'  Username: admin')
        self.stdout.write(f'  Password: admin123')

    def create_students(self):
        """Create sample student accounts"""
        students_data = [
            {
                'username': 'student1',
                'email': 'john@example.com',
                'full_name': 'John Doe',
                'department': 'CSE',
                'year': 1,
                'phone': '9876543210',
                'address': '123 Main St, New York, NY 10001',
                'guardian': 'Jane Doe',
            },
            {
                'username': 'student2',
                'email': 'alice@example.com',
                'full_name': 'Alice Smith',
                'department': 'ECE',
                'year': 2,
                'phone': '9876543211',
                'address': '456 Oak Ave, Los Angeles, CA 90001',
                'guardian': 'Bob Smith',
            },
            {
                'username': 'student3',
                'email': 'charlie@example.com',
                'full_name': 'Charlie Brown',
                'department': 'ME',
                'year': 3,
                'phone': '9876543212',
                'address': '789 Pine Rd, Chicago, IL 60601',
                'guardian': 'David Brown',
            },
            {
                'username': 'student4',
                'email': 'diana@example.com',
                'full_name': 'Diana Prince',
                'department': 'CE',
                'year': 1,
                'phone': '9876543213',
                'address': '321 Elm St, Houston, TX 77001',
                'guardian': 'William Prince',
            },
            {
                'username': 'student5',
                'email': 'eve@example.com',
                'full_name': 'Eve Johnson',
                'department': 'CSE',
                'year': 4,
                'phone': '9876543214',
                'address': '654 Maple Dr, Phoenix, AZ 85001',
                'guardian': 'Frank Johnson',
            },
        ]

        for data in students_data:
            if User.objects.filter(username=data['username']).exists():
                continue

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123'
            )

            StudentProfile.objects.create(
                user=user,
                full_name=data['full_name'],
                department=data['department'],
                year=data['year'],
                phone_number=data['phone'],
                address=data['address'],
                guardian_name=data['guardian'],
                guardian_phone=data['phone'],
            )

        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(students_data)} student accounts'))

    def create_rooms(self):
        """Create sample rooms"""
        rooms_data = [
            # Block A
            {'number': 'A101', 'block': 'Block A', 'floor': 1, 'capacity': 2, 'type': 'Double'},
            {'number': 'A102', 'block': 'Block A', 'floor': 1, 'capacity': 3, 'type': 'Shared'},
            {'number': 'A103', 'block': 'Block A', 'floor': 1, 'capacity': 1, 'type': 'Single'},
            {'number': 'A201', 'block': 'Block A', 'floor': 2, 'capacity': 2, 'type': 'Double'},
            {'number': 'A202', 'block': 'Block A', 'floor': 2, 'capacity': 1, 'type': 'Single'},
            # Block B
            {'number': 'B101', 'block': 'Block B', 'floor': 1, 'capacity': 3, 'type': 'Shared'},
            {'number': 'B102', 'block': 'Block B', 'floor': 1, 'capacity': 2, 'type': 'Double'},
            {'number': 'B103', 'block': 'Block B', 'floor': 1, 'capacity': 1, 'type': 'Single'},
            {'number': 'B201', 'block': 'Block B', 'floor': 2, 'capacity': 2, 'type': 'Double'},
            {'number': 'B202', 'block': 'Block B', 'floor': 2, 'capacity': 3, 'type': 'Shared'},
            # Block C
            {'number': 'C101', 'block': 'Block C', 'floor': 1, 'capacity': 2, 'type': 'Double'},
            {'number': 'C102', 'block': 'Block C', 'floor': 1, 'capacity': 1, 'type': 'Single'},
        ]

        for data in rooms_data:
            if Room.objects.filter(room_number=data['number']).exists():
                continue

            Room.objects.create(
                room_number=data['number'],
                block_name=data['block'],
                floor=data['floor'],
                capacity=data['capacity'],
                room_type=data['type'],
                status='Available',
                amenities='WiFi, Fan, Bed, Study Table, Wardrobe, AC'
            )

        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(rooms_data)} rooms'))

    def create_allocations(self):
        """Create sample room allocations"""
        students = User.objects.filter(username__startswith='student')
        rooms = Room.objects.all()[:len(students)]

        for student, room in zip(students, rooms):
            allocation = RoomAllocation.objects.create(
                student=student,
                room=room,
                status='Approved',
                applied_date=timezone.now() - timedelta(days=5)
            )
            allocation.allocated_date = timezone.now() - timedelta(days=3)
            allocation.save()

            room.current_occupancy += 1
            if room.current_occupancy >= room.capacity:
                room.status = 'Full'
            room.save()

        self.stdout.write(self.style.SUCCESS(f'✓ Created room allocations'))

    def create_complaints(self):
        """Create sample complaints"""
        students = User.objects.filter(username__startswith='student')
        
        complaints_data = [
            {
                'subject': 'Broken Fan',
                'description': 'The ceiling fan in my room is making strange noises and not working properly.',
                'priority': 'Medium',
            },
            {
                'subject': 'WiFi Network Issues',
                'description': 'The WiFi connection keeps dropping in Block A.',
                'priority': 'High',
            },
            {
                'subject': 'Water Leak in Bathroom',
                'description': 'There is a water leak from the ceiling in the bathroom.',
                'priority': 'High',
            },
            {
                'subject': 'Noise Complaint',
                'description': 'Excessive noise from neighboring room during night hours.',
                'priority': 'Medium',
            },
            {
                'subject': 'Cleaning Request',
                'description': 'Corridor needs urgent cleaning.',
                'priority': 'Low',
            },
        ]

        for idx, student in enumerate(students):
            if idx < len(complaints_data):
                data = complaints_data[idx]
                allocation = RoomAllocation.objects.filter(
                    student=student,
                    status='Approved'
                ).first()

                Complaint.objects.create(
                    student=student,
                    subject=data['subject'],
                    description=data['description'],
                    priority=data['priority'],
                    room=allocation.room if allocation else None,
                    status='Pending',
                    created_at=timezone.now() - timedelta(days=2)
                )

        self.stdout.write(self.style.SUCCESS(f'✓ Created sample complaints'))

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SAMPLE DATA SUMMARY')
        self.stdout.write('='*50)
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Rooms: {Room.objects.count()}')
        self.stdout.write(f'Allocations: {RoomAllocation.objects.count()}')
        self.stdout.write(f'Complaints: {Complaint.objects.count()}')
        self.stdout.write('='*50 + '\n')
