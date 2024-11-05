import re
import time
import secrets
import pandas as pd
from django.db import connection, transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import connection
from apps.account.models import User, Career, Campus
from apps.account.utils import validate_rut, normalize_name

class InitialDataLoadService:
    """
    Service to load initial data from an Excel file, including careers and user accounts.
    This service ensures data integrity and avoids duplicates while optimizing for performance.
    """
    @staticmethod
    def generate_secure_token(length=32):
        return secrets.token_hex(length)

    @staticmethod
    def parse_and_load_data_from_excel(file_path) -> list:
        """
        Parses an Excel file to load initial data including unique career names and user accounts,
        ensuring data integrity and avoiding duplicates. It measures the execution time and the number of database queries.

        :param file_path: Path to an Excel file containing initial data.
        :return: List of RUTs with issues.
        """
        # Start measuring time and reset DB query log
        start_time = time.time()

        data_frame = pd.read_excel(file_path, engine='openpyxl')
        InitialDataLoadService._create_careers(data_frame)
        problem_ruts = InitialDataLoadService._create_users(data_frame)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        print(f"Total DB queries: {len(connection.queries)}")

        return problem_ruts

    @staticmethod
    def _create_careers(data_frame: pd.DataFrame) -> None:
        """
        Creates unique career entries from the 'NOM.CARRERA' column in the data frame,
        excluding names 'STAFF', 'ADMIN', or empty values.

        :param data_frame: Data frame containing the 'NOM.CARRERA' column.
        """
        with transaction.atomic():
            careers = set(data_frame['NOM.CARRERA'].str.lower().apply(normalize_name).unique()) - {'staff', 'admin', '', 'nan'}
            existing_careers = set(Career.objects.values_list('name', flat=True))
            new_careers = [Career(name=career) for career in careers if career not in existing_careers]
            Career.objects.bulk_create(new_careers, ignore_conflicts=True)
    
    @staticmethod
    def _create_users(data_frame: pd.DataFrame) -> list:
        """
        Creates user accounts from the provided data frame, ensuring unique email addresses.
        Sets users to inactive if RUT is invalid and collects such RUTs for reporting.
        Adds users to the 'student' group and reactivates existing users found in the data frame.

        :param data_frame: Data frame with user data.
        :return: List of RUTs with validation issues.
        """
        problem_ruts = []
        data_frame = data_frame.dropna(subset=['RUT', 'MAIL']).copy()
        data_frame['MAIL'] = data_frame['MAIL'].str.lower().str.strip()
        data_frame = data_frame[~data_frame['RUT'].isin(['nan'])]        
        emails = data_frame['MAIL'].unique().tolist()
        created_emails_users = []
        created_runs_users = []

        start_time = time.time()
        with transaction.atomic():
            custom_password = make_password(InitialDataLoadService.generate_secure_token()),
            student_group, _ = Group.objects.get_or_create(name='student')
            User.objects.filter(groups=student_group).update(is_active=False)
            existing_users = User.objects.in_bulk(emails, field_name='email')
            campus = Campus.objects.get(id=1)
            careers = Career.objects.in_bulk(field_name='name')
            users_to_create = []

            for _, row in data_frame.iterrows():
                email = row['MAIL']
                if email in created_emails_users or email in existing_users:
                    continue

                if email in created_emails_users:
                    problem_ruts.append(run)
                    continue

                run_raw = str(row['RUT']).lower().strip()
                run = re.sub(r'\.|-', '', run_raw)
                is_active = validate_rut(run)

                if run in created_runs_users:
                    problem_ruts.append(run)
                    continue

                if not is_active:
                    problem_ruts.append(run)
                    continue

                career_name = normalize_name(row['NOM.CARRERA'].lower())
                career = careers.get(career_name)
                shift = str(row['JORNADA'])
                
                user = User(
                    # TODO: Save the next line comment in case that we must return to the old use case 
                    # username=email.split('@')[0],
                    username=row['USERNAME'].lower().strip(),
                    first_name=row['NOMBRES'],
                    last_name=f"{row['AP.PATERNO']} {row['AP.MATERNO']}",
                    email=email,
                    run=run,
                    phone=row['TELEFONO'],
                    shift= shift if shift.upper() == 'D' or shift.lower() == 'V' else 'D',
                    career=career,
                    campus=campus,
                    password=custom_password,
                    is_active=is_active
                )
                print(user.email)
                users_to_create.append(user)
                created_emails_users.append(email)
                created_runs_users.append(run)
            
            end_time = time.time()
            print(f"Execution time FORITERROW: {end_time - start_time} seconds")
            print(f"Total DB queries: {len(connection.queries)}")
            User.objects.bulk_create(users_to_create)
            newly_created_users = User.objects.filter(email__in=created_emails_users)
            for user in newly_created_users:
                user.groups.add(student_group)

            User.objects.filter(email__in=emails).update(is_active=True)
        return problem_ruts

