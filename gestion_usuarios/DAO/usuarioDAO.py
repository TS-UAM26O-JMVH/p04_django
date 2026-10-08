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

    #Codigo 22
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        """
        Obtiene un usuario por su ID si no ha sido eliminado.

        :param usuario_id: UUID del usuario a buscar.
        :return: Instancia de Usuario o None si no se encuentra.
        """
        usuario = Usuario.objects.filter(id=usuario_id, is_deleted=False).first()
        if not usuario:
            raise UsuarioNoEncontrado_404()
        return usuario

    @staticmethod
    def activar_usuario(pk):
        usuario = UsuarioDAO.obtener_usuario_por_id(pk)
        # este if es redundante porque obtener_usuario_por_id ya lanza excepción, pero lo dejo
        if not usuario:
            raise UsuarioNoEncontrado_404()  # <-- fatal corregido (faltaban paréntesis)

        if usuario.is_active:
            raise DatosInvalidos_400("El usuario ya estaba activo")

        usuario.is_active = True
        usuario.save()
        return usuario

    #esta funcion es responsable de validar los datos antes de insertar un nuevo registroen la BD
    @staticmethod
    def crear_usuario(
        username: str,
        password: str,
        date_of_birth: str,
        email: str,
        first_name: str,
        last_name: str,
    ):
        """
        Crea un nuevo usuario con validaciones.
        """
        # Validar email
        try:
            validate_email(email)
        except ValidationError:
            raise DatosInvalidos_400()

        # Validar username (máximo 20 caracteres)
        UsuarioParcialSerializer.validar_username(username)

        try:
            usuario = Usuario.objects.create(
                username=username,
                password=make_password(password),
                date_of_birth=date_of_birth,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            return usuario

        except IntegrityError:
            raise ConflictoUsuario_409()

        except DatabaseError:
            raise ErrorInternoServidor_500()

    #codigo 20:
    #implementación del método obtener_usuario_por_id()
    #permite recuperar un usuario específico mediante su identificador
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        """
        Obtiene un usuario por su ID si no ha sido eliminado.

        :param usuario_id: UUID del usuario a buscar.
        :return: Instancia de Usuario o None si no se encuentra.
        """
        usuario = Usuario.objects.filter(id=usuario_id, is_deleted=False).first()
        if not usuario:
            raise UsuarioNoEncontrado_404()
        return usuario

    @staticmethod
    def activar_usuario(pk):
        usuario = UsuarioDAO.obtener_usuario_por_id(pk)
        # este if es redundante porque obtener_usuario_por_id ya lanza excepción, pero lo dejo
        if not usuario:
            raise UsuarioNoEncontrado_404()  # <-- fatal corregido (faltaban paréntesis)

        if usuario.is_active:
            raise DatosInvalidos_400("El usuario ya estaba activo")

        usuario.is_active = True
        usuario.save()
        return usuario

    #COdigo 22: 
    @staticmethod
    #Esta función valida los datos antes de insertar un nuevo registro en la base de datos.
    def crear_usuario(
        username: str,
        password: str,
        date_of_birth: str,
        email: str,
        first_name: str,
        last_name: str,
    ):
        """
        Crea un nuevo usuario con validaciones.
        """
        # Validar email
        try:
            validate_email(email)
        except ValidationError:
            raise DatosInvalidos_400()

        # Validar username (máximo 20 caracteres)
        UsuarioParcialSerializer.validar_username(username)

        try:
            usuario = Usuario.objects.create(
                username=username,
                password=make_password(password),
                date_of_birth=date_of_birth,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            return usuario

        except IntegrityError:
            raise ConflictoUsuario_409()

        except DatabaseError:
            raise ErrorInternoServidor_500()