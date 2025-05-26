import reflex as rx


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
            class_name="flex-1",
        ),
        rx.el.button(
            "Track Activity",
            class_name="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6 flex items-center justify-between",
    )