# encoding: utf-8
from datetime import datetime

import todoist


def create_todoist_sync_client(api_token):
    return todoist.TodoistAPI(token=api_token)


def parse_todoist_date(date_string):
    if len(date_string) == 10:
        return datetime.strptime(date_string, "%Y-%m-%d")
    else:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")


def add_task_item(wf, sync_client, task):
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
