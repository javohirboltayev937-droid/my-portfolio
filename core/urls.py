from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects-all/', views.projects_list, name='projects_all'),
    # JSON API
    path('api/projects/', views.api_projects, name='api_projects'),
    path('api/projects/<int:pk>/', views.api_projects_detail, name='api_projects_detail'),
    path('api/contact/', views.api_contact, name='api_contact'),
]