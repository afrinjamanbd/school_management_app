from django.urls import path
from school_site import views

urlpatterns = [
    path('homepage/', views.home, name='hompage'),
    path('about/', views.about, name='about')
]


# 127.0.0.1/school_info/homepage
# 127.0.0.1/school_info/homepage