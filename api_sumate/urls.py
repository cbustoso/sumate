from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from apps.account.views.logout_view import logout_view
from apps.account.views.login_view import CustomLoginView
from apps.event.urls import urlpatterns as event_urlpatterns_api
from apps.semester.urls import urlpatterns_api as semester_urlpatterns_api
from apps.prize.urls import urlpatterns_api as prize_urlpatterns_api
from apps.account.urls import urlpatterns_api as account_urlpatterns_api, urlpatterns_views as account_urlpatterns_views
from apps.attendance.urls import urlpatterns_api as attendance_urlpatterns_api, urlpatterns_views as attendance_urlpatterns_views
from apps.general.urls import urlpatterns_views as general_urlpatterns_views
from apps.general.urls import urlpatterns_general_api

# API version prefix
api_version_prefix = 'api/v1/'


urlpatterns = [
    # Auth path
    path('', CustomLoginView.as_view(next_page=reverse_lazy('general:home')), name="login"),
    path('logout/', logout_view, name='logout'),

    # Admin path
    path('admin/', admin.site.urls, name="admin"),
    
    # App-specific paths
    path(f'{api_version_prefix}event/', include(event_urlpatterns_api), name='events_api'),
    path(f'{api_version_prefix}attendance/', include((attendance_urlpatterns_api, 'attendance_api'), namespace='attendance_api')),
    path(f'{api_version_prefix}prize/', include(prize_urlpatterns_api), name='prize_api'),
    path(f'{api_version_prefix}semester/', include(semester_urlpatterns_api), name='semester_api'),
    path(f'{api_version_prefix}account/', include((account_urlpatterns_api, 'account_api'), namespace='account_api')),
    path(f'{api_version_prefix}general/', include((urlpatterns_general_api, 'general_api'), namespace='general_api')),
    
    # View-specific paths (Non-API)
    path('', include((account_urlpatterns_views, 'account'), namespace='account_views')),
    path('', include((general_urlpatterns_views, 'general'), namespace='general_views')),
    path('', include((attendance_urlpatterns_views, 'attendance'), namespace='attendance_views')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.general.views.error.error_404'
handler500 = 'apps.general.views.error.error_500'