from rest_framework import serializers
from .models import Articulo, MovimientoInventario, SalidaInventario


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    articulo = serializers.PrimaryKeyRelatedField(queryset=Articulo.objects.all())
    cliente = serializers.SerializerMethodField()
    fecha_movimiento = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)


    # Campos que llegan del cliente (solo si es salida)
    cedula_cliente = serializers.IntegerField(required=False, write_only=True)
    nombre_cliente = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 'articulo', 'cantidad_total', 'descripcion',
            'fecha_movimiento', 'precio_total', 'tipo',
            'cedula_cliente', 'nombre_cliente', 'cliente'  # ← cliente es visible solo en GET
        ]
        read_only_fields = ['precio_total', 'fecha_movimiento', 'cliente']

    def get_cliente(self, obj):
        salida = getattr(obj, 'salida', None)
        if salida:
            return {
                'nombre_cliente': salida.nombre_cliente,
                'cedula_cliente': salida.cedula_cliente
            }
        return None  # o return {} si prefieres vacío

    def validate(self, data):
        articulo = data['articulo']
        cantidad = data['cantidad_total']
        tipo = data['tipo']

        if tipo == 'SALIDA' and cantidad > articulo.cantidad:
            raise serializers.ValidationError({'cantidad_total': 'La cantidad excede el stock disponible del artículo.'})

        if tipo == 'SALIDA' and ('cedula_cliente' not in data or 'nombre_cliente' not in data):
            raise serializers.ValidationError({'cliente': 'Debe proporcionar los datos del cliente para una salida.'})

        return data

    def create(self, validated_data):
        tipo = validated_data['tipo']
        articulo = validated_data['articulo']
        cantidad = validated_data['cantidad_total']
        descripcion = validated_data['descripcion']

        movimiento = MovimientoInventario.objects.create(
            articulo=articulo,
            cantidad_total=cantidad,
            descripcion=descripcion,
            tipo=tipo,
            precio_total=0  # temporal
        )

        if tipo == 'ENTRADA':
            articulo.cantidad += cantidad
            movimiento.precio_total = 0
        elif tipo == 'SALIDA':
            articulo.cantidad -= cantidad
            movimiento.precio_total = articulo.precio * cantidad

            SalidaInventario.objects.create(
                movimiento=movimiento,
                cedula_cliente=validated_data['cedula_cliente'],
                nombre_cliente=validated_data['nombre_cliente']
            )

        articulo.save()
        movimiento.save()
        return movimiento
