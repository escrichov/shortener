# URL Shortener
[![Build Status](https://travis-ci.org/escrichov/shortener.svg?branch=master)](https://travis-ci.org/escrichov/shortener)
[![codecov](https://codecov.io/gh/escrichov/shortener/branch/master/graph/badge.svg)](https://codecov.io/gh/escrichov/shortener)

Url shortener.

## Features

- Django 2.0+
- Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
- Development, Staging and Production settings with [django-configurations](https://django-configurations.readthedocs.org).
- Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
- Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
- HTTPS and other security related settings on Staging and Production.
- Procfile for running gunicorn with New Relic's Python agent.
- PostgreSQL database support with psycopg2.

## How to install

```bash
git clone https://github.com/escrichov/shortener
cp example.env .env
pipenv install --dev
pipenv run python manage.py collectstatic
pipenv run python manage.py migrate
```

## Development frontend (javascript scripts and sass styles)
```bash
pipenv run python manage.py runserver
npm run serve
```

## Run tests

```bash
pipenv run python manage.py test
```

## Install and compile javascript and styles

```bash
npm run install
npm run build
npm run serve
```

## Environment variables

These are common between environments. The `ENVIRONMENT` variable loads the correct settings, possible values are: `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT='DEVELOPMENT'
DJANGO_SECRET_KEY='dont-tell-eve'
DJANGO_DEBUG='yes'
```

These settings(and their default values) are only used on staging and production environments.

```
DJANGO_SESSION_COOKIE_SECURE='yes'
DJANGO_SECURE_BROWSER_XSS_FILTER='yes'
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF='yes'
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='yes'
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_REDIRECT_EXEMPT=''
DJANGO_SECURE_SSL_HOST=''
DJANGO_SECURE_SSL_REDIRECT='yes'
DJANGO_SECURE_PROXY_SSL_HEADER='HTTP_X_FORWARDED_PROTO,https'
DJANGO_SENDGRID_API_KEY=''
DJANGO_IPSTACK_APIKEY=''
DJANGO_SENTRY_DSN=''
DJANGO_STRIPE_PUBLIC_KEY=''
DJANGO_STRIPE_SECRET_KEY=''
```

## Deployment

It is possible to deploy to Heroku or to your own server.

### Heroku

```bash
$ heroku create
$ heroku addons:add heroku-postgresql:hobby-dev
$ heroku pg:promote DATABASE_URL
$ heroku config:set ENVIRONMENT=PRODUCTION
$ heroku config:set DJANGO_SECRET_KEY=`./manage.py generate_secret_key`
```

### API

API
In addition to the website, you can use these APIs to create, delete and get URLs.

Types
```
URL {
  id {string} Unique ID of the URL
  clicks {number} The amount of visits to this URL
  created_on {string} ISO timestamp of when the URL was created
  target {string} Where the URL will redirect to
  short_url {string} The shortened link (Usually https://cour.fun/id)
}
```
In order to use these APIs you need to generate an API key from settings. Never put this key in the client side of your app or anywhere that is exposed to others.

All API requests and responses are in JSON format.

Include the API key as ```X-API-Key``` in the header of all below requests. Available API endpoints with body parameters:

Get shortened URLs list:
```
GET /api/url/list
```
Returns:
```
Array<URL>
```
Create a shortened link:
```
POST /api/url/create
```
Body:
```
target: Original long URL to be shortened.
```
Returns:
```
URL object
```
Delete a shortened URL and Get stats for a shortened URL:
```
POST /api/url/delete/id
```
Returns:
```
{}
```
