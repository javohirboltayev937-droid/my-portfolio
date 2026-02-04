from django.shortcuts import render, redirect
from .models import Project, Message

def home(request):
    if request.method == "POST": # Agar kimdir xabar yuborsa
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        Message.objects.create(full_name=name, email=email, body=message_text)
        return redirect('home')

    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})
def all_projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def all_projects_view(request):
    projects = Project.objects.all()
    return render(request, 'all_projects.html', {'projects': projects})



def contact_view(request):
    if request.method == "POST":
        # Bu yerda xabarni saqlash kodi bo'ladi
        pass
    return render(request, 'contact.html')