from .config import get_config
from .logger import ProcessLogger
import requests
from requests.exceptions import RequestException
import time


class AuthManager:
    def __init__(self, username, password):
        LOG_PATH, base_url, token_time, _ = get_config()
        self.base_url = base_url
        self.token_time = float(token_time)
        self.username = username
        self.password = password
        self.logger = ProcessLogger(LOG_PATH)
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.expiration_time = None

    def authenticate(self):
            if self.access_token and time.time() < self.expiration_time:
                return

            self.get_new_tokens()
    def get_new_tokens(self):
        if not self.base_url:
            raise ValueError("Base URL not provided.")
        token_endpoint = f"{self.base_url}/api/token/"
        response = self.session.post(
            token_endpoint,
            data={"username": self.username, "password": self.password},
        )
        response.raise_for_status()

        tokens = response.json()
        self.access_token = tokens.get("access")
        self.refresh_token = tokens.get("refresh")
        expires_in = tokens.get("expires_in", self.token_time)
        self.expiration_time = time.time() + expires_in
        self.session.get(f"{self.base_url}/api/users/get-user/")


    def refresh_access_token(self):
        try:
            refresh_token_endpoint = f"{self.base_url}/api/token/refresh/"
            response = self.session.post(
                refresh_token_endpoint,
                data={"refresh": self.refresh_token},
            )
            response.raise_for_status()

            tokens = response.json()
            self.access_token = tokens.get("access")
            self.refresh_token = tokens.get("refresh")
            self.expiration_time = time.time() + self.token_time
        except RequestException as e:
            self.logger.error(f"Failed to refresh token: {e}")
            raise Exception("Failed to refresh token.")

    def get_authenticated_session(self):
        self.authenticate()

        if time.time() >= self.expiration_time:
            self.refresh_access_token()

        return self.session

    def make_authenticated_request(self, url, method="GET", data=None):
        try:
            session = self.get_authenticated_session()
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "*/*",
            }

            if method == "GET":
                response = session.get(url, headers=headers)
            elif method == "POST":
                response = session.post(url, headers=headers, data=data)
            elif method == "PUT":
                response = session.put(url, headers=headers, data=data)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 401:
                self.logger.info("Token expired, re-authenticating...")
                self.get_new_tokens()
                return self.make_authenticated_request(url, method, data)

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise Exception(f"Request failed: {e}")
