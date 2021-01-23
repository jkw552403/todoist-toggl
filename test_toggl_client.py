import os
import unittest
from unittest import TestCase

from toggle_client import TogglClient


class TestTogglClient(TestCase):

    API_TOKEN = "foobar"

    def setUp(self):
        self.toggl_client = TogglClient(api_token=self.API_TOKEN)
        self.test_time_entry_id = None

    def test_client(self):
        # Sync and see if projects exist in the returned data
        state = self.toggl_client.sync()
        assert "projects" in state
        # Check get_projects
        projects = self.toggl_client.get_projects()
        self.assertListEqual(state["projects"], projects)
        # Start a time entry
        entry = self.toggl_client.start_time_entry("foobar")
        assert "id" in entry
        # Get the current entry
        current = self.toggl_client.get_current_time_entry()
        # Somehow the formats of the "start" field from two endpoints are different
        # Just compare IDs here
        assert entry["id"] == current["id"]
        # Stop and delete the test time entry
        self.toggl_client.end_time_entry(entry["id"])
        self.toggl_client.delete_time_entry(entry["id"])


if __name__ == "__main__":
    TestTogglClient.API_TOKEN = os.environ["API_TOKEN"]
    unittest.main()
