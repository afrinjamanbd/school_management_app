from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .views import model_filter
from .models import (Teacher, ClassNSection, Student, Subjects)

class TeacherAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_data = {
            'name': 'John Doe',
            'age': 35,
            'salary': 25000,
            'email': 'johndoe@example.com',
            'joining_date': '2023-01-01',
            'educational_background': {'degree': 'MSc', 'field': 'Mathematics'}
        }
        self.teacher = Teacher.objects.create(**self.teacher_data)

    def test_get_all_teachers(self):
        response = self.client.get(reverse('teacher_api', kwargs={'pk': 'all'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_teacher(self):
        response = self.client.get(reverse('teacher_api', kwargs={'pk': self.teacher.email}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.teacher.email)

    def test_create_teacher(self):
        new_teacher_data = {
            'name': 'Jane Smith',
            'age': 30,
            'salary': 28000,
            'email': 'janesmith@example.com',
            'joining_date': '2023-02-01',
            'educational_background': {'degree': 'PhD', 'field': 'Physics'}
        }
        response = self.client.post(reverse('teacher_api', kwargs={'pk': 'new'}),
                                    new_teacher_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], new_teacher_data['email'])

    def test_get_teacher_not_found(self):
        response = self.client.get(reverse('teacher_api', kwargs={'pk': 'mailafrinjaman@gmail.com'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_db_filter(self):
        response = model_filter()
        expected_response = [{'name': 'John Doe',
                              'email': 'johndoe@example.com',
                              'educational_background': {'degree': 'MSc',
                                                         'field': 'Mathematics'
                                                         }
                            }]
        self.assertEqual(response, expected_response)
