from django.db import models
from django.db.models import Max


class Semester(models.Model):
    STATUS_CHOICES = [
        ('active', 'Vigente'),
        ('draft', 'No Publicado'),
        ('expired', 'Antiguo'),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name="Semestre")        
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    start = models.DateField(verbose_name="Comienza", null=False, blank=False)
    end = models.DateField(verbose_name="Comienza", null=False, blank=False)
    correlative = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            max_correlative = Semester.objects.aggregate(max_correlative=Max('correlative'))['max_correlative']
            self.correlative = (max_correlative or 0) + 1
        super(Semester, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        db_table = 'sumate_semestre'