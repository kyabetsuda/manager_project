# Generated by Django 2.0.4 on 2018-04-24 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20180419_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address_from',
        ),
        migrations.RemoveField(
            model_name='person',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='person',
            name='current_address',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.RemoveField(
            model_name='person',
            name='sex',
        ),
    ]
