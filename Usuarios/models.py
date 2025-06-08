from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    def create_user(self, correo, nombre_completo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico.')
        if not nombre_completo:
            raise ValueError('El usuario debe tener un nombre completo.')

        correo = self.normalize_email(correo)
        user = self.model(
            correo=correo,
            nombre_completo=nombre_completo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre_completo, password=None, **extra_fields):
        extra_fields.setdefault('es_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('es_admin') is not True:
            raise ValueError('El superusuario debe tener es_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, nombre_completo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(verbose_name='Correo', max_length=255, unique=True)
    nombre_completo = models.CharField(max_length=30, verbose_name='Nombre Completo')
    identificacion = models.CharField(max_length=10, verbose_name='Identificación')
    telefono = models.CharField(max_length=10, verbose_name='Teléfono')
    is_active = models.BooleanField(default=True)
    es_admin = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)

    # Token para recuperación de contraseña
    reset_password_token = models.CharField(max_length=200, blank=True, null=True)
    reset_password_token_expires_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_completo']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre_completo}".title()

    def create_reset_token(self):
        self.reset_password_token = get_random_string(50)
        self.reset_password_token_expires_at = timezone.now() + timedelta(hours=1)
        self.save()

    @property
    def is_staff(self):
        return self.es_admin
