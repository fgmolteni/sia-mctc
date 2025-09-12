from typing import Any, Optional

import reflex as rx

from components.logging import get_sia_logger
from components.db_users import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    get_user_statistics,
    search_users,
    update_user,
)
from sia.components.forms.organisms import search_filters
from sia.components.feedback.organisms import notifications
from sia.components.data_display.organisms import user_statistics, user_table
from sia.components.templates import user_management_template
from sia.components.feedback.toasts import ToastState
from sia.models.validation import User, UserCreate, UserUpdate
from sia.components.forms.inputs import apply_auto_transform
from sia.components.forms.inputs._validation import (
    validate_field_value,
    get_user_validation_rules,
)


# Logger fuera del estado (no serializable)
logger = get_sia_logger("pages.usuarios")


class UserState(rx.State):
    """Estado para manejar la página de usuarios con integración a PostgreSQL."""

    # Lista de usuarios actual
    users_data: list[dict[str, Any]] = []

    # Estados de loading y error
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # Estadísticas
    user_statistics: dict[str, int] = {
        "total_usuarios": 0,
        "activos": 0,
        "administradores": 0,
        "supervisores": 0,
        "usuarios": 0,
    }

    # Filtros
    search_term: str = ""
    role_filter: str = ""
    status_filter: str = ""

    # Modal de usuario
    show_user_modal: bool = False
    selected_user_id: Optional[int] = None

    # Formulario de usuario
    form_nombre: str = ""
    form_apellido: str = ""
    form_nombre_usuario: str = ""
    form_email: str = ""
    form_dni: str = ""
    form_contrasena: str = ""
    form_rol: str = "usuario"
    form_is_editing: bool = False

    # Estados de error de validación
    form_errors: dict[str, str] = {}
    has_validation_errors: bool = False

    # Estados de error específicos por campo
    has_nombre_error: bool = False
    has_apellido_error: bool = False
    has_nombre_usuario_error: bool = False
    has_email_error: bool = False
    has_dni_error: bool = False
    has_contrasena_error: bool = False
    has_rol_error: bool = False

    # Propiedades de mensaje de error específicas
    nombre_error_message: str = ""
    apellido_error_message: str = ""
    nombre_usuario_error_message: str = ""
    email_error_message: str = ""
    dni_error_message: str = ""
    contrasena_error_message: str = ""
    rol_error_message: str = ""

    def validate_field(self, field_name: str, value: str):
        """
        Valida un campo específico usando las reglas de _validation.py
        y actualiza el estado de errores en tiempo real.

        Args:
            field_name: Nombre del campo a validar
            value: Valor a validar
        """
        # Validar el campo usando las funciones existentes
        is_valid, error_message = validate_field_value(
            field_name, value, get_user_validation_rules()
        )

        # Actualizar propiedades específicas según el campo
        if field_name == "nombre":
            self.has_nombre_error = not is_valid
            self.nombre_error_message = error_message if not is_valid else ""
        elif field_name == "apellido":
            self.has_apellido_error = not is_valid
            self.apellido_error_message = error_message if not is_valid else ""
        elif field_name == "nombre_usuario":
            self.has_nombre_usuario_error = not is_valid
            self.nombre_usuario_error_message = error_message if not is_valid else ""
        elif field_name == "email":
            self.has_email_error = not is_valid
            self.email_error_message = error_message if not is_valid else ""
        elif field_name == "dni":
            self.has_dni_error = not is_valid
            self.dni_error_message = error_message if not is_valid else ""
        elif field_name == "contrasena":
            self.has_contrasena_error = not is_valid
            self.contrasena_error_message = error_message if not is_valid else ""
        elif field_name == "rol":
            self.has_rol_error = not is_valid
            self.rol_error_message = error_message if not is_valid else ""

        # Actualizar el diccionario de errores para compatibilidad
        if is_valid:
            # Si es válido, remover cualquier error previo para este campo
            if field_name in self.form_errors:
                new_errors = self.form_errors.copy()
                del new_errors[field_name]
                self.form_errors = new_errors
        else:
            # Si no es válido, agregar o actualizar el error
            new_errors = self.form_errors.copy()
            new_errors[field_name] = error_message
            self.form_errors = new_errors

        # Actualizar el estado general de validación
        self.has_validation_errors = len(self.form_errors) > 0

    def get_field_error(self, field_name: str) -> str:
        """
        Obtiene el mensaje de error para un campo específico.

        Args:
            field_name: Nombre del campo

        Returns:
            Mensaje de error o cadena vacía si no hay error
        """
        return self.form_errors.get(field_name, "")

    def has_field_error(self, field_name: str) -> bool:
        """
        Verifica si un campo tiene error de validación.

        Args:
            field_name: Nombre del campo

        Returns:
            True si el campo tiene error, False en caso contrario
        """
        return field_name in self.form_errors

    def validate_all_fields(self):
        """
        Valida todos los campos del formulario de una vez.
        Útil antes de enviar el formulario.
        """
        # Validar campos requeridos
        self.validate_field("nombre", self.form_nombre)
        self.validate_field("apellido", self.form_apellido)
        self.validate_field("nombre_usuario", self.form_nombre_usuario)
        self.validate_field("email", self.form_email)

        # DNI es opcional
        if self.form_dni.strip():
            self.validate_field("dni", self.form_dni)

        # Contraseña solo es requerida para crear usuario
        if not self.form_is_editing and self.form_contrasena:
            self.validate_field("contrasena", self.form_contrasena)

    def _convert_user_to_display_format(self, user: User) -> dict[str, Any]:
        """Convierte un modelo User de Pydantic al formato esperado por la UI."""
        # Mapear roles para display
        role_display_map = {
            "admin": "Administrador",
            "supervisor": "Supervisor",
            "usuario": "Usuario",
        }

        return {
            "id": user.id,
            "name": f"{user.nombre} {user.apellido}",
            "email": user.email,  # Usando el campo email real
            "dni": user.dni,  # Campo DNI agregado
            "role": role_display_map.get(user.rol, user.rol.title()),
            "area": "Ministerio C&T",  # Por ahora área fija
            "status": "Activo",  # Por ahora todos activos
            "permissions": "Sistema completo",  # Por ahora permisos genéricos
            "attributes": f"Rol: {user.rol}",
            "last_access": user.fecha_creacion.strftime("%d/%m/%Y")
            if user.fecha_creacion
            else "N/A",
            "avatar": user.nombre[0].upper() if user.nombre else "U",
            "actions": "",
        }

    def load_users(self):
        """Cargar usuarios desde la base de datos."""
        self.is_loading = True
        self.error_message = ""

        try:
            # Llamar a la función de la base de datos
            success, message, users = get_all_users()

            if success:
                # Convertir usuarios al formato de display
                self.users_data = [
                    self._convert_user_to_display_format(user) for user in users
                ]
                self.success_message = f"Se cargaron {len(users)} usuarios exitosamente"
                self.error_message = ""
            else:
                self.users_data = []
                self.error_message = f"Error al cargar usuarios: {message}"
                self.success_message = ""

        except Exception as e:
            self.users_data = []
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False
        return []

    def load_statistics(self):
        """Cargar estadísticas de usuarios."""
        try:
            success, message, stats = get_user_statistics()

            if success and stats:
                # Actualizar solo los valores que están presentes
                for key, value in stats.items():
                    if key in self.user_statistics:
                        self.user_statistics[key] = value
                logger.info(f"Estadísticas cargadas exitosamente: {stats}")
            else:
                logger.error(f"Error al cargar estadísticas: {message}")
                # No reinicializar si ya hay datos previos
                if not any(self.user_statistics.values()):
                    self.user_statistics = {
                        "total_usuarios": 0,
                        "activos": 0,
                        "administradores": 0,
                        "supervisores": 0,
                        "usuarios": 0,
                    }
        except Exception as e:
            logger.error(f"Excepción al cargar estadísticas: {e}")
            # Solo reinicializar si no hay datos previos
            if not any(self.user_statistics.values()):
                self.user_statistics = {
                    "total_usuarios": 0,
                    "activos": 0,
                    "administradores": 0,
                    "supervisores": 0,
                    "usuarios": 0,
                }
        return []

    def refresh_statistics(self):
        """Forzar actualización de estadísticas."""
        logger.info("Refrescando estadísticas manualmente")
        return self.load_statistics()

    def debug_statistics(self):
        """Método de debug para mostrar estadísticas en consola."""
        logger.info(f"Estado actual de user_statistics: {self.user_statistics}")
        try:
            success, message, stats = get_user_statistics()
            logger.info(
                f"Resultado directo de get_user_statistics(): success={success}, stats={stats}"
            )
        except Exception as e:
            logger.error(f"Error en debug_statistics: {e}")
        return []

    def search_users_filtered(self):
        """Buscar usuarios con filtros aplicados."""
        self.is_loading = True
        self.error_message = ""

        try:
            # Procesar filtros para enviar a la BD
            # Mapear valores de UI a valores de BD
            role_filter_map = {
                "Administrador": "admin",
                "Supervisor": "supervisor",
                "Usuario": "usuario",
                "Todos los roles": "",
                "": "",
            }

            status_filter_map = {
                "Activo": "active",
                "Inactivo": "inactive",
                "Todos los estados": "",
                "": "",
            }

            db_role_filter = role_filter_map.get(self.role_filter, "")
            db_status_filter = status_filter_map.get(self.status_filter, "")

            success, message, users = search_users(
                search_term=self.search_term,
                role_filter=db_role_filter,
                status_filter=db_status_filter,
            )

            if success:
                self.users_data = [
                    self._convert_user_to_display_format(user) for user in users
                ]
                self.success_message = f"Se encontraron {len(users)} usuarios"
                self.error_message = ""
            else:
                self.users_data = []
                self.error_message = f"Error en búsqueda: {message}"
                self.success_message = ""

        except Exception as e:
            self.users_data = []
            self.error_message = f"Error inesperado en búsqueda: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def set_search_term(self, term: str):
        """Establecer término de búsqueda."""
        self.search_term = term
        # Auto filtrar cuando se cambia el término
        return self.search_users_filtered()

    def set_role_filter(self, role: str):
        """Establecer filtro de rol."""
        self.role_filter = role
        # Auto filtrar cuando se cambia el rol
        return self.search_users_filtered()

    def set_status_filter(self, status: str):
        """Establecer filtro de estado."""
        self.status_filter = status
        # Auto filtrar cuando se cambia el estado
        return self.search_users_filtered()

    def clear_filters(self):
        """Limpiar todos los filtros."""
        self.search_term = ""
        self.role_filter = ""
        self.status_filter = ""

    def show_create_user_modal(self):
        """Mostrar modal para crear usuario."""
        self.show_user_modal = True
        self.form_is_editing = False
        self._clear_form()

    def show_edit_user_modal(self, user_id: int):
        """Mostrar modal para editar usuario."""
        self.show_user_modal = True
        self.form_is_editing = True
        self.selected_user_id = user_id
        self._load_user_to_form(user_id)

    def close_user_modal(self):
        """Cerrar modal de usuario."""
        self.show_user_modal = False
        self.selected_user_id = None
        self._clear_form()

    def _clear_form(self):
        """Limpiar formulario y errores de validación."""
        self.form_nombre = ""
        self.form_apellido = ""
        self.form_nombre_usuario = ""
        self.form_email = ""
        self.form_dni = ""
        self.form_contrasena = ""
        self.form_rol = "usuario"

        # Limpiar errores de validación (diccionario para compatibilidad)
        self.form_errors = {}
        self.has_validation_errors = False

        # Limpiar errores específicos por campo
        self.has_nombre_error = False
        self.nombre_error_message = ""
        self.has_apellido_error = False
        self.apellido_error_message = ""
        self.has_nombre_usuario_error = False
        self.nombre_usuario_error_message = ""
        self.has_email_error = False
        self.email_error_message = ""
        self.has_dni_error = False
        self.dni_error_message = ""
        self.has_contrasena_error = False
        self.contrasena_error_message = ""
        self.has_rol_error = False
        self.rol_error_message = ""

    def _load_user_to_form(self, user_id: int):
        """Cargar datos del usuario al formulario para edición."""
        try:
            # Obtener usuario directamente de la base de datos para tener datos precisos
            success, message, user = get_user_by_id(user_id)

            if success and user:
                self.form_nombre = user.nombre
                self.form_apellido = user.apellido
                self.form_nombre_usuario = user.nombre_usuario
                self.form_email = user.email
                self.form_dni = str(user.dni) if user.dni else ""
                self.form_rol = user.rol
                # No cargar contraseña por seguridad
                self.form_contrasena = ""
            else:
                logger.error(f"Error al cargar usuario para edición: {message}")
                self.error_message = f"Error al cargar usuario: {message}"

        except Exception as e:
            logger.error(f"Error inesperado al cargar usuario {user_id}: {e}")
            self.error_message = f"Error inesperado: {e}"

    def create_user_submit(self):
        """Crear nuevo usuario."""
        # Validar todos los campos antes de proceder
        self.validate_all_fields()

        # Si hay errores de validación, no proceder
        if self.has_validation_errors:
            self.error_message = (
                "Por favor corrige los errores de validación antes de continuar"
            )
            return

        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Crear objeto UserCreate
            # Convertir DNI a entero si está presente
            dni_value = None
            if self.form_dni.strip():
                try:
                    dni_value = int(self.form_dni.strip())
                except ValueError:
                    self.error_message = "El DNI debe ser un número válido"
                    self.is_loading = False
                    return

            user_data = UserCreate(
                nombre=self.form_nombre,
                apellido=self.form_apellido,
                nombre_usuario=self.form_nombre_usuario,
                email=self.form_email,
                dni=dni_value,
                contrasena=self.form_contrasena,
                rol=self.form_rol,
            )

            success, message, user_id = create_user(user_data)

            if success:
                self.success_message = message
                self.error_message = ""
                # Mostrar toast de éxito
                yield ToastState.show_success(
                    f"Usuario creado exitosamente: {self.form_nombre} {self.form_apellido}"
                )
                self.show_user_modal = False
                self._clear_form()
                # Recargar usuarios y estadísticas
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""
                # Mostrar toast de error
                yield ToastState.show_error(f"Error al crear usuario: {message}")

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""
            # Mostrar toast de error para excepciones
            yield ToastState.show_error(f"Error inesperado al crear usuario: {str(e)}")

        finally:
            self.is_loading = False

    def update_user_submit(self):
        """Actualizar usuario existente."""
        if not self.selected_user_id:
            return

        # Validar todos los campos antes de proceder
        self.validate_all_fields()

        # Si hay errores de validación, no proceder
        if self.has_validation_errors:
            self.error_message = (
                "Por favor corrige los errores de validación antes de continuar"
            )
            return

        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Crear objeto UserUpdate solo con campos modificados
            update_data = {}
            if self.form_nombre:
                update_data["nombre"] = self.form_nombre
            if self.form_apellido:
                update_data["apellido"] = self.form_apellido
            if self.form_nombre_usuario:
                update_data["nombre_usuario"] = self.form_nombre_usuario
            if self.form_email:
                update_data["email"] = self.form_email
            if self.form_dni.strip():
                try:
                    update_data["dni"] = int(self.form_dni.strip())
                except ValueError:
                    self.error_message = "El DNI debe ser un número válido"
                    self.is_loading = False
                    return
            if self.form_rol:
                update_data["rol"] = self.form_rol

            user_data = UserUpdate(**update_data)

            success, message, updated_user = update_user(
                self.selected_user_id, user_data
            )

            if success:
                self.success_message = message
                self.error_message = ""
                # Mostrar toast de éxito para actualización
                yield ToastState.show_success(
                    f"Usuario actualizado exitosamente: {self.form_nombre} {self.form_apellido}"
                )
                self.show_user_modal = False
                self._clear_form()
                self.selected_user_id = None
                # Recargar usuarios y estadísticas
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""
                # Mostrar toast de error
                yield ToastState.show_error(f"Error al actualizar usuario: {message}")

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""
            # Mostrar toast de error para excepciones
            yield ToastState.show_error(
                f"Error inesperado al actualizar usuario: {str(e)}"
            )

        finally:
            self.is_loading = False

    def delete_user_action(self, user_id: int):
        """Eliminar usuario."""
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            success, message = delete_user(user_id)

            if success:
                self.success_message = message
                self.error_message = ""
                # Mostrar toast de éxito para eliminación
                yield ToastState.show_success("Usuario eliminado exitosamente")
                # Recargar usuarios y estadísticas
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""
                # Mostrar toast de error
                yield ToastState.show_error(f"Error al eliminar usuario: {message}")

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""
            # Mostrar toast de error para excepciones
            yield ToastState.show_error(
                f"Error inesperado al eliminar usuario: {str(e)}"
            )

        finally:
            self.is_loading = False

    def clear_messages(self):
        """Limpiar mensajes de éxito y error."""
        self.success_message = ""
        self.error_message = ""

    def load_profiles(self):
        """Cargar perfiles de usuario."""
        # Por ahora es un método placeholder

    # Métodos setter para los campos del formulario
    def set_form_nombre(self, nombre: str):
        """Establecer nombre en el formulario con validación en tiempo real."""
        # Aplicar transformación automática (capitalizar)
        self.form_nombre = apply_auto_transform(nombre, "title")
        # Validar el campo en tiempo real
        self.validate_field("nombre", self.form_nombre)

    def set_form_apellido(self, apellido: str):
        """Establecer apellido en el formulario con validación en tiempo real."""
        # Aplicar transformación automática (capitalizar)
        self.form_apellido = apply_auto_transform(apellido, "title")
        # Validar el campo en tiempo real
        self.validate_field("apellido", self.form_apellido)

    def set_form_nombre_usuario(self, nombre_usuario: str):
        """Establecer nombre de usuario en el formulario con validación en tiempo real."""
        # Aplicar transformación automática (minúsculas)
        self.form_nombre_usuario = apply_auto_transform(nombre_usuario, "lowercase")
        # Validar el campo en tiempo real
        self.validate_field("nombre_usuario", self.form_nombre_usuario)

    def set_form_email(self, email: str):
        """Establecer email en el formulario con validación en tiempo real."""
        # Aplicar transformación automática (minúsculas)
        self.form_email = apply_auto_transform(email, "lowercase")
        # Validar el campo en tiempo real
        self.validate_field("email", self.form_email)

    def set_form_dni(self, dni: str):
        """Establecer DNI en el formulario con validación en tiempo real."""
        # Solo permitir números y limpiar espacios/puntos
        import re

        dni_clean = re.sub(r"[^\d]", "", dni)
        self.form_dni = dni_clean
        # Validar el campo en tiempo real
        self.validate_field("dni", self.form_dni)

    def set_form_contrasena(self, contrasena: str):
        """Establecer contraseña en el formulario con validación en tiempo real."""
        # No aplicar transformación para contraseñas (mantener original)
        self.form_contrasena = contrasena
        # Validar el campo en tiempo real (solo para crear usuario, no para editar)
        if not self.form_is_editing:
            self.validate_field("contrasena", self.form_contrasena)

    def set_form_rol(self, rol: str):
        """Establecer rol en el formulario."""
        self.form_rol = rol

    def load_test_data(self):
        """Cargar datos de prueba."""
        self.users_data = [
            {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@mctc.gov.py",
                "role": "Administrador",
                "area": "Ministerio C&T",
                "status": "Activo",
                "permissions": "Sistema completo",
                "attributes": "Rol: admin",
                "avatar": "J",
            },
            {
                "id": 2,
                "name": "María García",
                "email": "maria@mctc.gov.py",
                "role": "Usuario",
                "area": "Ministerio C&T",
                "status": "Activo",
                "permissions": "Solo lectura",
                "attributes": "Rol: usuario",
                "avatar": "M",
            },
        ]

    def on_load(self):
        """Ejecutar al cargar la página."""
        yield self.load_users()
        yield self.load_statistics()












def users_page() -> rx.Component:
    """Página principal de gestión de usuarios usando atomic design."""
    return user_management_template(
        statistics_component=user_statistics,
        filters_component=search_filters,
        table_component=user_table,
        notifications_component=notifications,
    )
