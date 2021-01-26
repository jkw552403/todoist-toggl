# Alfred workflow to integrate todoist with toggle

## Install Python libraries to the project
```
# If you don't want to install to the project root during development,
# you can change the target directory below. But remember to include dependencies when you create Alfreda package and add your target to PYTHONPATH when testing
pip install --target=. -r requirements.txt
```

## Test for Toggl API client
A simple test case is written for Toggl APIs:
```bash
# replace the token below and make sure
API_TOKEN=XXXXXX /usr/bin/python test_toggl_client.py
```
The test will create/start a new time entry, end it, and delete it.
