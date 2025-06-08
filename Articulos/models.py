from django.db import models
from Base.models import BaseModel 

class Articulo(BaseModel):
    nombre = models.CharField(max_length=150)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    umbral_minimo = models.PositiveIntegerField(default=5)
    descripcion = models.TextField()
    

    def __str__(self):
        return self.nombre

