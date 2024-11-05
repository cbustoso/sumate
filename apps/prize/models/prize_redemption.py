from django.db import models

from apps.account.models.user import User
from apps.semester.models.semester import Semester
from apps.prize.models.prize import Prize

class PrizeRedemption(models.Model):
    STATUS_CHOICES = [
        ('hold', 'Reservado'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
        ('expired', 'Expirado'),
    ]

    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name="prize", verbose_name="Premio")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student", verbose_name="Canjeado Por")
    provided_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="provided_by", verbose_name="Entregado Por")
    points = models.IntegerField(verbose_name="Puntos Gastados", default=0)
    comment = models.TextField(verbose_name="Comentarios", blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Canjeado el Semestre", related_name="redemption_semester")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Canje")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='hold', verbose_name="Estado")

    def __str__(self):
        return f"Canje de {self.points} puntos - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Canje"
        verbose_name_plural = "Canjes"
        db_table = 'sumate_premio_canje'