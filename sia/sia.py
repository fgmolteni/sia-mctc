
import reflex as rx
from rxconfig import config


from sia.pages.index import index
from sia.pages.login import login
from sia.views.forms_views import FormState
from sia.views.agent import agent_view, AgentState
from sia.views.vehicle import vehicle_view, VehicleState
#from sia.pages.playground import playground

class State(rx.State):
    """The app state."""

app = rx.App(
    stylesheets=[
        "/style.css",
        'https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap',
        'https://fonts.googleapis.com/css2?family=Inconsolata:wdth,wght@50..200,200..900&display=swap',
        'https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap',
        'https://fonts.googleapis.com/css2?family=Plaster&display=swap',
        'https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap'

    ],
)

app.add_page(index, route="/", on_load=FormState.on_load)
app.add_page(login, route="/login")
app.add_page(agent_view, route="/agentes", on_load=AgentState.on_load)
app.add_page(vehicle_view, route="/vehiculos", on_load=VehicleState.on_load)
#app.add_page(playground, route="/playground")



