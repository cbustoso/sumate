from django.db import models
from django.db.models import Case, Value, When, F, Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from utils.decorators.permissions import is_student
from apps.point.services.expired_points_service import ExpiredPointsService
from apps.account.models import User
from apps.prize.models.prize_redemption import PrizeRedemption
from apps.semester.models import Semester
from apps.attendance.models import Attendance
from apps.semester.services.semester_service import SemesterService

@user_passes_test(is_student)
def profile_view(request):
    """
    Display the profile of the currently logged-in user, including detailed statistics such as total events attended,
    total points earned, and total prizes redeemed.

    This view is protected and can only be accessed by users verified as students.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the profile page rendered, including user data and statistics.
    """
    user_id = request.user.id

    latest_active_semester = SemesterService.get_active_semester()

    total_attendances = Attendance.objects.filter(
        attendee_id=user_id,
        event__semester=latest_active_semester
    ).count()

    user = User.objects.filter(id=user_id).annotate(
        total_events_attended=Count('attendances'),
        total_points_earned=Coalesce(Sum('attendances__points'), 0),
    ).select_related('career', 'campus').get()

    attendances = Attendance.objects.filter(attendee_id=user_id).select_related('event', 'event__semester').annotate(
        event_name=F('event__name'),
        semester_name=F('event__semester__name'),
        points_awarded=F('points'),
        event_date=F('event__start')
    ).values(
        'event_name',
        'semester_name',
        'points_awarded',
        'event_date'
    ).order_by('-event__semester__correlative')

    redeemed_prizes = PrizeRedemption.objects.filter(student_id=user_id).select_related('prize', 'semester').annotate(
        prize_name=F('prize__name'),
        semester_name=F('semester__name'),  
        points_used=F('points'),
        redemption_status=Case(
            When(status='hold', then=Value('Reservado')),
            When(status='delivered', then=Value('Entregado')),
            When(status='canceled', then=Value('Cancelado')),
            When(status='expired', then=Value('Expirado')),
            default=Value('Desconocido'),
        output_field=models.CharField(),
        ),
        redemption_date=F('created_at')
    ).values(
        'prize_name',
        'semester_name',
        'points_used',
        'redemption_status',
        'redemption_date'
    )

    context = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "run": user.run,
        "shift": user.shift,
        "campus": user.campus.name if user.campus else '',
        "career": user.career.name if user.career else '',
        "points": user.points,
        "total_events_attended": total_attendances,
        "total_points_earned": user.total_points_earned,
        "attendances": attendances,
        "redeemed_prizes": redeemed_prizes,
        "expired_points_info": ExpiredPointsService.get_expired_points_for_user(user_id)
    }

    return render(request, 'student/profile.html', context)