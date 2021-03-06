# Generated by Django 2.1.2 on 2018-12-12 01:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('stripe_payment_token',
                 models.CharField(blank=True, max_length=32, null=True)),
                ('stripe_subscription_id',
                 models.CharField(blank=True, max_length=64, null=True)),
                ('stripe_customer_id',
                 models.CharField(blank=True, max_length=32, null=True)),
                ('state',
                 models.PositiveSmallIntegerField(
                     choices=[(0, 'Active'), (1, 'Cancelled'), (2, 'Paused')],
                     default=0)),
                ('user',
                 models.OneToOneField(
                     blank=True,
                     null=True,
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
