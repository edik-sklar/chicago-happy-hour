from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
