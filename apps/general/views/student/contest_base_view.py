from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from apps.account.models.user import User
from apps.event.models.event import Event
from apps.attendance.models.attendance import Attendance
from apps.settings.models import UploadedFile
from utils.decorators.permissions import is_student

def contest_base_view(request):
    total_events = Event.objects.filter(is_active=True).count()
    total_points = Attendance.objects.aggregate(Sum('points'))['points__sum']
    total_points = total_points or 0
    student_group = Group.objects.get(name='student')
    total_students = User.objects.filter(is_active=True, groups=student_group).count()
    bases = UploadedFile.objects.filter(name='bases').first()

    context = {
        'total_events': total_events,
        'total_points': total_points,
        'total_students': total_students,
        'bases': bases
    }
    return render(request, 'student/contest_base.html', context)
