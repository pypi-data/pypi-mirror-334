import requests
from urllib.parse import urlencode


# please write down your code below.



API_URL_ROOT: str = "http://127.0.0.1:8000/"


async def api_get_info(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/info/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    return response


async def api_signin(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/signin/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    return response


async def api_signout(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/signout/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    return response


async def api_signup(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/signup/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    return response


async def api_delete_account(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/delete/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.delete(url=url,
                             headers=headers,
                             json=data)

    return response


async def api_get_image(data=None):
    url = f"{API_URL_ROOT}api/v1/accounts/image/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.get(url=url,
                            headers=headers,
                            json=data)
    return response


async def api_update_location(data:dict):
    url = f"{API_URL_ROOT}api/v1/accounts/upload_geo/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    return response