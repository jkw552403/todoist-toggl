# Alfred workflow to integrate Todoist with Toggl Track

Simply show Todoist tasks and start Toggl Track time entries like [this integration](https://todoist.com/help/articles/use-toggl-track-with-todoist).

## How to install
Go to [release page](https://github.com/jkw552403/todoist-/releases), download the workflow, and open it on your Mac.

## Usage
- `tt:setting`: Set Todoist token and Toggl token
- `ttt`: Show Today tasks (similar to Todoist Today view).
- `tto`: Show running Toggl entry and you can click `Return` to stop it.
- In the task list,
  - You can select a task and complete it with `Command` + `Return`.
  - You can select a task and start tracking it with `Option` + `Return`. The time entry will use the same project name as the Todoist task if the project exists in Toggl.

## TODO
- [ ] Support refresh Todoist tasks manually
- [ ] Support searching by project names, labels, or filters.
- [ ] Upload to Packal

## Install Python libraries for development
```bash
# Python libraries are put to build/ directory
pip install --target=build -r requirements.txt
```

## Test for Toggl API client
A simple test case is written for Toggl APIs:
```bash
# replace the token below and make sure
API_TOKEN=XXXXXX /usr/bin/python test_toggl_client.py
```
The test will create/start a new time entry, end it, and delete it.
