import reflex as rx
from app.state import CompactCategoryData, WellnessState


def compact_category_card_component(
    category_data: CompactCategoryData,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                tag=category_data.icon,
                class_name=f"w-6 h-6 {category_data.color_text_class}",
            ),
            rx.el.p(
                category_data.name,
                class_name=f"text-sm font-semibold {category_data.color_text_class}",
            ),
            class_name="flex items-center gap-3 mb-2",
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
        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm cursor-pointer hover:shadow-md transition-shadow",
        on_click=lambda: WellnessState.select_category(
            category_data.id
        ),
    )