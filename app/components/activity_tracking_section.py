import reflex as rx
from app.state import WellnessState


def activity_tracking_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Activity Tracking",
                class_name="text-lg font-semibold text-gray-800",
            ),
            rx.el.p(
                "Track your time spent on activities in real-time",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex-1 mb-4 md:mb-0",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option(
                    "Select Category...",
                    value="",
                    disabled=True,
                ),
                rx.foreach(
                    WellnessState.category_options_for_select,
                    lambda cat_option: rx.el.option(
                        cat_option["label"],
                        value=cat_option["value"],
                    ),
                ),
                value=WellnessState.tracking_category_id,
                on_change=WellnessState.set_tracking_category,
                disabled=WellnessState.is_tracking_active,
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
            ),
            rx.el.select(
                rx.el.option(
                    "Select Subcategory...",
                    value="",
                    disabled=True,
                ),
                rx.foreach(
                    WellnessState.tracking_subcategory_options_for_select,
                    lambda sub_option: rx.el.option(
                        sub_option["label"],
                        value=sub_option["value"],
                    ),
                ),
                value=WellnessState.tracking_subcategory_id,
                on_change=WellnessState.set_tracking_subcategory,
                disabled=WellnessState.is_tracking_active
                | (
                    WellnessState.tracking_category_id == ""
                ),
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
            ),
            class_name="flex flex-col sm:flex-row gap-4 items-center w-full sm:w-auto",
        ),
        rx.el.div(
            rx.cond(
                WellnessState.is_tracking_active,
                rx.el.p(
                    WellnessState.tracking_elapsed_time_str,
                    class_name="text-2xl font-mono text-gray-700 min-w-[100px] text-center",
                ),
                rx.el.p(
                    "00:00:00",
                    class_name="text-2xl font-mono text-gray-400 min-w-[100px] text-center",
                ),
            ),
            rx.el.button(
                rx.cond(
                    WellnessState.is_tracking_active,
                    "Stop Tracking",
                    "Start Tracking",
                ),
                on_click=rx.cond(
                    WellnessState.is_tracking_active,
                    WellnessState.stop_activity_tracking,
                    WellnessState.start_activity_tracking,
                ),
                class_name=rx.cond(
                    WellnessState.is_tracking_active,
                    "bg-red-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-700 transition-colors w-full sm:w-auto",
                    "bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors w-full sm:w-auto",
                ),
            ),
            class_name="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto mt-4 sm:mt-0",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6 flex flex-col md:flex-row items-center justify-between gap-6",
    )