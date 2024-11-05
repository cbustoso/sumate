from django.urls import path
from apps.account.api.account_file_score_load_api import AccountFileScoreLoadApi
from apps.account.api.login_api import login_request
from apps.account.api.account_file_load_api import AccountFileLoadApi
from apps.account.api.status_api import statusApi
from apps.account.views.attendance_report import generate_attendee_excel
from apps.account.views.user_view import upload_file_initial_view, upload_file_score_view

app_name_account = 'account'

urlpatterns_api = [
    # Auth path
    path("auth/", login_request, name="login_api"),
    
    path('status/profile', statusApi.as_view(), name='status_account_api'),
    path('upload-file/initial', AccountFileLoadApi.as_view(), name='upload_file_initial_api'),
    path('upload-file/score', AccountFileScoreLoadApi.as_view(), name='upload_file_score_api'),
    path('career/<int:career_id>/attendees/excel/<int:semester_id>/', generate_attendee_excel, name='generate_attendee_excel'),
]

urlpatterns_views = [
    path('upload-file/initial', upload_file_initial_view, name='upload_file_initial'),
    path('upload-file/score', upload_file_score_view, name='upload_file_score'),
]