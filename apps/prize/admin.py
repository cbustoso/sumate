from django.apps import apps
from django.contrib import admin
from django.core.exceptions import ValidationError
from apps.prize.models import PrizeRedemption
from apps.prize.models.prize import Prize

app = apps.get_app_config('prize')
app.verbose_name = 'Gestión de Premios'

class PrizeAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'stock', 'points', 'is_active')
    ordering = ('-created_at',)

    class Meta:
        verbose_name = 'Premio'
        verbose_name_plural = 'Premios'
    
admin.site.register(Prize, PrizeAdmin)

class PrizeRedemptionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('get_student_email', 'get_prize_name', 'points', 'semester', 'get_provided_by_email', 'status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('points', 'student', 'get_student_run', 'provided_by', 'prize')
    search_fields = ('student__run', 'student__email')
    list_filter = ('status',)

    class Meta:
        verbose_name = 'Canje'
        verbose_name_plural = 'Canjes'
    
    def has_add_permission(self, request, obj=None):
        return False    
    
    def has_delete_permission(self, request, obj=None):
        return False    
    
    def save_model(self, request, obj, form, change):
        obj.provided_by = request.user
        if change and 'status' in form.changed_data:
            if obj.status == 'canceled':
                obj.student.points += obj.points
                obj.student.save()
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'hold':
            return ('prize', 'student', 'provided_by', 'points', 'comment', 'semester', 'status',) + self.readonly_fields
        return self.readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'prize')

    def get_student_email(self, obj):
        return obj.student.email if obj.student else "No aplica"
    get_student_email.short_description = 'Email del Usuario'

    def get_student_run(self, obj):
        return obj.student.run if obj.student else 'Sin rut asociado'
    get_student_run.short_description = 'Rut de usuario'

    def get_provided_by_email(self, obj):
        return obj.provided_by.email if obj.provided_by else "No aplica"
    get_provided_by_email.short_description = 'Entregado Por'

    def get_prize_name(self, obj):
        return obj.prize.name if obj.prize else "No aplica"
    get_prize_name.short_description = 'Nombre del Premio'

admin.site.register(PrizeRedemption, PrizeRedemptionAdmin)