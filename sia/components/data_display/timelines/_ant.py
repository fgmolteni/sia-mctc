import reflex as rx
from typing import List, Dict, Any, Optional


class AntTimeline(rx.Component):
    library = "antd"
    tag = "Timeline"
    items: rx.Var[List[Dict[str, Any]]]


class AntTimelineItem(rx.Component):
    library = "antd"
    tag = "Timeline.Item"
    color: rx.Var[str]
    colorText: rx.Var[str]


# Create instances of the components
timeline = AntTimeline.create
timeline_item = AntTimelineItem.create

# Helper function to create timeline with items prop
def create_timeline(items_list):
    """Create a timeline with items prop instead of child components.
    
    Args:
        items_list: List of dictionaries with timeline item properties
        
    Returns:
        Timeline component with items prop
    """
    return timeline(items=items_list)
