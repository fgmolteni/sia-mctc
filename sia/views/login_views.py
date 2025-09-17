import reflex as rx
from components.imagen_open import open_image
from sia.components.forms.buttons import button_general
from sia.styles.colors import ColorText
from sia.styles.sizes import SizeText
from sia.styles.fonts import FontWeight
from components.db_users import verify_user

img = open_image("/home/subco/project/sia-mctc/assets/logo.png")

class LoginState(rx.State):
    """Estado para manejar el formulario de login y sesión de usuario."""
    # Campos de login
    email: str = ""
    password: str = ""
    error_message: str = ""
    is_logged_in: bool = False
    
    # Información del usuario logueado
    current_user_id: int = 0
    user_name: str = ""
    user_email: str = ""
    user_role: str = ""
    avatar_initial: str = ""
    last_access: str = ""

    async def handle_login(self):
        """Maneja el intento de login con validación completa."""
        try:
            success, message, user = verify_user(self.email, self.password)
            
            if success and user:
                # Configurar sesión
                self.is_logged_in = True
                self.error_message = ""
                self.current_user_id = user.id
                
                # Cargar información del usuario directamente desde verify_user
                self.user_name = f"{user.nombre} {user.apellido}"
                self.user_email = user.email
                self.user_role = user.rol
                self.avatar_initial = user.nombre[0].upper() if user.nombre else "U"
                
                # Formatear fecha de último acceso
                from datetime import datetime
                self.last_access = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                # Redirigir a la página principal
                return rx.redirect("/")
            else:
                # Error de autenticación
                self.error_message = message or "Usuario o contraseña incorrectos"
                self.is_logged_in = False
                
        except Exception:
            # Error inesperado
            self.error_message = "Error de conexión. Inténtelo nuevamente."
            self.is_logged_in = False

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
            print(f"Error validando sesión: {str(e)}")
            return True  # Asumir válida si hay error de conectividad

    

def login_default_icons() -> rx.Component:
    return rx.box(
        rx.card(
            rx.vstack(
                # Logo and title
                rx.center(
                    rx.heading(
                        "Bienvenido",
                        font_size=SizeText.X_LARGE.value,
                        as_="h2",
                        text_align="center",
                        width="100%",
                        font_weight=FontWeight.BOLD.value,
                        color=ColorText.PRIMARY.value,
                    ),
                    direction="column",
                    spacing="5",
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
                button_general("Sign in", on_click=LoginState.handle_login),
                rx.cond(
                    LoginState.error_message != "",
                    rx.text(LoginState.error_message, color="red")
                ),
                
            ),
            max_width="28em",
            size="5",
            width="100%",
        ),
        display="flex",
        flex_direction="column",
        align="center",
        justify_content="center",   
    )
