# Deployment

It is possible to deploy to Heroku or to your own server.

### Heroku

```bash
heroku create
heroku addons:add heroku-postgresql:hobby-dev
heroku pg:promote DATABASE_URL
heroku config:set ENVIRONMENT=PRODUCTION
heroku config:set DJANGO_SECRET_KEY=`./manage.py generate_secret_key`
heroku config:set DJANGO_SENDGRID_API_KEY=apikey
heroku config:set DJANGO_IPSTACK_APIKEY=apikey
heroku config:set DJANGO_STRIPE_PUBLIC_KEY=public_key
heroku config:set DJANGO_STRIPE_SECRET_KEY=secret_key
```
