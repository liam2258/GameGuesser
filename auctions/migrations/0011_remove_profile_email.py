# Generated by Django 5.0 on 2023-12-11 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
