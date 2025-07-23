import reflex as rx

class AntBreadcrumb(rx.Component):
    library = "antd"
    tag = "Breadcrumb"

class AntBreadcrumbItem(rx.Component):
    library = "antd"
    tag = "Breadcrumb.Item"
    href: rx.Var[str]
    colorText: rx.Var[str]

# Create instances of the components
breadcrumb = AntBreadcrumb.create
breadcrumb_item = AntBreadcrumbItem.create