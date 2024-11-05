from django.contrib import admin
from django.apps import apps
from apps.enroll.models import Enroll


app = apps.get_app_config('enroll')
app.verbose_name = 'Gestión de Cuentas'

class EnrollAdmin(admin.ModelAdmin):
    list_display = ('get_semester_name', 'total_enrolled')
    list_filter = ('semester',)
    
    def get_semester_name(self, obj):
        return obj.semester.name
    
    get_semester_name.admin_order_field = 'semester__name'
    get_semester_name.short_description = 'Semestre'
    
admin.site.register(Enroll, EnrollAdmin)