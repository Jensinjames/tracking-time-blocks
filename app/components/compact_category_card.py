import reflex as rx
from app.state import CompactCategoryData, WellnessState


def compact_category_card_component(
    category_data: CompactCategoryData,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    tag=category_data.icon,
                    class_name=f"w-6 h-6 {category_data.color_text_class}",
                ),
                rx.el.p(
                    category_data.name,
                    class_name=f"text-sm font-semibold {category_data.color_text_class} flex-1",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                rx.icon(
                    tag="circle_x",
                    class_name="w-4 h-4 text-red-500 hover:text-red-700 opacity-75 hover:opacity-100",
                ),
                on_click=[
                    lambda: WellnessState.delete_category(
                        category_data.id
                    ),
                    rx.stop_propagation,
                ],
                class_name="p-1 rounded-full hover:bg-red-100 transition-colors absolute top-2 right-2",
                title=f"Delete category {category_data.name}",
            ),
            class_name="flex justify-between items-center mb-2 relative",
        ),
        rx.el.div(
            rx.el.div(
                style={
                    "width": f"{category_data.progress}%"
                },
                class_name=f"h-2 rounded-full {category_data.color_progress_class}",
            ),
            class_name="w-full bg-gray-200 rounded-full h-2 mb-1",
        ),
        rx.el.p(
            f"{category_data.progress:.1f}% complete",
            class_name="text-xs text-gray-500 text-right",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm cursor-pointer hover:shadow-md transition-shadow relative",
        on_click=lambda: WellnessState.select_category(
            category_data.id
        ),
    )