# encoding: utf-8
import sys

import click
from workflow.notify import notify

from common import create_workflow

log = None
wf = None


TODOIST_API_TOKEN = "TODOIST_API_TOKEN"
TOGGL_API_TOKEN = "TOGGL_API_TOKEN"


VARIABLES = {
    # variable name: (title, default value)
    TODOIST_API_TOKEN: ("Set Todoist API token", ""),
    TOGGL_API_TOKEN: ("Set Toggl API token", ""),
}


@click.option("--set-variable-value", envvar="SET_VARIABLE_VALUE")
@click.option("--set-variable-name", envvar="SET_VARIABLE_NAME")
@click.argument("query", required=False)
@click.command()
def cli(query, set_variable_name, set_variable_value):
    if set_variable_name and set_variable_value:
        # Set the value to workflow setting
        wf.settings[set_variable_name] = set_variable_value
        title = VARIABLES[set_variable_name][0]
        notify("{} successfully".format(title))
    elif set_variable_name:
        # Show only one item when the user selects
        title, default_value = VARIABLES[set_variable_name]
        current_value = wf.settings.get(set_variable_name, default_value)
        item = wf.add_item(
            title=title, valid=True, subtitle="Current value: {}".format(current_value)
        )
        item.setvar("SET_VARIABLE_NAME", set_variable_name)
        item.setvar("SET_VARIABLE_VALUE", query)
        wf.send_feedback()
    else:
        # Show all possible variables
        if query:
            variables = wf.filter(query, VARIABLES.items(), key=lambda item: item[1][0])
        else:
            variables = VARIABLES.items()
        for variable_name, (title, default_value) in variables:
            current_value = wf.settings.get(variable_name, default_value)
            item = wf.add_item(
                title=title,
                valid=True,
                subtitle="Current value: {}".format(current_value),
            )
            item.setvar("SET_VARIABLE_NAME", variable_name)
            item.setvar("VARIABLE_CURRENT_VALUE", current_value)
        wf.send_feedback()


def main(wf):
    cli()


if __name__ == u"__main__":
    wf = create_workflow()
    log = wf.logger
    sys.exit(wf.run(main))
