#gestion_usuarios/urls.py
#ARCHIVO DE GENERACION DE SWAGGER
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
   path('',include(router.urls)), #incluir las rutas generadas por el router
]
