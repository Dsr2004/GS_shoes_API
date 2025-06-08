from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import MovimientoInventario
from .serializers import MovimientoInventarioSerializer


# Función auxiliar para obtener un movimiento o lanzar 404
def obtener_movimiento(pk):
    try:
        return MovimientoInventario.objects.select_related('salida').get(pk=pk)
    except MovimientoInventario.DoesNotExist:
        raise Http404("Movimiento no encontrado.")


# Paginación
class MovimientoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Listado paginado de movimientos
class MovimientoListarView(ListAPIView):
    serializer_class = MovimientoInventarioSerializer
    pagination_class = MovimientoPagination

    def get_queryset(self):
        return MovimientoInventario.objects.select_related('articulo', 'salida').order_by('-fecha_movimiento')


# Obtener un movimiento individual
class MovimientoDetalleView(APIView):
    def get(self, request, pk):
        movimiento = obtener_movimiento(pk)
        serializer = MovimientoInventarioSerializer(movimiento)
        return Response(serializer.data)


# Crear un nuevo movimiento
class MovimientoCrearView(APIView):
    def post(self, request):
        serializer = MovimientoInventarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
