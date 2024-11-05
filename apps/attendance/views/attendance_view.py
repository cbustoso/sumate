from django.shortcuts import get_object_or_404, render
from apps.account.decorators.permissions import group_required
from apps.event.models import Event

@group_required('administrator')
def upload_file_attendance_view(request, id=None):
    """
    View for uploading an initial file 
    """
    event = get_object_or_404(Event, pk=id, is_active=True, semester__status__in=['active', 'draft'])
        
    context = {
        'event_id': event.id,
        'event_name': event.name,
    }

    return render(request, 'attendance/upload_attendance.html', context)