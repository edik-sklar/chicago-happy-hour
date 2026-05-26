from django.contrib import admin

from .models import Source, Venue, HappyHour

admin.site.register(Source)
admin.site.register(Venue)
admin.site.register(HappyHour)