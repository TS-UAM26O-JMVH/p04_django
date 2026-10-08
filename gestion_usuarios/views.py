from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from gestion_usuarios.DAO.usuarioDAO import UsuarioDAO
from gestion_usuarios.serializers import (
    UsuarioCompletoSerializer,
    UsuarioParcialSerializer,
    UsuarioContrasenaSerializer,
    PasswordResetRequestSerializer,
)
from gestion_usuarios.exceptions.usuarioExeptions import (
    UsuarioNoAutorizado_401,
    UsuarioProhibido_403,
    ErrorInternoServidor_500,
    UsuarioNoEncontrado_404,
    DatosInvalidos_400,
    ConflictoUsuario_409,
)


class UsuarioViewSet(viewsets.ViewSet):
    """
    API para la gestión de Usuarios.
    """

    @swagger_auto_schema(
        operation_summary="Obtener todos los usuarios",
        responses={
            200: "Éxito",
            401: "No autorizado",
            403: "Prohibido",
            500: "Error interno del servidor",
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Devuelve una lista de todos los usuarios con soporte para
        paginación, ordenamiento y filtrado de acuerdo a los campos
        de la tabla.
        """
        try:
            usuarios = UsuarioDAO.obtener_todos()
            serializer = UsuarioCompletoSerializer(
                usuarios,
                many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except UsuarioNoAutorizado_401 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except UsuarioProhibido_403 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#activa un usuario especifico mediante una peticion HTTP de tipo PATCH
@action(detail=True, methods=["patch"])
@swagger_auto_schema(
    operation_summary="Activar un usuario",
    responses={
        200: "Usuario activado correctamente",
        401: "No autorizado",
        400: "Error en la validación",
        404: "Usuario no encontrado",
    },
)
def activate(self, request, pk=None):
    """Activa un usuario estableciendo el campo is_active en true."""
    try:
        usuario = UsuarioDAO.activar_usuario(pk)
        return Response(
            {
                "mensaje": "Usuario activado correctamente",
                "usuario": UsuarioParcialSerializer(usuario).data,
            },
            status=status.HTTP_200_OK,
        )

    except UsuarioNoEncontrado_404 as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    except DatosInvalidos_400 as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)