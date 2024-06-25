env-create:
	python3 -m venv .venv
	echo "source .venv/bin/activate"

env-compile:
	pip-compile requirements.in --output-file requirements.txt

install:
	pip3 install -r requirements.txt

run:
	python3 main.py