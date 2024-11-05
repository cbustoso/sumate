from typing import Any
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from apps.account.models.campus import Campus
from apps.account.models.career import Career
from apps.account.models.user import User
from apps.semester.models.semester import Semester

admin.site.site_title = "Sumate / Panel de Administracion"
admin.site.site_header = "Duoc UC - Sede Alameda"
admin.site.index_title = "Panel de Administración"

app = apps.get_app_config('account')
app.verbose_name = 'Gestión de Cuentas'

admin.site.unregister(Group)

class UserAdminCustom(admin.ModelAdmin):
    actions = None
    list_display = ('email', 'formatted_run', 'points', 'get_career_name', 'shift', 'get_campus_name', 'is_active')
    search_fields = ('run', 'username', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'points', 'create_password')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Field Heading', {
            'fields': ('run', 'career', 'campus',),
        }),
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('create_password', 'points', 'last_login', 'date_joined', 'username')
        else:
            return ('create_password', 'points', 'last_login', 'date_joined',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
            obj.create_password = True
        super().save_model(request, obj, form, change)
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def formatted_run(self, obj):
        return obj.format_rut()
    formatted_run.short_description = 'RUT'


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('career', 'campus')

    def get_career_name(self, obj):
        return obj.career.name if obj.career else "No aplica"

    def get_campus_name(self, obj):
        return obj.campus.name if obj.campus else "No aplica"
    
    get_career_name.short_description = 'Carrera Alumno'
    get_campus_name.short_description = 'Sede Alumno'


admin.site.register(User, UserAdminCustom)

class CareerAdmin(admin.ModelAdmin):
    actions = None
    ordering = ('name',)
    list_display = ('name', 'download_attendee_report')

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

    def download_attendee_report(self, obj):
        semesters = Semester.objects.all()
        dropdown_html = '<select name="semester_id" id="semester_id_{}" style="margin-right: 5px; border-radius: 4px; border: 1px solid #ccc;">'.format(obj.pk)
        for semester in semesters:
            dropdown_html += '<option value="{}">{}</option>'.format(semester.pk, semester.name)
        dropdown_html += '</select>'

        button_html = '<button type="button" onclick="downloadReport({})" style="background-color: #4CAF50; color: white; padding: 8px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Descargar Reporte</button>'.format(obj.pk)

        return format_html(dropdown_html + button_html)

    download_attendee_report.short_description = 'Descargar Reporte de Asistentes'

    class Media:
        js = ('assets/js/admin/report_downloader.js',)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Career, CareerAdmin)


class CampusAdmin(admin.ModelAdmin):
    actions = None
    ordering = ('name',)
    
    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Campus, CampusAdmin)
