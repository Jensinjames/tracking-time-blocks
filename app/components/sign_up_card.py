import reflex as rx
from app.states.auth_state import AuthState


def sign_up_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Create an account",
                class_name="text-2xl font-bold tracking-tight text-gray-900",
            ),
            rx.el.p(
                "Enter your email and password to create your account.",
                class_name="text-sm text-gray-600",
            ),
            class_name="flex flex-col items-center text-center mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email",
                    html_for="email",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="email",
                    placeholder="user@example.com",
                    id="email",
                    name="email",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    html_for="password",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Create Account",
                type="submit",
                class_name="w-full bg-green-600 text-white font-semibold py-2.5 px-4 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors",
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account?",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.a(
                    "Sign in",
                    href="/sign-in",
                    class_name="ml-1 text-sm text-blue-600 hover:text-blue-700 font-medium underline",
                ),
                class_name="mt-6 text-center",
            ),
            on_submit=AuthState.sign_up,
            prevent_default=True,
            class_name="w-full",
        ),
        class_name="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-xl border border-gray-200",
    )