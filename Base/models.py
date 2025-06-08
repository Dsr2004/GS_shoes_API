import os
import re
from unidecode import unidecode
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .model_base import BaseModel

    
def normalizar_ruta(ruta):
    """
    Normaliza la ruta eliminando caracteres especiales y convirtiendo a minúsculas.
    """
    ruta = unidecode(ruta)
    ruta = ruta.replace(' ', '-')
    # Eliminar caracteres especiales excepto '-', '/', y '.'
    ruta = re.sub(r'[^a-zA-Z0-9\-\/\.]', '', ruta)
    return ruta

def guardar_archivo(instance, filename):
    """
    Genera la ruta normalizada para guardar el archivo.
    """
    full_path = f"{instance.ruta_archivo}/{filename}"
    normalized_path = normalizar_ruta(full_path)
    return normalized_path

class FileData(BaseModel):
    """
    Modelo para almacenar información sobre los archivos cargados.
    """
    archivo = models.FileField(upload_to=guardar_archivo, verbose_name="Archivo", max_length=400)
    ruta_archivo = models.TextField(verbose_name="Ruta del archivo", null=True, blank=True, default=None)
    nombre_archivo = models.TextField(verbose_name="Nombre del archivo")
    url_archivo = models.TextField(verbose_name="Url del archivo", null=True, blank=True, default=None)
    id_archivo = models.TextField(verbose_name="ID del archivo", null=True, blank=True, default=None)
    
    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        db_table = "archivos"

    def __str__(self):
        """
        Devuelve el nombre del archivo o la URL si existe.
        """
        if self.url_archivo:
            return f"{self.id_archivo} - {self.url_archivo}"
        else:
            return self.ruta_archivo
    
@receiver(post_delete, sender=FileData)
def borrar_archivo(sender, instance, **kwargs):
    """
    Borra el archivo físico cuando el objeto FileData se elimina de la base de datos.
    """
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)

@receiver(pre_save, sender=FileData)
def actualizar_archivo(sender, instance, **kwargs):
    """
    Actualiza el archivo cuando el objeto FileData se modifica. Elimina el archivo anterior si cambia.
    """
    if not instance.pk:
        return False

    try:
        old_file = FileData.objects.get(pk=instance.pk).archivo
    except FileData.DoesNotExist:
        return False

    new_file = instance.archivo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
