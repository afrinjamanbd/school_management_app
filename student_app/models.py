from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    salary = models.FloatField(null=False, blank=True, default=15000)
    email = models.EmailField(primary_key = True, max_length=150)
    joining_date = models.DateField(null=False)
    educational_background = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.email
    

class ClassNSection(models.Model):
    standard = models.PositiveIntegerField(null=True) 
    guide_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    total_student = models.PositiveIntegerField(null=False, blank=True, default=50)
    room_name =  models.CharField(max_length=50, unique=True)
    section = models.CharField(max_length=2, default='A')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.room_name


class Student(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher)
    address =  models.CharField(max_length=200, default='Dhaka')
    fees = models.FloatField(null=True, blank=True, default=3000.0)
    standard = models.ForeignKey(ClassNSection, on_delete=models.CASCADE, default='') 

    def __str__(self):
        return self.name
    

class Subjects(models.Model):
    name = models.CharField(max_length=50)
    classnsecions = models.JSONField(default=dict)

