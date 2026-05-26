from django.shortcuts import render
from .models import Venue

def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venues/venue_list.html', {'venues': venues})
def home(request):
    return render(request, 'venues/home.html')