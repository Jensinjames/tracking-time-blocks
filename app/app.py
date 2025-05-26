import reflex as rx
from app.pages.dashboard_page import dashboard_page
from app.pages.sign_in_page import sign_in_page
from app.pages.sign_up_page import sign_up_page
from app.states.auth_state import AuthState
from app.state import WellnessState
from app.config import settings


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.in_session,
            dashboard_page(),
            rx.el.div(
                rx.icon(
                    tag="loader",
                    class_name="animate-spin h-12 w-12 text-blue-500",
                ),
                rx.el.p(
                    "Loading...",
                    class_name="text-gray-600 mt-2",
                ),
                class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50 font-['Inter']",
            ),
        )
    )


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
    route="/",
    title=f"{settings.APP_NAME} | Dashboard",
    on_load=[
        AuthState.check_session,
        WellnessState.initial_app_load,
    ],
)
app.add_page(
    sign_in_page,
    route="/sign-in",
    title=f"{settings.APP_NAME} | Sign In",
)
app.add_page(
    sign_up_page,
    route="/sign-up",
    title=f"{settings.APP_NAME} | Sign Up",
)