from django.urls import path
import views

urlpatterns = [
    path('student_info/', views.home, name='hompage'),
    path('about/', views.about, name='about')
]