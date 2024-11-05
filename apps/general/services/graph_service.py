from django.db.models import Prefetch, Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.models import Group
from apps.attendance.models.attendance import Attendance
from apps.enroll.models import Enroll
from apps.event.models.event import Event
from apps.account.models.user import User
from apps.event.models.event_types import EventType
from apps.point.models.expirated_points import ExpiredPoints
from apps.point.services.expired_points_service import ExpiredPointsService
from apps.prize.models.prize import Prize
from apps.prize.models.prize_redemption import PrizeRedemption
from apps.semester.models.semester import Semester
from apps.semester.services.semester_service import SemesterService

def get_students_with_prizes():
    # Fetch all prizes ordered by the points required
    all_prizes = list(Prize.objects.filter(is_active=True).order_by('points'))

    # Fetch users with their related career
    users = User.objects.select_related('career').filter(groups__name='student').all()

    # Process the fetched data in Python
    user_data = []
    for user in users:
        # Determine redeemable and upcoming prizes using list comprehensions
        redeemable_prizes = [prize.name for prize in all_prizes if prize.points <= user.points]
        upcoming_prizes = [prize.name for prize in all_prizes if prize.points > user.points]

        # Get the next three upcoming prizes
        next_prizes = upcoming_prizes[:3]

        user_career = user.career.name if user.career else "Sin carrera asignada"
    
        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'run': user.run,
            'email': user.email,
            'career_name': user_career,
            'points': user.points,
            'redeemable_prizes': redeemable_prizes,
            'next_prizes': next_prizes
        }
        user_data.append(user_info)
    
    return [
        {
            "name": f"{user['first_name']} {user['last_name']}",
            "run": user['run'],
            "email": user['email'],
            "career": user['career_name'],
            "points": user['points'],
            "redeemable_prizes": user['redeemable_prizes'],
            "upcoming_prizes": user['next_prizes']
        }
        for user in user_data
    ]
    
def graph_points_to_expire():
    semester = SemesterService.get_oldest_active_semester()
    
    points_deduction_by_user, pending_redeems = ExpiredPointsService.get_expired_points_info(semester)
    
    users = User.objects.filter(id__in=list(points_deduction_by_user.keys()))
    
    user_data = []
    for user in users:
        points_to_deduct = points_deduction_by_user[user.id]
        actual_deduction = min(user.points, points_to_deduct)
        user_info = {
            'run': user.run,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'career': user.career.name if user.career else "Sin carrera asignada",
            'points': user.points,
            'actual_deduction': actual_deduction
        }
        user_data.append(user_info)
    
    return [
        {
            "name": user['name'],
            "run": user['run'],
            "email": user['email'],
            "career": user['career'],
            "points": user['points'],
            "actual_deduction": user['actual_deduction']
       } for user in user_data
    ]

def graph_non_attendees(): 
    users = User.objects.filter(
        groups__name='student',
        is_active=True,
        attendances__isnull=True
    ).prefetch_related(
        Prefetch('attendances', to_attr='attendances_list')
    ).all()
    
    return [
        {
            "run": user.run,
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}",
            "career": user.career.name if user.career else "Sin carrera asignada",
            "is_active": user.is_active,
            "points": user.points,
        } for user in users
    ]
    
def graph_redemption_prizes(semester: Semester):
    print (semester)
    if semester:
        redemptions = PrizeRedemption.objects.filter(semester=semester).select_related(
            'student', 'prize', 'semester'
        ).values(
            'student__run',
            'student__first_name',
            'student__last_name',
            'student__career__name',
            'student__email',
            'prize__name',
            'points',
            'created_at',
            'updated_at',
            'semester__name',
            'status'
        )
    else:
        redemptions = PrizeRedemption.objects.select_related(
            'student', 'prize', 'semester'
        ).values(
            'student__run',
            'student__first_name',
            'student__last_name',
            'student__career__name',
            'student__email',
            'prize__name',
            'points',
            'created_at',
            'updated_at',
            'semester__name',
            'status'
        )    
        
    return [
        {
            "run": redemption['student__run'],
            "email": redemption['student__email'],
            "name": f"{redemption['student__first_name']} {redemption['student__last_name']}",
            "career": redemption['student__career__name'],
            "prize": redemption['prize__name'],
            "points": redemption['points'],
            "created_at": redemption['created_at'],
            "updated_at": redemption['updated_at'],
            "semester": redemption['semester__name'],
            "status": redemption['status']
        } for redemption in redemptions
    ]
    
def graph_total_prizes(semester: Semester):
    if semester:
        expired_points = ExpiredPoints.objects.filter(expired_semester=semester).select_related('student', 'semester').values(
            'user__run',
            'user__first_name',
            'user__last_name',
            'user__career__name',
            'user__email',
            'total_points',
            'created_at',
            'expired_semester__name'
        ).order_by('-created_at')
    else: 
        expired_points = ExpiredPoints.objects.select_related('student', 'semester').values(
            'user__run',
            'user__first_name',
            'user__last_name',
            'user__career__name',
            'user__email',
            'total_points',
            'created_at',
            'expired_semester__name'
        ).order_by('-created_at')
    
    return [
        {
            "run": expired_point['user__run'],
            "email": expired_point['user__email'],
            "name": f"{expired_point['user__first_name']} {expired_point['user__last_name']}",
            "career": expired_point['user__career__name'],
            "total_points": expired_point['total_points'],
            "created_at": expired_point['created_at'],
            "semester": expired_point['expired_semester__name']
        } for expired_point in expired_points
    ]
    
    
def prizes_report(semester: Semester):
    if semester:
        prizes = PrizeRedemption.objects.filter(semester=semester).select_related('prize', 'semester').values(
        'prize__name',
        'semester__name'
        ).annotate(
            total_redemptions=Count('id')
        ).order_by('semester__name', 'prize__name')
    else:
        prizes = PrizeRedemption.objects.select_related('prize', 'semester').values(
            'prize__name',
            'semester__name'
        ).annotate(
            total_redemptions=Count('id')
        ).order_by('semester__name', 'prize__name')
    
    return [
        {
            'prize': prize['prize__name'],
            'semester': prize['semester__name'],
            'total_redemptions': prize['total_redemptions']
        } for prize in prizes
    ]

def prizes_montly_report(semester: Semester):
    chart_data = {}
        
    monthly_redemptions = PrizeRedemption.objects.values(
        'prize__name',  # Nombre del premio
        month=ExtractMonth('created_at'), 
        year=ExtractYear('created_at')
    ).annotate(
        count=Count('id') 
    ).order_by('year', 'month', 'prize__name')
    
    for redemption in monthly_redemptions:
        prize_name = redemption['prize__name']
        if prize_name not in chart_data:
            chart_data[prize_name] = [0] * 12 

        month_index = redemption['month'] - 1
        chart_data[prize_name][month_index] += redemption['count']
    
    return chart_data
    
def get_participation_stats_by_event_and_semester(semester: Semester, event: Event):
    stats = []
    enrolled = Enroll.objects.all()

    attendance_filter = {'event__isnull': False}

    if semester:
        attendance_filter['event__semester'] = semester
    if event:
        attendance_filter['event'] = event
        
    participating_students_per_event_semester = Attendance.objects.filter(
        **attendance_filter
    ).values('event__name', 'event__semester__name', 'event__semester__id').annotate(
        participating_students=Count('attendee_id', distinct=True)
    )
                
    stats = []
    for item in participating_students_per_event_semester:
        event_name = item['event__name'] or "Evento sin nombre"
        semester_name = item['event__semester__name'] or "Semestre sin nombre"
        semester_id = item['event__semester__id']
        participating_students = item['participating_students']
        
        enrolled_semester = enrolled.filter(semester_id=semester_id).first()
        total_students_available = enrolled_semester.total_enrolled if enrolled_semester else 0

        percentage = (participating_students / total_students_available * 100) if total_students_available > 0 else 0

        stats.append({
            'event': event_name,
            'semester': semester_name,
            'participating_students': participating_students,
            'total_students': total_students_available,
            'percentage': round(percentage, 2),
        })

    return stats

def get_participation_stats_by_event_type_and_semester(semester: Semester, event: EventType):
    enrolled = Enroll.objects.all()
    attendance_filter = {'event__isnull': False}
    semester_name = semester.name if semester else None
    
    if semester:
        attendance_filter['event__semester'] = semester
    if event:
        attendance_filter['event__event_type'] = event
    print(semester)
    participating_students_per_event_type_semester = Attendance.objects.filter(
        **attendance_filter
    ).values(
        'event__event_type__name',
        'event__semester__id'
    ).annotate(
        participating_students=Count('id') 
    ).order_by(
        'event__event_type__name', 'event__semester__id'
    )
    
    stats = []
    for item in participating_students_per_event_type_semester:
        event_type_name = item['event__event_type__name'] or "Tipo de evento sin nombre"
        semester_name = semester_name or "Semestre sin nombre"
        semester_id = item['event__semester__id']
        participating_students = item['participating_students']

        enrolled_semester = enrolled.filter(semester_id=semester_id).first()
        total_students_available = enrolled_semester.total_enrolled if enrolled_semester else 0
            
        percentage = (participating_students / total_students_available * 100) if total_students_available > 0 else 0

        stats.append({
            'event_type': event_type_name,
            'semester': semester_name,
            'participating_students': participating_students,
            'total_students': total_students_available,  # Total de estudiantes disponibles
            'percentage': round(percentage, 2),
        })

    return stats