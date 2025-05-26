import reflex as rx
from app.state import WellnessState, PieChartSegment
from typing import Dict, Union

TOOLTIP_PROPS = {
    "cursor": {"fill": "transparent"},
    "content_style": {
        "background": "white",
        "borderColor": "var(--gray-a6)",
        "borderWidth": "1px",
        "borderRadius": "0.5rem",
        "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
        "color": "var(--gray-12)",
        "fontSize": "0.875rem",
        "padding": "0.5rem 0.75rem",
    },
    "wrapper_style": {"zIndex": "1000"},
}


def create_gradient_definition(
    segment_data: PieChartSegment,
) -> rx.Component:
    is_spent_or_only_allocated = segment_data[
        "name"
    ].contains("(Spent)") | ~(
        segment_data["name"].contains("(Remaining)")
        | segment_data["name"].contains("(Allocated)")
    )
    opacity_start = rx.cond(
        is_spent_or_only_allocated, 0.9, 0.5
    )
    opacity_end = rx.cond(
        is_spent_or_only_allocated, 0.7, 0.2
    )
    return rx.el.svg.linear_gradient(
        rx.el.svg.stop(
            offset="5%",
            stop_color=segment_data["base_color"],
            stop_opacity=opacity_start,
        ),
        rx.el.svg.stop(
            offset="95%",
            stop_color=segment_data["base_color"],
            stop_opacity=opacity_end,
        ),
        id=segment_data["gradient_id"],
        x1="0",
        y1="0",
        x2="0",
        y2="1",
    )


def render_pie_cell(item: PieChartSegment) -> rx.Component:
    return rx.recharts.cell(fill=item["fill"])


def composite_donut_chart_component() -> rx.Component:
    return rx.el.div(
        rx.el.svg(
            rx.el.svg.defs(
                rx.foreach(
                    WellnessState.composite_donut_data,
                    create_gradient_definition,
                )
            ),
            class_name="w-0 h-0 absolute",
        ),
        rx.recharts.pie_chart(
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.pie(
                rx.foreach(
                    WellnessState.composite_donut_data,
                    render_pie_cell,
                ),
                data=WellnessState.composite_donut_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                inner_radius="60%",
                outer_radius="100%",
                stroke="var(--gray-a1)",
                stroke_width=1,
                padding_angle=1,
                label_line=False,
                label=False,
            ),
            width="100%",
            height=200,
        ),
        rx.el.div(
            rx.el.p(
                f"{WellnessState.overall_progress_value_for_donut_center}%",
                class_name="text-2xl font-bold text-gray-800",
            ),
            rx.el.p(
                WellnessState.donut_center_label,
                class_name="text-xs text-gray-500",
            ),
            class_name="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none",
        ),
        class_name="relative w-48 h-48 mx-auto",
    )