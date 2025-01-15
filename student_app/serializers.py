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


class InfoSerializer(serializers.ModelSerializer):
    classes = ClassNSectionSerializer(source='classnsection_set', many=True, read_only=True)
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ('name', 'email', 'age', 'salary', 'educational_background', 'classes', 'total_students')

    def get_total_students(self, obj):
        return sum(section.total_student for section in obj.classnsection_set.all())