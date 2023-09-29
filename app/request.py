import requests

from app import database


def get(url: str, headers=None):
    if not headers:
        default_headers = {
            'Content-Type': 'application/json'
        }
        headers = default_headers

    resp = requests.get(
        url=url, headers=headers
    )

    return resp


def post(url: str, data, headers=None):
    if not headers:
        default_headers = {
            'Content-Type': 'application/json',
            'x-csrf-token': database.oncall_user.csrf_token,
            'Cookie': f'oncall-auth={database.oncall_cookie_auth}'
        }
        headers = default_headers

    resp = requests.post(
        url=url, headers=headers, data=data
    )

    return resp


def put(url: str, data, headers=None):
    if not headers:
        default_headers = {
            'Content-Type': 'application/json',
        }
        headers = default_headers

    resp = requests.put(
        url=url, headers=headers, data=data
    )

    return resp
