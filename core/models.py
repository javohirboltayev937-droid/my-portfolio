from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    technology = models.CharField(max_length=100)
    github_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Message(models.Model): # Yangi: Sayt orqali yozishsa shu yerga tushadi
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} dan xabar"