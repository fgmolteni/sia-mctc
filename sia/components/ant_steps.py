import reflex as rx
from typing import List, Dict, Any

class AntSteps(rx.Component):
    """A component to display a step-by-step process."""
    library = "antd"
    tag = "Steps"

    # The items to display in the steps component.
    items: rx.Var[List[Dict[str, Any]]]

    # The current step.
    current: rx.Var[int]

    # The direction of the steps.
    direction: rx.Var[str]

# Create a factory function to make it easier to use the component.
ant_steps = AntSteps.create

def steps_example() -> rx.Component:
    """An example of how to use the AntSteps component."""
    return rx.box(
        ant_steps(
            items=[
                {"title": "Inicio", "icon": rx.icon(tag="home")},
                {"title": "Viaticos"},
                {"title": "Recomposicion"},
                {"title": "Finalizacion"},
            ],
            current=1,
            direction="horizontal",
        )
    )
