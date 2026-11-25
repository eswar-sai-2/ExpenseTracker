import requests
from supabase_config import SUPABASE_URL, SUPABASE_KEY

TIMEOUT = 20


def _headers():
    return {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
    }


def _read_response(response):
    try:
        result = response.json()
    except ValueError:
        result = {"message": response.text or "Unexpected server response."}

    if not response.ok:
        message = (
            result.get("msg")
            or result.get("message")
            or result.get("error_description")
            or result.get("error")
            or str(result)
        )
        raise Exception(message)
    return result


def signup(email, password):
    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/signup"
    response = requests.post(
        url,
        headers=_headers(),
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    return _read_response(response)


def login(email, password):
    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password"
    response = requests.post(
        url,
        headers=_headers(),
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    return _read_response(response)
