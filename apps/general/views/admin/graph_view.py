from django.shortcuts import render, redirect
from django.db.models import Prefetch, Count
from django.contrib.auth.decorators import user_passes_test

from apps.account.models.user import User
from apps.event.models.event import Event
from apps.event.models.event_types import EventType
from apps.general.services.graph_service import get_students_with_prizes
from apps.point.models.expirated_points import ExpiredPoints
from apps.point.services.expired_points_service import ExpiredPointsService
from apps.prize.models.prize_redemption import PrizeRedemption
from apps.semester.models.semester import Semester
from apps.semester.services.semester_service import SemesterService



def is_admin_superuser_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff or user.groups.filter(name='admin').exists())

def redirect_home():
    return redirect('/')

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def graph_reedemable_prizes_view(request):
    semesters = Semester.objects.filter(status='active').all().order_by('-correlative')
    
    context = {
        'semesters': semesters
    }
    
    return render(request, 'admin/reedemable_prizes.html', context)

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def graph_points_to_expire_view(request):
    return render(request, 'admin/points_to_expire.html')

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def non_attendees_view(request):
    return render(request, 'admin/non_attendees.html')

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def prize_redemption_view(request):
    semesters = Semester.objects.all().order_by('-correlative')
    
    context = {
        'semesters': semesters
    }
    
    return render(request, 'admin/prize_redemptions.html', context)

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def expired_points_view(request):
    semesters = Semester.objects.all().order_by('-correlative')
    
    context = {
        'semesters': semesters
    }
    
    return render(request, 'admin/expired_points.html', context)

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def prize_total_view(request):
    semesters = Semester.objects.all().order_by('-correlative')

    context = {
        'semesters': semesters
    }
    
    return render(request, 'admin/general_prizes.html', context)

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def participation_events_view(request):
    semesters = Semester.objects.all().order_by('-correlative')
    events = Event.objects.filter(is_active=True).order_by('name')

    context = {
        'semesters': semesters,
        'events': events
    }
    
    return render(request, 'admin/participation_events.html', context)

@user_passes_test(is_admin_superuser_staff, login_url='/', redirect_field_name=None)
def participation_type_events_view(request):
    semesters = Semester.objects.all().order_by('-correlative')
    event_types = EventType.objects.filter(is_active=True).order_by('name')

    context = {
        'semesters': semesters,
        'event_types': event_types
    }
    
    return render(request, 'admin/participation_type_events.html', context)
