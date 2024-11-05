from django.urls import path
from apps.general.api.graphs_api import ExpiredPointsAPI, GeneralGraphAPI, NonAttendeesAPI, ParticipationEventsAPI, ParticipationEventsTypesAPI, PointsToExpirePointsAPI, PrizesAPI, PrizesMonthlyAPI, RedemptionsAPI
from apps.general.views.admin.graph_view import participation_events_view, graph_points_to_expire_view, graph_reedemable_prizes_view, non_attendees_view, participation_type_events_view, prize_redemption_view, expired_points_view, prize_total_view
from apps.general.views.student.home_view import home_view
from apps.general.views.student.contest_base_view import contest_base_view
from apps.general.views.student.prizes_view import prizes_view
from apps.general.views.student.profile_view import profile_view
from apps.general.views.student.service_explanation_view import service_explanation_view


urlpatterns_views = [
    path('inicio/', home_view, name='home'),
    path('sumate/', service_explanation_view, name='service_explanation'),
    path('bases/', contest_base_view, name='contest_base'),
    path('premios/', prizes_view, name='prizes'),
    path('perfil/', profile_view, name='profile'),
    path('reportes/usuarios/premios/', graph_reedemable_prizes_view, name='report_reedemable_prizes'),
    path('reportes/usuarios/expirar/', graph_points_to_expire_view, name='report_expire_points'),
    path('reportes/usuarios/asistencias/', non_attendees_view, name='report_non_attendees'),
    path('reportes/usuarios/canjes/', prize_redemption_view, name='report_prize_redemption'),
    path('reportes/usuarios/expirados/', expired_points_view, name='report_expired_points'),
    path('reportes/asistencias/', prize_total_view, name='report_attendees'),
    path('reportes/premios/', prize_total_view, name='report_total_prizes'),
    path('reportes/eventos/', participation_events_view, name='report_events'),
    path('reportes/tipos-eventos/', participation_type_events_view, name='report_type_events'),
]

urlpatterns_general_api = [
    path('report/users/prizes/', GeneralGraphAPI.as_view()),
    path('report/users/expired/', PointsToExpirePointsAPI.as_view()),
    path('report/users/non-attendees/', NonAttendeesAPI.as_view()),
    path('report/users/redemptions/', RedemptionsAPI.as_view()),
    path('report/users/expired/points/', ExpiredPointsAPI.as_view()),
    path('report/participation/prizes/', PrizesAPI.as_view()),
    path('report/participation/prizes/monthly/', PrizesMonthlyAPI.as_view()),
    path('report/participation/events/', ParticipationEventsAPI.as_view()),
    path('report/participation/events-types/', ParticipationEventsTypesAPI.as_view()),
]