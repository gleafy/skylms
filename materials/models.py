from django.db import models
from django.conf import settings
from .validators import validate_youtube_url

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    description = models.TextField()

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_previews/", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    video_link = models.URLField(validators=[validate_youtube_url])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
