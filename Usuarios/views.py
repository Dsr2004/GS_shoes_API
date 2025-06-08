from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import (
    UsuarioSerializer,
    UsuarioLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer
)


def obtener_usuario(pk):
    try:
        return Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        raise Http404('Usuario no encontrado.')


class UsuarioPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UsuarioListarView(ListAPIView):
    serializer_class = UsuarioSerializer
    #permission_classes = [IsAuthenticated]
    search_fields = ['correo', 'nombre_completo']

    def get_queryset(self):
        return Usuario.objects.all()


class UsuarioObtenerView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        usuario = obtener_usuario(pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)


class UsuarioCrearView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioActualizarView(APIView):
    #permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        usuario = obtener_usuario(pk)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        usuario = obtener_usuario(pk)
        usuario.is_active = not usuario.is_active
        usuario.save()
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsuarioLoginView(APIView):
    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data['usuario']
        refresh = RefreshToken.for_user(usuario)

        response_data = {
            'access_token': str(refresh.access_token),
            'user':{
                'user_id': usuario.id,
                'correo': usuario.correo,
                'nombre_completo': usuario.nombre_completo
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UsuarioPasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data['correo']
            usuario.create_reset_token()
            return Response({"message": "Correo enviado con el token de recuperación."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioPasswordChangeView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "La contraseña ha sido cambiada exitosamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioGetProfileView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class UsuarioEnviarProfileView(APIView):
    #permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
