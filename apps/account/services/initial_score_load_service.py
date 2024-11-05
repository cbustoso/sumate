import re
import pandas as pd
from django.db import transaction
from django.contrib.auth.models import Group
from apps.semester.models.semester import Semester
from apps.account.models import User
from apps.prize.models import Prize, PrizeRedemption
from apps.attendance.models import Attendance
from apps.event.models import Event

class InitialScoreLoadService:
    """
    Service for loading initial data from an Excel file, updating existing user accounts with attendance and prize redemptions.
    """

    @staticmethod
    def parse_and_load_data_from_excel(file) -> None:
        """
        Parses an Excel file and loads initial data for existing users, including attendance records and prize redemptions.
        """
        data_frame = pd.read_excel(file, engine='openpyxl')
        return InitialScoreLoadService._load_score(data_frame)

    @staticmethod
    def _load_score(data_frame: pd.DataFrame) -> list:
        data_frame = data_frame[~data_frame['RUT'].isin(['nan'])]        

        missing_users = []

        with transaction.atomic():
            semester = Semester.objects.get(id=1)
            event = Event.objects.get(id=1)
        
            prize = Prize.objects.get(id=1)
            
            student_group, _ = Group.objects.get_or_create(name='student')
            users_dict = {user.run.lower().strip(): user for user in User.objects.filter(groups=student_group).exclude(run__exact='')}
            
            for _, row in data_frame.iterrows():
                run_raw = str(row['RUT']).lower().strip()
                run = re.sub(r'\.|-', '', run_raw)

                user = users_dict.get(run)
                
                if not user:
                    missing_users.append(run)
                    continue

                attendance_value = row.get('Asistencia 2023-2', 0)
                prize_redemption_value = row.get('Canjes 2023-2', 0)
                current_points = row.get('Puntaje Actual Febreo 2024', 0)
                
                if attendance_value > 0:
                    Attendance.objects.get_or_create(attendee=user, event=event, defaults={'points': attendance_value})

                if prize_redemption_value > 0:
                    PrizeRedemption.objects.get_or_create(prize=prize, student=user, defaults={'points': prize_redemption_value, 'semester': semester, 'status': 'delivered'})
                
                if current_points > 0:
                    user.points = current_points
                    user.save()

        return missing_users
