from django.urls import path
import student_app.views as views
from student_app.views import TeacherAPIView, InfoAPIView, ClassNSectionAPIView, StudentAPIView, SubjectsAPIView


urlpatterns = [
    path('student_info/', views.home, name='hompage'),
    path('add-techer/', views.create_teacher_info, name='create_teacher_info'),
    path('about/', views.about, name='about'),
    path('example/', views.new_m, name='newm'),
    path('db_filter/<str:email>', views.db_filter, name='db_filter'),
    path('teachers/<str:pk>', TeacherAPIView.as_view(), name='teacher_api'),
    path('info/<str:pk>', InfoAPIView.as_view(), name='info_api'),
    path('classsections/', ClassNSectionAPIView.as_view(), name='class_section_api'),
    path('students/', StudentAPIView.as_view(), name='student_api'),
    path('subjects/', SubjectsAPIView.as_view(), name='subject_api')
]