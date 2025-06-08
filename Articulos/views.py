from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import Articulo
from .serializers import ArticuloSerializer

def obtener_articulo(pk):
    try:
        return Articulo.objects.get(pk=pk)
    except Articulo.DoesNotExist:
        raise Http404('Artículo no encontrado.')

class ArticuloPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArticuloListarView(ListAPIView):
    serializer_class = ArticuloSerializer
    pagination_class = ArticuloPagination

    def get_queryset(self):
        return Articulo.objects.all().order_by('-created_at')

class ArticuloObtenerView(APIView):
    def get(self, request, pk):
        articulo = obtener_articulo(pk)
        serializer = ArticuloSerializer(articulo)
        return Response(serializer.data)

class ArticuloCrearView(APIView):
    def post(self, request):
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticuloActualizarView(APIView):
    def put(self, request, pk):
        articulo = obtener_articulo(pk)
        serializer = ArticuloSerializer(articulo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        articulo = obtener_articulo(pk)
        articulo.is_active = not articulo.is_active
        articulo.save()
        serializer = ArticuloSerializer(articulo)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticulosStockBajoView(APIView):
    def get(self, request):
        articulos = Articulo.objects.all()
        stock_bajo = []

        for articulo in articulos:
            if articulo.cantidad < articulo.umbral_minimo:
                porcentaje = round((articulo.cantidad / articulo.umbral_minimo) * 100, 2)
                estado = 'critico' if porcentaje <= 40 else 'medio'

                stock_bajo.append({
                    'codigo': f'#{articulo.id:03}',  # si quieres formato tipo #001
                    'nombre': articulo.nombre,
                    'stock': articulo.cantidad,
                    'umbral': articulo.umbral_minimo,
                    'porcentaje': porcentaje,
                    'estado': estado,
                })
        response = {
            'stockBajo': stock_bajo
        }
        return Response(stock_bajo)
    