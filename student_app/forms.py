from django import forms
from .models import Teacher, Student

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'age', 'salary', 'email', 'joining_date']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'standard'] 

