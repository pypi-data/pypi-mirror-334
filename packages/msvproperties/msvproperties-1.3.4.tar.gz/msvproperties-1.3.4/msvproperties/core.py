import json
from .config import get_config
from .process import ProcessLogic


class Lead:
    def __init__(self, session):
        _, base_url, _, _ = get_config()
        self.base_url = base_url
        self.auth_session = session
        session.authenticate()

    def insert(self, data):
        url = f"{self.base_url}/api/leads/"
        result, status = ProcessLogic(data, self.auth_session,force=data.force).start()
        if result:
            response = self.auth_session.make_authenticated_request(
                url, method="POST", data=json.dumps(data.model_dump())
            )
            print(response)
        else:
            print(status)
