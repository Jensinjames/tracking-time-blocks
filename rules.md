. **Directory structure**

   
rollen_dashboard/
   ├── app.py
   ├── state.py
   ├── models.py
   ├── pages/
   │   ├── login.py
   │   ├── dashboard.py
   │   ├── overview.py
   │   └── settings.py
   ├── components/
   │   ├── pie_chart.py
   │   ├── category_ribbon.py
   │   ├── entry_form.py
   │   └── activity_table.py
   └── styles/            # Tailwind config, global CSS


---

## 2. Style & Code Guidelines

* **PEP8 / Black** with 88‑char line length
* **Snake\_case** for functions/vars; **PascalCase** for classes
* **Type hints** everywhere
* Reflex components: one .py → one class/function
* Tailwind via reflex-tailwind for all styling

---

## 3. Data Models (models.py)

python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

class CategoryORM(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    color = Column(String)

class EntryORM(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    value = Column(Integer)
    timestamp = Column(DateTime)
    category = relationship('CategoryORM')

class Category(BaseModel):
    id: int
    name: str
    color: str

class Entry(BaseModel):
    id: int
    category_id: int
    value: int
    timestamp: datetime


---

## 4. App State & Actions (state.py)

python
import reflex as rx
from models import CategoryORM, EntryORM, Category, Entry
from sqlalchemy.orm import Session

class AppState(rx.State):
    categories: list[Category] = []
    entries:    list[Entry]    = []
    selected_date: date        = date.today()
    user: Optional[str]        = None

    @rx.action
    def load_categories(self):
        with Session() as db:
            rows = db.query(CategoryORM).all()
        self.categories = [Category.from_orm(r) for r in rows]

    @rx.action
    def add_category(self, name: str, color: str):
        with Session() as db:
            cat = CategoryORM(name=name, color=color)
            db.add(cat); db.commit(); db.refresh(cat)
        self.load_categories()

    @rx.action
    def load_entries(self):
        with Session() as db:
            rows = (
                db.query(EntryORM)
                  .filter(EntryORM.timestamp.date() == self.selected_date)
                  .all()
            )
        self.entries = [Entry.from_orm(r) for r in rows]

    @rx.action
    def add_entry(self, category_id: int, value: int, timestamp: datetime):
        with Session() as db:
            e = EntryORM(category_id=category_id, value=value, timestamp=timestamp)
            db.add(e); db.commit()
        self.load_entries()


---

## 5. Key Components

### PieChart (components/pie_chart.py)

python
import reflex as rx
from reflex_chartjs import Pie

class PieChart(rx.Component):
    def __init__(self, data: dict[str,int]):
        super().__init__()
        self.data = data

    def render(self):
        return Pie(
          data={
            "labels": list(self.data.keys()),
            "datasets": [{
               "data": list(self.data.values()),
               "backgroundColor": [c.color for c in rx.app.state.categories]
            }]
          }
        )


### CategoryRibbon (components/category_ribbon.py)

python
import reflex as rx

class CategoryRibbon(rx.Component):
    def render(self):
        return rx.HStack(
          *[
            rx.Box(cat.name, bg=cat.color, px=3, py=1, rounded="xl", key=cat.id)
            for cat in rx.app.state.categories
          ],
          spacing=2, overflow_x="auto"
        )


### EntryForm (components/entry_form.py)

python
import reflex as rx
from components import CategoryRibbon

class EntryForm(rx.Component):
    def render(self):
        return rx.VStack(
          *[
            rx.HStack(
              rx.Select(
                options=[(c.name, c.id) for c in rx.app.state.categories],
                on_change=lambda e, idx=i: rx.app.update_entry_category(idx, e.target.value)
              ),
              rx.Input(type="number", placeholder="Value",
                       on_change=lambda e, idx=i: rx.app.update_entry_value(idx, e.target.value)),
              rx.Input(type="datetime-local",
                       on_change=lambda e, idx=i: rx.app.update_entry_timestamp(idx, e.target.value)),
              rx.Button("Remove", on_click=lambda _, idx=i: rx.app.remove_entry(idx))
            )
            for i in range(len(rx.app.state.entries))
          ],
          rx.Button("Add Another", on_click=lambda _: rx.app.append_empty_entry()),
          spacing=2
        )


*(Use AppState actions to manage entries list and updates.)*

---

## 6. Pages & Routing (app.py)

python
import reflex as rx
from state import AppState

app = rx.App(state=AppState)
app.add_page(AppState.login_page,    route="/login",    auth=False)
app.add_page(AppState.dashboard_page,route="/",        auth=True)
app.add_page(AppState.overview_page, route="/overview",auth=True)
app.add_page(AppState.settings_page, route="/settings",auth=True)
app.compile()


**Page layout example**:

python
class AppState:
    @staticmethod
    def dashboard_page():
        return rx.VStack(
          PieChart(data=...), 
          CategoryRibbon(), 
          EntryForm(), 
          ActivityTable()
        )


---

## 7. Authentication

* Decorate login action:

  
python
  @rx.auth.login
  def login(self, username, password): ...

* Protect pages:

  
python
  @rx.auth.protected
  def dashboard_page(self): ...

* Store user in state; auto‑redirect to /login if not authenticated.

---

## 8. Feature Expectations

* **Pie Chart** + text summary on Home
* **“Today” Quick View** auto‑loads today’s entries
* **Category Ribbon** (scrollable colored strips)
* **Activity Table** with Goal / Actual / Deficiency row
* **Overview Tab** (Faith / Health / Work breakdown)
* **Dynamic Entry Form** (add/remove rows)
* **Responsive** on mobile (Tailwind breakpoints)
* **Reusable Auth** (signup/login/logout, session persistence)