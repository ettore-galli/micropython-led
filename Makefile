all_targets=led/ tests/ deploy/

install:
	pip install .
	pip install .[development]
	pip install .[micropython_deploy]
	pip install .[format]
	pip install .[lint]
	pip install .[test]

lint:
	black $(all_targets)
	ruff check $(all_targets)
	mypy $(all_targets)

test:
	pytest tests 

all: lint test

deploy-cleanup-all:
	mpremote run deploy/cleanup.py

partial-deploy-warning:
	@echo ------------------------------------------------
	@echo "WARNING! Deployed only code files; cleanup and" 
	@echo "run full deploy in case of dirty files"
	@echo ------------------------------------------------

deploy-microdot:
	deploy/safe_putdir.sh microdot
	mpremote fs cp microdot/__init__.py :microdot/__init__.py 
	mpremote fs cp microdot/microdot.py :microdot/microdot.py 

deploy-data-dir:
	deploy/safe_putdir.sh data

deploy-web:
	deploy/safe_rmdir.sh web
	mpremote fs cp -r led/web :web

deploy-common: 
	mpremote fs cp python_dummies/typing.py :typing.py 
	mpremote fs cp python_dummies/abc.py :abc.py 
	mpremote fs mkdir collections 
	mpremote fs cp python_dummies/collections/abc.py :collections/abc.py 

deploy-code:
	deploy/safe_putdir.sh led
	mpremote fs cp led/base.py :led/base.py 
	mpremote fs cp led/data_service.py :led/data_service.py 
	mpremote fs cp led/engine.py :led/engine.py 
	mpremote fs cp led/hardware.py :led/hardware.py 
	mpremote fs cp led/web_server.py :led/web_server.py 
	mpremote fs cp led/network_service.py :led/network_service.py 
	mpremote fs cp led/light_service.py :led/light_service.py 
	mpremote fs cp led/main.py :main.py 

deploy-dev: \
	deploy-web \
	deploy-code

	@make partial-deploy-warning
	mpremote reset

deploy-full: \
	deploy-cleanup-all \
	deploy-common \
	deploy-microdot \
	deploy-web \
	deploy-code \
	deploy-data-dir

	mpremote reset

 