from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher, ClassNSection, Student, Subjects
from .serializers import TeacherSerializer, ClassNSectionSerializer, StudentSerializer, SubjectsSerializer, InfoSerializer

def home(request):
    return JsonResponse({'status': "Success"})

def about(request):
    return JsonResponse({'status': "Success"})

def create_teacher_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        salary = request.POST.get('salary')
        joining_date = request.POST.get('joining_date')

        if all(name, age, email, salary, joining_date):
            try:
                Teacher.objects.create(name = name,
                                        age = age,
                                        email = email,
                                        salary = salary,
                                        joining_date = joining_date
                                        )
                return JsonResponse({"status": "Success", "messsage": "Congratulations!"})
            except Exception as e:
                return JsonResponse({'status': "Failed", "message": str(e)})
    return JsonResponse({'status': "Success", "message": "No data for get request"})

def create_student(request):
    student = Student()
    student.save()
    return JsonResponse("student created!")


def new_m(request):
    students = Student.objects.select_related('standard').all()
    for student in students:
        print(student.standard.room_name)
    serializer = StudentSerializer(students, many=True)
    return JsonResponse({'data': serializer.data})


def db_filter(reques, email):
    teachers = Teacher.objects.filter(salary__gt=15000, age__lt=70, email=email).values('name', 'joining_date')
    # serializer = TeacherSerializer(teachers, many=True, partial=True)
    return JsonResponse({'data': teachers})


def model_filter():
    teachers = Teacher.objects.filter(salary__gt=15000, age__lt=70).values('name',
                                                                           'email',
                                                                           'educational_background')
    return list(teachers)


class InfoAPIView(APIView):
    def get(self, request, pk=None):
        if pk == 'all':
            teachers = Teacher.objects.annotate(average_students=Avg('classnsection__total_student'))
            serializer = InfoSerializer(teachers, many=True)
            return Response(serializer.data)
        
        try:
            teacher = Teacher.objects.prefetch_related('classnsection_set').get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoSerializer(teacher)
        return Response(serializer.data)


class TeacherAPIView(APIView):
    def get(self, request, pk):
        if pk == 'all':
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data)
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)  
        serializer = TeacherSerializer(teacher, many=False)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        teacher.delete()
        return Response({'message': 'Teacher deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class ClassNSectionAPIView(APIView):
    def get(self, request):
        sections = ClassNSection.objects.all()
        serializer = ClassNSectionSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassNSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectsAPIView(APIView):
    def get(self, request):
        subjects = Subjects.objects.all()
        serializer = SubjectsSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


