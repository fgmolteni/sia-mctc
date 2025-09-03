import reflex as rx
from sia.views.login_views import login_default_icons
from sia.components.navigation.navbars import navbar_user
from sia.components.feedback.banners import top_banner_gradient
from sia.views.footer_login import footer_login

class LoginTransitionState(rx.State):
    opacity: str = "0"

    def set_opacity(self):
        self.opacity = "1"

class Spline(rx.Component):
    library = "@splinetool/react-spline"
    lib_dependencies: list[str] = ["@splinetool/runtime@1.5.5", "@splinetool/react-spline"]
    tag = "Spline"
    is_default = True
    scene: rx.Var[str]

spline = Spline.create

scene_1 = "https://prod.spline.design/6SNYlarzbo0-xZgs/scene.splinecode" #hole particule
scene_2 = "https://prod.spline.design/lyu6KMjx6GdU0uuL/scene.splinecode" 
scene_3 = "https://prod.spline.design/UNk43TNC4EyUDUII/scene.splinecode" # hole black
scene_4 = "https://prod.spline.design/MPMkLHd8PjLS9k09/scene.splinecode" #bg wave point color

def spline_demo(**kwargs):
    return spline(scene=scene_3, **kwargs)


def login() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar_user(),
            top_banner_gradient(),
            align_items="center",
        ),
        # Fondo Spline
        spline_demo(
            style={
                "position": "absolute",
                "width": "100%",
                "height": "100vh",
                "scale": 1,
                "opacity": LoginTransitionState.opacity,
                "transition": "opacity 5s ease-in-out"
            },
            on_mount=LoginTransitionState.set_opacity,
        ),
        # Tarjeta de login centrada
        rx.hstack(
            rx.box(
                rx.vstack(
                    login_default_icons(),
                    width="100%",
                    height="100vh",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    z_index="1",
                ),
                width="800px",
                
            ),
            position="relative",
            #z_index="1",
            width="100vw",
            height="100vh",
            justify_content="flex-end",
            align_items="center",
        ),
        footer_login(),
        position="relative",
        width="100vw",
        height="100vh",
        overflow="hidden", 
    )
