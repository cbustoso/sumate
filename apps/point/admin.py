from django.apps import apps
from django.contrib import admin

from apps.point.models.expirated_points import ExpiredPoints


app = apps.get_app_config('point')
app.verbose_name = 'Gestión de Puntos'

class ExpiredPointsAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('get_user_email', 'get_user_run', 'total_points', 'get_executed_semester', 'get_expired_semester', 'created_at')
    readonly_fields = ('user', 'total_points', 'executed_semester', 'expired_semester', 'created_at',)
    ordering = ('-created_at',)

    class Meta:
        verbose_name = 'Punto'
        verbose_name_plural = 'Puntos'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'executed_semester', 'expired_semester')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.admin_order_field = 'user__email'
    get_user_email.short_description = 'Email del Usuario'

    def get_user_run(self, obj):
        return obj.user.run
    get_user_run.admin_order_field = 'user__run'
    get_user_run.short_description = 'RUN del Usuario'

    def get_executed_semester(self, obj):
        return obj.executed_semester.name
    get_executed_semester.admin_order_field = 'executed_semester__name'
    get_executed_semester.short_description = 'Semestre Ejecutado'

    def get_expired_semester(self, obj):
        return obj.expired_semester.name
    get_expired_semester.admin_order_field = 'expired_semester__name'
    get_expired_semester.short_description = 'Semestre Expirado'

    
    def has_add_permission(self, request):
        return False        
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ExpiredPoints, ExpiredPointsAdmin)
