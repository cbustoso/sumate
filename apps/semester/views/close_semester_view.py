from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.semester.models import Semester
from apps.semester.services.semester_service import SemesterService


class CloseSemesterView(APIView):
    """
    Expires the specified semester, expires all related events, 
    and deducts points from users as applicable.
    """
    def post(self, request, *args, **kwargs):
        try:
            semester_id = request.data.get('semester_id')
            if not semester_id:
                return Response({"error": "Semester ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                expiring_semester = Semester.objects.get(pk=semester_id, status='active')
            except Semester.DoesNotExist:
                return Response({"error": "Semester not found."}, status=status.HTTP_404_NOT_FOUND)
            
            expired_semester = SemesterService.close_semesters_and_update_points(expiring_semester)
            
            if not expired_semester:
                return Response({"success": "No es posible cerrar el semestre aun."}, status=status.HTTP_200_OK)
            
            return Response({"success": f"Semestre: {expired_semester.name}, Correlativo: {expired_semester.correlative} cerrado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)