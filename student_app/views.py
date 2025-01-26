from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
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
            teachers=Teacher.objects.annotate(average_students=Avg('classnsection_total_student'))
            serializer = InfoSerializer(teachers, many=True)
            return Response(serializer.data)
        try:
            teachers = Teacher.objects.prefetch_related('classnsection_set').get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status= status.HTTP_404_NOT_FOUND)
        
        serializer = InfoSerializer(teachers)
        return Response(serializer.data)

    def post(self, request, pk=None):
        try:
            teachers = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error':'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teachers, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            teachers = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error':'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teachers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            teachers = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error':'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherSerializer(teachers, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        teacher.delete()
        return Response({'message': 'Teacher deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

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
    def get(self, request, pk):
        if pk == 'all':
            sections = ClassNSection.objects.all()
            serializer = ClassNSectionSerializer(sections, many=True)
            return Response(serializer.data)
        try:
            sections = ClassNSection.objects.prefetch_related('class_section_api').get(pk=pk)
        except ClassNSection.DoesNotExist:
            return Response({'error': 'ClassNSection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClassNSectionSerializer(sections)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassNSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            sections = ClassNSection.objects.get(pk=pk)
        except ClassNSection.DoesNotExist:
            return Response({'error': 'ClassNSection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClassNSectionSerializer(sections, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            sections = ClassNSection.objects.get(pk=pk)
        except ClassNSection.DoesNotExist:
            return Response({'error': 'ClassNSection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClassNSectionSerializer(sections, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        sections = ClassNSection.objects.get(pk=pk)
        sections.delete()
        return Response({'error': 'ClassNSection not found'}, status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(APIView):
    def get(self, request, pk):
        if pk == 'all':
            students = Student.objects.all()
            serializer = TeacherSerializer(students, many=True)
            return Response(serializer.data)
        try:
            students = Student.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)  
        serializer = TeacherSerializer(students, many=False)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Students not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Students not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serailizer = StudentSerializer(student, data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data, status=status.HTTP_201_CREATED)
        return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = Student.objects.get(pk=pk)
        student.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

class SubjectsAPIView(APIView):
    def get(self, request, pk):
        if pk == 'all':
            subjects = Subjects.objects.all()
            serializer = SubjectsSerializer(subjects, many=True)
            return Response(serializer.data)
        try:
            subjects = Subjects.objects.get(pk=pk)
        except Subjects.DoesNotExist:
            return Response({'errors':'Subjects not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try: 
            subjects = Subjects.objects.get(pk=pk)     
        except Subjects.DoesNotExist:
            return Response({'errors':'Subjects not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubjectsSerializer(subjects, data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            subjects = Subjects.objects.get(pk=pk)
        except Subjects.DoesNotExist:
            return Response({'errors':'Subjects not found'}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = SubjectsSerializer(subjects, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subjects = Subjects.objects.get(pk=pk)
        subjects.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

