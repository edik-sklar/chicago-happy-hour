from django.db import models

class Source(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    url = models.URLField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Venue(models.Model):
    def __str__(self):
        return self.name
    name             = models.CharField(max_length=200)
    neighborhood     = models.CharField(max_length=100)
    address          = models.TextField()
    lat              = models.FloatField(null=True)
    lng              = models.FloatField(null=True)
    website_url      = models.URLField(blank=True)
    facebook_url     = models.URLField(blank=True)
    instagram_url    = models.CharField(max_length=100, blank=True)
    google_place_id  = models.CharField(max_length=100, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)


class HappyHour(models.Model):
    def __str__(self):
        return f"{self.venue.name} — {self.day_of_week}"
    venue         = models.ForeignKey(Venue, on_delete=models.CASCADE)
    day_of_week   = models.TextField()
    start_time    = models.TimeField()
    end_time      = models.TimeField()
    deal          = models.TextField()
    source        = models.CharField(max_length=50)
    last_verified = models.DateField(null=True)
    created_at    = models.DateTimeField(auto_now_add=True)