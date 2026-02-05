from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Message


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        message_text = request.POST.get('message')

        Message.objects.create(
            full_name=name,
            phone=phone,
            email=email,
            body=message_text
        )


        messages.success(request, "Xabaringiz yuborildi!")

        return redirect('home')

    projects = Project.objects.all()

    return render(request, 'home.html', {'projects': projects})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'all_projects.html', {'projects': projects})