from django.db import models
from Base.models import BaseModel 
from Articulos.models import Articulo

class MovimientoInventario(BaseModel):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='movimientos')
    cantidad_total = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=255)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.tipo} - {self.descripcion}"


class SalidaInventario(models.Model):
    cedula_cliente = models.BigIntegerField()
    nombre_cliente = models.CharField(max_length=255)
    movimiento = models.OneToOneField(MovimientoInventario, on_delete=models.CASCADE, related_name='salida', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_cliente} ({self.cedula_cliente})"
    