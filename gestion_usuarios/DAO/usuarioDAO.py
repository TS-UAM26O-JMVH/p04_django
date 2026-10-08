from gestion_usuarios.models import Usuario
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import timedelta
from gestion_usuarios.serializers import UsuarioParcialSerializer, UsuarioContrasenaSerializer
from gestion_usuarios.exceptions.usuarioExeptions import (
    DatosInvalidos_400,
    UsuarioNoEncontrado_404,
    ConflictoUsuario_409,
    ErrorInternoServidor_500,
    UsuarioNoAutorizado_401,
    UsuarioProhibido_403,
)
from django.db.utils import IntegrityError, DatabaseError
import uuid


class UsuarioDAO:
    """
    Data Access Object (DAO) para la gestión de usuarios en la base de datos.
    Proporciona métodos para realizar operaciones CRUD sobre el modelo Usuario.
    """

    @staticmethod
    def obtener_todos():
        return Usuario.object.all()