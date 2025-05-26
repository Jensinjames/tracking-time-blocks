import reflex as rx
from app.pages.dashboard_page import dashboard_page
from app.state import WellnessState
from app.config import settings


def index() -> rx.Component:
    return dashboard_page()


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
        radius="medium",
    ),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    title=settings.APP_NAME,
    on_load=WellnessState.on_load,
)