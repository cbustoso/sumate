from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    points = models.IntegerField(verbose_name="Puntos")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    def __str__(self):
        return self.name    

    class Meta:
        verbose_name = "Tipo Evento"
        verbose_name_plural = "Tipos de Eventos"
        db_table = 'sumate_tipo_evento'