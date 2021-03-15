# encoding: utf-8
from datetime import datetime

import todoist
from workflow import ICON_INFO, Workflow3

from toggl_client import TogglClient

__version__ = "0.1.0"

################
# Alfred utilities
################


def create_workflow():
    wf = Workflow3(
        update_settings={
            "github_slug": "jkw552403/todoist-toggl",
            "version": __version__,
        }
    )
    # Copied from https://www.deanishe.net/alfred-workflow/guide/update.html
    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item(
            "New version available",
            "Action this item to install the update",
            autocomplete="workflow:update",
            icon=ICON_INFO,
        )
    return wf


################
# Todoist utilities
################

TODOIST_STATE_NAME = "todoist_state"
TODOIST_STATE_MAX_AGE = 600


def create_todoist_sync_client(api_token):
    return todoist.TodoistAPI(token=api_token)


def parse_todoist_date(date_string):
    """
    Parse date string from Todoist APIs responses.
    """
    if len(date_string) == 10:
        return datetime.strptime(date_string, "%Y-%m-%d")
    else:
        return datetime.strptime(date_string.strip("Z"), "%Y-%m-%dT%H:%M:%S")


def get_todoist_state(wf, sync_client):
    """
    Return todoist state from workflow cache if the state exists and is not outdated.
    Otherwise, use Todoist sync API to retrieve the latest state.
    """
    if (
        wf.cached_data(TODOIST_STATE_NAME) is None
        or wf.cached_data_age(TODOIST_STATE_NAME) > TODOIST_STATE_MAX_AGE
    ):
        wf.logger.debug("Start syncing with Todoist...")
        sync_client.sync()
        state = sync_client.state
        wf.cache_data(TODOIST_STATE_NAME, state)
    else:
        wf.logger.debug("Use cached Todoist state")
        state = wf.cached_data(TODOIST_STATE_NAME)
    return state


def add_task_item(wf, sync_client, task):
    """
    Create Alfred item for a Todoist task.
    """
    # project map for showing names in results
    project_id_map = {pro["id"]: pro for pro in sync_client.state["projects"]}
    item = wf.add_item(
        title=task["content"],
        arg=str(task["id"]),
        subtitle=u"#{}".format(project_id_map[task["project_id"]]["name"]),
        valid=False,
    )
    # Add modifier for completion
    item.add_modifier(
        "cmd",
        subtitle="Complete this task",
        valid=True,
        arg="--complete {}".format(task["id"]),
    )
    # Add modifier for tracking
    item.add_modifier(
        "alt",
        subtitle="Start tracking",
        valid=True,
        arg="--track {}".format(task["id"]),
    )


################
# Toggl utilities
################

TOGGL_PROJECT_MAP_MAX_AGE = 86400
TOGGL_PROJECT_MAP_NAME = "toggl_project_map"


def create_toggl_client(api_token):
    return TogglClient(api_token)


def get_toggl_project_map(wf, toggl_client):
    """
    This function returns a dictionary mapping project names back to IDs.
    """
    if (
        wf.cached_data(TOGGL_PROJECT_MAP_NAME) is None
        or wf.cached_data_age(TOGGL_PROJECT_MAP_NAME) > TOGGL_PROJECT_MAP_MAX_AGE
    ):
        wf.logger.debug("Get project data from Toggl API...")
        projects = toggl_client.get_projects()
        project_map = {}
        for project in projects:
            project_map[project["name"]] = project["id"]
        wf.cache_data(TOGGL_PROJECT_MAP_NAME, project_map)
    else:
        wf.logger.debug("Use cached project data")
        project_map = wf.cached_data(TOGGL_PROJECT_MAP_NAME)
    return project_map
