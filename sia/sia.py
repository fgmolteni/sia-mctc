
import reflex as rx
from rxconfig import config


from sia.pages.index import index
from sia.pages.login import login

class State(rx.State):
    """The app state."""



app = rx.App()
app.add_page(index, route="/")
app.add_page(login, route="/login")



