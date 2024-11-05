from django.shortcuts import render
from apps.event.models.event import Event

def home_view(request):
    events = Event.objects.filter(status='enabled', is_active=True).order_by('-start')
    
    context = {
        'events': events,
    }

    return render(request, 'student/home.html', context)
