from django.db import models
from django.contrib.auth.admin import User


# Create your models here.

class PlayList(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
