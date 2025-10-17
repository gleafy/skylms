from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson
from users.models import User

class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com', 
            password='testpass'
        )
        self.course = Course.objects.create(
            title="Test Course", 
            owner=self.user
        )
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Test Description", 
            "video_link": "https://www.youtube.com/watch?v=test",
            "course": self.course.id,
            "owner": self.user.id
        }

    def test_lesson_create_valid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/lessons/',
            self.lesson_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_invalid_url(self):
        invalid_data = self.lesson_data.copy()
        invalid_data["video_link"] = "https://invalid.com/video"
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/lessons/',
            invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)