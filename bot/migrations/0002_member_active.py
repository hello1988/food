# Generated by Django 2.0.2 on 2018-02-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
