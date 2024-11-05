from typing import List, Dict, Tuple
from django.db.models import Q
from collections import defaultdict
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.account.models.user import User
from apps.attendance.models.attendance import Attendance
from apps.point.models import ExpiredPoints
from apps.semester.models.semester import Semester
from apps.prize.models.prize_redemption import PrizeRedemption


class ExpiredPointsService:
    @staticmethod
    def get_expired_points_info(expiring_semester: Semester) -> Tuple[Dict[int, int], List[Dict]]:
        """
        Gets information on points to expire and affected users without making any point adjustments.
        
        Parameters:
        - expiring_semester (Semester): The semester for which information will be obtained.
        
        Returns:
        - Tuple[Dict[int, int], List[Dict]]: A dictionary with points to be deducted per user
          and a list of users with pending redemptions.
        """
        points_deduction_by_user: Dict[int, int] = defaultdict(int)

        # Determine the next semester (correlative N+1)
        active_semesters = Semester.objects.filter(Q(status='active') | Q(pk=expiring_semester.pk))

       
        # Fetch attendance records for the expiring semester
        attendance_records = Attendance.objects.filter(
            event__semester=expiring_semester
        ).select_related('attendee').values_list('attendee__id', 'points')

        for attendee_id, points in attendance_records:
            points_deduction_by_user[attendee_id] += points

        if not active_semesters:
            return points_deduction_by_user, []

        # Fetch redemption records for the next semester
        redemption_records = PrizeRedemption.objects.filter(
            semester__in=active_semesters
        ).exclude(status='canceled').select_related('student').values_list('student__id', 'points')

        for student_id, points in redemption_records:
            points_deduction_by_user[student_id] = max(points_deduction_by_user.get(student_id, 0) - points, 0)

        # Fetch pending redemptions for the expiring semester
        pending_redeems = PrizeRedemption.objects.filter(
            semester=expiring_semester,
            status='hold'
        ).select_related('student', 'prize').all()
        
        users_with_pending_redeems = [
            {
                'run': redeem.student.run,
                'first_name': redeem.student.first_name,
                'last_name': redeem.student.last_name,
                'email': redeem.student.email,
                'redeem_name': redeem.prize.name,
                'points_to_return': redeem.points
            }
            for redeem in pending_redeems
        ]
        
        return points_deduction_by_user, users_with_pending_redeems

    @staticmethod
    def adjust_user_points_for_expired_semester(expiring_semester: Semester) -> None:
        """
        Deducts points from users based on their attendances in the expiring semester
        and redemptions in the immediate next semester.
        
        Parameters:
        - expiring_semester (Semester): The semester for which points will be adjusted.
        """
        points_deduction_by_user, pending_redeems = ExpiredPointsService.get_expired_points_info(expiring_semester)

        if not points_deduction_by_user:
            return

        users_to_update: List[User] = []
        expired_points_records: List[ExpiredPoints] = []

        users = User.objects.filter(id__in=list(points_deduction_by_user.keys()))
        with transaction.atomic():
            for user in users:
                points_to_deduct = points_deduction_by_user[user.id]
                actual_deduction = min(user.points, points_to_deduct)
                user.points -= actual_deduction
                users_to_update.append(user)

                # Prepare ExpiredPoints records
                expired_points_records.append(ExpiredPoints(
                    user=user,
                    total_points=actual_deduction,
                    executed_semester=expiring_semester,
                    expired_semester=expiring_semester
                ))

            # Bulk update users' points
            User.objects.bulk_update(users_to_update, ['points'])

            # Bulk create ExpiredPoints records
            ExpiredPoints.objects.bulk_create(expired_points_records)

            # Update pending redemptions to expired
            PrizeRedemption.objects.filter(
                semester=expiring_semester,
                status='hold'
            ).update(status='expired')

    @staticmethod
    def get_expired_points_for_user(user_id):
        user = get_object_or_404(User, pk=user_id)
        
        return ExpiredPoints.objects.filter(user=user).select_related('expired_semester').order_by('-created_at')

