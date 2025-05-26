import reflex as rx
from typing import Dict


class AuthState(rx.State):
    users: Dict[str, str] = {
        "admin@reflex.com": "password123"
    }
    in_session: bool = True
    logged_in_user_email: str | None = "admin@reflex.com"

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast.error(
                "Email and password are required."
            )
            return
        if email in self.users:
            yield rx.toast.error("Email already in use.")
        else:
            self.users[email] = password
            self.in_session = True
            self.logged_in_user_email = email
            yield rx.toast.success(
                "Account created successfully!"
            )
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast.error(
                "Email and password are required."
            )
            return
        if (
            email in self.users
            and self.users[email] == password
        ):
            self.in_session = True
            self.logged_in_user_email = email
            yield rx.toast.success(
                "Signed in successfully!"
            )
            return rx.redirect("/")
        else:
            self.in_session = False
            self.logged_in_user_email = None
            yield rx.toast.error(
                "Invalid email or password."
            )

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.logged_in_user_email = None
        yield rx.toast.info("Signed out successfully.")
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/sign-in")