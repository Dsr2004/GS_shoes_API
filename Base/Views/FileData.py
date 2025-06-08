import os
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404, JsonResponse
from ..models import FileData


def get_file(pk):
    try:
        return FileData.objects.get(pk=pk)
    except FileData.DoesNotExist:
        raise Http404('Archivo no encontrado')


class FileRetrieve(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        file_instance = get_file(pk)
        file_path = file_instance.file.path

        if not os.path.exists(file_path):
            raise Http404('Archivo no encontrado en el sistema de archivos')

        with open(file_path, "rb") as file:
            file_content = file.read()
            encoded_string = base64.b64encode(file_content).decode('utf-8')

        response_data = {
            'file_name': file_instance.file_name,
            'file_content': encoded_string,
        }
        return JsonResponse(response_data)
