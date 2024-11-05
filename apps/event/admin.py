from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from asyncio import format_helpers
from django.apps import apps
from django.contrib import admin
from apps.event.models.event_types import EventType
from apps.event.models.event import Event


app = apps.get_app_config('event')
app.verbose_name = 'Gestión de Eventos'


class EventAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'id', 'get_event_type_points', 'get_event_type_name', 'semester', 'get_semester_status', 'status', 'start', 'created_at', 'add_attendance')
    ordering = ('-created_at',)
    exclude = ('created_by',)


    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def has_delete_permission(self, request, obj=None):
        return False        

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event_type')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_event_type_points(self, obj):
        return obj.event_type.points
    get_event_type_points.admin_order_field = 'event_type__points'
    get_event_type_points.short_description = 'Puntos del Evento'
    
    def get_event_type_name(self, obj):
        return obj.event_type.name
    get_event_type_name.admin_order_field = 'event_type__name'
    get_event_type_name.short_description = 'Tipo Evento'

    def get_semester_status(self, obj):
        if obj.semester.status == 'active':
            return mark_safe('<span style="color: green;">Activo</span>')
        elif obj.semester.status == 'expired':
            return mark_safe('<span style="color: red;">Expirado</span>')
        elif obj.semester.status == 'draft':
            return mark_safe('<span style="color: blue;">No Publicado</span>')
        else:
            return obj.semester.status
    get_semester_status.admin_order_field = 'semester__status'
    get_semester_status.short_description = 'Estado Semestre'

    def add_attendance(self, obj):
        if obj.semester.status == 'draft':
            return format_html('<span class="th-add-attendance">No publicado</span>')
        elif obj.semester.status == 'expired':
            return format_html('<span class="th-add-attendance">Semestre Finalizado</span>')
        elif not obj.is_active:
            return format_html('<span class="th-add-attendance">Inactivo</span>')
        
        url = reverse('attendance_views:upload_file_attendance', args=[obj.id])
        return format_html('<a class="button th-add-attendance" style="min-width: 250px;" href="{}">Agregar</a>', url)
    add_attendance.short_description = 'Asistencia'

admin.site.register(Event, EventAdmin)    

class EventTypeAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'points', 'is_active', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(EventType, EventTypeAdmin)