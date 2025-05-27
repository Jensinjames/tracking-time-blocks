import reflex as rx
from app.state import DailyStat


def daily_overview_card_component(
    stat: DailyStat,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    tag=stat.icon,
                    class_name=f"w-6 h-6 {stat.icon_color}",
                ),
                class_name=f"p-3 rounded-lg {stat.icon_bg_color}",
            ),
            rx.el.div(
                rx.el.span(
                    f"{stat.change_percent}%",
                    class_name=f"text-sm font-medium {stat.change_color}",
                ),
                rx.icon(
                    tag=rx.cond(
                        stat.change_percent >= 0,
                        "arrow-up",
                        "arrow-down",
                    ),
                    class_name=f"w-4 h-4 {stat.change_color}",
                ),
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.h3(
            stat.title,
            class_name="text-sm font-semibold text-gray-500 mb-1",
        ),
        rx.el.p(
            stat.value,
            class_name="text-2xl font-bold text-gray-800",
        ),
        rx.cond(
            stat.sub_value,
            rx.el.p(
                stat.sub_value,
                class_name="text-sm text-gray-500",
            ),
            rx.fragment(),
        ),
        rx.el.p(
            stat.description,
            class_name="text-xs text-gray-500 mt-1",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex-1 min-w-[200px]",
    )