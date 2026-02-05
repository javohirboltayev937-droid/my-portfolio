from .models import Project, Message
from django.contrib import admin
from .models import ContactMessage

admin.site.register(ContactMessage)

admin.site.register(Project)
admin.site.register(Message)