from django.db import transaction
from apps.semester.models import Semester
from apps.point.services.expired_points_service import ExpiredPointsService

class SemesterService:
    @staticmethod
    def get_active_semester() -> Semester:
        """
        Fetches the active semester with the highest correlative.
        """
        return Semester.objects.filter(status='active').order_by('-correlative').first()
    
    @staticmethod
    def get_oldest_active_semester() -> Semester:
        """
        Fetches the oldest active semester.
        """
        return Semester.objects.filter(status='active').order_by('correlative').first()

    @staticmethod
    def close_semesters_and_update_points(expiring_semester: Semester) -> Semester:
        """
        Transitions semesters by expiring the oldest active semester, activating the next draft semester,
        and updates points for all affected users.
        """
        with transaction.atomic():        
            SemesterService.mark_semester_as_expired(expiring_semester)

            ExpiredPointsService.adjust_user_points_for_expired_semester(expiring_semester)

            return expiring_semester
        
    @staticmethod
    def mark_semester_as_expired(semester):
        semester.status = 'expired'
        semester.save()

    @staticmethod
    def activate_upcoming_semester(semester):
        semester.status = 'active'
        semester.save()

    

