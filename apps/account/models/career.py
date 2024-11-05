from django.db import models


class Career(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, unique=True, verbose_name="Carrera")
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        db_table = 'sumate_carrera'    

    def __str__(self):
        return self.name