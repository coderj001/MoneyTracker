# Generated by Django 3.1.5 on 2021-01-28 23:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210128_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 28, 23, 0, 25, 317131, tzinfo=utc)),
        ),
    ]