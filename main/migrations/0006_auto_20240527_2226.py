# Generated by Django 3.2.10 on 2024-05-27 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20240527_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account_info',
            name='email_token',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='user_token',
        ),
    ]