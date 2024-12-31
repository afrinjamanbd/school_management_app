from django.contrib import admin

from .models import Teacher, Student, ClassNSection
from .forms import TeacherForm, StudentForm

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('name', 'email', 'salary')
    search_fields = ('name',)
    list_filter = ('salary',)


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('name', 'fees')
    search_fields = ('id',)

class ClassNSectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(ClassNSection, ClassNSectionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
