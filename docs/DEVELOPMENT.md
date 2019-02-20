# URL Shortener

## Getting started

```bash
git clone https://github.com/escrichov/shortener
cp example.env .env
pipenv install --dev
pipenv run python manage.py collectstatic
pipenv run python manage.py migrate
npm install
make run
```

## Development

### Create superuser

```bash
python manage.py createsuperuser
```

### Run django server and gulp watch

```bash
make run
```

### Format files

```bash
make format
```

### Lint all code

```bash
make lint
```

## Testing

### Install chromedriver to run tests

You need chromedriver to run selenium functional tests.

Install chromedriver in Mac OS X

```bash
brew tap caskroom/cask
brew cask instal chromedriver
```

In other OS: [Download chromedriver binary](http://chromedriver.chromium.org/getting-started)


### Run tests

```bash
pipenv run python manage.py test
```

## Deploy

### Install pre-push hook

```
cp pre-push.sh .git/hooks/pre-push
```

### Upload executing pre push hooks

```
make release
```

By default pre-push hook execute tests and linter. You can disable it executing:

```
make release force
```

## Environment variables

These are common between environments. The `ENVIRONMENT` variable loads the correct settings, possible values are: `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT='DEVELOPMENT'
DJANGO_SECRET_KEY='dont-tell-eve'
DJANGO_DEBUG='yes'
DJANGO_SENDGRID_API_KEY=''
DJANGO_IPSTACK_APIKEY=''
DJANGO_STRIPE_PUBLIC_KEY=''
DJANGO_STRIPE_SECRET_KEY=''
```

These settings(and their default values) are only used on staging and production environments.

```
DJANGO_SENTRY_DSN=''
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
