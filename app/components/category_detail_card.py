import reflex as rx
from app.state import (
    CategoryDetail,
    SubCategoryGoal,
    WellnessState,
)


def sub_category_progress_item(
    sub_category: SubCategoryGoal,
    parent_progress_color_class: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                sub_category.name,
                class_name="text-sm font-medium text-gray-700",
            ),
            rx.el.p(
                f"{sub_category.time_spent:.1f} / {sub_category.allocated_time:.1f} hrs",
                class_name=f"text-xs {parent_progress_color_class.replace('bg-', 'text-').replace('-500', '-600')} font-semibold",
            ),
            class_name="flex justify-between items-baseline",
        ),
        rx.el.div(
            rx.el.div(
                style={
                    "width": f"{sub_category.progress}%"
                },
                class_name=f"h-2 rounded {parent_progress_color_class}",
            ),
            class_name="w-full bg-gray-200 rounded h-2 mt-1",
        ),
        class_name="py-3",
    )


def category_detail_card_component(
    category_detail: CategoryDetail,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    tag=category_detail.icon,
                    class_name=f"w-8 h-8 {category_detail.color_text_class}",
                ),
                class_name=f"p-3 rounded-lg {category_detail.color_bg_class} mr-4",
            ),
            rx.el.div(
                rx.el.h3(
                    category_detail.name,
                    class_name="text-xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Overall Progress",
                    class_name="text-sm text-gray-500",
                ),
            ),
            class_name="flex items-center mb-4 pb-4 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Overall",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.p(
                    f"{category_detail.overall_progress:.1f}%",
                    class_name=f"text-sm font-semibold {category_detail.color_text_class}",
                ),
                class_name="flex justify-between items-baseline mb-1",
            ),
            rx.el.div(
                rx.el.div(
                    style={
                        "width": f"{category_detail.overall_progress}%"
                    },
                    class_name=f"h-3 rounded-full {category_detail.color_progress_bg_class}",
                ),
                class_name="w-full bg-gray-200 rounded-full h-3",
            ),
            class_name="mb-6",
        ),
        rx.el.h4(
            "Subcategory Goals",
            class_name="text-md font-semibold text-gray-700 mb-2",
        ),
        rx.el.div(
            rx.cond(
                category_detail.subcategories.length() > 0,
                rx.foreach(
                    category_detail.subcategories,
                    lambda sub_cat: sub_category_progress_item(
                        sub_cat,
                        category_detail.color_progress_bg_class,
                    ),
                ),
                rx.el.p(
                    "No subcategories defined yet. Add some using the form on the left!",
                    class_name="text-sm text-gray-500 py-4 text-center",
                ),
            ),
            class_name="divide-y divide-gray-200 max-h-96 overflow-y-auto",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm w-full",
    )