import reflex as rx
from sia.pages.login import login
from sia.pages.user_control import user_control
from sia.views.agent import AgentState
from sia.views.vehicle import vehicle_view, VehicleState
from sia.pages.index import index
from sia.pages.agentes import agentes_pages
from sia.pages.usuarios import users_page, UserState
from sia.pages.profiles import profiles_page
from sia.pages.gallery import gallery_page


class State(rx.State):
    pass

app = rx.App(
    stylesheets=[
        "/style.css",
        'https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap',
    ],
    theme=rx.theme(
        appearance="light",
        has_background=True,
        accent_color="green",
        gray_color="slate",
        radius="small",
        scaling="100%",
    ),
)

app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(agentes_pages, route="/agentes", on_load=AgentState.on_load)
app.add_page(vehicle_view, route="/vehiculos", on_load=VehicleState.on_load)
app.add_page(users_page, route="/users", on_load=UserState.load_users)
app.add_page(user_control, route="/register")
app.add_page(profiles_page, route="/users/profiles",  on_load=UserState.load_profiles)
app.add_page(gallery_page, route="/gallery")
#app.add_page(users_page, route="/usuarios", on_load=UserState.load_users)
