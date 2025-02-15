all_targets=led_ui/ tests/ deploy/

install:
	pip install .
	pip install ."[development]"
	pip install ."[micropython_deploy]"
	pip install ."[format]"
	pip install ."[lint]"
	pip install ."[test]"

lint:
	black $(all_targets)
	ruff check $(all_targets)
	mypy $(all_targets)

test:
	export PYTHONPATH=./led_ui; pytest tests/led_ui 

all: lint test

deploy-micro-cleanup-all:
	mpremote run deploy/cleanup.py

deploy-micro-common: 
	mpremote fs cp python_dummies/typing.py :typing.py 
	mpremote fs cp python_dummies/abc.py :abc.py 
	mpremote fs mkdir collections 
	mpremote fs cp python_dummies/collections/abc.py :collections/abc.py 

deploy: deploy-micro-cleanup-all deploy-micro-common
	mpremote fs mkdir led_ui 
	mpremote fs cp led_ui/base.py :led_ui/base.py 
	mpremote fs cp led_ui/logic.py :led_ui/logic.py 
	mpremote fs cp led_ui/led.py :led_ui/led.py 
	mpremote fs cp led_ui/timer.py :led_ui/timer.py 
	mpremote fs cp led_ui/button.py :led_ui/button.py 
	
	mpremote fs cp led_ui/main.py :main.py 
	mpremote reset

 