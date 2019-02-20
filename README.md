# URL Shortener
[![Build Status](https://travis-ci.org/escrichov/shortener.svg?branch=master)](https://travis-ci.org/escrichov/shortener)
[![codecov](https://codecov.io/gh/escrichov/shortener/branch/master/graph/badge.svg)](https://codecov.io/gh/escrichov/shortener)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4172b033b6ec441983df62d40d3e7499)](https://www.codacy.com/app/escrichov/shortener?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=escrichov/shortener&amp;utm_campaign=Badge_Grade)

Url shortener.

<img alt="Url Shortener" src="https://raw.githubusercontent.com/escrichov/shortener/master/landing.png" width="500">


## Features

-   Python 3.6+
-   Django 2.0+
-   Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
-   Development, Staging and Production settings with [django-configurations](https://django-configurations.readthedocs.org).
-   Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
-   Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
-   HTTPS and other security related settings on Staging and Production.
-   Procfile for running gunicorn with New Relic's Python agent.
-   [PostgreSQL](https://www.postgresql.org) database support with psycopg2.
-   Heroku ready.
-   [Bootstrap 4](https://getbootstrap.com/docs/4.0).
-   [Browsersync](https://www.browsersync.io) enabled.
-   [Sass](https://sass-lang.com/) for styles.
-   [Gulp](https://gulpjs.com/) for javascript and style management.
-   Simple Makefile for running development commands.
-   Integrated linters and autoformatters. [yapf](https://github.com/google/yapf), [eslint](https://eslint.org), [stylelint](https://stylelint.io), [jsonlint](https://www.npmjs.com/package/jsonlint), [remark](https://github.com/remarkjs/remark)
-   Well tested. [Selenium](https://www.seleniumhq.org) functional tests and django unit testing.
-   Good code quality.
-   [Sentry](https://sentry.io) for error tracking.
-   [Sendgrid](https://sendgrid.com) for email sending.
-   [Rest API](docs/API.md)

## [Getting started](docs/DEVELOPMENT.md)

## [Deployment](docs/DEPLOYMENT.md)

## [API](docs/API.md)

## Inspiration

-   [Kutt.it](https://github.com/thedevs-network/kutt)
