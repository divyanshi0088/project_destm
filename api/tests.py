from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Teacher, Student, User


from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from api.models import Teacher, Student

User = get_user_model()

class UserAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a teacher user
        self.teacher_user = User.objects.create_user(
            username='teacher1', email='teacher1@example.com', password='password123', role='teacher'
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        
        # Create a student user
        self.student_user = User.objects.create_user(
            username='student1', email='student1@example.com', password='password123', role='student'
        )
        self.student = Student.objects.create(user=self.student_user, teacher=self.teacher)

        # API Endpoints
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
        self.dashboard_url = '/api/dashboard/'

        # Fetch and store authentication tokens for tests
        self.teacher_access_token = self.get_access_token('teacher1@example.com', 'password123')
        self.student_access_token = self.get_access_token('student1@example.com', 'password123')

    def get_access_token(self, email, password):
        """Helper function to log in a user and return access token"""
        response = self.client.post(self.login_url, {'email': email, 'password': password}, format='json')
        return response.data['tokens']['access'] if response.status_code == 200 else None

    def test_register_teacher(self):
        """Test teacher registration"""
        data = {
            'username': 'newteacher',
            'email': 'newteacher@example.com',
            'password': 'password123',
            'password_confirmation': 'password123',
            'role': 'teacher'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Teacher registered successfully')

    def test_register_student_without_teacher(self):
        """Test that student registration fails if no teacher ID is provided"""
        data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password': 'password123',
            'password_confirmation': 'password123',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_student_with_teacher(self):
        """Test student registration with a valid teacher ID"""
        data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password': 'password123',
            'password_confirmation': 'password123',
            'role': 'student',
            'teacher_id': self.teacher.id
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Student registered successfully')

    def test_dashboard_access_teacher(self):
        """Test teacher dashboard access with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_access_token}')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'teacher')
        self.assertIn('students', response.data)

    def test_dashboard_access_student(self):
        """Test student dashboard access with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_access_token}')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'student')
        self.assertIn('teacher', response.data)

    def test_unauthorized_dashboard_access(self):
        """Test dashboard access without authentication"""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

