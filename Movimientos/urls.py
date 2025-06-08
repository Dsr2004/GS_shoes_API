from django.urls import path
from .views import *

urlpatterns = [
    path('movimientos/', MovimientoListarView.as_view(), name='movimiento-listar'),
    path('movimientos/crear/', MovimientoCrearView.as_view(), name='movimiento-crear'),
    path('movimientos/<int:pk>/', MovimientoDetalleView.as_view(), name='movimiento-detalle'),
]