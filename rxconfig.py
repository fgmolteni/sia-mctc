import reflex as rx

config = rx.Config(
    app_name="sia",
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Lexend+Tera&display=swap",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
