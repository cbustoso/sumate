import os
from datetime import datetime
from django.db import models
from django.db import models, transaction
from django.core.exceptions import ValidationError

def prize_image_file_path(instance, filename):
    """Generates a unique file path for prize images by appending a timestamp."""
    ext = filename.split('.')[-1]
    filename = f'{instance.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.{ext}'
    return os.path.join('prizes/', filename)

class Prize(models.Model):
    name = models.CharField(max_length=255, verbose_name="Premio")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(
        upload_to=prize_image_file_path, 
        height_field=None, 
        width_field=None, 
        max_length=100,
        verbose_name="Imagen",
        null=True,
        blank=True
    )
    stock = models.IntegerField(verbose_name="Stock")
    points = models.IntegerField(verbose_name="Puntos necesarios")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Premio"
        verbose_name_plural = "Premios"
        db_table = 'sumate_premio'

    def deduct_stock(self, quantity=1):
        """
        Deducts a specified quantity from the prize's stock.

        :param quantity: The amount to deduct from the stock. Must be greater than zero.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a deducir debe ser mayor que cero.")
        if self.stock < quantity:
            raise ValidationError("No hay suficiente stock disponible para completar el canje.")
        
        with transaction.atomic():
            self.stock -= quantity
            self.save(update_fields=['stock'])