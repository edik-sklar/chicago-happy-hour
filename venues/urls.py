from django.urls import path
from . import views

urlpatterns = [
    path('venues/', views.venue_list, name='venue-list'),
]