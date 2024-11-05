from typing import List
from django.db import transaction 
from django.contrib.auth.models import Group
from apps.account.models.user import User

class AccountService:
    @staticmethod
    def bulk_users_points_update(users: List[User]) -> None:
        """
        Bulk updates 'points' for a list of User instances.
        
        Parameters:
        - users: Users with 'points' already set to new values.
        """
        return User.objects.bulk_update(users, ['points'])
    
    @staticmethod
    def validate_create_password(username: str):
        with transaction.atomic():
            student_group, _ = Group.objects.get_or_create(name='student')
            user_to_validate = User.objects.filter(username=username.strip().lower(), create_password=False, groups=student_group)
            if user_to_validate and len(user_to_validate) == 1:
                user_to_set_password = user_to_validate[0]
                if user_to_set_password.run:
                    user_to_set_password.set_password(user_to_set_password.run)
                    user_to_set_password.create_password = True
                    user_to_set_password.save()
