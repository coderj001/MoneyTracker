# Generated by Django 3.1.5 on 2021-01-28 13:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userpreferences', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Userpreferenc',
            new_name='Userpreference',
        ),
    ]
