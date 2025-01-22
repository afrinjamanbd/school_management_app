import json
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

class ClassNSectionAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a teacher with email as primary key
        self.guide_teacher = Teacher.objects.create(
            name="Mr. Smith",
            age=40,
            salary=20000,
            email="smith@example.com",
            joining_date="2020-01-01"
        )

        # Data for ClassNSection
        self.class_data = {
            'standard': 10,
            'guide_teacher': self.guide_teacher.email,  
            'room_name': 'Room A',
            'section': 'A',
            'total_student': 40
        }
        # Create ClassNSection instance
        self.class_section = ClassNSection.objects.create(
            standard=self.class_data['standard'],
            guide_teacher=self.guide_teacher,  
            room_name=self.class_data['room_name'],
            section=self.class_data['section'],
            total_student=self.class_data['total_student']
        )

    def test_get_all_sections(self):
        # Test for retrieving all sections
        response = self.client.get(reverse('class_section_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_create_section(self):
        # Create another teacher
        guide_teacher_new = Teacher.objects.create(
            name="Ms. Taylor",
            age=35,
            salary=22000,
            email="sajjad0mahmud@gmail.com", 
            joining_date="2021-06-15"
        )

        # Data for new ClassNSection
        new_section_data = {
            'standard': 12,
            'guide_teacher': guide_teacher_new.email,  
            'room_name': 'Room B',
            'section': 'B',
            'total_student': 45
        }

        # Test creating a new ClassNSection
        response = self.client.post(
            reverse('class_section_api'),
            json.dumps(new_section_data),  
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['room_name'], new_section_data['room_name'])


class StudentAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.teacher = Teacher.objects.create(
            name="John Doe",
            age=35,
            salary=25000,
            email="johndoe@example.com",
            joining_date="2023-01-01"
        )

        self.class_section = ClassNSection.objects.create(
            standard=5,
            guide_teacher=self.teacher,
            room_name="Room A",
            section="A",
            total_student=30
        )

        self.student_data = {
            'name': 'Jane Doe',
            'address': 'Dhaka',
            'fees': 3000,
            'standard': self.class_section.id,
            'teachers': [self.teacher.email]
        }
        self.student = Student.objects.create(
            name=self.student_data['name'],
            address=self.student_data['address'],
            fees=self.student_data['fees'],
            standard=self.class_section
        )
        self.student.teachers.add(self.teacher)

    def test_get_all_students(self):
        response = self.client.get(reverse('student_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], self.student.name)


    def test_create_student(self):
        new_student_data = {
            'name': 'Jack Smith',
            'address': 'Chittagong',
            'fees': 4000,
            'standard': self.class_section.id,
            'teachers': [self.teacher.email]
        }
        response = self.client.post(
            reverse('student_api'),
            json.dumps(new_student_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], new_student_data['name'])



class SubjectsAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.subject_data = {
            'name': 'Mathematics',
            'classnsecions': {'class_1': ['section_A', 'section_B']}
        }

        self.subject = Subjects.objects.create(
            name=self.subject_data['name'],
            classnsecions=self.subject_data['classnsecions']
        )

    def test_get_all_subjects(self):
        response = self.client.get(reverse('subject_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


    def test_create_subject(self):
        new_subject_data = {
            'name': 'Science',
            'classnsecions': {'class_2': ['section_A']}
        }
        response = self.client.post(
            reverse('subject_api'),
            json.dumps(new_subject_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], new_subject_data['name'])

   