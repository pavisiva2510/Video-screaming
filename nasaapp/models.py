from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    video_url=models.URLField(null=True)

    def __str__(self):
        return self.name


