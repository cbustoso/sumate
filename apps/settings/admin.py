from django.contrib import admin
from django.apps import apps
from django.contrib import admin
from apps.settings.models import UploadedFile


app = apps.get_app_config('settings')
app.verbose_name = 'Configuraciones'

class SettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UploadedFile, SettingsAdmin)