from rest_framework import serializers
from .models import Teacher, ClassNSection, Student, Subjects

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ClassNSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassNSection
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
