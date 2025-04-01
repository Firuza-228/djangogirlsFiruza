from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
