from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
      path('', views.index, name='index'),
      path('index', views.index, name='index'),
      path('contact', views.contact, name="contact"),
      path('python', views.python, name="python"),
      path('php', views.php, name="php"),
      path('java', views.java, name="java"),
      path('javascript', views.javascript, name="javascript"),
      path('rubi', views.rubi, name="rubi"),
      path('blog/<slug:slug>/', views.blog_detail, name="blog_detail"),
      path('<slug:slug>/add_comment/', views.add_comment, name='add_comment')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)