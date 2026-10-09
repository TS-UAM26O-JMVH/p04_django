#gestion_usuarios/urls.py
#ARCHIVO DE GENERACION DE SWAGGER
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestion_usuarios.views import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
   path('',include(router.urls)), #incluir las rutas generadas por el router
]
