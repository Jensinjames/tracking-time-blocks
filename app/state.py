import reflex as rx
from typing import List, Dict, TypedDict, Optional, Any
from app.states.secure_state import SecureState
from app.config import settings


class DailyStat(rx.Base):
    icon: str
    icon_color: str
    icon_bg_color: str
    title: str
    value: str
    sub_value: str | None = None
    description: str
    change_percent: float
    change_color: str


class CategorySummaryItem(rx.Base):
    id: str
    name: str
    icon: str
    color_text_class: str
    color_bg_class: str


class CompactCategoryData(rx.Base):
    id: str
    name: str
    icon: str
    progress: float
    color_text_class: str
    color_progress_class: str


class SubCategoryGoal(rx.Base):
    id: str
    name: str
    allocated_time: float
    time_spent: float
    progress: float


class CategoryDetail(rx.Base):
    id: str
    name: str
    icon: str
    color_key: str
    total_allocated_time: float
    total_time_spent: float
    overall_progress: float
    subcategories: List[SubCategoryGoal]
    color_bg_class: str
    color_text_class: str
    color_border_class: str
    color_progress_bg_class: str
    base_color_hex: str


class PieChartSegment(TypedDict):
    name: str
    value: float
    fill: str
    base_color: str
    gradient_id: str


SelectOption = TypedDict(
    "SelectOption", {"label": str, "value": str}
)


class WellnessState(SecureState):
    current_user: str = settings.DEFAULT_USER
    daily_stats: list[DailyStat] = [
        DailyStat(
            icon="time_line",
            icon_color="text-blue-500",
            icon_bg_color="bg-blue-100",
            title="Time Tracked",
            value="3.5 hrs",
            description="Today's activity",
            change_percent=15,
            change_color="text-green-500",
        ),
        DailyStat(
            icon="check_circle_line",
            icon_color="text-green-500",
            icon_bg_color="bg-green-100",
            title="Goals Achieved",
            value="2/5",
            description="Completed tasks",
            change_percent=-10,
            change_color="text-red-500",
        ),
        DailyStat(
            icon="mood_line",
            icon_color="text-yellow-500",
            icon_bg_color="bg-yellow-100",
            title="Mood Score",
            value="7/10",
            description="Self-reported",
            change_percent=5,
            change_color="text-green-500",
        ),
        DailyStat(
            icon="heart_line",
            icon_color="text-pink-500",
            icon_bg_color="bg-pink-100",
            title="Wellness Score",
            value="78%",
            description="Overall well-being",
            change_percent=2,
            change_color="text-green-500",
        ),
    ]
    new_category_name: str = ""
    new_category_icon: str = (
        settings.ICONS_LIST[0]
        if settings.ICONS_LIST
        else "box"
    )
    new_category_color_key: str = "blue"
    selected_category_for_subcategory: str = ""
    new_subcategory_name: str = ""
    new_subcategory_allocated_time: str = "1.0"
    selected_category_for_entry: str = ""
    selected_subcategory_for_entry: str = ""
    new_time_entry_hours: str = "0.5"
    categories: Dict[str, CategoryDetail] = {}
    current_category_detail: CategoryDetail | None = None
    icons_options: list[str] = settings.ICONS_LIST
    color_key_options: list[str] = list(
        settings.COLOR_MAP.keys()
    )
    _private_wellness_data: str = (
        "This is sensitive wellness data"
    )

    def _get_color_details(
        self, color_key: str
    ) -> Dict[str, str]:
        return settings.COLOR_MAP.get(
            color_key.lower(),
            settings.COLOR_MAP[settings.DEFAULT_COLOR_KEY],
        )

    def _recalculate_category_progress(
        self, category_id: str
    ):
        if category_id in self.categories:
            category = self.categories[category_id]
            total_allocated = sum(
                (
                    sub.allocated_time
                    for sub in category.subcategories
                )
            )
            total_spent = sum(
                (
                    sub.time_spent
                    for sub in category.subcategories
                )
            )
            category.total_allocated_time = total_allocated
            category.total_time_spent = total_spent
            category.overall_progress = (
                round(
                    total_spent / total_allocated * 100, 1
                )
                if total_allocated > 0
                else 0.0
            )
            self.categories[category_id] = category
            if (
                self.current_category_detail
                and self.current_category_detail.id
                == category_id
            ):
                self.current_category_detail = category

    @rx.event
    def create_new_category(self, form_data: dict):
        name = form_data.get(
            "new_category_name", ""
        ).strip()
        icon = form_data.get("new_category_icon")
        color_key = form_data.get("new_category_color_key")
        if not name or not icon or (not color_key):
            return rx.toast.error(
                "Category name, icon, and color are required."
            )
        category_id = name.lower().replace(" ", "_")
        if category_id in self.categories:
            return rx.toast.error(
                f"Category '{name}' already exists."
            )
        color_details = self._get_color_details(color_key)
        new_cat = CategoryDetail(
            id=category_id,
            name=name,
            icon=icon,
            color_key=color_key,
            total_allocated_time=0.0,
            total_time_spent=0.0,
            overall_progress=0.0,
            subcategories=[],
            color_bg_class=color_details["bg"],
            color_text_class=color_details["text"],
            color_border_class=color_details["border"],
            color_progress_bg_class=color_details[
                "progress_bg"
            ],
            base_color_hex=color_details["base"],
        )
        self.categories[category_id] = new_cat
        self.new_category_name = ""
        self.new_category_icon = (
            self.icons_options[0]
            if self.icons_options
            else "box"
        )
        self.new_category_color_key = (
            self.color_key_options[0]
            if self.color_key_options
            else "blue"
        )
        yield rx.toast.success(
            f"Category '{name}' created."
        )

    @rx.event
    def add_subcategory_goal(self, form_data: dict):
        category_id = form_data.get(
            "selected_category_for_subcategory"
        )
        name = form_data.get(
            "new_subcategory_name", ""
        ).strip()
        try:
            allocated_time = float(
                form_data.get(
                    "new_subcategory_allocated_time", 0
                )
            )
        except ValueError:
            return rx.toast.error(
                "Invalid allocated time. Please enter a number."
            )
        if (
            not category_id
            or not name
            or allocated_time <= 0
        ):
            return rx.toast.error(
                "Parent category, subcategory name, and positive allocated time are required."
            )
        if category_id not in self.categories:
            return rx.toast.error(
                "Selected parent category not found."
            )
        category = self.categories[category_id]
        subcategory_id = f"{category_id}_{name.lower().replace(' ', '_')}"
        if any(
            (
                sub.id == subcategory_id
                for sub in category.subcategories
            )
        ):
            return rx.toast.error(
                f"Subcategory '{name}' already exists in '{category.name}'."
            )
        new_sub = SubCategoryGoal(
            id=subcategory_id,
            name=name,
            allocated_time=allocated_time,
            time_spent=0.0,
            progress=0.0,
        )
        category.subcategories.append(new_sub)
        self._recalculate_category_progress(category_id)
        self.selected_category_for_subcategory = ""
        self.new_subcategory_name = ""
        self.new_subcategory_allocated_time = "1.0"
        yield rx.toast.success(
            f"Subcategory '{name}' added to '{category.name}'."
        )

    @rx.event
    def add_time_entry(self, form_data: dict):
        category_id = form_data.get(
            "selected_category_for_entry"
        )
        subcategory_id = form_data.get(
            "selected_subcategory_for_entry"
        )
        try:
            hours_spent = float(
                form_data.get("new_time_entry_hours", 0)
            )
        except ValueError:
            return rx.toast.error(
                "Invalid time spent. Please enter a number."
            )
        if (
            not category_id
            or not subcategory_id
            or hours_spent <= 0
        ):
            return rx.toast.error(
                "Category, subcategory, and positive time spent are required."
            )
        if category_id not in self.categories:
            return rx.toast.error(
                "Selected category not found."
            )
        category = self.categories[category_id]
        subcategory_found = False
        for sub in category.subcategories:
            if sub.id == subcategory_id:
                sub.time_spent += hours_spent
                sub.progress = (
                    round(
                        sub.time_spent
                        / sub.allocated_time
                        * 100,
                        1,
                    )
                    if sub.allocated_time > 0
                    else (
                        100.0 if sub.time_spent > 0 else 0.0
                    )
                )
                subcategory_found = True
                break
        if not subcategory_found:
            return rx.toast.error(
                "Selected subcategory not found."
            )
        self._recalculate_category_progress(category_id)
        self.selected_category_for_entry = ""
        self.selected_subcategory_for_entry = ""
        self.new_time_entry_hours = "0.5"
        yield rx.toast.success(
            f"Logged {hours_spent:.2f} hrs for subcategory."
        )

    @rx.event
    def handle_category_change_for_entry(
        self, category_id: str
    ):
        self.selected_category_for_entry = category_id
        self.selected_subcategory_for_entry = ""

    @rx.event
    def select_category(self, category_id: str):
        if category_id and category_id in self.categories:
            self.current_category_detail = self.categories[
                category_id
            ]
        else:
            self.current_category_detail = None
            if category_id:
                yield rx.toast.error("Category not found.")

    @rx.event
    def logout(self):
        self.current_user = settings.DEFAULT_USER
        print(
            f"Secure token during logout: {self._secret_token}"
        )
        print(
            f"Private wellness data: {self._private_wellness_data}"
        )
        yield rx.toast.info("Logged out (simulated).")

    @rx.var
    def category_options_for_select(
        self,
    ) -> list[SelectOption]:
        return [
            {"label": cat.name, "value": cat.id}
            for cat_id, cat in self.categories.items()
        ]

    @rx.var
    def subcategory_options_for_select(
        self,
    ) -> list[SelectOption]:
        if (
            self.selected_category_for_entry
            and self.selected_category_for_entry
            in self.categories
        ):
            category = self.categories[
                self.selected_category_for_entry
            ]
            return [
                {"label": sub.name, "value": sub.id}
                for sub in category.subcategories
            ]
        return []

    @rx.var
    def category_summary_list(
        self,
    ) -> list[CategorySummaryItem]:
        return [
            CategorySummaryItem(
                id=cat.id,
                name=cat.name,
                icon=cat.icon,
                color_text_class=cat.color_text_class,
                color_bg_class=cat.color_bg_class,
            )
            for cat_id, cat in self.categories.items()
        ]

    @rx.var
    def compact_categories_list(
        self,
    ) -> list[CompactCategoryData]:
        return [
            CompactCategoryData(
                id=cat.id,
                name=cat.name,
                icon=cat.icon,
                progress=cat.overall_progress,
                color_text_class=cat.color_text_class,
                color_progress_class=cat.color_progress_bg_class,
            )
            for cat_id, cat in self.categories.items()
        ]

    @rx.var
    def composite_donut_data(self) -> list[PieChartSegment]:
        data: list[PieChartSegment] = []
        if not self.categories:
            return [
                PieChartSegment(
                    name="No Data",
                    value=100,
                    fill="#E5E7EB",
                    base_color="#E5E7EB",
                    gradient_id="grad_no_data",
                )
            ]
        for cat_id, category in self.categories.items():
            base_hex = category.base_color_hex
            allocated_remaining_value = (
                category.total_allocated_time
                - category.total_time_spent
            )
            if allocated_remaining_value > 0.001:
                grad_id_allocated = (
                    f"gradient_{category.id}_allocated"
                )
                data.append(
                    PieChartSegment(
                        name=f"{category.name} (Allocated)",
                        value=allocated_remaining_value,
                        fill=f"url(#{grad_id_allocated})",
                        base_color=base_hex,
                        gradient_id=grad_id_allocated,
                    )
                )
            if category.total_time_spent > 0.001:
                grad_id_spent = (
                    f"gradient_{category.id}_spent"
                )
                data.append(
                    PieChartSegment(
                        name=f"{category.name} (Spent)",
                        value=category.total_time_spent,
                        fill=f"url(#{grad_id_spent})",
                        base_color=base_hex,
                        gradient_id=grad_id_spent,
                    )
                )
        if not data:
            return [
                PieChartSegment(
                    name="No Activity Data",
                    value=100,
                    fill="#D1D5DB",
                    base_color="#D1D5DB",
                    gradient_id="grad_no_activity",
                )
            ]
        return data

    @rx.var
    def overall_progress_value_for_donut_center(
        self,
    ) -> float:
        total_allocated_all_categories = sum(
            (
                c.total_allocated_time
                for c in self.categories.values()
            )
        )
        total_spent_all_categories = sum(
            (
                c.total_time_spent
                for c in self.categories.values()
            )
        )
        if total_allocated_all_categories == 0:
            return 0.0
        return round(
            total_spent_all_categories
            / total_allocated_all_categories
            * 100,
            1,
        )

    def on_load(self):
        if not self.categories:
            initial_categories_data = [
                {
                    "id": "fitness",
                    "name": "Fitness",
                    "icon": "heart_pulse",
                    "color_key": "blue",
                    "subs": [
                        ("Morning Run", 1, 0.5),
                        ("Gym Session", 4, 1.5),
                    ],
                },
                {
                    "id": "learning",
                    "name": "Learning",
                    "icon": "book_open",
                    "color_key": "green",
                    "subs": [
                        ("Online Course", 8, 7),
                        ("Read Book", 2, 1),
                    ],
                },
                {
                    "id": "mindfulness",
                    "name": "Mindfulness",
                    "icon": "plant",
                    "color_key": "teal",
                    "subs": [
                        ("Meditation", 0.5, 0.25),
                        ("Journaling", 0.5, 0.5),
                    ],
                },
            ]
            for cat_data in initial_categories_data:
                color_details = self._get_color_details(
                    cat_data["color_key"]
                )
                category = CategoryDetail(
                    id=cat_data["id"],
                    name=cat_data["name"],
                    icon=cat_data["icon"],
                    color_key=cat_data["color_key"],
                    total_allocated_time=0.0,
                    total_time_spent=0.0,
                    overall_progress=0.0,
                    subcategories=[],
                    color_bg_class=color_details["bg"],
                    color_text_class=color_details["text"],
                    color_border_class=color_details[
                        "border"
                    ],
                    color_progress_bg_class=color_details[
                        "progress_bg"
                    ],
                    base_color_hex=color_details["base"],
                )
                for (
                    sub_name,
                    sub_alloc,
                    sub_spent,
                ) in cat_data["subs"]:
                    sub_id = f"{category.id}_{sub_name.lower().replace(' ', '_')}"
                    sub_progress = (
                        round(
                            sub_spent / sub_alloc * 100, 1
                        )
                        if sub_alloc > 0
                        else 0
                    )
                    category.subcategories.append(
                        SubCategoryGoal(
                            id=sub_id,
                            name=sub_name,
                            allocated_time=sub_alloc,
                            time_spent=sub_spent,
                            progress=sub_progress,
                        )
                    )
                self.categories[category.id] = category
                self._recalculate_category_progress(
                    category.id
                )
            if self.categories:
                first_category_id = list(
                    self.categories.keys()
                )[0]
                self.current_category_detail = (
                    self.categories[first_category_id]
                )

    @rx.event
    def reveal_secrets_server_side(self):
        print(
            f"Accessing secret token: {self._secret_token}"
        )
        print(
            f"Accessing private wellness data: {self._private_wellness_data}"
        )
        print(f"Current secure counter: {self.counter}")
        yield rx.toast.info(
            "Secrets printed to server console."
        )