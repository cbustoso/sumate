from django.db import models

from apps.account.models.user import User

from ...semester.models.semester import Semester

class ExpiredPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Estudiante")
    total_points = models.IntegerField(verbose_name="Total de Puntos Descontados")
    executed_semester = models.ForeignKey(Semester, related_name="executed_semesters", on_delete=models.CASCADE, verbose_name="Semestre Ejecutado")
    expired_semester = models.ForeignKey(Semester, related_name="expired_semesters", on_delete=models.CASCADE, verbose_name="Semestre Expirado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    def __str__(self):
        return f"Total de {self.total_points} puntos expirados - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Punto Expirado"
        verbose_name_plural = "Puntos Expirados"
        db_table = 'sumate_puntos_expirados'