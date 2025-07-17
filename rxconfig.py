import reflex as rx
import sia.styles.styles as styles

config = rx.Config(
    app_name="sia",
    stylesheets=styles.STYLESHEETS,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
