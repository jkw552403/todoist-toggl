from urlparse import urljoin

import requests

TOGGL_CLIENT_NAME = "todoist-toggl"


class TogglClient:
    """
    Simple wrapper for Toggl API
    """

    API_ENDPOINT = "https://api.track.toggl.com/api/v8/"

    def __init__(self, api_token):
        self.api_token = api_token
        self.state = None

    @property
    def auth(self):
        """
        Pack auth info as a tuple for requests
        """
        return (self.api_token, "api_token")

    def sync(self):
        """
        Get all the connected data of the user from the API
        See https://github.com/toggl/toggl_api_docs/blob/50ca982bba5eb41d1f852cc67e6ca903875524f9/chapters/users.md
        """
        res = requests.get(
            urljoin(self.API_ENDPOINT, "me"),
            params={"with_related_data": "true"},
            auth=self.auth,
        )
        res.raise_for_status()
        self.state = res.json()["data"]
        return self.state

    def get_projects(self):
        if self.state is None:
            self.sync()
        return self.state["projects"]

    def start_time_entry(self, description, pid=None):
        data = {
            "time_entry": {
                "description": description,
                "created_with": TOGGL_CLIENT_NAME,
            }
        }
        if pid:
            data["time_entry"]["pid"] = pid
        res = requests.post(
            urljoin(self.API_ENDPOINT, "time_entries/start"), json=data, auth=self.auth,
        )
        res.raise_for_status()
        return res.json()["data"]

    def end_time_entry(self, time_entry_id):
        res = requests.put(
            urljoin(self.API_ENDPOINT, "time_entries/{}/stop".format(time_entry_id)),
            auth=self.auth,
        )
        res.raise_for_status()
        return res.json()["data"]

    def get_current_time_entry(self):
        res = requests.get(
            urljoin(self.API_ENDPOINT, "time_entries/current"), auth=self.auth
        )
        res.raise_for_status()
        return res.json()["data"]

    def delete_time_entry(self, time_entry_id):
        res = requests.delete(
            urljoin(self.API_ENDPOINT, "time_entries/{}".format(time_entry_id)),
            auth=self.auth,
        )
        res.raise_for_status()
