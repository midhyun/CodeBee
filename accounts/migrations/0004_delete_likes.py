# Generated by Django 3.2.13 on 2022-11-15 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20221115_1715'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likes',
        ),
    ]