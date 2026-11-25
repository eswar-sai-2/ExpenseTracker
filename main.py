from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from auth import signup, login
from expense import ExpenseStore


# ---------------- COLORS ----------------

BG = (0.955, 0.965, 0.98, 1)
WHITE = (1, 1, 1, 1)
NAVY = (0.075, 0.14, 0.27, 1)
BLUE = (0.16, 0.36, 0.72, 1)
GREEN = (0.08, 0.57, 0.39, 1)
RED = (0.76, 0.19, 0.22, 1)
TEXT = (0.12, 0.16, 0.23, 1)
MUTED = (0.43, 0.48, 0.56, 1)
PALE = (0.91, 0.94, 0.98, 1)

CATEGORIES = (
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Health",
    "Entertainment",
    "Other"
)

Window.clearcolor = BG


# ---------------- REUSABLE WIDGETS ----------------

def label(text, size=14, color=TEXT, bold=False,
          height=None, halign="left"):

    widget = Label(
        text=str(text),
        font_size=f"{size}sp",
        color=color,
        bold=bold,
        halign=halign,
        valign="middle",
        shorten=True,
        shorten_from="right"
    )

    if height is not None:
        widget.size_hint_y = None
        widget.height = dp(height)

    widget.bind(
        size=lambda obj, value:
        setattr(obj, "text_size", (value[0], None))
    )

    return widget


def button(text, callback, color=GREEN,
           height=46, text_size=14):

    widget = Button(
        text=text,
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_down="",
        background_color=color,
        color=WHITE,
        bold=True,
        font_size=f"{text_size}sp"
    )

    widget.bind(on_release=callback)

    return widget


def field(hint, password=False, input_filter=None):

    return TextInput(
        hint_text=hint,
        password=password,
        multiline=False,
        input_filter=input_filter,
        size_hint_y=None,
        height=dp(49),
        padding=[dp(14), dp(13), dp(14), dp(10)],
        background_normal="",
        background_active="",
        background_color=WHITE,
        foreground_color=TEXT,
        hint_text_color=MUTED,
        cursor_color=BLUE,
        font_size="15sp"
    )


def card(orientation="vertical", padding=14,
         spacing=8, height=None):

    box = BoxLayout(
        orientation=orientation,
        padding=dp(padding),
        spacing=dp(spacing),
        size_hint_y=None
    )

    if height is not None:
        box.height = dp(height)

    with box.canvas.before:
        Color(*WHITE)
        box._bg = RoundedRectangle(
            pos=box.pos,
            size=box.size,
            radius=[dp(16)]
        )

    box.bind(
        pos=lambda obj, value:
        setattr(obj._bg, "pos", value),
        size=lambda obj, value:
        setattr(obj._bg, "size", value)
    )

    return box


# =====================================================
#                    MAIN APP
# =====================================================

class ExpenseTrackerApp(App):

    def build(self):

        self.title = "Expense Tracker"
        self.store = None
        self.email = ""

        self.manager = ScreenManager(
            transition=NoTransition()
        )

        self.auth_screen = Screen(name="auth")
        self.dashboard_screen = Screen(name="dashboard")

        self.manager.add_widget(self.auth_screen)
        self.manager.add_widget(self.dashboard_screen)

        self.show_auth()

        return self.manager

    # =================================================
    #                 AUTHENTICATION
    # =================================================

    def show_auth(self, message="", success=False):

        self.auth_screen.clear_widgets()

        # Scrollable login screen
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(3)
        )

        page = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            padding=[
                dp(20),
                dp(24),
                dp(20),
                dp(24)
            ],
            spacing=dp(12)
        )

        page.bind(minimum_height=page.setter("height"))

        # Heading
        page.add_widget(
            label(
                "EXPENSE TRACKER",
                13,
                BLUE,
                True,
                28,
                "center"
            )
        )

        page.add_widget(
            label(
                "Welcome back",
                28,
                NAVY,
                True,
                42,
                "center"
            )
        )

        page.add_widget(
            label(
                "Sign in to track your spending",
                14,
                MUTED,
                False,
                30,
                "center"
            )
        )

        # Login form
        form = card(
            padding=18,
            spacing=11
        )

        form.size_hint_x = 1
        form.height = dp(390)

        form.add_widget(
            label(
                "Email address",
                13,
                TEXT,
                True,
                22
            )
        )

        self.email_input = field("Enter your email")
        form.add_widget(self.email_input)

        form.add_widget(
            label(
                "Password",
                13,
                TEXT,
                True,
                22
            )
        )

        # Password row
        password_row = BoxLayout(
            size_hint_y=None,
            height=dp(49),
            spacing=dp(6)
        )

        self.password_input = field(
            "Enter your password",
            password=True
        )

        password_row.add_widget(self.password_input)

        self.password_toggle = button(
            "Show",
            self.toggle_password,
            PALE,
            49,
            12
        )

        self.password_toggle.size_hint_x = None
        self.password_toggle.width = dp(64)
        self.password_toggle.color = NAVY

        password_row.add_widget(self.password_toggle)

        form.add_widget(password_row)

        # Status message
        self.auth_status = label(
            message,
            12,
            GREEN if success else RED,
            False,
            42,
            "center"
        )

        form.add_widget(self.auth_status)

        # Login
        form.add_widget(
            button(
                "LOGIN",
                self.do_login,
                BLUE,
                47
            )
        )

        # Signup
        form.add_widget(
            button(
                "CREATE ACCOUNT",
                self.do_signup,
                GREEN,
                47
            )
        )

        page.add_widget(form)

        # Footer
        page.add_widget(
            label(
                "Your expenses are private to your account.",
                12,
                MUTED,
                False,
                40,
                "center"
            )
        )

        scroll.add_widget(page)

        self.auth_screen.add_widget(scroll)

        self.manager.current = "auth"

    def toggle_password(self, *_):

        self.password_input.password = (
            not self.password_input.password
        )

        self.password_toggle.text = (
            "Show"
            if self.password_input.password
            else "Hide"
        )

    def auth_values(self):

        email = self.email_input.text.strip()
        password = self.password_input.text

        if not email or not password:
            raise ValueError(
                "Please enter your email and password."
            )

        if len(password) < 6:
            raise ValueError(
                "Password must be at least 6 characters."
            )

        return email, password

    def do_signup(self, *_):

        try:

            email, password = self.auth_values()

            result = signup(email, password)

            if result.get("access_token"):

                self.start_session(result, email)

            else:

                self.auth_status.text = (
                    "Account created. You can now log in."
                )

                self.auth_status.color = GREEN

        except Exception as exc:

            self.auth_status.text = str(exc)
            self.auth_status.color = RED

    def do_login(self, *_):

        try:

            email, password = self.auth_values()

            result = login(email, password)

            self.start_session(result, email)

        except Exception as exc:

            self.auth_status.text = str(exc)
            self.auth_status.color = RED

    def start_session(self, result, email):

        token = result.get("access_token")

        if not token:

            self.auth_status.text = (
                "No access token received. Please log in again."
            )

            return

        try:

            self.store = ExpenseStore(token)
            self.email = email

            self.store.load_expenses()

            self.show_dashboard()

        except Exception as exc:

            self.store = None

            self.auth_status.text = (
                f"Could not load your expenses: {exc}"
            )

            self.auth_status.color = RED

    # =================================================
    #                    DASHBOARD
    # =================================================

    def show_dashboard(self):

        self.dashboard_screen.clear_widgets()

        outer = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(12)],
            spacing=dp(10)
        )

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )

        title_box = BoxLayout(
            orientation="vertical",
            spacing=0
        )

        title_box.add_widget(
            label(
                "My expenses",
                23,
                NAVY,
                True,
                29
            )
        )

        title_box.add_widget(
            label(
                self.email,
                10,
                MUTED,
                False,
                17
            )
        )

        header.add_widget(title_box)

        header.add_widget(
            button(
                "LOG OUT",
                self.logout,
                NAVY,
                38,
                11
            )
        )

        outer.add_widget(header)

        # Scrollable dashboard
        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        content = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None,
            padding=[0, dp(2), 0, dp(12)]
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Total spending card
        summary = card(
            padding=17,
            spacing=5,
            height=132
        )

        with summary.canvas.before:
            Color(*NAVY)

            summary._bg = RoundedRectangle(
                pos=summary.pos,
                size=summary.size,
                radius=[dp(18)]
            )

        summary.bind(
            pos=lambda obj, value:
            setattr(obj._bg, "pos", value),
            size=lambda obj, value:
            setattr(obj._bg, "size", value)
        )

        summary.add_widget(
            label(
                "TOTAL SPENDING",
                11,
                (0.78, 0.85, 0.96, 1),
                True,
                22
            )
        )

        self.total_label = label(
            "₹0.00",
            30,
            WHITE,
            True,
            43
        )

        summary.add_widget(self.total_label)

        self.count_label = label(
            "0 expenses",
            12,
            (0.84, 0.89, 0.96, 1),
            False,
            22
        )

        summary.add_widget(self.count_label)

        content.add_widget(summary)

        # Add expense card
        add_card = card(
            padding=14,
            spacing=9
        )

        add_card.bind(
            minimum_height=add_card.setter("height")
        )

        add_card.add_widget(
            label(
                "Add an expense",
                17,
                NAVY,
                True,
                28
            )
        )

        self.amount_input = field(
            "Amount in ₹",
            input_filter="float"
        )

        self.category_input = Spinner(
            text="Choose category",
            values=CATEGORIES,
            size_hint_y=None,
            height=dp(47),
            background_normal="",
            background_color=PALE,
            color=TEXT,
            font_size="14sp"
        )

        self.description_input = field(
            "Description (optional)"
        )

        add_card.add_widget(self.amount_input)
        add_card.add_widget(self.category_input)
        add_card.add_widget(self.description_input)

        add_card.add_widget(
            button(
                "+  ADD EXPENSE",
                self.add_expense,
                GREEN,
                45
            )
        )

        self.dashboard_status = label(
            "",
            11,
            RED,
            False,
            25
        )

        add_card.add_widget(self.dashboard_status)

        content.add_widget(add_card)

        # Category summary
        cat_card = card(
            padding=14,
            spacing=7
        )

        cat_card.bind(
            minimum_height=cat_card.setter("height")
        )

        cat_card.add_widget(
            label(
                "Spending by category",
                16,
                NAVY,
                True,
                27
            )
        )

        self.category_summary = label(
            "No spending recorded yet.",
            12,
            MUTED,
            False,
            42
        )

        cat_card.add_widget(self.category_summary)

        content.add_widget(cat_card)

        # Recent expenses
        content.add_widget(
            label(
                "Recent expenses",
                17,
                NAVY,
                True,
                30
            )
        )

        self.rows = GridLayout(
            cols=1,
            spacing=dp(8),
            size_hint_y=None
        )

        self.rows.bind(
            minimum_height=self.rows.setter("height")
        )

        content.add_widget(self.rows)

        scroll.add_widget(content)

        outer.add_widget(scroll)

        self.dashboard_screen.add_widget(outer)

        self.manager.current = "dashboard"

        self.refresh_dashboard()

    # =================================================
    #                  ADD EXPENSE
    # =================================================

    def add_expense(self, *_):

        try:

            raw_amount = self.amount_input.text.strip()
            category = self.category_input.text

            if not raw_amount:
                raise ValueError(
                    "Please enter an amount."
                )

            if category == "Choose category":
                raise ValueError(
                    "Please choose a category."
                )

            amount = float(raw_amount)

            if amount <= 0:
                raise ValueError(
                    "Amount must be greater than zero."
                )

            self.store.add_expense(
                amount,
                category,
                self.description_input.text.strip()
            )

            self.amount_input.text = ""
            self.description_input.text = ""

            self.category_input.text = "Choose category"

            self.dashboard_status.text = (
                "Expense added successfully."
            )

            self.dashboard_status.color = GREEN

            self.refresh_dashboard()

        except Exception as exc:

            self.dashboard_status.text = str(exc)
            self.dashboard_status.color = RED

    # =================================================
    #                 REFRESH DASHBOARD
    # =================================================

    def refresh_dashboard(self):

        if not self.store:
            return

        try:

            self.store.load_expenses()

            items = self.store.expenses

            self.total_label.text = (
                f"₹{self.store.calculate_total():,.2f}"
            )

            self.count_label.text = (
                f"{len(items)} expense record(s)"
            )

            totals = self.store.category_totals()

            if totals:

                self.category_summary.text = "\n".join(
                    f"•  {name}: ₹{value:,.2f}"
                    for name, value in sorted(
                        totals.items(),
                        key=lambda x: -x[1]
                    )
                )

                self.category_summary.height = dp(
                    min(140, 25 * len(totals) + 8)
                )

            else:

                self.category_summary.text = (
                    "No spending recorded yet."
                )

                self.category_summary.height = dp(35)

            self.rows.clear_widgets()

            if not items:

                empty = card(
                    padding=14,
                    height=72
                )

                empty.add_widget(
                    label(
                        "No expenses yet. Add your first expense above.",
                        12,
                        MUTED,
                        False,
                        42,
                        "center"
                    )
                )

                self.rows.add_widget(empty)

            else:

                for item in items:
                    self.add_expense_row(item)

        except Exception as exc:

            self.dashboard_status.text = (
                f"Could not refresh: {exc}"
            )

            self.dashboard_status.color = RED

    # =================================================
    #                EXPENSE ROWS
    # =================================================

    def add_expense_row(self, item):

        row = card(
            padding=11,
            spacing=5
        )

        row.bind(
            minimum_height=row.setter("height")
        )

        top = BoxLayout(
            size_hint_y=None,
            height=dp(27),
            spacing=dp(6)
        )

        top.add_widget(
            label(
                item.get("category", "Other"),
                14,
                NAVY,
                True,
                25
            )
        )

        top.add_widget(
            label(
                f"₹{float(item.get('amount', 0)):,.2f}",
                14,
                GREEN,
                True,
                25,
                "right"
            )
        )

        row.add_widget(top)

        desc = item.get("description") or "No description"

        row.add_widget(
            label(
                desc,
                11,
                MUTED,
                False,
                23
            )
        )

        actions = BoxLayout(
            size_hint_y=None,
            height=dp(34),
            spacing=dp(8)
        )

        actions.add_widget(
            button(
                "EDIT",
                lambda *_args, data=item:
                self.edit_expense(data),
                BLUE,
                32,
                11
            )
        )

        actions.add_widget(
            button(
                "DELETE",
                lambda *_args, data=item:
                self.confirm_delete(data),
                RED,
                32,
                11
            )
        )

        row.add_widget(actions)

        self.rows.add_widget(row)

    # =================================================
    #                   EDIT EXPENSE
    # =================================================

    def edit_expense(self, item):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(9)
        )

        amount = field(
            "Amount",
            input_filter="float"
        )

        amount.text = str(item.get("amount", ""))

        category = Spinner(
            text=item.get("category", "Other"),
            values=CATEGORIES,
            size_hint_y=None,
            height=dp(46),
            color=TEXT,
            background_normal="",
            background_color=PALE
        )

        description = field(
            "Description (optional)"
        )

        description.text = (
            item.get("description") or ""
        )

        status = label(
            "",
            11,
            RED,
            False,
            25
        )

        popup = Popup(
            title="Edit expense",
            content=box,
            size_hint=(0.88, None),
            height=dp(310),
            auto_dismiss=False
        )

        box.add_widget(amount)
        box.add_widget(category)
        box.add_widget(description)
        box.add_widget(status)

        actions = BoxLayout(
            size_hint_y=None,
            height=dp(44),
            spacing=dp(8)
        )

        actions.add_widget(
            button(
                "CANCEL",
                lambda *_: popup.dismiss(),
                MUTED,
                42,
                11
            )
        )

        def save(*_):

            try:

                value = float(amount.text)

                if value <= 0:
                    raise ValueError(
                        "Amount must be greater than zero."
                    )

                self.store.update_expense(
                    item["id"],
                    value,
                    category.text,
                    description.text.strip()
                )

                popup.dismiss()

                self.refresh_dashboard()

            except Exception as exc:

                status.text = str(exc)

        actions.add_widget(
            button(
                "SAVE",
                save,
                GREEN,
                42,
                11
            )
        )

        box.add_widget(actions)

        popup.open()

    # =================================================
    #                  DELETE EXPENSE
    # =================================================

    def confirm_delete(self, item):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )

        box.add_widget(
            label(
                "Are you sure you want to delete this expense?",
                14,
                TEXT,
                False,
                55,
                "center"
            )
        )

        actions = BoxLayout(
            size_hint_y=None,
            height=dp(46),
            spacing=dp(9)
        )

        popup = Popup(
            title="Confirm deletion",
            content=box,
            size_hint=(0.86, None),
            height=dp(175),
            auto_dismiss=False
        )

        actions.add_widget(
            button(
                "CANCEL",
                lambda *_: popup.dismiss(),
                MUTED,
                43,
                11
            )
        )

        def delete_now(*_):

            try:

                self.store.delete_expense(item["id"])

                popup.dismiss()

                self.dashboard_status.text = (
                    "Expense deleted."
                )

                self.dashboard_status.color = GREEN

                self.refresh_dashboard()

            except Exception as exc:

                popup.dismiss()

                self.dashboard_status.text = (
                    f"Delete failed: {exc}"
                )

                self.dashboard_status.color = RED

        actions.add_widget(
            button(
                "DELETE",
                delete_now,
                RED,
                43,
                11
            )
        )

        box.add_widget(actions)

        popup.open()

    # =================================================
    #                      LOGOUT
    # =================================================

    def logout(self, *_):

        self.store = None
        self.email = ""

        self.show_auth(
            "You have logged out successfully.",
            success=True
        )


# =====================================================
#                    RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    ExpenseTrackerApp().run()