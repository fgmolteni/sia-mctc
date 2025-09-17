import reflex as rx
from sia.components.forms.buttons import button_general
from sia.styles.colors import ColorText, Color
from sia.styles.sizes import SizeText, SizeSpace
from sia.styles.fonts import FontWeight, FontFamily
from sia.styles.border import CommonBorders, BorderRadius
from components.db_users import verify_user

class LoginState(rx.State):
    """Estado para manejar el formulario de login y sesión de usuario."""
    # Campos de login
    email: str = ""
    password: str = ""
    error_message: str = ""
    is_logged_in: bool = False
    is_loading: bool = False  # Estado de carga durante login
    
    # Información del usuario logueado
    current_user_id: int = 0
    user_name: str = ""
    user_email: str = ""
    user_role: str = ""
    avatar_initial: str = ""
    last_access: str = ""
    
    # Estados de validación
    has_validation_errors: bool = False
    field_errors: dict[str, str] = {}

    def validate_login_fields(self) -> bool:
        """Valida los campos de login antes del envío."""
        errors = {}
        is_valid = True
        
        # Validar email/username
        if not self.email.strip():
            errors["email"] = "Este campo es obligatorio"
            is_valid = False
        elif len(self.email.strip()) < 3:
            errors["email"] = "Debe tener al menos 3 caracteres"
            is_valid = False
        
        # Validar contraseña
        if not self.password.strip():
            errors["password"] = "La contraseña es obligatoria"
            is_valid = False
        elif len(self.password.strip()) < 6:
            errors["password"] = "La contraseña debe tener al menos 6 caracteres"
            is_valid = False
        
        self.field_errors = errors
        self.has_validation_errors = not is_valid
        return is_valid
    
    async def handle_login(self):
        """Maneja el intento de login con validación completa."""
        # Limpiar errores previos
        self.error_message = ""
        self.field_errors = {}
        
        # Validar campos antes del envío
        if not self.validate_login_fields():
            return  # No continuar si hay errores de validación
        
        # Iniciar estado de carga
        self.is_loading = True
        
        try:
            success, message, user = verify_user(self.email.strip(), self.password)
            
            if success and user:
                # Configurar sesión exitosa
                self._setup_user_session(user)
                
                # Log de evento de seguridad
                from components.logging import get_sia_logger
                logger = get_sia_logger('auth')
                logger.info("Login exitoso", extra={
                    'action': 'login_success',
                    'user_id': user.id,
                    'user_role': user.rol,
                    'login_method': 'email' if '@' in self.email else 'username'
                })
                
                # Limpiar formulario
                self.password = ""  # Por seguridad
                
                # Redirigir a la página principal
                return rx.redirect("/")
            else:
                # Error de autenticación
                self._handle_login_error(message)
                
        except Exception as e:
            # Error inesperado
            self._handle_login_error("Error de conexión. Verifique su red e inténtelo nuevamente.")
            
            # Log del error para debugging
            from components.logging import get_sia_logger
            logger = get_sia_logger('auth')
            logger.error(f"Error inesperado en login: {str(e)}", extra={
                'action': 'login_error',
                'error_type': type(e).__name__
            })
        
        finally:
            # Finalizar estado de carga
            self.is_loading = False
    
    def _setup_user_session(self, user):
        """Configura la sesión del usuario después de login exitoso."""
        self.is_logged_in = True
        self.error_message = ""
        self.current_user_id = user.id
        
        # Cargar información del usuario
        self.user_name = f"{user.nombre} {user.apellido}"
        self.user_email = user.email
        self.user_role = user.rol
        self.avatar_initial = user.nombre[0].upper() if user.nombre else "U"
        
        # Formatear fecha de último acceso
        from datetime import datetime
        self.last_access = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def _handle_login_error(self, message: str):
        """Maneja errores de login con mensajes apropiados."""
        self.is_logged_in = False
        
        # Mensajes de error más específicos
        if "Usuario o contraseña incorrectos" in message:
            self.error_message = "Las credenciales ingresadas son incorrectas. Verifique su email/usuario y contraseña."
        elif "conexión" in message.lower():
            self.error_message = "Error de conexión con el servidor. Inténtelo nuevamente en unos momentos."
        elif "base de datos" in message.lower():
            self.error_message = "Servicio temporalmente no disponible. Contacte al administrador."
        else:
            self.error_message = message or "Error desconocido. Inténtelo nuevamente."

    def load_user_info(self):
        """
        Método de respaldo para recargar información del usuario.
        Se usa cuando se necesita actualizar datos después del login inicial.
        """
        if self.current_user_id == 0:
            # No hay usuario logueado
            return
            
        try:
            from components.db_users import get_user_by_id
            success, message, user = get_user_by_id(self.current_user_id)
            
            if success and user:
                # Actualizar información del usuario
                self.user_name = f"{user.nombre} {user.apellido}"
                self.user_email = user.email
                self.user_role = user.rol
                self.avatar_initial = user.nombre[0].upper() if user.nombre else "U"
                
                # Actualizar timestamp de último acceso
                from datetime import datetime
                self.last_access = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                return True  # Éxito
            else:
                # Log del error para debugging
                print(f"Error al cargar usuario {self.current_user_id}: {message}")
                return False
                
        except Exception as e:
            # Log del error para debugging
            print(f"Excepción al cargar usuario {self.current_user_id}: {str(e)}")
            return False
    
    def refresh_user_session(self):
        """
        Refresca la información de la sesión del usuario.
        Útil para mantener datos actualizados durante la sesión.
        """
        success = self.load_user_info()
        if not success:
            # Si falla la recarga, mantener datos existentes
            print("Advertencia: No se pudo refrescar la información del usuario")

    def handle_logout(self):
        """
        Maneja el cierre de sesión completo.
        Limpia todos los datos de la sesión y redirige al login.
        """
        # Limpiar estado de autenticación
        self.is_logged_in = False
        self.current_user_id = 0
        self.error_message = ""
        
        # Limpiar información del usuario
        self.user_name = ""
        self.user_email = ""
        self.user_role = ""
        self.avatar_initial = ""
        self.last_access = ""
        
        # Limpiar formulario de login
        self.email = ""
        self.password = ""
        
        # Log de evento de seguridad
        from components.logging import get_sia_logger
        logger = get_sia_logger('auth')
        logger.info("Usuario cerró sesión", extra={'action': 'logout'})
        
        return rx.redirect("/login")

    def validate_session(self):
        """
        Valida que la sesión actual siga siendo válida.
        Útil para verificar que el usuario no haya sido deshabilitado.
        """
        if not self.is_logged_in or self.current_user_id == 0:
            return False
            
        try:
            from components.db_users import get_user_by_id
            success, message, user = get_user_by_id(self.current_user_id)
            
            if success and user:
                # Verificar que el usuario siga activo (si hay campo activo en el futuro)
                return True
            else:
                # Usuario no existe o fue deshabilitado
                self.handle_logout()
                return False
                
        except Exception as e:
            # Error de conexión, mantener sesión pero registrar error
            from components.logging import get_sia_logger
            logger = get_sia_logger('auth')
            logger.error(f"Error validando sesión: {str(e)}", extra={
                'action': 'session_validation_error',
                'user_id': self.current_user_id
            })
            return True  # Asumir válida si hay error de conectividad
    
    def get_user_display_role(self) -> str:
        """Retorna el rol del usuario en formato de display."""
        role_mapping = {
            "admin": "Administrador",
            "supervisor": "Supervisor", 
            "usuario": "Usuario"
        }
        return role_mapping.get(self.user_role, self.user_role.title())
    
    def is_admin(self) -> bool:
        """Verifica si el usuario actual es administrador."""
        return self.user_role == "admin"
    
    def is_supervisor_or_admin(self) -> bool:
        """Verifica si el usuario actual es supervisor o administrador."""
        return self.user_role in ["admin", "supervisor"]
    
    def clear_errors(self):
        """Limpia todos los mensajes de error."""
        self.error_message = ""
        self.field_errors = {}
        self.has_validation_errors = False

    

def simple_logo() -> rx.Component:
    """Logo simple con texto SIA para el login."""
    return rx.hstack(
        rx.text(
            "S",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            color=ColorText.PRIMARY.value,
        ),
        rx.text(
            "i",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            font_style="italic",
            color=ColorText.ACCENT.value,
        ),
        rx.text(
            "A",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            color=ColorText.PRIMARY.value,
        ),
        spacing="0",
        align="center",
        padding=SizeSpace.SMALL.value,
    )


def login_default_icons() -> rx.Component:
    return rx.box(
        rx.card(
            rx.vstack(
                # Logo SIA y titulo
                rx.center(
                    rx.vstack(
                        simple_logo(),
                        rx.heading(
                            "Bienvenido",
                            font_size=SizeText.X_LARGE.value,
                            as_="h2",
                            text_align="center",
                            width="100%",
                            font_weight=FontWeight.BOLD.value,
                            color=ColorText.PRIMARY.value,
                            margin_top=SizeSpace.SMALL.value,
                        ),
                        align="center",
                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                ),
                # Username input
                rx.vstack(
                    rx.text(
                        "Usuario/Email",
                        font_size=SizeText.MEDIUM.value,
                        font_weight=FontWeight.MEDIUM.value,
                        text_align="left",
                        width="100%",
                        color=ColorText.PRIMARY.value,
                    ),
                    rx.input(
                        rx.input.slot(rx.icon(tag="user")),
                        placeholder="user@correo.com",
                        type="email",
                        size="3",
                        width="100%",
                        on_change=LoginState.set_email,
                        value=LoginState.email,
                    ),
                    spacing="2",
                    width="100%",
                ),
                # Password input
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Contraseña",
                            font_size=SizeText.MEDIUM.value,
                            font_weight=FontWeight.MEDIUM.value,
                            color=ColorText.PRIMARY.value,
                        ),
                    ),
                    rx.input(
                        rx.input.slot(rx.icon(tag="lock")),
                        placeholder="Ingrese su contraseña",
                        type="password",
                        size="3",
                        width="100%",
                        on_change=LoginState.set_password,
                        value=LoginState.password,
                    ),
                    rx.vstack(
                        rx.link(
                            "Olvide mi contraseña",
                            href="#",
                            font_size=SizeText.SMALL.value,
                            color=ColorText.ACCENT.value,
                        ),
                        justify="between",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.cond(
                    LoginState.is_loading,
                    rx.button(
                        rx.spinner(loading=True, size="1"),
                        " Iniciando sesión...",
                        disabled=True,
                        width="100%",
                        size="3",
                    ),
                    button_general("Iniciar Sesión", on_click=LoginState.handle_login),
                ),
                rx.cond(
                    LoginState.error_message != "",
                    rx.text(
                        LoginState.error_message,
                        color="red",
                        font_size=SizeText.SMALL.value,
                        text_align="center",
                        padding=SizeSpace.SMALL.value,
                    )
                ),
                
            ),
            max_width="28em",
            size="5",
            width="100%",
        ),
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        min_height="100vh",
        background=Color.background.value,
        padding=SizeSpace.MEDIUM.value,
    )
