.PHONY: clean install

PY_SCRIPTS=common.py handle_task.py setting.py today.py toggl_current.py toggl_client.py
# Please add your workflow directory here
DEST=foobar

build: requirements.txt
	pip install --target=build -r requirements.txt

install: build $(PY_SCRIPTS)
	cp -r build/* $(DEST) && cp $(PY_SCRIPTS) $(DEST)

clean:
	rm -rf build
