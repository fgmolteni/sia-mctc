import reflex as rx
from sia.components.ant_timeline import timeline, timeline_item
from sia.styles.colors import Color, ColorText

timeline(
    timeline_item(rx.text("Create a services site 2015-09-01",
                  color="white"), color=Color.accent.value),
    timeline_item(rx.text("Solve initial network problems 2015-09-01",
                  color="white"), color=Color.accent.value),
    timeline_item(rx.text("Technical testing 2015-09-01",
                  color="white"), color=Color.accent.value),
    timeline_item(rx.text("Network", color="white"),
                  color=Color.warning.value),
)
