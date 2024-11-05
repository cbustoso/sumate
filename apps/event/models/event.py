import os
from datetime import datetime
from django.db import models
from apps.account.models.user import User
from apps.event.models.event_types import EventType
from apps.semester.models import Semester

def event_image_file_path(instance, filename):
    """Generates a unique file path for event images by appending a timestamp."""
    ext = filename.split('.')[-1]
    filename = f'{instance.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.{ext}'
    return os.path.join('events/', filename)

class Event(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'Habilitado'),
        ('finished', 'Finalizado'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(
        upload_to=event_image_file_path, 
        height_field=None, 
        width_field=None, 
        max_length=100,
        verbose_name="Imagen",
        null=True,
        blank=True
    )
    start = models.DateTimeField(verbose_name="Fecha Inicio", null=False, blank=False)
    end = models.DateTimeField(verbose_name="Fecha Término", null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name="Tipo Evento", related_name="event_type")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Semestre", related_name="semester")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enabled', verbose_name="Estado")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        db_table = 'sumate_evento'