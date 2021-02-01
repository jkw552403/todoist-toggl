# encoding: utf-8
import sys

import click
from workflow.notify import notify

from common import create_toggl_client, create_workflow
from setting import TOGGL_API_TOKEN

log = None
wf = None


@click.option(
    "--stop",
    type=int,
    default=None,
    help="This value is the ID of the entry the user wants to stop",
)
@click.command()
def cli(stop):
    toggl_client = create_toggl_client(wf.settings[TOGGL_API_TOKEN])
    if stop:
        log.debug(u"Stop the current entry {}".format(stop))
        toggl_client.end_time_entry(stop)
        notify(u"Stop the current entry")
    else:
        log.debug("View the current entry")
        current_entry = toggl_client.get_current_time_entry()
        log.debug(u"Current entry: {}".format(current_entry))
        if current_entry:
            item = wf.add_item(
                title=u"Current entry: {}".format(current_entry["description"]),
                subtitle=u"Press CMD + Enter to stop this entry",
                valid=False,
            )
            item.add_modifier(
                "cmd",
                subtitle="Stop this entry",
                valid=True,
                arg="--stop {}".format(current_entry["id"]),
            )
        else:
            wf.add_item("There is no running entry")
        wf.send_feedback()


def main(wf):
    cli()


if __name__ == u"__main__":
    wf = create_workflow()
    log = wf.logger
    sys.exit(wf.run(main))
