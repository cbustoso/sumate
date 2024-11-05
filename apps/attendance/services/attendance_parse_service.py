import pandas as pd
from typing import List, Tuple
from django.db.models import QuerySet
from apps.account.models import User
from django.db.models.functions import Lower

class AttendanceFileParserService:
    @staticmethod
    def parse_attendance_file(file, key: str = 'RUT') -> Tuple[List[User], List[str]]:
        """
        Parses an attendance file to extract attendee information more efficiently.

        Parameters:
        - file: The uploaded file containing attendance data.
        - key (str): The column name in the Excel file that contains the unique identifiers for attendees. Defaults to 'RUT'.

        Returns:
        Tuple[List[User], List[str]]: A tuple containing a list of User instances found and a list of RUTs not found.
        """
        data_frame = pd.read_excel(file)
        if key not in data_frame.columns:
            raise KeyError(f"El identificador '{key}' no existe en el archivo.")

        unique_ruts = set(str(rut).lower() for rut in data_frame[key].unique())
        
        matching_users = User.objects.annotate(lower_run=Lower('run')
        ).filter(lower_run__in=[rut.lower() for rut in unique_ruts], is_active=True)
        
        found_ruts = {str(user.run).lower() for user in matching_users}
        not_found_ruts = unique_ruts - found_ruts

        found_users = list(matching_users)
        not_found_users = list(not_found_ruts)

        return found_users, not_found_users