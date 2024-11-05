from django.db import models


class Campus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_active = models.BooleanField('Is Active', default=True)
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"
        db_table = 'sumate_sede'