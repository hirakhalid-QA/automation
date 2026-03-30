from playwright.sync_api import APIRequestContext

from modules.http import post_form


def login(request_context: APIRequestContext, email: str, password: str) -> dict:
    payload = {
        "email": email,
        "password": password,
    }
    return post_form(
        request_context=request_context,
        endpoint="/api/accounts/login/",
        data=payload,
        action="Login API",
    )

