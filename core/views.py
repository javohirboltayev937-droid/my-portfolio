import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.views.decorators.http import require_http_methods

from .models import Project, Message
from .telegram import send_telegram_message


def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'all_projects.html', {'projects': projects})


# ===== JSON API =====

def api_projects(request):
    """GET /api/projects/ — barcha loyihalar JSON formatida."""
    qs = Project.objects.all().values('id', 'title', 'description', 'technology', 'github_link', 'image')
    result = []
    for p in qs:
        if p['image']:
            p['image_url'] = request.build_absolute_uri('/media/' + p['image'])
        else:
            p['image_url'] = None
        del p['image']
        result.append(p)
    return JsonResponse({'projects': result})


@require_http_methods(["POST"])
def api_contact(request):
    """POST /api/contact/ — kontakt formasini saqlaydi va Telegramga yuboradi."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': "Noto'g'ri so'rov formati."}, status=400)

    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    message_text = (data.get('message') or '').strip()

    if not name or not phone or not message_text:
        return JsonResponse({'success': False, 'error': "Barcha maydonlar to'ldirilishi shart."}, status=400)

    Message.objects.create(full_name=name, phone=phone, body=message_text)

    text = (
        "🔔 <b>Yangi xabar — Portfolio</b>\n\n"
        f"👤 <b>Ism:</b> {escape(name)}\n"
        f"📞 <b>Telefon:</b> {escape(phone)}\n"
        f"💬 <b>Xabar:</b>\n{escape(message_text)}"
    )
    send_telegram_message(text)

    return JsonResponse({'success': True, 'message': "Xabaringiz yuborildi! Tez orada bog'lanamiz."})


def api_projects_detail(request, pk):
    """GET /api/projects/<id>/ — bitta loyiha ma'lumoti."""
    try:
        p = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Loyiha topilmadi.'}, status=404)
    data = {
        'id': p.pk,
        'title': p.title,
        'description': p.description,
        'technology': p.technology,
        'github_link': p.github_link,
        'image_url': request.build_absolute_uri(p.image.url) if p.image else None,
    }
    return JsonResponse(data)