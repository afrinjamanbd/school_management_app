from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Teacher, Student


# Create your views here.
def show_teacher_info(request):
    if request.mehtod == 'POST':
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





