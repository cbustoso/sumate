from django.urls import path
from apps.semester.views.close_semester_view import CloseSemesterView
from apps.semester.views.semester_attendance_report import generate_attendee_excel


urlpatterns_api = [
    path('close', CloseSemesterView.as_view(), name='close_semester'),
    path('attendees/excel/<int:semester_id>/', generate_attendee_excel, name='generate_attendee_excel_semester'),
]