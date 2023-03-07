from dataclasses import dataclass
import dataclasses
from functools import lru_cache

import httpx
import toml


@dataclass
class PocketBaseConnection:
    pocketbase_url: str


@dataclass
class PocketBaseUser:
    token: str
    username: str
    verified: bool
    name: str

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@lru_cache(1)
def get_connection(file_path: str = ".streamlit/secrets.toml") -> PocketBaseConnection:
    creds = toml.load(file_path)
    return PocketBaseConnection(pocketbase_url=creds["pocketbase_url"])

def get_authenticated_user(username: str, password: str) -> PocketBaseUser:
    creds = get_connection()
    response = httpx.post(
        f"{creds.pocketbase_url}/api/collections/users/auth-with-password",
        json={
            "identity": username,
            "password": password,
        },
        timeout=5,
    )
    response.raise_for_status()
    auth_data = response.json()
    token = auth_data["token"]
    record = auth_data["record"]
    user = PocketBaseUser(token=token, **record)
    if not user.verified:
        raise Exception('User Not Verified in PocketBase')
    return user
