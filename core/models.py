from django.db import models

# Create your models here.
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código de la Marca")
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.name


class Product(models.Model):
    ORIGIN_CHOICES = [
        ('VENTA', 'Venta'),
        ('COMPRA', 'Compra'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Marca")
    item_code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Código SAP")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES, verbose_name="Origen")
    family = models.CharField(max_length=100, verbose_name="Familia")
    subfamily = models.CharField(max_length=100, verbose_name="Subfamilia")
    is_truck_mounted = models.BooleanField(default=False, verbose_name="Sobre Camión")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"[{self.brand.code}] {self.item_code} - {self.description}"

