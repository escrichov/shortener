##### VARIABLES #####

VERSION ?= 1.0
APP=shortener
COMMIT=`git rev-parse HEAD`

#####################


##### MAIN #####

.PHONY: build run test release help

build: app_js_build app_build

run:
	$(MAKE) -j 2 app_run app_js_run

format: app_format app_js_format app_css_format app_json_format

lint: app_lint app_js_lint app_css_lint app_md_lint

test: app_test

deploy:
	@git push

deploy-force:
	@git push --no-verify

deploy-heroku:
	@git push heroku master

deploy-heroku-force:
	@git push --no-verify heroku master

################


##### Django #####

app_test:
	@pipenv run python manage.py test

app_build:
	@pipenv run python manage.py collectstatic --noinput

app_migrate:
	@pipenv run python manage.py migrate

app_run:
	@pipenv run python manage.py runserver

app_lint:
	@pipenv run pylint --rcfile=config/.pylintrc shortener_app shortener users payments functional_tests

app_bandit:
	@bandit -r .

app_format:
	@yapf -r -p -i .

##################

##### JS #####

app_js_build:
	@npm run build

app_js_run:
	@npm run serve

app_js_lint:
	@npm run js-lint

app_js_format:
	@npm run js-format

app_css_lint:
	@npm run css-lint

app_css_format:
	@npm run css-format

app_md_lint:
	@npm run md-lint

app_json_format:
	@npm run json-format

##################


##### Utils #####

help:
	@perl -ne'print "$$1\n" if /^([^\.][\w\.]*):/' Makefile

#################
