import reflex as rx
from sia.components.data_display.timelines import timeline
from sia.styles.colors import Color

timeline(items=[
    {"children": rx.text("Create a services site 2015-09-01", color="white"), "color": Color.accent.value},
    {"children": rx.text("Solve initial network problems 2015-09-01", color="white"), "color": Color.accent.value},
    {"children": rx.text("Technical testing 2015-09-01", color="white"), "color": Color.accent.value},
    {"children": rx.text("Network", color="white"), "color": Color.warning.value},
])

# Alternative using the helper function
# create_timeline([
#     {"children": rx.text("Create a services site 2015-09-01", color="white"), "color": Color.accent.value},
#     {"children": rx.text("Solve initial network problems 2015-09-01", color="white"), "color": Color.accent.value},
#     {"children": rx.text("Technical testing 2015-09-01", color="white"), "color": Color.accent.value},
#     {"children": rx.text("Network", color="white"), "color": Color.warning.value},
# ])
