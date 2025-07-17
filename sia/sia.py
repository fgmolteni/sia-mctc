
import reflex as rx
from rxconfig import config


from sia.pages.index import index
from sia.pages.login import login

class State(rx.State):
    """The app state."""

app = rx.App(
    stylesheets=[
        'https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap',
        'https://fonts.googleapis.com/css2?family=Inconsolata:wdth,wght@50..200,200..900&display=swap'

    ],
)

app.add_page(index, route="/")
app.add_page(login, route="/login")



