from django.shortcuts import render, redirect
from .models import Project, Message


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        message_text = request.POST.get('message')

        # Telefon raqam bilan birga saqlaymiz
        Message.objects.create(
            full_name=name,
            phone=phone,
            email=email,
            body=message_text
        )
        return redirect('home')

    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'all_projects.html', {'projects': projects})