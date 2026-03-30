from playwright.sync_api import APIRequestContext, APIResponse


class ApiResponseError(RuntimeError):
    pass


def ensure_ok(response: APIResponse, action: str) -> None:
    if response.ok:
        return

    body = response.text()
    raise ApiResponseError(
        f"{action} failed with status {response.status}.\n"
        f"URL: {response.url}\n"
        f"Response: {body}"
    )


def post_form(
    request_context: APIRequestContext,
    endpoint: str,
    data: dict,
    action: str,
) -> dict:
    response = request_context.post(endpoint, multipart=data)
    ensure_ok(response, action)
    return response.json()


def post_json(
    request_context: APIRequestContext,
    endpoint: str,
    payload: dict,
    action: str,
) -> dict:
    response = request_context.post(endpoint, data=payload)
    ensure_ok(response, action)
    return response.json()

