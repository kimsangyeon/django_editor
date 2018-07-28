from django.db import models
from django.utils import timezone
from froala_editor.fields import FroalaField
from django.conf import settings

class Page(models.Model):
    contents = FroalaField(plugins=settings.FROALA_EDITOR_PLUGINS)

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class UploadFileModel(models.Model):
    file = models.FileField(null=True)
    extension = models.TextField(default='')