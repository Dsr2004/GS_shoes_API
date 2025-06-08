from django.urls import path
from .views import *

urlpatterns = [
    path('articulos/', ArticuloListarView.as_view(), name='articulosListar'),
    path('articulos/<int:pk>/', ArticuloObtenerView.as_view(), name='articuloObtener'),
    path('articulos/crear/', ArticuloCrearView.as_view(), name='articuloCrear'),
    path('articulos/actualizar/<int:pk>/', ArticuloActualizarView.as_view(), name='articuloActualizar'),
    path('articulos/stock-bajo/', ArticulosStockBajoView.as_view(), name='stock-bajo'),
]