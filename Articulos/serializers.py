from rest_framework import serializers
from .models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    stock_bajo = serializers.SerializerMethodField()
    
    class Meta:
        model = Articulo
        fields = '__all__'
        
    def get_stock_bajo(self, obj):
        return obj.cantidad < obj.umbral_minimo
