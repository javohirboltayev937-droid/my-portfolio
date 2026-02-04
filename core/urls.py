from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects-all/', views.projects_list, name='projects_all'),
]