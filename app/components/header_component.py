import reflex as rx
from app.state import WellnessState
from app.config import settings


def header_component() -> rx.Component:
    flower_icon_tag = (
        "flower-2"
        if "flower-2" in settings.ICONS_LIST
        else "flower"
    )
    user_icon_tag = "user-cog"
    logout_icon_tag = "log-out"
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Wellness Dashboard",
                class_name="text-2xl font-semibold text-gray-800",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag=flower_icon_tag,
                        class_name="text-gray-600",
                    ),
                    class_name="p-2 rounded-md hover:bg-gray-100",
                ),
                rx.el.div(
                    rx.icon(
                        tag=user_icon_tag,
                        class_name="text-gray-600",
                    ),
                    rx.el.span(
                        WellnessState.current_user,
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    class_name="flex items-center gap-2 p-2 bg-gray-100 rounded-md cursor-pointer hover:bg-gray-200",
                ),
                rx.el.button(
                    rx.icon(
                        tag=logout_icon_tag,
                        class_name="text-gray-600",
                    ),
                    rx.el.span(
                        "Log out",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    on_click=WellnessState.logout,
                    class_name="flex items-center gap-2 p-2 rounded-md hover:bg-gray-100",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name="px-6 py-4 bg-white border-b border-gray-200",
    )