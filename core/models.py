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


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado para Compra'),
        ('RECHAZADO', 'Rechazado (Sobrestock)'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_requests', verbose_name="Producto")
    quantity = models.IntegerField(verbose_name="Cantidad")
    unit_cost_usd = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Costo Unitario (USD)")
    requested_by = models.CharField(max_length=150, verbose_name="Solicitado por")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE', verbose_name="Estado S&OP")
    planned_date = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mes Compra Planificado")
    decision_note = models.TextField(blank=True, null=True, verbose_name="Comentarios del Planificador")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Solicitud")

    @property
    def total_cost_usd(self):
        return self.quantity * self.unit_cost_usd

    class Meta:
        verbose_name = "Solicitud de Compra"
        verbose_name_plural = "Solicitudes de Compra"

    def __str__(self):
        return f"{self.requested_by} - {self.product.item_code} ({self.quantity} u) - {self.status}"

