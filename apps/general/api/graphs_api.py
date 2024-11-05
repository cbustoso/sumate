from rest_framework import status
from rest_framework.response import Response

from apps.event.models.event import Event
from apps.event.models.event_types import EventType
from apps.semester.models.semester import Semester
from decorator.auth_decorator import admin_superuser_required
from apps.general.services.graph_service import get_participation_stats_by_event_and_semester, get_participation_stats_by_event_type_and_semester, get_students_with_prizes, graph_non_attendees, graph_points_to_expire, graph_redemption_prizes, graph_total_prizes, prizes_montly_report, prizes_report
from renderer_classes.base_renderer import BaseListView


class GeneralGraphAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            return Response(get_students_with_prizes())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class PointsToExpirePointsAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            return Response(graph_points_to_expire())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class NonAttendeesAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:         
            return Response(graph_non_attendees())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RedemptionsAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None

            return Response(graph_redemption_prizes(semester))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)            
        
class ExpiredPointsAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None

            return Response(graph_total_prizes(semester))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PrizesAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None

            return Response(prizes_report(semester))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PrizesMonthlyAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None

            return Response(prizes_montly_report(semester))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ParticipationEventsAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)
            event_id = request.query_params.get('event', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None
                
            if event_id is not None and event_id != 'Todos':
                event = Event.objects.get(id=event_id)
            else:
                event = None
                
            return Response(get_participation_stats_by_event_and_semester(semester, event))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ParticipationEventsTypesAPI(BaseListView):
    @admin_superuser_required
    def get(self, request, *args, **kwargs):
        try:
            semester_id = request.query_params.get('semester', None)
            event_type_id = request.query_params.get('event_type', None)

            if semester_id is not None and semester_id != 'Todos':
                semester = Semester.objects.get(id=semester_id)
            else:
                semester = None
                
            if event_type_id is not None and event_type_id != 'Todos':
                event = EventType.objects.get(id=event_type_id)
            else:
                event = None
                
            return Response(get_participation_stats_by_event_type_and_semester(semester, event))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
