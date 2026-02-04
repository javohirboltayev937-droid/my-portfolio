from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.all_projects_view, name='projects_page'),
    path('contact/', views.contact_view, name='contact_page'),
]