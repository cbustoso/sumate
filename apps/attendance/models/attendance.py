from django.db import models

from apps.account.models import User
from apps.event.models import Event


class Attendance(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances", verbose_name="Asistente")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Evento")
    points = models.IntegerField(verbose_name="Puntos del Evento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        db_table = 'sumate_asistencia'

    def __str__(self):
       return f'{self.event.name} - {self.attendee.username}'
    