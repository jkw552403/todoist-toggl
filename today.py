# encoding: utf-8
import sys
from datetime import datetime, timedelta

import click
from common import (
    add_task_item,
    create_todoist_sync_client,
    get_todoist_state,
    parse_todoist_date,
)
from setting import TODOIST_API_TOKEN
from workflow import Workflow3

log = None
wf = None


def overdue_today(due_dt):
    if due_dt:
        return due_dt < datetime.today().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
    return False


def due_today(due_dt):
    if due_dt:
        return due_dt.date() == datetime.today().date()
    return False


@click.command()
def cli():
    sync_client = create_todoist_sync_client(wf.settings[TODOIST_API_TOKEN])
    todoist_state = get_todoist_state(wf, sync_client)
    items = todoist_state["items"]
    log.debug("There are {} tasks".format(len(items)))
    task_data = []
    for task in items:
        due = task["due"]
        due_date = due.get("date", None) if due else None
        due_dt = parse_todoist_date(due_date) if due else None
        if (
            overdue_today(due_dt)
            and task["is_deleted"] == 0
            and task["date_completed"] is None
        ):
            # Add values for sorting tasks
            task_data.append(
                (
                    due_today(due_dt),  # due before today will be shown at the top
                    -len(
                        due_date
                    ),  # longer due date means the due date has not only date but time
                    due_dt,
                    task["priority"],
                    task["day_order"],
                    task,
                )
            )
    log.debug("Get {} tasks in Today view".format(len(task_data)))
    log.debug("Task data: {}".format(task_data))
    task_data.sort()
    for t in task_data:
        add_task_item(wf, sync_client, t[-1])
    wf.send_feedback()


def main(wf):
    cli()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
