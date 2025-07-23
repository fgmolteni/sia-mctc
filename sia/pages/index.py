from audioop import reverse
import reflex as rx
from sia.components.buttons import *
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.sizes import *

from sia.components.headers import name_app_wth_logo

from sia.views.sidebar import sidebar_main as sidebar
from sia.views.playground import playground 
from sia.views.forms_views import FormState

from sia.components.navbar import navbar




def index():
    return rx.vstack(
        navbar(),
        rx.hstack(
            sidebar(),
            playground(),

        ),
        
        spacing="2",
        align_items="stretch",
        width="100%",
        min_height="100vh",
        bg=Color.background.value,
        padding_x="10px",
    )
