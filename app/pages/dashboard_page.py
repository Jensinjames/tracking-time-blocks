import reflex as rx
from app.state import WellnessState
from app.components.header_component import header_component
from app.components.daily_overview_card import (
    daily_overview_card_component,
)
from app.components.composite_donut_chart import (
    composite_donut_chart_component,
)
from app.components.category_detail_card import (
    category_detail_card_component,
)
from app.components.compact_category_card import (
    compact_category_card_component,
)
from app.components.activity_tracking_section import (
    activity_tracking_section,
)
from app.components.crud_forms import (
    category_creation_form,
    subcategory_goal_form,
    time_entry_form,
)


def dashboard_page() -> rx.Component:
    return rx.el.div(
        header_component(),
        rx.el.main(
            rx.el.section(
                rx.el.h2(
                    "Daily Overview",
                    class_name="text-xl font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        WellnessState.daily_stats,
                        daily_overview_card_component,
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
                ),
                class_name="mb-6",
            ),
            rx.el.section(
                rx.el.h2(
                    "Manage Categories & Goals",
                    class_name="text-xl font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    category_creation_form(),
                    subcategory_goal_form(),
                    time_entry_form(),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="mb-6",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Category Performance",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Category Overview",
                                class_name="text-lg font-semibold text-gray-700",
                            ),
                            class_name="flex items-center justify-between mb-4",
                        ),
                        composite_donut_chart_component(),
                        rx.el.div(
                            rx.foreach(
                                WellnessState.category_summary_list,
                                lambda item: rx.el.div(
                                    rx.icon(
                                        tag=item.icon,
                                        class_name=f"w-5 h-5 mr-3 {item.color_text_class}",
                                    ),
                                    rx.el.span(
                                        item.name,
                                        class_name=f"text-sm font-medium {item.color_text_class}",
                                    ),
                                    class_name="flex items-center p-2 cursor-pointer hover:bg-gray-100 rounded-md",
                                    on_click=lambda: WellnessState.select_category(
                                        item.id
                                    ),
                                ),
                            ),
                            class_name="mt-4 space-y-1",
                        ),
                        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm w-full lg:w-1/4",
                    ),
                    rx.el.div(
                        rx.cond(
                            WellnessState.current_category_detail,
                            category_detail_card_component(
                                WellnessState.current_category_detail
                            ),
                            rx.el.div(
                                "Select a category to see details.",
                                class_name="p-4 text-gray-500 text-center",
                            ),
                        ),
                        class_name="w-full lg:w-1/2 px-0 lg:px-4 flex justify-center items-start",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(
                                WellnessState.compact_categories_list,
                                compact_category_card_component,
                            ),
                            class_name="grid grid-cols-1 gap-4",
                        ),
                        class_name="w-full lg:w-1/4 space-y-4",
                    ),
                    class_name="flex flex-col lg:flex-row gap-6",
                ),
                class_name="mb-6",
            ),
            activity_tracking_section(),
            class_name="p-6 bg-gray-50 min-h-screen font-['Inter']",
        ),
    )