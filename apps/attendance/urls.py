from django.urls import path
from apps.attendance.api.attendance_file_upload_api import AttendanceFileUploadApi
from apps.attendance.views.attendance_view import upload_file_attendance_view


urlpatterns_api = [
    path('file', AttendanceFileUploadApi.as_view(), name='post_attendance_api')
]

urlpatterns_views = [    
    path('upload-file/attendance/<int:id>/', upload_file_attendance_view, name='upload_file_attendance'),
]