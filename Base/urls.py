from django.urls import path
from .Views.FileData import FileRetrieve


urlpatterns = [
    #FILES
    path('archivos/obtener_por_id/<int:pk>/', FileRetrieve.as_view(), name='archivoObtener')
    ]
