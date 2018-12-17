# Django 2.0+ project template

This is a simple Django 2.0+ project template with my preferred setup. Most Django project templates make way too many assumptions or are just way too complicated. I try to make the least amount of assumptions possible while still trying provide a useful setup. Most of my projects are deployed to Heroku, so this is optimized for that but is not necessary.

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
$ django-admin.py startproject \
  --template=https://github.com/jpadilla/django-project-template/archive/master.zip \
  --name=Procfile \
  --extension=py,md,env \
  project_name
$ mv example.env .env
$ pipenv install --dev
$ pipenv shell --anyway
$ python manage.py collectstatic
$ python manage.py migrate
```

## Development frontend (javascript scripts and sass styles)
```bash
python manage.py runserver
npm run serve
```

## Run tests

```bash
pipenv shell --anyway
python manage.py test
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


## License

The MIT License (MIT)

Copyright (c) 2018-2018 Carlos Escriche

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
