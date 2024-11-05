from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.apps import apps
from django.db.models import Case, BooleanField, When, Min


from .models import Semester
from apps.point.services.expired_points_service import ExpiredPointsService

app = apps.get_app_config('semester')
app.verbose_name = 'Gestión de Semestres'

class SemesterAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'correlative', 'status', 'start', 'end', 'close_semester_button')
    readonly_fields = ('correlative',)
    ordering = ('-correlative',)
    fields = ('name', 'correlative', 'status', 'start', 'end')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        min_correlative_active = queryset.filter(status='active').aggregate(min_correlative=Min('correlative'))['min_correlative']
        min_correlative_draft = queryset.filter(status='draft').aggregate(min_correlative=Min('correlative'))['min_correlative']
        queryset = queryset.annotate(
            is_oldest_active=Case(
                When(correlative=min_correlative_active, then=True),
                default=False,
                output_field=BooleanField()
            ),
            is_editable=Case(
                When(correlative=min_correlative_draft, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        return queryset
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['choices'] = [choice for choice in db_field.choices if choice[0] != 'expired']
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.is_editable:
            return self.readonly_fields + ('status',)
        return self.readonly_fields 

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('close_semester/<int:semester_id>/', self.admin_site.admin_view(self.close_semester_view), name='close_semester'),
        ]
        return custom_urls + urls

    def close_semester_button(self, obj):
        close_semester_html = ''
        
        if obj.is_oldest_active:
            url = reverse('admin:close_semester', args=[obj.pk])
            close_semester_html = format_html('<a class="button" href="{}" style="background-color: #025992; color: white; padding: 8px 10px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; margin-left: 15px">Cerrar</a>', url)
            
        button_html = '<button type="button" onclick="downloadReport({})" style="background-color: #4CAF50; color: white; padding: 8px 10px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; margin-left: 15px">Descargar Reporte</button>'.format(obj.pk)

        return format_html(close_semester_html + button_html)
    close_semester_button.short_description = 'Acciones'

    class Media:
        js = ('assets/js/admin/report_downloader_semester.js',)

    def close_semester_view(self, request, semester_id):
        semester = Semester.objects.get(pk=semester_id)

        points_deduction_by_user, users_with_pending_redeems = ExpiredPointsService.get_expired_points_info(semester)

        total_points_expiring = sum(points_deduction_by_user.values())
        total_users_affected = len(users_with_pending_redeems)

        context = {
            'semester_id': semester_id,
            'semester_name': semester.name,
            'semester_start_date': semester.start,
            'semester_end_date': semester.end,
            'total_points_expiring': total_points_expiring,
            'total_users_affected': total_users_affected,
            'users_with_pending_redeems': users_with_pending_redeems,
        }
        return render(request, 'close_semester.html', context)

admin.site.register(Semester, SemesterAdmin)
