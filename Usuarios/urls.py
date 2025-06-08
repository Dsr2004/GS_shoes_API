from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', UsuarioListarView.as_view(), name='usuariosListar'),
    path('usuarios/<int:pk>/', UsuarioObtenerView.as_view(), name='usuarioObtener'),
    path('usuarios/crear/', UsuarioCrearView.as_view(), name='usuarioCrear'),
    path('usuarios/actualizar/<int:pk>/', UsuarioActualizarView.as_view(), name='usuarioActualizar'),
    path('usuarios/login/', UsuarioLoginView.as_view(), name='usuarioLogin'),
    path('usuarios/rest-password-request/', UsuarioPasswordResetRequestView.as_view(), name='usuarioResetPasswordRequest'),
    path('usuarios/rest-password/', UsuarioPasswordChangeView.as_view(), name='usuarioResetPassword'),
    
    path('usuarios/perfil-get/', UsuarioGetProfileView.as_view(), name='usuarioGetPerfil'),
    path('usuarios/perfil-enviar/', UsuarioEnviarProfileView.as_view(), name='usuarioEnviarPerfil'),
]