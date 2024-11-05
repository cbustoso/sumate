from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from renderer_classes.base_renderer import BasePostView
from apps.attendance.services.attendance_service import AttendanceService
from apps.attendance.services.attendance_parse_service import AttendanceFileParserService


class AttendanceFileUploadApi(BasePostView):
    """
    Uploads an attendance file and creates attendance records for the users mentioned in the file,
    updating their points according to the specified event.
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        event_id = request.POST.get('event_id')

        if not file:
            return Response({"error": "Debe cargar un archivo."}, status=status.HTTP_400_BAD_REQUEST)
        if not event_id:
            return Response({"error": "ID de evento no entregado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event_id = int(event_id)
        except ValueError:
            return Response({"error": "ID de evento no es válido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            found_users, not_found_ruts = AttendanceFileParserService.parse_attendance_file(file)
            attendances_created = AttendanceService.register_attendees(found_users, event_id)

            if attendances_created or not_found_ruts:
                message = {"message": "Asistencia cargada exitósamente.", "not_found_ruts": not_found_ruts}
                if not_found_ruts:
                    message["not_found_ruts"] = not_found_ruts
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "No se crearon asistencias, puede que los usuarios ya hayan sido registrados para el evento o que el evento no exista."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)