# Generated by Django 3.2.10 on 2024-05-27 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_account_info_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account_info',
            old_name='dob',
            new_name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='datejoined',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='email_verified',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='link',
        ),
        migrations.RemoveField(
            model_name='account_info',
            name='username',
        ),
    ]
