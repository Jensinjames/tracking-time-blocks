import reflex as rx
from app.state import WellnessState


def category_creation_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Create New Category",
            class_name="text-lg font-semibold text-gray-700 mb-3",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Category Name:",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.input(
                    default_value=WellnessState.new_category_name,
                    name="new_category_name",
                    placeholder="e.g., Fitness",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Icon:",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.select(
                    rx.foreach(
                        WellnessState.icons_options,
                        lambda icon_name: rx.el.option(
                            icon_name, value=icon_name
                        ),
                    ),
                    value=WellnessState.new_category_icon,
                    on_change=WellnessState.set_new_category_icon,
                    name="new_category_icon",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Color Theme:",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.select(
                    rx.foreach(
                        WellnessState.color_key_options,
                        lambda color_key: rx.el.option(
                            color_key.capitalize(),
                            value=color_key,
                        ),
                    ),
                    value=WellnessState.new_category_color_key,
                    on_change=WellnessState.set_new_category_color_key,
                    name="new_category_color_key",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Create Category",
                type="submit",
                class_name="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
            ),
            on_submit=WellnessState.create_new_category,
            prevent_default=True,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def subcategory_goal_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Add Subcategory Goal",
            class_name="text-lg font-semibold text-gray-700 mb-3",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Parent Category:",
                    class_name="text-sm font-medium text-gray-600",
                ),
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
                    value=WellnessState.selected_category_for_subcategory,
                    on_change=WellnessState.set_selected_category_for_subcategory,
                    name="selected_category_for_subcategory",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Subcategory Name:",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.input(
                    default_value=WellnessState.new_subcategory_name,
                    name="new_subcategory_name",
                    placeholder="e.g., Morning Run",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Allocated Time (hours):",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.input(
                    default_value=WellnessState.new_subcategory_allocated_time,
                    name="new_subcategory_allocated_time",
                    placeholder="e.g., 1.5",
                    type="number",
                    step="0.1",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Add Subcategory Goal",
                type="submit",
                class_name="w-full bg-green-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-700 transition-colors",
            ),
            on_submit=WellnessState.add_subcategory_goal,
            prevent_default=True,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def time_entry_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Log Time Entry",
            class_name="text-lg font-semibold text-gray-700 mb-3",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Category:",
                    class_name="text-sm font-medium text-gray-600",
                ),
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
                    value=WellnessState.selected_category_for_entry,
                    on_change=WellnessState.handle_category_change_for_entry,
                    name="selected_category_for_entry",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Subcategory Goal:",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Subcategory...",
                        value="",
                        disabled=True,
                    ),
                    rx.foreach(
                        WellnessState.subcategory_options_for_select,
                        lambda sub_option: rx.el.option(
                            sub_option["label"],
                            value=sub_option["value"],
                        ),
                    ),
                    value=WellnessState.selected_subcategory_for_entry,
                    on_change=WellnessState.set_selected_subcategory_for_entry,
                    name="selected_subcategory_for_entry",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                    disabled=WellnessState.selected_category_for_entry
                    == "",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Time Spent (hours):",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.input(
                    default_value=WellnessState.new_time_entry_hours,
                    name="new_time_entry_hours",
                    placeholder="e.g., 0.75",
                    type="number",
                    step="0.01",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Log Time",
                type="submit",
                class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors",
            ),
            on_submit=WellnessState.add_time_entry,
            prevent_default=True,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )