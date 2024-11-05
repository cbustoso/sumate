from django.db import models
from apps.semester.models import Semester

class Enroll(models.Model):
    semester = models.OneToOneField(Semester, on_delete=models.CASCADE, related_name='enroll')
    total_enrolled = models.PositiveIntegerField(verbose_name="Total Matriculados")

    def __str__(self):
        return f"{self.semester.name} (Total Matriculados: {self.total_enrolled})"

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        db_table = 'enroll'