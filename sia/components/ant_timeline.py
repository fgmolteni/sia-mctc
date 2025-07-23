import reflex as rx

class AntTimeline(rx.Component):
    library = "antd"
    tag = "Timeline"

class AntTimelineItem(rx.Component):
    library = "antd"
    tag = "Timeline.Item"
    color: rx.Var[str]
    colorText: rx.Var[str]

# Create instances of the components
timeline = AntTimeline.create
timeline_item = AntTimelineItem.create
