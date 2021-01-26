# encoding: utf-8
import sys

import click
from common import create_todoist_sync_client, get_todoist_state
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
    sync_client = create_todoist_sync_client()
    todoist_state = get_todoist_state(wf, sync_client)
    item = next(item for item in todoist_state["items"] if item["id"] == task_id)
    if track:
        # TODO
        # 1. Get item name and use it for time entry description
        # 2. Get project name and try to map it to Toggl project
        #    If project with the same name exists, set pid to this project ID
        #    Else, pid = None
        # Update notify message to show tracking project
        notify(u"Start tracking", item[u"content"])
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
