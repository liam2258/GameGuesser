# Generated by Django 4.1.2 on 2023-12-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profile_images')),
                ('avatar', models.CharField(max_length=50)),
                ('about', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
