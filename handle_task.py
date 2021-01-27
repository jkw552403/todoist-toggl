# encoding: utf-8
import sys

import click
from common import (
    create_todoist_sync_client,
    create_toggl_client,
    get_todoist_state,
    get_toggl_project_map,
)
from setting import TODOIST_API_TOKEN, TOGGL_API_TOKEN
from workflow import Workflow3
from workflow.notify import notify

log = None
wf = None


@click.option("--track", is_flag=True)
@click.option("--complete", is_flag=True)
@click.argument("task_id", type=int)
@click.command()
def cli(task_id, complete, track):
    if track and complete:
        raise ValueError("Only one of track and complete can be true.")
    sync_client = create_todoist_sync_client(wf.settings[TODOIST_API_TOKEN])
    todoist_state = get_todoist_state(wf, sync_client)
    item = next(item for item in todoist_state["items"] if item["id"] == task_id)
    if track:
        # TODO
        # Get project name and try to map it to Toggl project
        todoist_project_name = next(
            (
                p["name"]
                for p in todoist_state["projects"]
                if p["id"] == item["project_id"]
            ),
            None,
        )
        toggl_client = create_toggl_client(wf.settings[TOGGL_API_TOKEN])
        toggl_project_map = get_toggl_project_map(wf, toggl_client)
        # If project with the same name exists, set pid to this project ID
        toggl_project_id = toggl_project_map.get(todoist_project_name)
        # Start a new time entry
        toggl_client.start_time_entry(item["content"], toggl_project_id)
        # Update notify message to show tracking project
        notify(
            u"Start tracking",
            "{} ({})".format(
                item["content"],
                todoist_project_name if toggl_project_id else "No Project",
            ),
        )
    if complete:
        item.complete()
        sync_client.commit()
        notify(u"Complete task", item[u"content"])


def main(wf):
    cli()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
