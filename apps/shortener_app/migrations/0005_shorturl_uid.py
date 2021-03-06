# Generated by Django 2.1.2 on 2018-11-25 14:00

from django.db import migrations, models
import shortener_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener_app', '0004_shorturl_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='uid',
            field=models.CharField(
                default=shortener_app.models.generate_random_uid,
                max_length=6,
                unique=True),
        ),
    ]
