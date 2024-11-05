import uuid as uuid_lib
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from .campus import Campus
from .career import Career


class User(AbstractUser):
    SHIFT_CHOICES = [
        ('D', 'Diurno'),
        ('V', 'Vespertino'),
        ('N', 'Sin información'),
    ]

    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    run = models.CharField(max_length=10, blank=True, null=True, unique=True, verbose_name="Run")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=120, blank=True, null=True, verbose_name="Teléfono")
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, default='D', verbose_name="Jornada")
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career', blank=True, null=True, verbose_name="Carrera")
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='campus', blank=True, null=True, verbose_name="Sede")
    points = models.IntegerField(verbose_name="Puntos Actuales", default=0)
    create_password = models.BooleanField(verbose_name="¿Se creó la contraseña?", default=False)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        if self.points < 0:
            self.points = 0
        super().save(*args, **kwargs)


    def deduct_points_for_prize_redeem(self, points_to_deduct: int) -> None:
        if points_to_deduct > self.points:
            raise ValueError("El usuario no tiene suficientes puntos para canjear el premio.")
        
        with transaction.atomic():
            self.points -= points_to_deduct
            self.save(update_fields=['points'])

    def award_points_for_attendance(self, points_to_award: int) -> None:
        if points_to_award <= 0:
            raise ValueError("La cantidad de puntos a otorgar debe ser mayor que cero.")
        
        with transaction.atomic():
            self.points += points_to_award
            self.save(update_fields=['points'])

    def format_rut(self) -> str:
        rut = self.run

        if not rut:
            return "Este usuario no tiene rut asociado."
        rut_body = rut[:-1]
        verifier = rut[-1]
        
        rut_body = rut_body[::-1]
        rut_body = '.'.join(rut_body[i:i+3] for i in range(0, len(rut_body), 3))
        rut_body = rut_body[::-1]

        return f"{rut_body}-{verifier}"
