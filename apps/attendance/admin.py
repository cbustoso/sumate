from django.contrib import admin
from apps.attendance.models import Attendance
# Ensure Event is imported if not automatically available
from apps.event.models import Event

class EventListFilter(admin.SimpleListFilter):
    title = 'Evento'
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. Each tuple is a pair (value, 'title')
        representing each available filter option.
        """
        events = Event.objects.all()
        return [(event.id, event.name) for event in events]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value selected by the user.
        """
        if self.value():
            return queryset.filter(event__id=self.value())
        return queryset

class AttendanceAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('attendee', 'get_event_semester', 'event', 'points', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('attendee__run', 'event__name')
    list_filter = ('event__semester__name',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        """
        Enhances the default queryset by prefetching related data to improve performance.
        """
        return super().get_queryset(request).select_related('event', 'event__semester')

    def get_event_semester(self, obj):
        """
        Retrieves the semester name for the event associated with the attendance record.
        """
        return obj.event.semester.name
    
    get_event_semester.short_description = 'Event Semester'

admin.site.register(Attendance, AttendanceAdmin)
